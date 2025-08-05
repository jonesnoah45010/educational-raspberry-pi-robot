import requests
import json
from local_agent_tools import *
from basic_web_scraping import basic_web_scrape, contains_url, extract_urls
import pickle





class chat_agent:
    def __init__(self, model="dolphin-phi:latest", model_encoding=None, name="Robot", url="http://localhost:11434/api", context_window_limit=2048):
        self.conversation_history = []
        self.model=model
        self.model_encoding=model_encoding
        self.url=url
        self.name=name
        self.context_window_limit=context_window_limit
        if type(name) is str:
            self.add_context("Your name is " + self.name)



    def token_count(self, message):
        """
        Counts the number of words in the message as a simple approximation of token count.
        """
        if isinstance(message, list):
            all_text = " ".join([m["content"] for m in message if "content" in m])
        elif isinstance(message, dict):
            all_text = message.get("content", "")
        else:
            all_text = str(message)

        return len(all_text.strip().split())

    def current_tokens_used(self):
        """
            returns how many tokens are currently being used for the entire conversation history
        """
        return self.token_count(self.conversation_history)

    def is_within_context_window(self, context_window_limit=None, current_message=None):
        """
            returns True if the current conversation history is within the context_window_limit
        """
        if context_window_limit is None:
            context_window_limit = self.context_window_limit
        current_token_count = self.current_tokens_used()
        if current_message is not None: 
            current_token_count += self.token_count({"role": "user", "content": current_message})
        return current_token_count <= context_window_limit

    def tokens_left(self):
        """
            returns how many tokes are left before the current conversation goes out of the context_window_limit
        """
        context_window_limit = self.context_window_limit
        t = self.current_tokens_used()
        return int(context_window_limit) - int(t)

    def refresh_conversation(self, summary_size=500, summarize_prompt=None, summary_reference_prompt=None, show=False):
        """
            summarizes the current conversation, deletes the conversation history and then inserts the 
            summary as the new conversation history.  Used to avoid going out od the context_window_limit
        """
        if summarize_prompt is None:
            summarize_prompt = "Summarize the following conversation ... "
        summarize_prompt += str(self.conversation_history)
        summary = self.respond(message=summarize_prompt,show=show)
        if summary_reference_prompt is None:
            summary_reference_prompt = "This is a summary of the conversation so far ... " + str(summary)
        else:
            summary_reference_prompt += " " + str(summary)
        self.conversation_history = []
        self.add_context(summary_reference_prompt)

    def add_context(self, system_prompt):
        """
            add system prompts to contextualize the current conversation
        """
        self.conversation_history.append({"role": "system", "content": system_prompt})

    def respond(self, message, show=True, finish_stream=True, stream=True):
        """
            sends HTTP POST request with message to Ollama API and returns response
        """
        payload = {
            "model": self.model,
            "prompt": message,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url+"/generate", headers=headers, data=json.dumps(payload), stream=stream)
        if finish_stream is False:
            return response
        full_text = ""
        if show:
            print(str(self.name)+": ")
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                data = json.loads(chunk)
                word = data.get("response", "").strip().replace("\n","")
                if word:
                    if show:
                        print(word, end=" ", flush=True)
                    full_text += word + " "
        return full_text


    def chat(self, message, show=True, stream=True, conversation=True, auto_refresh=True, 
             show_tokens_left=False, refresh_summary_size=500, refresh_summarize_prompt=None, 
             refresh_summary_reference_prompt=None, speech_ready=False):
        """
        Main chat method for communicating with the agent.
        If speech_ready=True and stream=True, the response will be chunked by punctuation boundaries.
        """

        if conversation:
            self.conversation_history.append({"role": "user", "content": message})

        if show_tokens_left and auto_refresh:
            print(f"{self.name}: Tokens left until refresh: {self.tokens_left()}")

        if auto_refresh and not self.is_within_context_window(current_message=message):
            if show:
                print(f"{self.name}: CONTEXT WINDOW LIMIT ABOUT TO GO OUT OF BOUNDS, REFRESHING CONVERSATION")
            self.refresh_conversation(summary_size=refresh_summary_size, 
                                      summarize_prompt=refresh_summarize_prompt, 
                                      summary_reference_prompt=refresh_summary_reference_prompt)

        payload = {
            "model": self.model,
            "messages": self.conversation_history
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url+"/chat", headers=headers, json=payload, stream=stream)

        if stream:
            def stream_generator():
                full_text = ""
                if show:
                    print(self.name + ": ", end="", flush=True)
                for chunk in response.iter_lines(decode_unicode=True):
                    if chunk:
                        try:
                            data = json.loads(chunk)
                            content = data.get("message", {}).get("content", "")
                            if content:
                                if show:
                                    print(content, end="", flush=True)
                                full_text += content
                                yield content
                        except json.JSONDecodeError:
                            continue
                if conversation and full_text:
                    self.conversation_history.append({"role": "assistant", "content": full_text})

            # Apply speech chunking if requested
            if speech_ready:
                return split_stream_into_speech_chunks(stream_generator())
            else:
                return stream_generator()

        else:
            full_text = ""
            if show:
                print(self.name + ": ", end="")
            if response.status_code == 200:
                try:
                    json_objects = response.text.strip().split("\n")
                    for obj in json_objects:
                        data = json.loads(obj)
                        content = data.get("message", {}).get("content", "")
                        if content:
                            if show:
                                print(content, end="", flush=True)
                            full_text += content
                except json.JSONDecodeError:
                    full_text = f"Error: Invalid JSON response from Ollama API"
            else:
                full_text = f"Error: {response.status_code}, {response.text}"

            if conversation and full_text:
                self.conversation_history.append({"role": "assistant", "content": full_text})
            return full_text








    def save_agent(self, filepath=None, keep_in_memory=False):
        """
        Saves the current instance of ollama_chat_agent to a pickle file or returns raw bytes if keep_in_memory is True.
        Excludes semantic_db and sql_db to avoid potential pickling issues.
        """
        try:
            data_to_save = self.__dict__.copy()  # Create a copy of the object's attributes
            data_to_save.pop("semantic_db", None)  # Remove database attributes before pickling
            data_to_save.pop("sql_db", None)
            
            pickled_data = pickle.dumps(data_to_save)
            
            if keep_in_memory:
                return pickled_data
            
            if filepath:
                with open(filepath, 'wb') as f:
                    f.write(pickled_data)
                print(f"Agent saved successfully to {filepath}")
            
        except Exception as e:
            print(f"Error saving agent: {e}")
            return None

    @staticmethod
    def load_agent(data, keep_in_memory=False):
        """
        Loads an instance of ollama_chat_agent from a pickle file or from raw bytes if keep_in_memory is True.
        Reinitializes semantic_db and sql_db after loading.
        """
        try:
            if keep_in_memory:
                saved_data = pickle.loads(data)
            else:
                with open(data, 'rb') as f:
                    saved_data = pickle.load(f)
            
            # Create a new instance and restore its attributes
            agent = ollama_chat_agent()
            agent.__dict__.update(saved_data)
            
            print("Agent loaded successfully")
            return agent
        except Exception as e:
            print(f"Error loading agent: {e}")
            return None













if __name__ == "__main__":
    agent = ollama_chat_agent(name="Bob", model="llama3.2")
    while True:
        prompt = input("You:\n")
        response_stream = agent.chat(prompt)
        print("Agent: ")
        for chunk in response_stream:
            print(chunk, end="")
        print("\n")
        if prompt == "bye":
            break


























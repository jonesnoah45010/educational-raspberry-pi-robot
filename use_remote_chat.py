import time
import os
import use_text_to_speech
from local_agent_tools import *
# from use_speech_recognition import say

FILE_PATH = "/home/robot/Desktop/robot/robot_app/remote_chat.txt"

def send_command_to_remote_model(command, prompt, timeout=10.0):
    # Send command to remote
    with open(FILE_PATH, "w") as f:
        f.write(f"COMMAND: {command}\nPROMPT: {prompt}\nRESPONSE:\n")

    def response_stream():
        last_response = ""
        last_mtime = 0
        last_data_time = time.time()

        while True:
            time.sleep(0.1)
            try:
                mtime = os.path.getmtime(FILE_PATH)
                if mtime == last_mtime:
                    # Check timeout if no new data
                    if time.time() - last_data_time > timeout:
                        print(f"\n[Stream ended: no new data for {timeout} seconds]")
                        return
                    continue
                last_mtime = mtime

                with open(FILE_PATH, "r") as f:
                    lines = f.readlines()
            except FileNotFoundError:
                continue

            # Parse streamed response
            response_lines = []
            in_response = False
            for line in lines:
                if "RESPONSE_DONE: true" in line:
                    return  # end the generator
                if line.startswith("RESPONSE:"):
                    response_lines.append(line[len("RESPONSE:"):])
                    in_response = True
                elif in_response:
                    response_lines.append(line)

            current_response = "".join(response_lines)
            if len(current_response) > len(last_response):
                new_part = current_response[len(last_response):]
                yield new_part
                last_response = current_response
                last_data_time = time.time()

    return response_stream()



def is_remote_model_done():
    try:
        with open(FILE_PATH, "r") as f:
            return "RESPONSE_DONE: true" in f.read()
    except FileNotFoundError:
        return False



if __name__ == "__main__":
    cmd = input("Enter command (chat or add_context): ").strip()
    prompt = input("Enter prompt/context: ")
    stream = send_command_to_remote_model(cmd, prompt)

    print("RESPONSE STREAM:")
    i = 1
    c=[]
    for chunk in stream:
        c.append(chunk)
        print(i)
        i+=1
        print(repr(chunk))
        print(str(is_remote_model_done()))
#         try:
#             use_text_to_speech.say(clean_string(chunk))
#         except:
#             print("say issue")
    print("\n")
    print(str(is_remote_model_done()))


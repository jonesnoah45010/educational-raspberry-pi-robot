import os
import time
from use_speaker import play_audio, set_volume
import subprocess
from local_agent_tools import clean_string
import re
# installed voices = (kal_diphone)


def text_to_speech_to_wav(text, filename="tts.wav", voice="kal_diphone"):
    # Remove old file if it exists
    if os.path.exists(filename):
        os.remove(filename)

    # Properly call text2wave via subprocess
    try:
        subprocess.run(
            ["text2wave", "-eval", f"(voice_{voice})", "-o", filename],
            input=text,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error generating speech: {e}")

    return filename


def split_into_10_word_chunks(text):
    words = text.split()
    chunks = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]
    return chunks


def split_into_chunks_by_sentences(text):
    # Split the text into parts by period or newline
    sentences = re.split(r'[.\n?]+', text)
    # Remove any empty strings caused by consecutive periods or newlines
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        words_in_sentence = sentence.split()
        if current_word_count + len(words_in_sentence) > 10:
            # If adding this sentence exceeds 10 words, start a new chunk
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = words_in_sentence
            current_word_count = len(words_in_sentence)
        else:
            current_chunk.extend(words_in_sentence)
            current_word_count += len(words_in_sentence)
    
    # Add any leftover words as the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks



def say(text):
    if "." in text or "\n" in text or "?" in text:
        chunks = split_into_chunks_by_sentences(text)
        for chunk in chunks:
            say(chunk)
    else:
        f = text_to_speech_to_wav(text)
        if os.path.exists(f):
            play_audio(f)
        else:
            print("Error: WAV file not created.")


def simple_say(text):
    if text in ["","\n"]:
        return
    f = text_to_speech_to_wav(text)
    if os.path.exists(f):
        play_audio(f)
    else:
        print("Error: WAV file not created.")







if __name__ == "__main__":
    set_volume()
    say("I am a robot that can talk")























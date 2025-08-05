# import os
# 
# import alsaaudio
# import time
# import queue
# import json
# from vosk import Model, KaldiRecognizer
# 
# 
# 
# 
# def record(file="recording.wav", duration=5, card=3, device=0):
#     os.system(f"arecord -D plughw:{str(card)},{str(device)} -f cd -d {str(duration)} {file}")
# 
# 
# 
# 
# 
# # Load Vosk model
# MODEL_PATH = "/home/robot/Desktop/robot/robot_app/vosk-model-small-en-us-0.15"
# model = Model(MODEL_PATH)
# 
# # Initialize speech recognition
# recognizer = KaldiRecognizer(model, 16000)
# recognizer.SetWords(True)
# 
# # Queue for audio processing
# audio_queue = queue.Queue()
# 
# # Setup ALSA PCM capture (updated API)
# stream = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE, mode=alsaaudio.PCM_NORMAL, device="plughw:CARD=Device,DEV=0",
#                         channels=1, rate=16000, format=alsaaudio.PCM_FORMAT_S16_LE, periodsize=4000)
# 
# # State variables
# keyword_detected = False
# transcribing = False
# transcription = []
# last_speech_time = time.time()
# 
# print("Listening for the keyword 'robot'...")
# 
# if __name__ == "__main__":
#     while True:
#         length, data = stream.read()  # No extra keyword arguments needed
# 
#         if length:
#             audio_queue.put(data)
# 
#             # Process speech recognition
#             if recognizer.AcceptWaveform(data):
#                 result = json.loads(recognizer.Result())
#                 text = result.get("text", "").lower()
# 
#                 if text:
#                     print(f"Recognized: {text}")
# 
#                     # Check for the keyword "robot"
#                     if "robot" in text and not keyword_detected:
#                         keyword_detected = True
#                         transcribing = True
#                         transcription = []
#                         print("\n[Robot detected!] Now transcribing...\n")
# 
#                     # Transcribe everything after "robot" is heard
#                     if transcribing:
#                         transcription.append(text)
#                         last_speech_time = time.time()
# 
#             # Stop transcribing if silence is detected (more than 2 seconds without words)
#             if transcribing and (time.time() - last_speech_time > 2):
#                 print("\n[Silence detected for 2+ seconds] Transcription stopped.\n")
#                 print("Final Transcription:", " ".join(transcription))
#                 keyword_detected = False
#                 transcribing = False
#                 transcription = []
#                 print("\nListening for 'robot' again...\n")
# 





















import os
import alsaaudio
import time
import queue
import json
import threading
from vosk import Model, KaldiRecognizer


def record(file="recording.wav", duration=5, card=3, device=0):
    os.system(f"arecord -D plughw:{str(card)},{str(device)} -f cd -d {str(duration)} {file}")

# Global variables
speech_log = []
listening_thread = None
stop_listening = threading.Event()

# Load Vosk model
MODEL_PATH = "/home/robot/Desktop/robot/robot_app/vosk-model-small-en-us-0.15"
model = Model(MODEL_PATH)

def start_speech_listening(name="robot", stop_talking_delay=1, card=3, device=0):
    global listening_thread, stop_listening
    stop_listening.clear()
    
    def listen():
        recognizer = KaldiRecognizer(model, 16000)
        recognizer.SetWords(True)
        
        stream = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE, mode=alsaaudio.PCM_NORMAL, 
                                device=f"plughw:{card},{device}",
                                channels=1, rate=16000, format=alsaaudio.PCM_FORMAT_S16_LE, periodsize=4000)
        
        keyword_detected = False
        transcribing = False
        transcription = []
        last_speech_time = time.time()

        print(f"Listening for the keyword '{name}'...")

        while not stop_listening.is_set():
            length, data = stream.read()
            if length:
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").lower()
                    
                    if text:
                        print(f"Recognized: {text}")
                        
                        if name.lower() in text and not keyword_detected:
                            keyword_detected = True
                            transcribing = True
                            transcription = []
                            print(f"\n[{name} detected!] Now transcribing...\n")

                        if transcribing:
                            transcription.append(text)
                            last_speech_time = time.time()

                if transcribing and (time.time() - last_speech_time > stop_talking_delay):
                    entry = {"timestamp": time.strftime('%Y-%m-%d %H:%M:%S'), "content": " ".join(transcription)}
                    speech_log.append(entry)
                    print("\n[Silence detected] Transcription stopped.\n")
                    print("Final Transcription:", entry)
                    keyword_detected = False
                    transcribing = False
                    transcription = []
                    print(f"\nListening for '{name}' again...\n")
    
    listening_thread = threading.Thread(target=listen, daemon=True)
    listening_thread.start()

def stop_speech_listening():
    global stop_listening, listening_thread
    stop_listening.set()
    if listening_thread is not None:
        listening_thread.join()
        listening_thread = None
    print("Speech listening stopped.")



def words_after_keyword(sentence: str, keyword: str) -> str:
    words = sentence.split()
    if keyword in words:
        index = words.index(keyword)
        return " ".join(words[index + 1:])
    return ""

def get_last_speech(name="robot"):
    global speech_log
    try:
        content = speech_log[-1]["content"]
        return words_after_keyword(content,name)
    except:
        return None

def clear_speech_log():
    global speech_log
    speech_log = []

def remove_last_item_from_speech_log():
    global speech_log
    try:
        del speech_log[-1]
    except:
        pass
    


if __name__ == "__main__":
    start_speech_listening()
    
    for i in range(30):
        time.sleep(2)
        print("______________________________________")
        print(get_last_speech())
        print("______________________________________")
    
    stop_speech_listening()
    
    
    



















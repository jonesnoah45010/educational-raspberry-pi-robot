import os
import time
import json
import threading
import alsaaudio
from vosk import Model, KaldiRecognizer
from use_text_to_speech import say as basic_say
import subprocess

# Globals
speech_log = []
speech_log_lock = threading.Lock()
listening_thread = None
stop_listening = threading.Event()
pause_listening = threading.Event()
transcript_file = None
start_timestamp_str = None

# Load model
MODEL_PATH = "/home/robot/Desktop/robot/robot_app/vosk-model-small-en-us-0.15"
model = Model(MODEL_PATH)


MIC_CARD = None
MIC_DEVICE = None

def detect_usb_microphone():
    global MIC_CARD, MIC_DEVICE
    try:
        output = subprocess.check_output(["arecord", "-l"], text=True)
    except Exception as e:
        print(f"[ERROR] Could not list recording devices: {e}")
        MIC_CARD = 0
        MIC_DEVICE = 0
        return

    current_card = None
    for line in output.splitlines():
        line = line.strip()

        if line.startswith("card"):
            parts = line.split(":")
            if len(parts) >= 2:
                card_info = parts[1]
                card_number = parts[0].split()[1]
                current_card = card_number

        if "USB" in line and current_card is not None:
            MIC_CARD = int(current_card)
            MIC_DEVICE = 0  # Default device usually 0
            print(f"Detected USB microphone at card {MIC_CARD}, device {MIC_DEVICE}")
            return

    print("[WARNING] USB microphone not found. Defaulting to card 0, device 0.")
    MIC_CARD = 0
    MIC_DEVICE = 0


def get_text_after_keyword(text, keyword):
    keyword = keyword.lower()
    words = text.strip().split()
    try:
        index = words.index(keyword)
        return " ".join(words[index + 1:])
    except ValueError:
        return ""

def start_speech_listening(name="robot", stop_talking_delay=2, card=None, device=None):
    global listening_thread, stop_listening, transcript_file, start_timestamp_str

    if card is None:
        card = MIC_CARD
    if device is None:
        device = MIC_DEVICE

    stop_listening.clear()

    # Prepare transcript file
    os.makedirs("transcripts", exist_ok=True)
    start_timestamp_str = time.strftime("%Y%m%d_%H%M%S")
    transcript_file = os.path.join("transcripts", f"transcript_{start_timestamp_str}.txt")
    with open(transcript_file, "w"): pass

    def listen():
        try:
            recognizer = KaldiRecognizer(model, 16000)
            recognizer.SetWords(True)

            stream = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE, mode=alsaaudio.PCM_NORMAL,
                                   device=f"plughw:{card},{device}")
            stream.setchannels(1)
            stream.setrate(16000)
            stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            stream.setperiodsize(4000)

            keyword_detected = False
            transcribing = False
            transcription = []
            last_speech_time = time.time()

            print(f"Listening for the keyword '{name}'...")

            while not stop_listening.is_set():
                if pause_listening.is_set():
                    time.sleep(0.1)
                    continue

                length, data = stream.read()
                if length and recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").lower()
                    timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S')

                    if text:
                        print(f"Recognized: {text}")
                        with open(transcript_file, "a") as f:
                            f.write(f"{text} | {timestamp_str}\n")

                        if name.lower() in text and not keyword_detected:
                            keyword_detected = True
                            transcribing = True
                            transcription = []
                            print(f"\n[{name} detected!] Now transcribing...\n")

                        if transcribing:
                            transcription.append(text)
                            last_speech_time = time.time()

                if transcribing and (time.time() - last_speech_time > stop_talking_delay):
                    entry = {
                        "timestamp": timestamp_str,
                        "content": get_text_after_keyword(" ".join(transcription), name),
                        "response": None
                    }
                    with speech_log_lock:
                        speech_log.append(entry)
                    print("\n[Silence detected] Transcription stopped.\n")
                    print("Final Transcription:", entry)
                    keyword_detected = False
                    transcribing = False
                    transcription = []
                    print(f"\nListening for '{name}' again...\n")

        except Exception as e:
            print(f"[ERROR in listening thread]: {e}")

    listening_thread = threading.Thread(target=listen, daemon=True)
    listening_thread.start()

def stop_speech_listening():
    global stop_listening, listening_thread, transcript_file, start_timestamp_str
    stop_listening.set()
    if listening_thread:
        listening_thread.join()
        listening_thread = None

    # Rename transcript file with start/end
    if transcript_file and start_timestamp_str:
        stop_timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        new_name = f"transcript_{start_timestamp_str}_{stop_timestamp_str}.txt"
        new_path = os.path.join("transcripts", new_name)
        os.rename(transcript_file, new_path)
        print(f"Transcript saved as: {new_path}")

    print("Speech listening stopped.")

def get_last_speech():
    with speech_log_lock:
        return speech_log[-1]["content"] if speech_log else None

def get_speech_log_entry(i=-1):
    with speech_log_lock:
        return speech_log[i] if speech_log else None

def set_speech_log_response(response, i=-1):
    with speech_log_lock:
        if speech_log: speech_log[i]["response"] = response

def remove_speech_log_entry(i=-1):
    with speech_log_lock:
        if speech_log: del speech_log[i]

def pause_speech_listening():
    pause_listening.set()

def resume_speech_listening():
    pause_listening.clear()

# Optional: Use espeak or flite to talk on Raspberry Pi
def say(text):
    if text:
        pause_speech_listening()
        try:
#             os.system(f'espeak "{text}"')  # or use flite
            basic_say(text)
        except Exception as e:
            print(f"[ERROR] say() failed: {e}")
        finally:
            resume_speech_listening()



detect_usb_microphone()

# Demo / test loop
if __name__ == "__main__":
    start_speech_listening()

    try:
        while True:
            time.sleep(1)
            print("_________________________")
            with speech_log_lock:
                print(speech_log)
            entry = get_speech_log_entry()
            if entry and entry["response"] is None:
                response = entry["content"]
                say(response)
                set_speech_log_response(response)
            if entry and entry["content"] in ["goodbye", "bye", "quit", "end"]:
                break
    except KeyboardInterrupt:
        pass
    finally:
        stop_speech_listening()

















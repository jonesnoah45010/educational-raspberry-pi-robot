import os
import time
import subprocess

SPEAKER_HW_DEVICE = None  # Will be set automatically

def detect_usb_speaker():
    """Detect the ALSA device for the USB speaker."""
    global SPEAKER_HW_DEVICE

    # List all sound cards and devices
    try:
        output = subprocess.check_output(["aplay", "-l"], text=True)
    except Exception as e:
        print(f"Error detecting audio devices: {e}")
        return

    # Parse the output to find the USB device
    current_card = None
    for line in output.splitlines():
        line = line.strip()

        if line.startswith("card"):
            parts = line.split(":")
            if len(parts) >= 2:
                card_info = parts[1]
                card_number = parts[0].split()[1]
                current_card = card_number
                # Optional: print(card_info)  # for debugging

        if "USB" in line and current_card is not None:
            SPEAKER_HW_DEVICE = f"hw:{current_card},0"
            print(f"Detected USB speaker at {SPEAKER_HW_DEVICE}")
            return

    # Fallback if USB speaker not found
    print("Warning: No USB speaker detected. Defaulting to hw:0,0")
    SPEAKER_HW_DEVICE = "hw:0,0"


# def play_audio(filename):
#     os.system(f"cvlc -A alsa --alsa-audio-device {SPEAKER_HW_DEVICE} --play-and-exit {filename}")

# def play_audio(filepath):
#     os.system(f"aplay {filepath}")


def play_audio(filepath):
    try:
        subprocess.run(["aplay", filepath], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio: {e}")



# def play_mp3(name):
#     os.system(f"cvlc -A alsa --alsa-audio-device {SPEAKER_HW_DEVICE} --play-and-exit audio/{name}.mp3")

# def play_mp3(name):
#     os.system(f"mpg123 audio/{name}.mp3")

def play_mp3(name):
    try:
        subprocess.run(["mpg123", f"audio/{name}.mp3"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error playing MP3: {e}")


def set_volume(percent=80):
    os.system(f"amixer -c {SPEAKER_HW_DEVICE.split(':')[1].split(',')[0]} cset numid=3 {str(percent)}%")


def startup_sound():
    set_volume(80)
    time.sleep(0.5)
    for _ in range(3):
        play_mp3("beep")
        time.sleep(0.5)


def shut_down_sound():
    set_volume(80)
    time.sleep(0.5)
    play_mp3("shut_down")


# Automatically detect device on import
detect_usb_speaker()

if __name__ == "__main__":
    startup_sound()


import os
import subprocess




def capture_photo(name="last_photo", rotation=None, hflip=False, vflip=True):
    # Ensure the "images" folder exists
    os.makedirs("images", exist_ok=True)

    # Base command
    command = ["libcamera-still", "-o", f"images/{name}.jpg", "--timeout", "1", "--nopreview"]

    # Add optional transformations
    if rotation in [0, 90, 180, 270]:
        command += ["--rotation", str(rotation)]
    if hflip:
        command.append("--hflip")
    if vflip:
        command.append("--vflip")

    # Run the command
    try:
        subprocess.run(command, check=True)
        print(f"Photo captured successfully: images/{name}.jpg")
    except subprocess.CalledProcessError as e:
        print(f"Error capturing photo: {e}")







def capture_photo_bytes(rotation=None, hflip=False, vflip=True):
    # Base command to output to stdout
    command = ["libcamera-still", "-o", "-", "--timeout", "1", "--nopreview"]

    # Add optional transformations
    if rotation in [0, 90, 180, 270]:
        command += ["--rotation", str(rotation)]
    if hflip:
        command.append("--hflip")
    if vflip:
        command.append("--vflip")

    # Run the command and capture stdout, suppress stderr
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL  # suppress camera logs
        )
        return result.stdout  # Image bytes
    except subprocess.CalledProcessError as e:
        print(f"Error capturing photo: {e}")
        return None
    













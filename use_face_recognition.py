import face_recognition
import sys
import numpy as np
import pickle
import os



PICKLE_FILE = "known_faces.pkl"

def face_load_image(image_path):
    return face_recognition.load_image_file(image_path)


def face_encode_image(image_path):
    if type(image_path) is np.ndarray:
        img = image_path
    else:
        img = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(img)
    return encoding

def image_contains_face(image_path):
    if type(image_path) is np.ndarray:
        img = image_path
    else:
        img = face_recognition.load_image_file(image_path)
    encoding = face_encode_image(image_path)
    if not encoding:
        return False
    return True



def compare_face_encodings(encodings1, encodings2):
    
    # Ensure a face was detected in both images
    if not encodings1:
        print(f"No face detected in {image1_path}")
        return
    if not encodings2:
        print(f"No face detected in {image2_path}")
        return

    # Compare the first face found in each image
    result = face_recognition.compare_faces([encodings1[0]], encodings2[0])

    if result[0]:
        print("The images contain the same face.")
        return True
    else:
        print("The images contain different faces.")
        return False



def compare_face_images(image1_path, image2_path):
    
    # Load the images
    if type(image1_path) is np.ndarray:
        img1 = image1_path
    else:
        img1 = face_recognition.load_image_file(image1_path)
    
    if type(image2_path) is np.ndarray:
        img2 = image2_path
    else:
        img2 = face_recognition.load_image_file(image2_path)

    # Detect face encodings in both images
    encodings1 = face_recognition.face_encodings(img1)
    encodings2 = face_recognition.face_encodings(img2)

    # Ensure a face was detected in both images
    if not encodings1:
        print(f"No face detected in {image1_path}")
        return
    if not encodings2:
        print(f"No face detected in {image2_path}")
        return

    # Compare the first face found in each image
    result = face_recognition.compare_faces([encodings1[0]], encodings2[0])

    if result[0]:
        print("The images contain the same face.")
        return True
    else:
        print("The images contain different faces.")
        return False




def face_encoding_similarity(encodings1, encodings2):

    if not encodings1 or not encodings2:
        print("No face detected in one or both images.")
        return None

    distance = face_recognition.face_distance([encodings1[0]], encodings2[0])[0]
    print(f"Face distance score: {distance}")

    if distance < 0.4:
        print("Highly similar faces")
    elif distance < 0.6:
        print("Moderately similar faces")
    else:
        print("Faces are different")

    return distance



def face_image_similarity(image1_path, image2_path):
    
    if type(image1_path) is np.ndarray:
        img1 = image1_path
    else:
        img1 = face_recognition.load_image_file(image1_path)
    
    if type(image2_path) is np.ndarray:
        img2 = image2_path
    else:
        img2 = face_recognition.load_image_file(image2_path)

    encodings1 = face_recognition.face_encodings(img1)
    encodings2 = face_recognition.face_encodings(img2)

    if not encodings1 or not encodings2:
        print("No face detected in one or both images.")
        return None

    distance = face_recognition.face_distance([encodings1[0]], encodings2[0])[0]
    print(f"Face distance score: {distance}")

    if distance < 0.4:
        print("Highly similar faces")
    elif distance < 0.6:
        print("Moderately similar faces")
    else:
        print("Faces are different")

    return distance




def detect_facial_landmarks(image_path):
    if type(img) is np.ndarray:
        img = image_path
    else:
        img = face_recognition.load_image_file(image_path)
    face_landmarks_list = face_recognition.face_landmarks(img)

    if not face_landmarks_list:
        print("No facial landmarks detected.")
        return

    for i, face_landmarks in enumerate(face_landmarks_list):
        print(f"Face {i+1}:")
        for feature, points in face_landmarks.items():
            print(f"  {feature}: {points}")


def detect_multiple_faces(image_path):
    if type(img) is np.ndarray:
        img = image_path
    else:
        img = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(img)

    if not face_locations:
        print("No faces detected.")
    else:
        print(f"Detected {len(face_locations)} face(s).")

    return face_locations


def count_faces(image_path):
    if type(img) is np.ndarray:
        img = image_path
    else:
        img = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(img)

    if not face_locations:
        print("No faces detected.")
    else:
        print(f"Detected {len(face_locations)} face(s).")

    return len(face_locations)

























def save_known_faces(known_faces):
    """Saves the known faces dictionary to a pickle file."""
    with open(PICKLE_FILE, "wb") as f:
        pickle.dump(known_faces, f)
    print("Known faces saved successfully.")

def load_known_faces():
    """Loads the known faces dictionary from a pickle file."""
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, "rb") as f:
            return pickle.load(f)
    return {}


def clear_known_faces():
    """Deletes the pickle file to clear all stored faces."""
    if os.path.exists(PICKLE_FILE):
        os.remove(PICKLE_FILE)
        print("Known faces cleared successfully.")
    else:
        print("No stored faces to clear.")


def add_new_face(image_or_encoding, name):
    """Adds a new face to the known faces dictionary."""
    print(type(image_or_encoding))
    
    if type(image_or_encoding) is list:
        if len(image_or_encoding) > 0:
            image_or_encoding = image_or_encoding[0]
        else:
            print("recognize_face given empty list as param")
            return None
    
    # Check if the input is an encoding or an image path
    if isinstance(image_or_encoding, np.ndarray):
        encodings = [image_or_encoding]
    else:
        img = face_recognition.load_image_file(image_or_encoding)
        encodings = face_recognition.face_encodings(img)

    if not encodings:
        print(f"No face found in {image_or_encoding}.")
        return

    # Store only the first detected face encoding
    known_faces[name] = encodings[0]

    save_known_faces(known_faces)
    print(f"Added {name} to known faces.")


def recognize_face(image_or_encoding):
    """Checks if a face is already in the known faces dictionary."""

    if not known_faces:
        print("No known faces available.")
        return None
    
    if type(image_or_encoding) is list:
        if len(image_or_encoding) > 0:
            image_or_encoding = image_or_encoding[0]
        else:
            print("recognize_face given empty list as param")
            return None
    # Check if the input is an encoding or an image path
    if isinstance(image_or_encoding, np.ndarray):
        encodings = [image_or_encoding]
    else:
        img = face_recognition.load_image_file(image_or_encoding)
        encodings = face_recognition.face_encodings(img)

    if not encodings:
        print("No face detected in the image.")
        return None

    unknown_encoding = encodings[0]
    names = list(known_faces.keys())
    encodings_list = list(known_faces.values())

    # Compare against stored faces
    results = face_recognition.compare_faces(encodings_list, unknown_encoding)
    distances = face_recognition.face_distance(encodings_list, unknown_encoding)

    if True in results:
        best_match_index = np.argmin(distances)
        print(f"Recognized as {names[best_match_index]}.")
        return names[best_match_index]
    else:
        print("Face not recognized.")
        return None





known_faces = load_known_faces()

# Example usage from command line
if __name__ == "__main__":
    img = "images/test_face_recognition/obama1.jpg"
    print("image: " + str(img))
    load_known_faces()
    print("loaded known faces")
    face = face_encode_image(img)
    print("image encoded")
    name = recognize_face(face)
    print("name first attempt: " + str(name))
    if not name:
        add_new_face(face,"Obama")
        name = recognize_face(face)
    save_known_faces(known_faces)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

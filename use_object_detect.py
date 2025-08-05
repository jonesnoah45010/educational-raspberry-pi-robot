from PIL import Image, ImageOps
import numpy as np
import tflite_runtime.interpreter as tflite
from use_camera import capture_photo

class classification_model:
    def __init__(self, model_path="frog_or_dog_model.tflite", class_names="frog_or_dog_labels.txt"):
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        with open(class_names, "r") as f:
            self.class_names = f.readlines()

    def classify(self, image_path):
        image = Image.open(image_path).convert("RGB")
        image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)

        # Normalize to [-1, 1] for float model
        input_data = np.expand_dims(np.asarray(image).astype(np.float32) / 127.5 - 1, axis=0)

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])

        prediction = output_data[0]
        index = np.argmax(prediction)
        class_name = self.class_names[index].strip().split()[1]
        confidence_score = prediction[index]

        return {
            "image": image_path,
            "class": class_name,
            "confidence_score": confidence_score
        }

    def identify(self, image_path):
        return self.classify(image_path)["class"]
    
    
    def capture_and_identify(self):
        capture_photo("object_detect")
        return self.identify("images/object_detect.jpg")
    






    
    
if __name__ == "__main__":
    model = classification_model()
#     print(model.classify("images/test_object_detect/dog.jpg"))
#     print(model.classify("images/test_object_detect/frog.jpg"))
    i = model.capture_and_identify()
    print(i)


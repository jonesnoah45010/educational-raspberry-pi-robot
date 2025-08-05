import time
import sys
import random
from use_camera import capture_photo
from use_dist_sensor import start_dist_sensor, stop_dist_sensor, get_dist
from use_speaker import play_mp3, play_audio, set_volume, startup_sound, shut_down_sound 
from use_drive_controller import drive_controller
from use_speech_recognition import say, start_speech_listening, stop_speech_listening, get_speech_log_entry, set_speech_log_response 
from use_color_detect import detect_color
from use_object_detect import classification_model
from chat_agent import chat_agent
from use_image_display import ImageViewer
from use_sentiment_classifier import SentimentClassifier
from use_remote_chat import send_command_to_remote_model
from local_agent_tools import *

if __name__ == "__main__":
    set_volume(80)
    sentiment_classifier = SentimentClassifier()
    viewer = ImageViewer("/home/robot/Desktop/robot/robot_app/images/display_images")
    viewer.start()
    viewer.show_image("thinking.jpg")
    # agent = chat_agent(model="dolphin-phi:latest")
    # agent.add_context("You are a cute frog who likes to be silly and responds concisely.")
    # agent.add_context("You should only respond with 20 words or less")    
    # response_stream = agent.chat("tell me a friendly greeting.",stream=True,speech_ready=True)
    # say("thinking of a way to say hello.")
    # time.sleep(5)
    # for chunk in response_stream:
        # say(chunk)
    viewer.show_image("neutral.jpg")
    frog_or_dog_model = classification_model(model_path="frog_or_dog_model.tflite", class_names="frog_or_dog_labels.txt")
    driver = drive_controller()
    driver.stop()
    start_speech_listening()
    start_dist_sensor()
    startup_sound()
    
    
    def determine_face(you_said):
        sentiment = sentiment_classifier.classify(you_said)
        to_show = "neutral.jpg"
        if sentiment == "neutral":
            to_show = "neutral.jpg"
            viewer.show_image(to_show)
        if sentiment == "hostile":
            to_show = "angry.jpg"
            viewer.show_image(to_show)
        if sentiment == "friendly":
            to_show = "happy.jpg"
            viewer.show_image(to_show)
        return to_show


    try:
        while True:
            time.sleep(0.5)
            entry = get_speech_log_entry()
            if entry and entry["response"] is None:
                you_said = entry["content"]                    
                if you_said == "move forward":
                    response = "moving forward"
                    say(response)
                    set_speech_log_response(response)
                    driver.forward_step(0.5)
                elif you_said == "move back":
                    response = "moving back"
                    say(response)
                    set_speech_log_response(response)
                    driver.backward_step(0.5)
                elif you_said == "turn right":
                    response = "turning right"
                    say(response)
                    set_speech_log_response(response)
                    driver.right_step(0.5)
                elif you_said == "turn left":
                    response = "turning left"
                    say(response)
                    set_speech_log_response(response)
                    driver.left_step(0.5)
                elif you_said in ["detect distance","detects distance"]:
                    d = int(get_dist())
                    response = f"distance detected {d} inches"
                    say(response)
                    set_speech_log_response(response)
                elif you_said == "what color is this":
                    color = detect_color()
                    response = f"color detected is {color}"
                    say(response)
                    set_speech_log_response(response)
                elif you_said in ["dog or frog","frog or dog","is this a dog or a frog","is this a frog or a dog"]:
                    viewer.show_image("thinking.jpg")
                    say("viewing object")
                    identity = frog_or_dog_model.capture_and_identify()
                    viewer.show_image("neutral.jpg")
                    response = f"I think that is a {identity}"
                    say(response)
                    set_speech_log_response(response)
                elif you_said in ["happy face","happy faith","happy fate"]:
                    response = f"showing happy face"
                    say(response)
                    set_speech_log_response(response)
                elif you_said in ["sad face","sad faith","sad fate"]:
                    viewer.show_image("sad.jpg")
                    response = f"showing sad face"
                    say(response)
                    set_speech_log_response(response)
                elif you_said in ["angry face","angry faith","angry fate"]:
                    viewer.show_image("angry.jpg")
                    response = f"showing angry face"
                    say(response)
                    set_speech_log_response(response)
                elif you_said.lower() in ["goodbye", "good bye", "bye", "quit", "end", "exit"]:
                    viewer.show_image("thinking.jpg")
                    # response_stream = agent.chat(you_said,stream=True,speech_ready=True)
                    viewer.show_image("sad.jpg")
                    say("goodbye")
                    # response = ""
                    # for chunk in response_stream:
                        # response += chunk
                        # say(chunk)
                    # set_speech_log_response(response)
                    break
                else:
                    viewer.show_image("thinking.jpg")
                    say("I do not know what to say to that")
                    # response_stream = agent.chat(you_said,stream=True,speech_ready=True)
#                     response_stream = send_command_to_remote_model("chat", you_said)
                    # say("thinking of a response")
                    face = determine_face(you_said)
                    sentiment = sentiment_classifier.classify(you_said)
                    response = f"I think what you said was {sentiment}"
                    say(response)
                    set_speech_log_response(response)
#                     response = ""
#                     i=0
#                     for chunk in response_stream:
#                         i+=1
#                         print("chunk "+str(i))
#                         chunky = clean_string(chunk)
#                         print(chunky)
#                         response += chunky
#                         say(chunky)
#                     print("RESPONSE: " + response)
#                     set_speech_log_response(response)
#                     
    except KeyboardInterrupt:
        pass
    finally:
        stop_speech_listening()
        driver.stop()
        stop_dist_sensor()
        shut_down_sound()
        




    
    
    
    
    
    
    
    

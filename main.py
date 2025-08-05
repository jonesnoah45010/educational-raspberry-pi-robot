import time
import sys
import random
from use_camera import capture_photo
from use_dist_sensor import start_dist_sensor, stop_dist_sensor, get_dist
from use_speaker import play_mp3, set_volume, startup_sound, shut_down_sound 
from use_drive_controller import drive_controller
from use_speech_recognition import say, start_speech_listening, stop_speech_listening, get_speech_log_entry, set_speech_log_response 
from use_color_detect import detect_color
from use_object_detect import classification_model
# from use_keyboard import get_current_key





# INITIALIZATION

print("ROBOT START")
startup_sound()
start_dist_sensor()
driver = drive_controller()
driver.stop()







# YOUR CODE HERE
say("Hello")
go = True
while go:
    driver.forward()
    if get_dist() < 10:
        driver.stop()
        color = detect_color()
        if color == "red":
            say("red detected")
            go = False
        else:
            say(color + " detected")
            driver.right_step(0.3)






# DEINITIALIZATION

print("ROBOT STOP")
driver.stop()
stop_dist_sensor()
shut_down_sound()






















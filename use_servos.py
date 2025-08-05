import pi_servo_hat
import time
import sys

servos = pi_servo_hat.PiServoHat()


if servos.is_connected() == False:
    print("The Qwiic PCA9685 device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    quit()


def fl_forward():
    servos.move_servo_position(0, 90)

def fl_backward():
    servos.move_servo_position(0, 0)

def fr_forward():
    servos.move_servo_position(1, 0)

def fr_backward():
    servos.move_servo_position(1, 90)

def bl_forward():
    servos.move_servo_position(2, 90)

def bl_backward():
    servos.move_servo_position(2, 0)

def br_forward():
    servos.move_servo_position(3, 0)

def br_backward():
    servos.move_servo_position(3, 90)

    
def stop():
    servos.sleep()
    servos.restart()




def forward():
    bl_forward()
    br_forward()
    fl_forward()
    fr_forward()

def backward():
    bl_backward()
    br_backward()
    fl_backward()
    fr_backward()


def left():
    br_forward()
    fr_forward()
    bl_backward()
    fl_backward()


def right():
    br_backward()
    fr_backward()
    bl_forward()
    fl_forward()




def forward_step(seconds):
    forward()
    time.sleep(seconds)
    stop()



def backward_step(seconds):
    backward()
    time.sleep(seconds)
    stop()


def right_step(seconds):
    right()
    time.sleep(seconds)
    stop()

def left_step(seconds):
    left()
    time.sleep(seconds)
    stop()


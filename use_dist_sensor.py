import time
import sys
import qwiic_vl53l1x

dist_sensor = qwiic_vl53l1x.QwiicVL53L1X()
dist_sensor.sensor_init()





def start_dist_sensor():
    dist_sensor.start_ranging()


def stop_dist_sensor():
    dist_sensor.stop_ranging()


def get_dist():
    distance = dist_sensor.get_distance()
    distanceInches = distance / 25.4
    return distanceInches
    
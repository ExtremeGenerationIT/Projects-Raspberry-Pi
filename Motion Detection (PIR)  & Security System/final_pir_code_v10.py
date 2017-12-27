# ExtremeGeneration.it

import RPi.GPIO as GPIO
import time
import datetime
import picamera


GPIO.setmode(GPIO.BCM)
# Specify Pin Numbers
PIR_PIN = 4
# RGB Led
R = 17  # red color Led
G = 18  # green color Led
B = 27  # blue color Led
# IR Receiver
IR_PIN = 6
# Buzzer
BUZZER_PIN = 12
# Camera
camera = picamera.PiCamera()
camera.vflip = True


def setup():
    # Set mode (number of pin as written on the breadboard)
    GPIO.setmode(GPIO.BCM)
    # PIR SENSOR pin
    GPIO.setup(PIR_PIN, GPIO.IN)
    # RGB LED pins
    GPIO.setup(R, GPIO.OUT)
    GPIO.setup(G, GPIO.OUT)
    GPIO.setup(B, GPIO.OUT)
    # IR RECEIVER
    GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Buzzer pins
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    # GPIO.add_event_detect(IR_PIN, GPIO.FALLING, callback=disable_alarm)
    set_blue()


# Functions for RGB LED
def set_blue():
    GPIO.output(R, GPIO.HIGH)
    GPIO.output(G, GPIO.HIGH)
    GPIO.output(B, GPIO.LOW)


def set_red():
    GPIO.output(B, GPIO.HIGH)
    GPIO.output(G, GPIO.HIGH)
    GPIO.output(R, GPIO.LOW)


def set_green():
    GPIO.output(B, GPIO.HIGH)
    GPIO.output(G, GPIO.LOW)
    GPIO.output(R, GPIO.HIGH)


def start_alarm():
    print('Set the alarm on')
    # Start the alarm
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    # TODO: Add any other kind of functions you may need!
    # Allow the user to identify and switch off the alarm
    while True:
        if (GPIO.input(IR_PIN) == False):
            disable_alarm()
            break
    time.sleep(0.01)


# The user disabled alarm, wait for 5 minutes before start detecting motion
def disable_alarm():
    print('Disabling alarm. . .')
    try:
        camera.stop_recording()
    except:
        print('PiCamera is unavailable')
    # Cleanup the GPIO
    GPIO.cleanup()
    # Setup again the GPIO
    setup()
    # Set the green light
    set_green()
    # Set standby time
    idle_time = 60 * 5  # TODO: set idle time
    # Do nothing until the time is elapsed
    time.sleep(idle_time)
    set_blue()
    # Start to detect motion again
    motion_detection()


def one_minute_window(ts, st):
    try:
        camera.start_recording('/home/pi/Desktop/motion_' + st + '.h264')
    except:
        print('PiCamera is unavailable ')
    set_red()
    warning_time = 60 # Set seconds to allow the User to identify
    while (time.time() < ts + warning_time):
        # Check if we receive any IR signal from remote control
        if (GPIO.input(IR_PIN) == False):
            print('IR signal detected! User identified.')
            disable_alarm()
        time.sleep(0.01)
    # If user did not switch it off, start the alarm!
    start_alarm()


def motion_detection():
    # setup() #Set the GPIO
    print('Ready to detect motion!')
    # Each second check for motions
    while True:
        if GPIO.input(PIR_PIN):
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print('MOTION DETECTED at: ' + st)
            # one minutes to disable alarm
            one_minute_window(ts, st)
        time.sleep(1)



def destroy():
    GPIO.cleanup()
    camera.close()
    # setup()


if __name__ == "__main__":
    try:
        GPIO.cleanup()
        setup()
        motion_detection()
        # motion_thread.start()
    except KeyboardInterrupt:
        destroy()

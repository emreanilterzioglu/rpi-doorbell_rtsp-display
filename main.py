import signal
import sys
import RPi.GPIO as GPIO


bellButton_input = 16 #Outside bell button sense
unlockButton_input = 18 #door_unlock button sense
audio_output = 12 #pwm Output for doorbell sound play

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def unlock_callback():
    print("Door Unlocked!")

def bellButton_callback()
    print("DoorBell Ringing!")

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(bellButton_input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(bellButton_input, GPIO.FALLING, 
            callback=bellButton_callback, bouncetime=100)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(unlockButton_input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(unlockButton_input, GPIO.FALLING,
            callback=unlock_callback, bouncetime=100)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

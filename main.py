import signal
import sys
import RPi.GPIO as GPIO


bellButton_input = 16 #Outside bell button sense
unlockButton_input = 22 #door_unlock button sense
audio_output = 12 #pwm Output for doorbell sound play
#14 & 16 GND

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def unlock_callback(channel):
    print("Door Unlocked!")

def bellButton_callback(channel):
    print("DoorBell Ringing!")

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(bellButton_input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(bellButton_input, GPIO.FALLING, 
            callback=bellButton_callback, bouncetime=500)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(unlockButton_input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(unlockButton_input, GPIO.FALLING,
            callback=unlock_callback, bouncetime=500)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

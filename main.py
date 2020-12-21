import signal
import sys
import RPi.GPIO as GPIO
import os
import time
import thread

bellButton_input = 16 #Outside bell button sense
unlockButton_input = 22 #door_unlock button sense
audio_output = 12 #pwm Output for doorbell sound play
#14 & 16 GND
is_live = False

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def unlock_callback(channel):
    print("Door Unlocked!")
    deactivateISR(channel)
    #startVideoStream()
    activateISR(channel)

def bellButton_callback(channel):
    print("DoorBell Ringing!")
    thread.start_new_thread(startVideoStream,(channel,))
    print("Video Thread Started!")

def startVideoStream(channel):
    deactivateISR(channel)
    print("DEBUG 1!")
    #os.system('tvservice -p')
    #os.system('omxplayer --no-keys --avdict rtsp_transport:tcp "rtsp://admin:admin123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0" &')
    print("DEBUG 2!")
    #os.system('omxplayer /opt/vc/src/hello_pi/hello_video/test.h264 &')
    print("DEBUG 3!")    
    time.sleep(10)
    print("DEBUG 4!")
    #os.system('killall omxplayer.bin')
    print("DEBUG 5!")    
    #os.system('tvservice -o')
    print("DEBUG 6!")
    activateISR(channel)

def setup():
    time.sleep(0.1)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(bellButton_input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(bellButton_input, GPIO.FALLING,
            callback=bellButton_callback, bouncetime=1000)

    time.sleep(1)


    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(unlockButton_input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(unlockButton_input, GPIO.FALLING,
            callback=unlock_callback, bouncetime=1000)

def activateISR(channel):
   time.sleep(0.1)

   if channel == bellButton_input:
       GPIO.add_event_detect(bellButton_input, GPIO.FALLING,callback=bellButton_callback, bouncetime=1000)
       print("BellButton ISR Activated!")

   if channel == unlockButton_input:
       GPIO.add_event_detect(unlockButton_input, GPIO.FALLING,callback=unlock_callback, bouncetime=1000)
       print("UnlockButton ISR Activated!")

def deactivateISR(channel):
    time.sleep(0.1)
    GPIO.remove_event_detect(channel)

if __name__ == '__main__':

    setup()

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

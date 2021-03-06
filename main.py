import signal
import sys
import RPi.GPIO as GPIO
import os
import time
import thread
import logging

bellButton_input = 16 #Outside bell button sense
unlockButton_input = 22 #door_unlock button sense
#audio_output = 12 #pwm Output for doorbell sound play
#14 & 16 GND


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def unlock_callback(channel):
    logging.info("Door Unlocked")
    thread.start_new_thread(stopVideoStream,(channel,))
    logging.info("Video Stopped")

def bellButton_callback(channel):
    logging.info("DoorBell Ringing!")
    thread.start_new_thread(startVideoStream,(channel,))
    logging.info("Video Thread Started!")

def startVideoStream(channel):
    logging.info("Video Started")
    deactivateISR(channel)
    print("DEBUG 1!")
    os.system('tvservice -p')
    #os.system('omxplayer --no-keys --avdict rtsp_transport:tcp "rtsp://admin:admin123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0" &')
    print("DEBUG 2!")
    os.system('omxplayer /home/pi/testvideo.mp4 &')
    print("DEBUG 3!")    
    time.sleep(60)
    print("DEBUG 4!")
    os.system('killall omxplayer.bin')
    print("DEBUG 5!")    
    os.system('tvservice -o')
    print("DEBUG 6!")
    activateISR(channel)

def stopVideoStream(channel):
    logging.info("Video Stopped")
    deactivateISR(channel)
    time.sleep(10)
    os.system('killall omxplayer.bin')
    os.system('tvservice -o')
    activateISR(channel)

def setup():
    logging.info("Setup Initialized")
    os.system('tvservice -o')
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
       logging.info("BellButton ISR Activated!")

   if channel == unlockButton_input:
       GPIO.add_event_detect(unlockButton_input, GPIO.FALLING,callback=unlock_callback, bouncetime=1000)
       logging.info("UnlockButton ISR Activated!")

def deactivateISR(channel):
    time.sleep(0.1)
    GPIO.remove_event_detect(channel)

if __name__ == '__main__':

    logging.basicConfig(filename="/home/pi/log.txt",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)


    setup()

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

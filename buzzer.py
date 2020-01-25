import RPi.GPIO as GPIO
from time import sleep
import time
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# Configure the count of pixels:
PIXEL_COUNT = 60


# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)


def blink_color(pixels, blink_times=5, wait=0.1, color=(255,0,0)):
    step =1
    for i in range(blink_times):
        # blink two times, then wait
        pixels.clear()
        for j in range(2):
            for k in range(pixels.count()):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.08)
            pixels.clear()
            pixels.show()
            time.sleep(0.08)
        time.sleep(wait)
    for k in range(pixels.count()):    
        pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
    pixels.show()
    
    for j in range(int(256 // step)):
        for i in range(pixels.count()):
            r, g, b = pixels.get_pixel_rgb(i)
            r = int(max(0, r - step))
            g = int(max(0, g - step))
            b = int(max(0, b - step))
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( r, g, b ))
        pixels.show()
        if wait > 0:
            time.sleep(0.01)



# Sets the Pi so it knows we are using the physical pin numbering
GPIO.setmode(GPIO.BOARD)

# Sets up pin 21 as an input
GPIO.setup(40,GPIO.IN, GPIO.PUD_UP)
GPIO.setup(38,GPIO.IN, GPIO.PUD_UP)

time_stamp_blue = time.time()
time_stamp_red = time.time()
time_buzzer = time.time()

def my_callback(channel):
    global time_stamp_blue
    global time_stamp_red
    global time_buzzer
    time_now = time.time()
    #print(f'ariving IT {channel} at {time_now}')

    if channel == 40:
        if ((time_now - time_stamp_blue) >= 0.3): #bouncing blue (gpio40)
            if (time_now - time_buzzer >= 6): #wait 3s pour prendre la main
                time_buzzer = time_now
                print(f"falling edge detected on {channel}\n")
                blink_color(pixels, blink_times = 3, color=(255, 0, 0))
                #time_buzzer = time_now
            time_stamp_blue = time_now
    elif channel ==38:
        if ((time_now - time_stamp_red) >= 0.3): #bouncing red (gpio38)
            if (time_now - time_buzzer >= 6): #wait 3s pour prendre la main
                time_buzzer = time_now
                blink_color(pixels, blink_times = 3, color=(0, 0, 255))
                print(f"falling edge detected on {channel}\n")
                #time_buzzer = time_now
            time_stamp_red = time_now

  



# when a falling edge is detected on port 17, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(40, GPIO.FALLING, callback=my_callback, bouncetime=200)  
  
# when a falling edge is detected on port 23, regardless of whatever   
# else is happening in the program, the function my_callback2 will be run  
# 'bouncetime=300' includes the bounce control written into interrupts2a.py  
GPIO.add_event_detect(38, GPIO.FALLING, callback=my_callback, bouncetime=200)  


if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()

    
    # Runs function
    try:
        while(1):
            sleep(5)

    except KeyboardInterrupt:  
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
    GPIO.cleanup()

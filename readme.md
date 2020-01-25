# Buzzer for Raspberry #

A two buzzers system that I developped for game quizz with friends.


## Needed ##

* Two big button dome or equivalent
* A WS2801 Led strip
* A raspberry (v.3 model B)
* An external 5V power supply


1. Wiring

2. Launch

Once everythoig connected 

* Make sure spi connection is activated (type raspi-config in a terminal then 5. Interface Option > P4 SPI Enable)

* Install WS2801 driver:
```
pip install adafruit-ws2801
```

* Install GPio managment:
```
sudo apt install python3-rpi.gpio
```


* Run the script with python3:

```
python buzzer.py
```

When a buzzer is pushed, the team has 6 seconds before a new push is detected.




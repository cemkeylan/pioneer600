#!/usr/bin/python
# -*- coding:utf-8 -*-
# Cem KEYLAN
# 2018
# Version 1.0


import RPi.GPIO as GPIO
import smbus
import spidev as SPI
import SSD1306
import time
import Image
import ImageDraw
import ImageFont
import os
import add_module

KEY = 20
address = 0x20
main_menu = 1
submenus = 1


def beep_on():
	bus.write_byte(address,0x7F&bus.read_byte(address))
def beep_off():
	bus.write_byte(address,0x80|bus.read_byte(address))
def led_off():
	bus.write_byte(address,0x10|bus.read_byte(address))
def led_on():
	bus.write_byte(address,0xEF&bus.read_byte(address))


def oled(Line1, Line2, Line3=""):
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top), str(Line1), font=font1, fill=255)
        draw.text((x, top+20), str(Line2), font=font2, fill=255)
	draw.text((x, top+40), str(Line3), font=font2, fill=255)
        disp.image(image)
        disp.display()

def MyInterrupt(KEY):
	print("KEY PRESS")

def menu ():
	global values
	global submenus
	global main_menu

	if values == "up" :
		submenus = submenus - 1
	elif values == 'down' :
		submenus = submenus + 1
	elif values == "right" :
		main_menu = main_menu + 1
		submenus = 1
	elif values == "left" :
		main_menu = main_menu - 1
		submenus = 1

	if main_menu == 5:
		main_menu = 1
	if main_menu == 0:
		main_menu = 4

	# Main Information delivering up status
	if main_menu == 1 :

		if submenus == 4:
			submenus = 1
		if submenus ==0:
			submenus =3

		if submenus == 1:
			if len(os.popen("hostname -I").read()) == 1 :
				upstatus = "Down"
			else:
				upstatus = "UP"
			oled("Status = " + upstatus,os.popen("hostname -I").read(),"by Cem Keylan")
		elif submenus == 3 :
			if "active" in os.popen("sudo service ssh status").read():
				upssh = "UP"
			else:
				upssh = "DOWN"
			oled("SSH Server", upssh)
		elif submenus == 2 :
			if len(os.popen("hostname -I").read()) is not 1:
				if "unreachable" in os.popen("nc 8.8.8.8 53 -zv").read():
					oled("Connection", "could NOT be","established.")
				else:
					oled("Connection","could be","established.")


	# Device Info
	elif main_menu == 2:

		if submenus == 5:
			submenus = 1
		if submenus ==0:
			submenus =4

		if submenus == 4 :
			oled("Device Info","CPU Temperature=",(add_module.getCPUtemperature()+" C"))
		elif submenus == 2 :
			oled("Device Info","Free RAM",(str(int(add_module.getRAMinfo()[2])/1024)+" MB"))
		elif submenus == 3 :
			oled("Device Info","CPU Usage",(str(add_module.getCPUuse())+" %"))
		elif submenus == 1 :
			oled("Device Info","Disk Usage",add_module.getDiskSpace()[3])

	#aç kapa
	elif main_menu == 3 :

		if submenus == 4:
			submenus = 1
		if submenus == 0:
			submenus = 3

		elif submenus == 1 :
			oled("System","Close App","Press Button")
			if GPIO.input(KEY) == 0:
				if len(os.popen("hostname -I").read()) is not 1:
					exit ()
				else:
					oled("System","Close App","Must be connected")
					time.sleep(2)
		elif submenus == 2 :
			oled("System","Reboot","Press Button")
			if GPIO.input(KEY) == 0:
				os.popen('sudo reboot')
		elif submenus == 3 :
			oled("System","Halt System","Press Button")
			if GPIO.input(KEY) == 0:
				os.popen('sudo halt')


	#interfaces
	elif main_menu == 4 :
		note = os.popen("sudo ifconfig").read()
		if submenus == 3 :
			submenus = 1
		if submenus == 0 :
			submenus = 2
		elif submenus == 2 :
			if "eth0" in note:
				oled("Interfaces", "Eth0 Enabled", "Press Button")
				if GPIO.input(KEY) == 0:
					os.popen("sudo ifconfig eth0 down")
			else:
				oled("Interfaces", "Eth0 Disabled", "Press Button")
				if GPIO.input(KEY) == 0:
					os.popen("sudo ifconfig eth0 up")
		elif submenus == 1:
			if "wlan0" in note:
				oled("Interfaces","Wlan0 Enabled", "Press Button")
				if GPIO.input(KEY) == 0:
					os.popen("sudo ifconfig wlan0 down")
			else:
				oled("Interfaces","Wlan0 Disabled", "Press Button")
				if GPIO.input(KEY) == 0:
					os.popen("sudo ifconfig wlan0 up")


	else :
		print ("Something went wrong")

	return (submenus)

# Raspberry Pi pin configuration:
RST = 19
# Note the following are only used with SPI:
DC = 16
bus = 0
device = 0

# 128x64 display with hardware SPI:
disp = SSD1306.SSD1306(RST, DC, SPI.SpiDev(bus,device))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 1
top = padding
x = padding
# Load default font.
# font = ImageFont.load_default()
font_dir =  os.path.dirname(os.path.realpath(__file__)) +"/KeepCalm-Medium.ttf"
font1 = ImageFont.truetype(font_dir, 15)
font2 = ImageFont.truetype(font_dir, 14)

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY,GPIO.IN,GPIO.PUD_UP)
#GPIO.add_event_detect(KEY,GPIO.FALLING,MyInterrupt,200)

#bmp = BMP180()
bus = smbus.SMBus(1)

print("Starting...")
print("Version 1.0")

try:
	while True:

		bus.write_byte(address,0x0F|bus.read_byte(address))
		value = bus.read_byte(address) | 0xF0
		if value != 0xFF:
			led_on()
			if (value | 0xFE) != 0xFF:
				values= "left"
			elif (value | 0xFD) != 0xFF:
				values= "up"
			elif (value | 0xFB) != 0xFF:
				values= "down"
			else :
				values= "right"
			while value != 0xFF:
				bus.write_byte(address,0x0F|bus.read_byte(address))
				value = bus.read_byte(address) | 0xF0
				time.sleep(0.01)
			led_off()
			submenus=menu()

		time.sleep(0.1)
		values= "YOK"
		submenus=menu()

# for keyboard interrupt
except (KeyboardInterrupt, SystemExit):
	print ("Keyboard Interrupt")
	# Clear display.
	disp.clear()
	disp.display()

except:
	print ("ERROR")
	# Clear display.
	oled("There was an error","")
	time.sleep(2)
	disp.clear()
	disp.display()

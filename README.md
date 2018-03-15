Introduction: 
		Email Notifier is a Raspberry Pi based project using SenseHAT along with the Pi that notifies when the user gets any new email. Right now it shows whenever it gets a new email irrespective of the sender and the content. But it can be customized and priorities can be assigned so that it will notify only when an important email is received. Any model of Raspberry Pi (Except Raspberry Pi 1 A/B) can be used for this project provided it has an active internet connection. The user can also integrate other services like social media notifications, which I will cover in some other post. As a notification, the RGB LEDs present over the SenseHAT is used and all LED simultaneously glow RED if a new email is received. Again the LEDs can generate many colors and generated color for notification can be customized depending upon the sender of the mail and priority. Instead of SenseHAT external WS2812B based modules like neopixel can also be used with a little b it of tinkering of the code or even normal RGB LEDs can be used with GPIOs. The code is written in python.
Required Hardware:
o	Raspberry Pi
o	SenseHAT for Raspberry Pi
o	SD card for Raspberry Pi with Raspbian
o	Power Supply for Raspberry Pi

Hardware Setup:
o	Insert the SD card to the Raspberry Pi
o	Connect the SenseHAT module to the Pi GPIO header
o	Connect an Ethernet cable to the Pi with internet connectivity (For wired Ethernet connection. Not required if Wi-Fi is used.)
o	If Pi is not to be operated headless mode, connect a Display, Keyboard, and Mouse to Raspberry Pi.
o	Connect the power supply to the Raspberry Pi and turn it on and wait till it gets booted up.

Python packages used:
	sense _hat: Support for SenseHAT add-on board for Raspberry Pi
	imaplib: Supports IMAP protocol to fetch emails from Gmail.
	Datetime: The datetime module supplies classes for manipulating dates and times in both simple and complex ways
	Time		: This module provides various time-related functions

Getting Started:
	SSH Access: 
		If the Raspberry Pi is being used in Headless mode i: e. no Display is connected, it can be accessed from other PC using SSH but both should have to be on the same network. Plug in the SD card to any PC and create an empty file named SSH to boot folder to enable SSH connection. If the file is not created, as per the new Raspbian OS Raspberry Pi will not accept SSH connection. Connect to the Pi using SSH if that is being used or otherwise open up the terminal in Raspberry Pi in the connected display by using Keyboard and mouse.
	After we have access to terminal of Pi by using SSH or Display we then need to add the package to support SenseHAT on Raspberry Pi. To do that uses the following commands,
		$sudo apt-get update 
		$sudo apt-get install sense-hat

	After SenseHAT library is installed copy the code below to a file and make the necessary changes like username, password etc. and run the code.
		$sudo python file_name.py

	To run the script automatically on boot you can use crontab.

Code/ Downloads:
	 
Conclusion: 
	The Notifier works fine and as in the code it has been tested with Gmail. But it can be used with any Email service provider. Along with the LEDs, some additional peripherals can be used with the Raspberry Pi to make an interactive email client. This project demonstrates the usage of email and the concept can even be used in other applications like home automation.

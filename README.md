Email Notifier
--------------------------------------------------------------- 
Introduction: Email Notifier is a Raspberry Pi based project using SenseHAT along with the Pi that notifies when the user gets any new email. Right now it shows whenever it gets a new email irrespective of the sender and the content. But it can be customized and priorities can be assigned so that it will notify only when an important email is received. Any model of Raspberry Pi (Except Raspberry Pi 1 A/B) can be used for this project provided it has an active internet connection. The user can also integrate other services like social media notifications, which I will cover in some other post. As a notification, the RGB LEDs present over the SenseHAT is used and produces and email icon, ehich blinks if a new email is received. Again the LEDs can generate many colors and generated icon for notification can be customized depending upon the sender of the mail and priority. Instead of SenseHAT external WS2812B based modules like neopixel can also be used with a little bit of tinkering of the code or even normal RGB LEDs can be used with GPIOs. The code is written in python.
Required Hardwares:
--------------------------------------------------------------------
Raspberry Pi
SenseHAT for Raspberry Pi
SD card for Raspberry Pi with Raspbian
Power Supply for Raspberry Pi

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
After we have access to terminal of Pi by using SSH or Display we then need to add the package to support SenseHAT on Raspberry Pi . To do that uses the following commands,
$sudo apt-get update 
$sudo apt-get install sense-hat
We then need to add the packages to support email on Raspberry Pi as by default the required packages are not installed. As python packages can be installed by using pip (By default not installed), it has to be installed first to the pi. To install pip and later email package use the following commands,

$sudo apt-get install python-pip #install pip for python package installation.
$sudo pip install email
After SenseHAT and email libraries are installed copy the code below to a file and make the necessary changes like username, password etc. and run the code.
$sudo python file_name.py

To run the script automatically on boot you can use crontab.

Code/ Downloads:
import imaplib
import datetime
import time
import email
from sense_hat import SenseHat


IMAP_ADDRESS='imap.gmail.com'
EMAIL_ID='your_id@gmail.com'#Replace with your Email ID
PASSWORD='your_pwd' #Replace your Email Password
sense = SenseHat()

X = [255, 0, 0]  # Red
O = [0, 0, 0]  # off

email_icon = [  ## Change this for notification color.
O, O, O, O, O, O, O, O,
X, X, X, X, X, X, X, X,
X, X, O, O, O, O, X, X,
X, O, X, O, O, X, O, X,
X, O, O, X, X, O, O, X,
X, O, O, O, O, O, O, X,
X, X, X, X, X, X, X, X,
O, O, O, O, O, O, O, O
]
#sense.set_pixels(email_icon)
# Function to read email inbox
def read_email():
  try:
    print 'Checking new Emails.'
    mail = imaplib.IMAP4_SSL(IMAP_ADDRESS)
    mail.login(EMAIL_ID,PASSWORD)
    #mail.select()

    mail.select(readonly=1)#Email will not marked as seen.
    type, data = mail.search(None, '(UNSEEN)')#only fetch unread emails
    mail_ids = data[0]
    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    for i in id_list:
      typ, data = mail.fetch(i, '(RFC822)' )

      for response_part in data:
        if isinstance(response_part, tuple):
         msg = email.message_from_string(response_part[1])
        #print msg['from']
        try:
          try:
            time_delta=(datetime.datetime.now()-datetime.datetime.strptime(msg['date'][0:25],'%a, %d %b %Y %H:%M:%S')).total_seconds()#Email date format Mon, 19 Feb 2018 23:34:11 -0800 (PST) or
          except Exception,e:
          #print str(e)
            time_delta=(datetime.datetime.now()-datetime.datetime.strptime(msg['date'][0:20],'%d %b %Y %H:%M:%S')).total_seconds()#Email date format 20 Feb 2018 03:03:48 -050
            print time_delta
          if(time_delta < 180): #Notify only email is recived in last 3 minutes
            glow_led(msg['from'],msg['subject'])
        except Exception,e:
          print ''
          print str(e)
      #print 'Unable to convert time.'
  except Exception, e:
    print str(e)

def glow_led(sender,subject):
  print 'New message is about to get notified from '+sender
  i=0
  for i in range(0,10): #Blink the LEDs for 10 times
    sense.set_pixels(email_icon)
    time.sleep(1)
    sense.clear()
    time.sleep(0.5)
    i+=1

print 'Welcome Email Notifier'

while 1:
  read_email()
  time.sleep(60)#check for new emails every 60 seconds.

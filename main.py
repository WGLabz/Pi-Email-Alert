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

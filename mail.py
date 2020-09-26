#!/usr/bin/env python3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import base


# https://www.google.com/settings/security/lesssecureapps
# https://accounts.google.com/DisplayUnlockCaptcha

# Send an email letter with an appropriate report attached
# --- in
# * str(report_type)
# * str(report_path_)
# * str(report_name_)
# * str(date_)
# --- out
# None
# -----------------
def regular_report(report_type, report_path_, report_name_, date_):
    mail_content = '''
    Hello,

    Find the report document attached.
    
    Best Regards,
    Your Bot
    '''

    message = MIMEMultipart() # instance of MIMEMultipart 
    message['From'] = base.SENDER_ADDRESS
    message['To'] = base.RECEIVER_ADDRESS
    message['Subject'] = 'Binance bot; ' + base.TRADING_PAIR + ' (' + report_type + ' Report: ' + date_ + ')'
      
    message.attach(MIMEText(mail_content, 'plain'))  # attach the body with the msg instance 
    
    attachment = open(report_path_, "rb") # open the file to be sent 
      
    payload = MIMEBase('application', 'octet-stream') # instance of MIMEBase and named as 'payload'
    payload.set_payload((attachment).read())  # To change the payload into encoded form 
      
    encoders.encode_base64(payload)  # encode into base64 

    payload.add_header('Content-Disposition', "attachment; filename= %s" % report_name_)  # attach the instance 'payload' to instance 'message' 
    message.attach(payload) 
      
    session = smtplib.SMTP('smtp.gmail.com', 587)  # creates SMTP session 
    session.starttls()  # start TLS for security  
    session.login(base.SENDER_ADDRESS, base.SENDER_PASS)  # Authentication

    text = message.as_string()  # Converts the Multipart msg into a string 

    session.sendmail(base.SENDER_ADDRESS, base.RECEIVER_ADDRESS, text)  # sending the mail
    session.quit() # terminating the session

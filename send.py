#!/usr/bin/env python3

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import bot

# https://www.google.com/settings/security/lesssecureapps
# https://accounts.google.com/DisplayUnlockCaptcha

def send_daily_report(report_name_, date_):
    mail_content = '''
    Hello,
    
    This is a Daily Report email.
    Find the report document attached.
    
    Best Regards,
    Your Bot
    '''

    message = MIMEMultipart() # instance of MIMEMultipart 
    message['From'] = bot.SENDER_ADDRESS
    message['To'] = bot.RECEIVER_ADDRESS
    message['Subject'] = 'Binance bot; ' + bot.TRADING_PAIR + ' (Daily Report: ' + date_ + ')'
      
    message.attach(MIMEText(mail_content, 'plain'))  # attach the body with the msg instance 
    
    attachment = open('reports/daily/' + report_name_, "rb") # open the file to be sent 
      
    payload = MIMEBase('application', 'octet-stream') # instance of MIMEBase and named as 'payload'
    payload.set_payload((attachment).read())  # To change the payload into encoded form 
      
    encoders.encode_base64(payload)  # encode into base64 

    payload.add_header('Content-Disposition', "attachment; filename= %s" % report_name_)  # attach the instance 'payload' to instance 'message' 
    message.attach(payload) 
      
    session = smtplib.SMTP('smtp.gmail.com', 587)  # creates SMTP session 
    session.starttls()  # start TLS for security  
    session.login(bot.SENDER_ADDRESS, bot.SENDER_PASS)  # Authentication

    text = message.as_string()  # Converts the Multipart msg into a string 

    session.sendmail(bot.SENDER_ADDRESS, bot.RECEIVER_ADDRESS, text)  # sending the mail
    session.quit() # terminating the session
    
def send_weekly_report(report_name_, date_):
    mail_content = '''
    Hello,
    
    This is a Weekly Report email.
    Find the report document attached.
    
    Best Regards,
    Your Bot
    '''

    message = MIMEMultipart() # instance of MIMEMultipart 
    message['From'] = bot.SENDER_ADDRESS
    message['To'] = bot.RECEIVER_ADDRESS
    message['Subject'] = 'Binance bot; ' + bot.TRADING_PAIR + ' (Weekly Report: ' + date_ + ')'
      
    message.attach(MIMEText(mail_content, 'plain'))  # attach the body with the msg instance 
    
    attachment = open('reports/weekly/' + report_name_, "rb") # open the file to be sent 
      
    payload = MIMEBase('application', 'octet-stream') # instance of MIMEBase and named as 'payload'
    payload.set_payload((attachment).read())  # To change the payload into encoded form 
      
    encoders.encode_base64(payload)  # encode into base64 

    payload.add_header('Content-Disposition', "attachment; filename= %s" % report_name_)  # attach the instance 'payload' to instance 'message' 
    message.attach(payload) 
      
    session = smtplib.SMTP('smtp.gmail.com', 587)  # creates SMTP session 
    session.starttls()  # start TLS for security  
    session.login(bot.SENDER_ADDRESS, bot.SENDER_PASS)  # Authentication

    text = message.as_string()  # Converts the Multipart msg into a string 

    session.sendmail(bot.SENDER_ADDRESS, bot.RECEIVER_ADDRESS, text)  # sending the mail
    session.quit() # terminating the session
    
def send_monthly_report(report_name_, date_):
    mail_content = '''
    Hello,
    
    This is a Monthly Report email.
    Find the report document attached.
    
    Best Regards,
    Your Bot
    '''

    message = MIMEMultipart() # instance of MIMEMultipart 
    message['From'] = bot.SENDER_ADDRESS
    message['To'] = bot.RECEIVER_ADDRESS
    message['Subject'] = 'Binance bot; ' + bot.TRADING_PAIR + ' (Monthly Report: ' + date_ + ')'
      
    message.attach(MIMEText(mail_content, 'plain'))  # attach the body with the msg instance 
    
    attachment = open('reports/monthly/' + report_name_, "rb") # open the file to be sent 
      
    payload = MIMEBase('application', 'octet-stream') # instance of MIMEBase and named as 'payload'
    payload.set_payload((attachment).read())  # To change the payload into encoded form 
      
    encoders.encode_base64(payload)  # encode into base64 

    payload.add_header('Content-Disposition', "attachment; filename= %s" % report_name_)  # attach the instance 'payload' to instance 'message' 
    message.attach(payload) 
      
    session = smtplib.SMTP('smtp.gmail.com', 587)  # creates SMTP session 
    session.starttls()  # start TLS for security  
    session.login(bot.SENDER_ADDRESS, bot.SENDER_PASS)  # Authentication

    text = message.as_string()  # Converts the Multipart msg into a string 

    session.sendmail(bot.SENDER_ADDRESS, bot.RECEIVER_ADDRESS, text)  # sending the mail
    session.quit() # terminating the session

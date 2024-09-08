from email.message import EmailMessage
import os
import random
import smtplib

# smpt_object = smtplib.SMTP('smpt.gmail.com', 587)

otp: str = ""
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

try:
    for i in range(6):
        otp += str(random.randint(6, 9))

    # provision the server and its host for 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Add senders email credentials
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    to_mail = "24hozblog@gmail.com"

    # Message subject body and format
    msg = EmailMessage()
    msg['Subject'] = "OTP Verfication"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_mail
    msg.set_content('Your OTP is: ' + otp)

    server.send_message(msg)

    # otp verification
    user_otp = input("Enter Your OTP: ")
    if user_otp == otp:
        print('valid')
    else:
        print("invalid")
    print('Email sent')
except Exception as e:
    print({'error': 'Network error'}, e)

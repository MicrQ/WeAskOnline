#!/usr/bin/env python3
from email.message import EmailMessage
import os
import random
import smtplib
import ssl

from flask import jsonify

# smpt_object = smtplib.SMTP('smpt.gmail.com', 587)

def send_token(email: str = None):
    otp: str = ""
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    if not email:
        return jsonify({"error": "Email required"}), 400

    try:
        for i in range(2):
            otp += str(random.randint(10809, 99999))

        # provision the server and its host for sending email with SSL
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)

        # Add senders email credentials
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        RECIEVER_EMAIL = email.lower()

        # Message subject body and format
        msg = EmailMessage()
        msg['Subject'] = "OTP Verfication"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIEVER_EMAIL
        msg.set_content('Your OTP is: ' + otp)

        server.sendmail(EMAIL_ADDRESS, RECIEVER_EMAIL, msg.as_string())
        print('Email sent')

        # otp verification
    except Exception as e:
        print("Email not sent")
        print({'error': 'Network error'}, e)

def verify_token(token: int, user_token: int) -> bool:
    """
    Used to verify token sent to users email and check if the OTP passed is
    Valid"""
    if not user_token:
        return jsonify({"error": "Please, provide OTP"}), 400
    if token == user_token:
        return True
    else:
        return False

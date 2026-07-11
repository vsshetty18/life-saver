"""
Notification Utilities
Handles sending SMS (via Twilio) and Email (via SMTP) alerts.
Both functions fail gracefully (return False) instead of crashing the app,
since notification services can go down or have bad credentials.
"""

import smtplib
from email.mime.text import MIMEText
from flask import current_app
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def send_sms(to_number, message):
    """
    Sends an SMS using Twilio.
    Returns True if sent successfully, False otherwise.
    """
    try:
        account_sid = current_app.config["TWILIO_ACCOUNT_SID"]
        auth_token = current_app.config["TWILIO_AUTH_TOKEN"]
        from_number = current_app.config["TWILIO_PHONE_NUMBER"]

        # If Twilio credentials are not set up, skip silently (useful during dev/demo)
        if not account_sid or not auth_token or not from_number:
            print("[SMS] Twilio not configured. Skipping SMS send.")
            return False

        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        print(f"[SMS] Sent successfully to {to_number}")
        return True

    except TwilioRestException as e:
        print(f"[SMS] Twilio error: {e}")
        return False
    except Exception as e:
        print(f"[SMS] Unexpected error: {e}")
        return False


def send_email(to_email, subject, body):
    """
    Sends an email using SMTP (e.g. Gmail).
    Returns True if sent successfully, False otherwise.
    """
    try:
        smtp_server = current_app.config["SMTP_SERVER"]
        smtp_port = current_app.config["SMTP_PORT"]
        smtp_email = current_app.config["SMTP_EMAIL"]
        smtp_password = current_app.config["SMTP_PASSWORD"]

        # If SMTP credentials are not set up, skip silently (useful during dev/demo)
        if not smtp_server or not smtp_email or not smtp_password:
            print("[EMAIL] SMTP not configured. Skipping email send.")
            return False

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = smtp_email
        msg["To"] = to_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # secure the connection
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, to_email, msg.as_string())

        print(f"[EMAIL] Sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"[EMAIL] Unexpected error: {e}")
        return False

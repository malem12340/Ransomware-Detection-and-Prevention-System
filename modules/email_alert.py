import smtplib
import time
import os

from email.message import EmailMessage
from dotenv import load_dotenv


# Load .env file
load_dotenv()


class EmailAlert:

    def __init__(self):

        # ---------------------------------------
        # Gmail Configuration
        # ---------------------------------------

        self.sender_email = os.getenv("EMAIL_SENDER")
        self.app_password = os.getenv("EMAIL_APP_PASSWORD")
        self.receiver_email = os.getenv("EMAIL_RECEIVER")

        # ---------------------------------------
        # Email Cooldown
        # ---------------------------------------

        self.cooldown_seconds = 60

        # Store last email time for each alert type
        self.last_sent = {}


    def send_alert(self, alert_type, description, severity):

        current_time = time.time()

        # ---------------------------------------
        # Check Cooldown
        # ---------------------------------------

        last_time = self.last_sent.get(alert_type, 0)

        if current_time - last_time < self.cooldown_seconds:

            print(
                f"📧 Email skipped - {alert_type} "
                f"(cooldown active)"
            )

            return


        # ---------------------------------------
        # Check Email Configuration
        # ---------------------------------------

        if not self.sender_email:
            print("❌ EMAIL_SENDER is not configured")
            return

        if not self.app_password:
            print("❌ EMAIL_APP_PASSWORD is not configured")
            return

        if not self.receiver_email:
            print("❌ EMAIL_RECEIVER is not configured")
            return


        # ---------------------------------------
        # Create Email
        # ---------------------------------------

        message = EmailMessage()

        message["Subject"] = (
            f"RDPS Security Alert - {severity}"
        )

        message["From"] = self.sender_email
        message["To"] = self.receiver_email


        body = f"""
RANSOMWARE DETECTION AND PREVENTION SYSTEM
===========================================

Security Alert Detected

Alert Type : {alert_type}
Severity   : {severity}

Description:
{description}

Please check the RDPS dashboard immediately.

This is an automated security notification.
"""

        message.set_content(body)


        # ---------------------------------------
        # Send Email
        # ---------------------------------------

        try:

            with smtplib.SMTP_SSL(
                "smtp.gmail.com",
                465
            ) as server:

                server.login(
                    self.sender_email,
                    self.app_password
                )

                server.send_message(message)


            # Save time only after successful email
            self.last_sent[alert_type] = current_time

            print("📧 Email alert sent successfully")


        except Exception as e:

            print("❌ Email sending failed:", e)
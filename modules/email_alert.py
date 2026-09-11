import smtplib
import time
from email.message import EmailMessage


class EmailAlert:

    def __init__(self):

        # Sender Gmail address
        self.sender_email = "YOUR_GMAIL@gmail.com"

        # Google App Password
        self.app_password = "16_DIGIT_APP_PASSWORD"

        # Email where you want to receive alerts
        self.receiver_email = "YOUR_GMAIL@gmail.com"
         # Email cooldown in seconds
        self.cooldown_seconds = 60

        # Store last email time for each alert type
        self.last_sent = {}

    def send_alert(self, alert_type, description, severity):
        current_time = time.time()

        # Check cooldown
        last_time = self.last_sent.get(alert_type, 0)

        if current_time - last_time < self.cooldown_seconds:

            print(
                f"📧 Email skipped - {alert_type} "
                f"(cooldown active)"
            )

            return

        message = EmailMessage()

        message["Subject"] = f"🚨 RDPS Security Alert - {severity}"
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

        try:

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

                server.login(
                    self.sender_email,
                    self.app_password
                )

                server.send_message(message)
                # Save time only after successful email
            self.last_sent[alert_type] = current_time

            print("📧 Email alert sent successfully")

        except Exception as e:

            print(" Email sending failed:", e)
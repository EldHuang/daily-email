import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASS"]

class Email:
    def __init__(self):
        self.connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
        self.connection.starttls()
        self.connection.login(user=EMAIL, password=PASSWORD)

        self.date = datetime.now()
        self.weekday = self.date.strftime("%A")
        self.month = self.date.strftime("%b")
        self.day = self.date.strftime("%d")
        self.year = self.date.strftime("%Y")

    def send_email(self, info):
        msg = EmailMessage()

        infoStr = ""
        for name, content in info.items():
            infoStr += f"{name} >>> {content['overall']}\n                "

        msg["Subject"] = f"{self.weekday}, {self.month} {self.day}, {self.year} Morning Update"
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg.set_content(
            f"""
            Good morning! Here is today's update.
            
            -------- GRADES --------
                {infoStr}
            """
        )

        self.connection.send_message(msg)

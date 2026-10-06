import os
from string import Template
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


    def get_time_of_day(self, hour):
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Nighttime"


    def send_email(self, html_table):
        msg = EmailMessage()
        time_of_day = self.get_time_of_day(hour=(datetime.now().hour)-8)

        msg["Subject"] = f"{self.weekday}, {self.month} {self.day}, {self.year} | {time_of_day} Update"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        # Read html template file
        with open("templates/email_template.html", encoding="utf-8") as file:
            template_content = file.read()

        # Format data into email + pass parameters
        html_template = Template(template_content)
        html_body = html_template.substitute(
            date=f"{self.weekday}, {self.month} {self.day}, {self.year}",
            time_of_day=time_of_day,
            grades_table=html_table,
        )

        msg.add_alternative(html_body, subtype='html')

        self.connection.send_message(msg)

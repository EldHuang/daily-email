import os
from string import Template
import pandas as pd
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

        self.compiledData = {
            "Subject": [],
            "Letter": [],
            "Percent": [],
        }
        self.grades_table = None

    def convert_data(self, info):
        for name, content in info.items():
            self.compiledData["Subject"].append(name)
            self.compiledData["Letter"].append(content['overall'])
            self.compiledData["Percent"].append(content['current_score'])
        pd.set_option('display.unicode.east_asian_width', True)

        self.grades_table = pd.DataFrame(self.compiledData)

    def send_email(self):
        msg = EmailMessage()

        msg["Subject"] = f"{self.weekday}, {self.month} {self.day}, {self.year} Morning Update"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        # Include Mandarin Characters
        html_table = self.grades_table.to_html(index=False, justify='left')

        # Read html file
        with open("email_template.html", encoding="utf-8") as file:
            template_content = file.read()

        # Format data into email
        html_template = Template(template_content)
        html_body = html_template.substitute(
            date=f"{self.weekday}, {self.month} {self.day} {self.year}",
            grades_table=html_table,
        )

        msg.add_alternative(html_body, subtype='html')

        self.connection.send_message(msg)

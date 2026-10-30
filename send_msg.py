from string import Template
import smtplib
from datetime import datetime
from email.message import EmailMessage
import pytz




class Email:
    def __init__(self, email, password):
        self.EMAIL = email
        self.PASSWORD = password
        self.connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
        self.connection.starttls()
        self.connection.login(user=self.EMAIL, password=self.PASSWORD)

        pacific = pytz.timezone('America/Los_Angeles')
        
        self.date = datetime.now(pacific)
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
        time_of_day = self.get_time_of_day(hour=datetime.now().hour)

        msg["Subject"] = f"{self.weekday}, {self.month} {self.day}, {self.year} | {time_of_day} Update"
        msg["From"] = self.EMAIL
        msg["To"] = self.EMAIL

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

import os
import requests
from dotenv import load_dotenv

class Weather:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("WEATHER_TOKEN")
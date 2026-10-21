import os
import requests
from dotenv import load_dotenv

class Weather:
    def __init__(self):
        # load_dotenv()
        self.token = os.environ.get("WEATHER_TOKEN")

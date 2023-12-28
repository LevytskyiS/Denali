from configparser import ConfigParser

config = ConfigParser()
config.read("config/config.ini")

API_KEY = config.get("TG", "API_KEY")
MY_ID = config.get("TG", "MY_ID")

INSTAGRAM_LOGIN = config.get("TG", "INSTAGRAM_LOGIN")
INSTAGRAM_PASSWORD = config.get("TG", "INSTAGRAM_PASSWORD")

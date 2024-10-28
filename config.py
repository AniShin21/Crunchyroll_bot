# config.py

import os

API_ID = int(os.getenv("API_ID", "22713841"))  # Replace with your actual API_ID
API_HASH = os.getenv("API_HASH", "972be8fd02f4e9d94f7978d63d13bc00")  # Replace with your actual API_HASH
BOT_TOKEN = os.getenv("BOT_TOKEN", "7879690371:AAHGgAVoLe92D-r3vTs4I7oUGAcwDaG6p70")  # Replace with your actual BOT_TOKEN
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "6043529845 7138310520 6450266465").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

START_MSG = os.environ.get("START_MESSAGE", "<b><i>Welcome, {first}{last}!\n 🍥 You've entered the Crunchyroll Premium Bot! Unlock Premium accounts with 20 points/coins. Join our channel below and stay connected for free points surprises from the bot owner. Start collecting and dive into endless anime streaming! 🎌✨📺</i></b>")

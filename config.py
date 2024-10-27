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

START_MSG = os.environ.get("START_MESSAGE", "Hᴇʟʟᴏ ᴛʜᴇʀᴇ {first}!\nɪ ᴀᴍ ᴀ ꜰɪʟᴇ ʙᴏᴛ\nᴘᴏᴡᴇʀᴇᴅ ʙʏ : @HKB_ANIME\nɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ᴘʀɪᴠᴀᴛᴇ ꜰɪʟᴇꜱ\nᴛʜʀᴏᴜɢʜ ᴛʜᴇ ꜱᴘᴇᴄɪᴀʟ ʟɪɴᴋꜱ ♡")

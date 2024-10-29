from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, TG_BOT_WORKERS
from flask import Flask, request
import os

app = Flask(__name__)  # Create a Flask application

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="CrunchyrollBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS
        )

telegram_bot = Bot()  # Create an instance of the Bot class

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.json
    return 'Webhook received!', 200

if __name__ == "__main__":
    try:
        telegram_bot.start()  # Non-blocking start of the Pyrogram bot
        print("Bot started successfully!")
        app.run(host='0.0.0.0', port=8080)  # Start Flask server on port 8080
    except Exception as e:
        print(f"Failed to start the bot: {e}")

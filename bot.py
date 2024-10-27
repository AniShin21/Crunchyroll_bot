from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, TG_BOT_WORKERS  # Ensure all necessary imports
from pyromod import listen
class Bot(Client):
    def __init__(self):
        super().__init__(
            name="CrunchyrollBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"},  # Load plugins from the plugins folder
            workers=TG_BOT_WORKERS  # Number of workers for handling messages
        )

if __name__ == "__main__":
    app = Bot()  # Create an instance of the Bot class
    app.run()  # Start the bot

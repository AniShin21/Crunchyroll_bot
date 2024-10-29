from pyrogram import Client
from pyromod import listen
from config import API_ID, API_HASH, BOT_TOKEN, TG_BOT_WORKERS
from aiohttp import web  # Import aiohttp for running a web server
import asyncio

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

    async def start_server(self):
        """Start a dummy web server for Koyeb deployment"""
        app = web.Application()
        app.add_routes([web.get("/", self.handle)])
        runner = web.AppRunner(app)
        await runner.setup()
        port = int(os.getenv("PORT", 8080))  # Use PORT env variable, default to 8080
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        print(f"Web server running on port {port}")

    async def handle(self, request):
        """Simple handler for web server requests"""
        return web.Response(text="CrunchyrollBot is running!")

    async def start(self):
        await super().start()  # Start the bot
        await self.start_server()  # Start the web server

    async def stop(self, *args):
        await super().stop()
        print("CrunchyrollBot has stopped")

if __name__ == "__main__":
    app = Bot()
    app.run()  # Start both the bot and the dummy web server

# plugins/broadcast.py

from pyrogram import filters, Client
from pyrogram.types import Message
from database import full_userbase, del_user
import asyncio
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from config import ADMINS

@Client.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Client, message: Message):
    if message.reply_to_message:
        users = await full_userbase()  # Fetch the list of users from the database
        broadcast_msg = message.reply_to_message
        total, successful, blocked, deleted, unsuccessful = 0, 0, 0, 0, 0

        pls_wait = await message.reply("Broadcasting message... This might take a while.")

        for chat_id in users:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except Exception as ex:
                unsuccessful += 1
                print(f"Failed to broadcast to {chat_id}: {ex}")

            total += 1

        status = f"""<b><u>Broadcast Completed</u></b>
Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked: <code>{blocked}</code>
Deleted: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code>"""

        await pls_wait.edit(status)

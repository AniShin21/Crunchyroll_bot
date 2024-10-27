# ban_unban.py

from pyrogram import Client, filters
from pyrogram.types import Message
from accounts_store import banned_users, BANNED_MESSAGE, unban
from config import ADMINS

# Command to ban a user
@Client.on_message(filters.command("ban") & filters.user(ADMINS))
async def ban_user(client: Client, message: Message):
    try:
        user_id = int(message.command[1])
        if user_id not in banned_users:
            banned_users.append(user_id)
            await message.reply_text(f"User {user_id} has been banned.")
        else:
            await message.reply_text("User is already banned.")
    except (IndexError, ValueError):
        await message.reply_text("Usage: /ban <user_id>")

# Command to unban a user
@Client.on_message(filters.command("unban") & filters.user(ADMINS))
async def unban_user(client: Client, message: Message):
    try:
        user_id = int(message.command[1])
        if user_id in banned_users:
            banned_users.remove(user_id)
            await message.reply_text(f"User {user_id} has been unbanned.")
        else:
            await message.reply_text("User is not banned.")
    except (IndexError, ValueError):
        await message.reply_text("Usage: /unban <user_id>")

# Notify banned users when they try to access restricted commands
@Client.on_message(~unban)
async def notify_banned_user(client: Client, message: Message):
    await message.reply_text(BANNED_MESSAGE)

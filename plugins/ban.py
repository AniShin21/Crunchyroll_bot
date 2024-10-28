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
            await message.reply_text(f"𝚄𝚜𝚎𝚛 {user_id} 𝚑𝚊𝚜 𝚋𝚎𝚎𝚗 𝚋𝚊𝚗𝚗𝚎𝚍.")
        else:
            await message.reply_text("𝚄𝚜𝚎𝚛 𝚒𝚜 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚋𝚊𝚗𝚗𝚎𝚍.")
    except (IndexError, ValueError):
        await message.reply_text("𝚄𝚜𝚊𝚐𝚎: /𝚋𝚊𝚗 <𝚞𝚜𝚎𝚛_𝚒𝚍>")

# Command to unban a user
@Client.on_message(filters.command("unban") & filters.user(ADMINS))
async def unban_user(client: Client, message: Message):
    try:
        user_id = int(message.command[1])
        if user_id in banned_users:
            banned_users.remove(user_id)
            await message.reply_text(f"User {user_id} has been unbanned.")
        else:
            await message.reply_text("𝚄𝚜𝚎𝚛 𝚒𝚜 𝚗𝚘𝚝 𝚋𝚊𝚗𝚗𝚎𝚍.")
    except (IndexError, ValueError):
        await message.reply_text("𝚄𝚜𝚊𝚐𝚎: /𝚞𝚗𝚋𝚊𝚗 <𝚞𝚜𝚎𝚛_𝚒𝚍>")

# Notify banned users when they try to access restricted commands
@Client.on_message(~unban)
async def notify_banned_user(client: Client, message: Message):
    await message.reply_text(BANNED_MESSAGE)

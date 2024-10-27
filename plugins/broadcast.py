# broadcast.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import full_userbase, del_user
import asyncio
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from config import ADMINS

REPLY_ERROR = "<code>Use this command as a reply to any Telegram message without any spaces.</code>"

@Client.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Client, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message

        total, successful, blocked, deleted, unsuccessful = 0, 0, 0, 0, 0

        try:
            buttons_message = await client.ask(
                message.from_user.id,
                "Please send the button text and URL in this format: \nButtonText1:URL1 \nButtonText2:URL2\n\nOr type 'skip' to skip adding buttons.",
                timeout=600
            )
        except asyncio.TimeoutError:
            await message.reply("⏳ Time ran out. Proceeding without adding buttons.")
            buttons_message = None

        buttons = []
        if buttons_message and buttons_message.text.strip().lower() != 'skip':
            button_pairs = buttons_message.text.split(',')
            for pair in button_pairs:
                parts = pair.split(':', 1)
                if len(parts) == 2:
                    text, url = parts
                    buttons.append(
                        [InlineKeyboardButton(text.strip(), url=url.strip())])

        reply_markup = InlineKeyboardMarkup(buttons) if buttons else None

        pls_wait = await message.reply("<i>Broadcasting Message... This will take some time.</i>")

        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id, reply_markup=reply_markup)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id, reply_markup=reply_markup)
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

<b>Total Users:</b> <code>{total}</code>
<b>Successful:</b> <code>{successful}</code>
<b>Blocked Users:</b> <code>{blocked}</code>
<b>Deleted Accounts:</b> <code>{deleted}</code>
<b>Unsuccessful:</b> <code>{unsuccessful}</code>"""

        await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

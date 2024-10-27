from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import START_MSG

# /start command handler
@Client.on_message(filters.command('start') & filters.private)
async def start_message(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="Owner", callback_data="owner"),  # Added callback_data for Owner button
            InlineKeyboardButton(text="Close", callback_data="close"),
        ]
    ]
    
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='Help',
                    callback_data="help"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply_text(
        text=START_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )


# Callback query handler
@Client.on_callback_query(filters.regex('^(close|help|owner)$'))  # Handle only these callback queries
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    
    if data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    elif data == "help":
        await query.message.edit(
            text="<b>Use /claim to claim the points\n\nUse /get to claim your daily account</b>",
            parse_mode=ParseMode.HTML
        )
    
    elif data == "owner":
        await query.answer("Owner button clicked!", show_alert=True)  # Example action for Owner button

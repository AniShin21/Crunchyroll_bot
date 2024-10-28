from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import START_MSG
from accounts_store import unban, add_user


# /start command handler
@Client.on_message(filters.command('start') & filters.private & unban)
async def start_message(client: Client, message: Message, is_callback: bool = False):
    # Get user details
    user_id = message.from_user.id
    username = message.from_user.username or None  # Handle cases where username may be None

    # Add the user to user_data
    await add_user(user_id, username)

    buttons = [
        [
            InlineKeyboardButton(text="Owner", url="https://t.me/SikeNez"),
            InlineKeyboardButton(text="Help", callback_data="help")
        ],
        [
            InlineKeyboardButton(text="Main Channel", url="https://t.me/+Z6twNxKQAKk5NDE5")
        ]
    ]

    # Create the message text
    welcome_text = START_MSG.format(
        first=message.from_user.first_name,
        last=message.from_user.last_name or "",  # Handle cases where last name may be None
        username=None if not username else '@' + username,
        mention=message.from_user.mention,
        id=user_id
    )

    if is_callback:
        # If this is triggered by a callback, edit the existing message
        await message.edit_text(
            text=welcome_text,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
    else:
        # If it's a regular /start command, send a new message
        await message.reply_text(
            text=welcome_text,
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True,
            disable_web_page_preview=True
        )

# User commands with details for the help message
user_commands = [
    {
        "command": "/id",
        "emoji": "🆔",
        "usage": "Displays your user ID.",
        "description": "Use /id to see your unique Telegram user ID."
    },
    {
        "command": "/gift",
        "emoji": "🎁",
        "usage": "Gift coins to other users.",
        "description": "Use /gift followed by the user ID and amount to transfer coins to another user."
    },
    {
        "command": "/balance",
        "emoji": "💰",
        "usage": "Check your coin balance.",
        "description": "Use /balance to view your current coin balance."
    },
    {
        "command": "/redeem",
        "emoji": "🎫",
        "usage": "Redeem a promotional code.",
        "description": "Enter /redeem followed by a code to unlock special features or coins."
    },
    {
        "command": "/leaderboard",
        "emoji": "🏆",
        "usage": "Shows the top users.",
        "description": "Use /leaderboard to see the users with the most coins or points."
    },
    {
        "command": "/get",
        "emoji": "📥",
        "usage": "This will provide a Premium Account",
        "description": "Use /get to get a Premium Account\nIf you have 20 coins"
    }
]

# Function to display the help menu with commands
async def show_help(client: Client, query: CallbackQuery, page: int = 0):
    # Calculate which commands to show on the current page
    start_idx = page * 2
    end_idx = start_idx + 2
    page_commands = user_commands[start_idx:end_idx]

    # Create help text for the current page
    help_text = "<b>User Commands Help</b>\n\n"
    for cmd in page_commands:
        help_text += f"{cmd['emoji']} <b>{cmd['command']}</b>\n"
        help_text += f"<i>Usage:</i> {cmd['usage']}\n"
        help_text += f"<i>Description:</i> {cmd['description']}\n\n"

    # Set up pagination buttons with Home and Close options
    buttons = [
        [InlineKeyboardButton("Home 🏠", callback_data="home")]
    ]

    if page > 0:
        buttons[0].insert(0, InlineKeyboardButton("⬅️ Back", callback_data=f"help_page_{page - 1}"))
    if end_idx < len(user_commands):
        buttons[0].append(InlineKeyboardButton("Next ➡️", callback_data=f"help_page_{page + 1}"))

    reply_markup = InlineKeyboardMarkup(buttons)

    # Edit the help message
    await query.message.edit_text(
        text=help_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

# Callback query handler
@Client.on_callback_query(filters.regex(r"^(close|help|help_page_\d+|home)$"))
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data

    if data == "close":
        await query.message.delete()
        await query.answer("Closed.")

    elif data == "help":
        await show_help(client, query, page=0)
        await query.answer()

    elif data == "home":
        # Return to the start message by editing the current message
        await start_message(client, query.message, is_callback=True)
        await query.answer("Back to Home.")

    elif data.startswith("help_page_"):
        page = int(data.split("_")[-1])
        await show_help(client, query, page=page)
        await query.answer("Navigated to the next page.")

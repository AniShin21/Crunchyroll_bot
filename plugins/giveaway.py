from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import random
import asyncio

from config import ADMINS  # Import ADMINS from your config
from accounts_store import user_data  # Import user_data for accounts
giveaway_info = {}  # Store current giveaway info
entries = []  # Store unique user entries for the giveaway

# Command to start a giveaway (Admin-only)
@Client.on_message(filters.command("st_giving") & filters.user(ADMINS))
async def start_giveaway(client: Client, message: Message):
    # Reset giveaway and entry data
    giveaway_info.clear()
    entries.clear()
    giveaway_info['initiated_by'] = message.from_user.id
    giveaway_info['active'] = True

    await message.reply_text(
        "Starting giveaway setup.\n\n1️⃣ Enter the **number of winners** (e.g., '3' for 1st, 2nd, and 3rd):",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="cancel_giveaway")]])
    )
    giveaway_info['step'] = 'num_winners'

@Client.on_message(filters.text & filters.user(lambda _, __, msg: giveaway_info.get('initiated_by') == msg.from_user.id))
async def setup_giveaway_steps(client: Client, message: Message):
    # Ensure giveaway setup is active
    if not giveaway_info.get('active'):
        return

    step = giveaway_info.get('step')

    if step == 'num_winners':
        # Step 1: Capture number of winners
        try:
            giveaway_info['num_winners'] = int(message.text)
            giveaway_info['rewards'] = []
            giveaway_info['step'] = 'reward'
            giveaway_info['current_winner'] = 1
            await message.reply_text(f"Enter the **coin reward** for the 1st winner:")
        except ValueError:
            await message.reply_text("Please enter a valid number for the number of winners.")

    elif step == 'reward':
        # Step 2: Capture rewards for each winner
        try:
            reward = int(message.text)
            giveaway_info['rewards'].append(reward)
            if len(giveaway_info['rewards']) < giveaway_info['num_winners']:
                winner_position = len(giveaway_info['rewards']) + 1
                await message.reply_text(f"Enter the coin reward for the {winner_position}nd winner:")
            else:
                giveaway_info['step'] = 'time_limit'
                await message.reply_text("Enter the **time limit** for the giveaway in minutes:")
        except ValueError:
            await message.reply_text("Please enter a valid number for the coin reward.")

    elif step == 'time_limit':
        # Step 3: Capture time limit
        try:
            minutes = int(message.text)
            giveaway_info['end_time'] = datetime.now() + timedelta(minutes=minutes)
            giveaway_info['step'] = None  # Giveaway setup complete
            await message.reply_text(
                f"🎉 Giveaway Started!\n**Number of winners:** {giveaway_info['num_winners']}\n"
                f"**Rewards:** {giveaway_info['rewards']}\n**Ends at:** {giveaway_info['end_time'].strftime('%d-%m-%y / %I:%M %p')}"
            )
            asyncio.create_task(auto_declare_winner(client, message))
        except ValueError:
            await message.reply_text("Please enter a valid number of minutes for the time limit.")

# Command for users to join the giveaway
@Client.on_message(filters.command("luckey") & filters.private)
async def enter_giveaway(client: Client, message: Message):
    user_id = message.from_user.id
    if giveaway_info.get("end_time") and datetime.now() >= giveaway_info["end_time"]:
        await message.reply_text("This giveaway has ended.")
        return
    if user_id in entries:
        await message.reply_text("You have already entered this giveaway!")
        return
    entries.append(user_id)
    await message.reply_text("You have entered the giveaway! Good luck!")

# Automatically declare winner after giveaway ends
async def auto_declare_winner(client: Client, message: Message):
    await asyncio.sleep((giveaway_info["end_time"] - datetime.now()).total_seconds())
    if giveaway_info.get("step") is None:
        await declare_winner(client, message)

# Declare winners function
async def declare_winner(client: Client, message: Message):
    if not entries:
        await client.send_message(giveaway_info['initiated_by'], "No participants in the giveaway.")
        return

    winners = random.sample(entries, min(len(entries), giveaway_info['num_winners']))
    result_message = "🎉 Giveaway Winners 🎉\n\n"
    for idx, user_id in enumerate(winners, start=1):
        user_coins = giveaway_info['rewards'][idx - 1] if idx - 1 < len(giveaway_info['rewards']) else giveaway_info['rewards'][-1]
        user_data[user_id]['coins'] += user_coins  # Add coins to user balance
        result_message += f"{idx}. User ID: {user_id} | Coins Awarded: {user_coins}\n"

    # Confirm result with admin
    await client.send_message(
        giveaway_info['initiated_by'], result_message,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes", callback_data="confirm_result"),
             InlineKeyboardButton("No", callback_data="reselect_winner")]
        ])
    )

# Confirm result
@Client.on_callback_query(filters.regex("confirm_result"))
async def confirm_winner(client: Client, callback_query):
    await callback_query.message.edit_text("Winners confirmed and prizes distributed!")
    giveaway_info.clear()
    entries.clear()

# Reselect winners
@Client.on_callback_query(filters.regex("reselect_winner"))
async def reselect_winner(client: Client, callback_query):
    await callback_query.message.edit_text("Reselecting winners...")
    await declare_winner(client, callback_query.message)

# Cancel giveaway setup
@Client.on_callback_query(filters.regex("cancel_giveaway"))
async def cancel_giveaway(client: Client, callback_query):
    giveaway_info.clear()
    entries.clear()
    await callback_query.message.edit_text("Giveaway setup cancelled.")

# Command to stop the giveaway manually
@Client.on_message(filters.command("stp_giving") & filters.user(ADMINS))
async def stop_giveaway(client: Client, message: Message):
    giveaway_info.clear()
    entries.clear()
    await message.reply_text("Giveaway has been stopped.")

# Command to check total entries in giveaway
@Client.on_message(filters.command("giveaway_entries") & filters.user(ADMINS))
async def check_entries(client: Client, message: Message):
    if not entries:
        await message.reply_text("No entries received yet for this giveaway.")
        return
    entries_message = f"Total entries: {len(entries)}\n\n"
    for user_id in entries:
        entries_message += f"User ID: {user_id}\n"
    await message.reply_text(entries_message)

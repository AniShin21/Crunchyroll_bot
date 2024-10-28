from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from accounts_store import user_data, unban  # Import the user data store
from database import get_leaderboard, full_userbase
from config import ADMINS


# Command to check user's balance
@Client.on_message(filters.command('balance') & filters.private & unban)
async def check_balance(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Check if the user exists in user_data
    if user_id not in user_data:
        # If the user doesn't exist in the data, initialize them with default values
        user_data[user_id] = {'coins': 0, 'invites': 0, 'claimed_accounts': [], 'last_claim': None, 'claims_today': 0}

    # Retrieve the user's coin balance
    user_balance = user_data[user_id]['coins']
    
    # Send the user their balance
    await message.reply_text(f"💰 𝚈𝚘𝚞𝚛 𝚌𝚞𝚛𝚛𝚎𝚗𝚝 𝚋𝚊𝚕𝚊𝚗𝚌𝚎 𝚒𝚜: {user_balance} 𝚌𝚘𝚒𝚗𝚜")




@Client.on_message(filters.command('leaderboard') & unban)
async def show_leaderboard(client: Client, message: Message):
    """Display the leaderboard."""
    leaderboard = await get_leaderboard()  # Fetch the leaderboard data

    if not leaderboard:
        await message.reply_text("𝙽𝚘 𝙳𝚊𝚝𝚊 𝙵𝚘𝚛 𝙻𝚎𝚊𝚍𝚎𝚛𝚋𝚘𝚊𝚛𝚍")
        return

    # Format the leaderboard message
    leaderboard_message = "<b>𝙻𝚎𝚊𝚍𝚎𝚛𝚋𝚘𝚊𝚛𝚍:</b>\n\n"
    for rank, (user_id, data) in enumerate(leaderboard, start=1):
        coins = data.get('coins', 0)  # Retrieve the user's coins
        
        # Fetch user details dynamically using the Telegram API
        try:
            user = await client.get_users(user_id)
            user_first_name = user.first_name
            user_last_name = user.last_name or ""  # Handle cases where the last name may be None

            # Format the display of names
            display_name = f"{user_first_name} {user_last_name}".strip()  # Strip any excess spaces

        except Exception as e:
            display_name = "Unknown User"  # Fallback if user details can't be fetched

        leaderboard_message += f"{rank}. User ID: <code>{user_id}</code> | Name: <b>{display_name}</b> | Balance: <code>{coins}</code> coins\n"

    await message.reply_text(leaderboard_message)

async def get_leaderboard():
    """Function to retrieve the leaderboard data."""
    leaderboard = []
    
    for user_id, data in user_data.items():
        coins = data.get('coins', 0)  # Get coins, default to 0 if not present
        leaderboard.append((user_id, {'coins': coins}))

    leaderboard.sort(key=lambda x: x[1]['coins'], reverse=True)  # Sort by coins in descending order
    return leaderboard

############______________USERS_________________####################
@Client.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def list_users(client, message):
    """Display the list of users."""
    user_count = len(user_data)

    # Create a message for the user list
    user_list_message = "<b>𝚃𝚘𝚝𝚊𝚕 𝚄𝚜𝚎𝚛𝚜:</b> <code>{}</code>\n\n".format(user_count)

    # Check if there are users to display
    if user_data:
        for user_id, info in user_data.items():
            # Fetch user details dynamically using the Telegram API
            try:
                user = await client.get_users(user_id)
                user_first_name = user.first_name
                user_last_name = user.last_name or ""  # Handle cases where the last name may be None

                # Format the display of names
                display_name = f"{user_first_name} {user_last_name}".strip()  # Strip any excess spaces

                # Append to the user list message
                user_list_message += f"User ID: <code>{user_id}</code> | Name: <b>{display_name}</b>\n"

            except Exception:
                # If user details cannot be fetched, fallback to 'Unknown User'
                user_list_message += f"User ID: <code>{user_id}</code> | Name: <b>Unknown User</b>\n"

        await message.reply_text(user_list_message)
    else:
        await message.reply_text("No users found.")










@Client.on_message(filters.command("gift") & filters.private)
async def gift_coins(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if the user has an entry in user_data, if not, initialize it
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'invites': 0, 'claimed_accounts': [], 'last_claim': None, 'claims_today': 0}

    try:
        # Split the message text to get recipient ID and amount of coins
        command_parts = message.text.split()
        recipient_id = int(command_parts[1])  # Target user's ID
        coins_to_gift = int(command_parts[2])  # Amount of coins to gift

        # Check if the sender has enough coins
        if user_data[user_id]['coins'] < coins_to_gift:
            await message.reply_text(f"𝚈𝚘𝚞 𝚍𝚘𝚗'𝚝 𝚑𝚊𝚟𝚎 𝚎𝚗𝚘𝚞𝚐𝚑 𝚌𝚘𝚒𝚗𝚜 𝚝𝚘 𝚐𝚒𝚏𝚝. 𝚈𝚘𝚞𝚛 𝚌𝚞𝚛𝚛𝚎𝚗𝚝 𝚋𝚊𝚕𝚊𝚗𝚌𝚎 𝚒𝚜 {user_data[user_id]['coins']} 𝚌𝚘𝚒𝚗𝚜.")
            return

        # Check if the recipient has an entry in user_data, if not, initialize it
        if recipient_id not in user_data:
            user_data[recipient_id] = {'coins': 0, 'invites': 0, 'claimed_accounts': [], 'last_claim': None, 'claims_today': 0}

        # Deduct coins from sender and add to recipient
        user_data[user_id]['coins'] -= coins_to_gift
        user_data[recipient_id]['coins'] += coins_to_gift

        # Notify the sender and the recipient
        await message.reply_text(f"𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢 𝚐𝚒𝚏𝚝𝚎𝚍 {coins_to_gift} 𝚌𝚘𝚒𝚗𝚜 𝚝𝚘 𝚞𝚜𝚎𝚛 {recipient_id}. 𝚈𝚘𝚞𝚛 𝚗𝚎𝚠 𝚋𝚊𝚕𝚊𝚗𝚌𝚎 𝚒𝚜 {user_data[user_id]['coins']} 𝚌𝚘𝚒𝚗𝚜.")
        
        try:
            await client.send_message(recipient_id, f"𝚈𝚘𝚞 𝚑𝚊𝚟𝚎 𝚛𝚎𝚌𝚎𝚒𝚟𝚎𝚍 {coins_to_gift} 𝚌𝚘𝚒𝚗𝚜 𝚏𝚛𝚘𝚖 𝚞𝚜𝚎𝚛 {user_id}. 𝚈𝚘𝚞𝚛 𝚗𝚎𝚠 𝚋𝚊𝚕𝚊𝚗𝚌𝚎 𝚒𝚜 {user_data[recipient_id]['coins']} 𝚌𝚘𝚒𝚗𝚜!")
        except Exception as e:
            await message.reply_text(f"𝙲𝚘𝚞𝚕𝚍 𝚗𝚘𝚝 𝚗𝚘𝚝𝚒𝚏𝚢 𝚝𝚑𝚎 𝚛𝚎𝚌𝚒𝚙𝚒𝚎𝚗𝚝 𝚍𝚒𝚛𝚎𝚌𝚝𝚕𝚢: {e}")

    except (IndexError, ValueError):
        await message.reply_text("𝚄𝚜𝚊𝚐𝚎: /𝚐𝚒𝚏𝚝 <𝚞𝚜𝚎𝚛_𝚒𝚍> <𝚊𝚖𝚘𝚞𝚗𝚝_𝚘𝚏_𝚌𝚘𝚒𝚗𝚜>")


@Client.on_message(filters.command("id") & filters.private)
async def my_id(client: Client, message: Message):
    user_id = message.from_user.id
    await message.reply_text(f"𝓨𝓸𝓾𝓻 𝓣𝓮𝓵𝓮𝓰𝓻𝓪𝓶 𝓾𝓼𝓮𝓻 𝓘𝓓 𝓲𝓼: {user_id}")

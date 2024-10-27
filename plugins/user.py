from pyrogram import Client, filters
from pyrogram.types import Message
from accounts_store import user_data  # Import the user data store
from database import get_leaderboard, full_userbase
from config import ADMINS



# Command to check user's balance
@Client.on_message(filters.command('balance') & filters.private)
async def check_balance(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Check if the user exists in user_data
    if user_id not in user_data:
        # If the user doesn't exist in the data, initialize them with default values
        user_data[user_id] = {'coins': 0, 'invites': 0, 'claimed_accounts': [], 'last_claim': None, 'claims_today': 0}

    # Retrieve the user's coin balance
    user_balance = user_data[user_id]['coins']
    
    # Send the user their balance
    await message.reply_text(f"💰 Your current balance is: {user_balance} coins.")




@Client.on_message(filters.command('leaderboard'))
async def show_leaderboard(client: Client, message: Message):
    """Display the leaderboard."""
    leaderboard = await get_leaderboard()  # Fetch the leaderboard data

    if not leaderboard:
        await message.reply_text("No Data For Leaderboard")
        return

    # Format the leaderboard message
    leaderboard_message = "<b>Leaderboard:</b>\n\n"
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
WAIT_MSG = "Please Wait.."


@Client.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Client, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")





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
            await message.reply_text(f"You don't have enough coins to gift. Your current balance is {user_data[user_id]['coins']} coins.")
            return

        # Check if the recipient has an entry in user_data, if not, initialize it
        if recipient_id not in user_data:
            user_data[recipient_id] = {'coins': 0, 'invites': 0, 'claimed_accounts': [], 'last_claim': None, 'claims_today': 0}

        # Deduct coins from sender and add to recipient
        user_data[user_id]['coins'] -= coins_to_gift
        user_data[recipient_id]['coins'] += coins_to_gift

        # Notify the sender and the recipient
        await message.reply_text(f"Successfully gifted {coins_to_gift} coins to user {recipient_id}. Your new balance is {user_data[user_id]['coins']} coins.")
        
        try:
            await client.send_message(recipient_id, f"You have received {coins_to_gift} coins from user {user_id}. Your new balance is {user_data[recipient_id]['coins']} coins!")
        except Exception as e:
            await message.reply_text(f"Could not notify the recipient directly: {e}")

    except (IndexError, ValueError):
        await message.reply_text("Usage: /gift <user_id> <amount_of_coins>")


@Client.on_message(filters.command("id") & filters.private)
async def my_id(client: Client, message: Message):
    user_id = message.from_user.id
    await message.reply_text(f"Your Telegram user ID is: {user_id}")

# accounts_store.py
from pyrogram import filters
# In-memory store for premium accounts and user data
premium_accounts = []  # Store premium accounts
used_accounts = []     # Store used accounts

# Store user-specific data
user_data = {}



async def add_user(user_id):
    """Add a user to user_data if not already present."""
    if user_id not in user_data:
        # Initialize user data
        user_data[user_id] = {
            "first_name": None,
            "last_name": None,
            "username": None,
            "other_data": {}  # Add any other fields you want to track
        }



# List of banned user IDs
banned_users = []

# Message to display for banned users
BANNED_MESSAGE = "❌ 𝖸𝗈𝗎 𝖺𝗋𝖾 𝖻𝖺𝗇𝗇𝖾𝖽 𝖿𝗋𝗈𝗆 𝗎𝗌𝗂𝗇𝗀 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍."

# Filter to allow only unbanned users
unban = filters.create(lambda _, __, message: message.from_user.id not in banned_users)

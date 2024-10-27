# accounts_store.py
from pyrogram import filters
# In-memory store for premium accounts and user data
premium_accounts = []  # Store premium accounts
used_accounts = []     # Store used accounts

# Store user-specific data
user_data = {}





# List of banned user IDs
banned_users = []

# Message to display for banned users
BANNED_MESSAGE = "🚫 You are banned from using this bot."

# Filter to allow only unbanned users
unban = filters.create(lambda _, __, message: message.from_user.id not in banned_users)

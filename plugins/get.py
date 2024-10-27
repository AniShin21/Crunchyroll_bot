from pyrogram import Client, filters
from pyrogram.types import Message
from accounts_store import premium_accounts, user_data  # Ensure this points to your account storage
from datetime import datetime

@Client.on_message(filters.command("get") & filters.private)
async def get_account(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Initialize user data if not present, with 'claimed_accounts' as an empty list by default
    user_info = user_data.get(user_id, {'coins': 0, 'claimed_accounts': []})
    
    if 'claimed_accounts' not in user_info:
        user_info['claimed_accounts'] = []  # Ensure 'claimed_accounts' key exists

    # Check if user has enough coins to claim an account
    if user_info['coins'] < 20:
        await message.reply_text(
            "💰 You need at least 20 coins to claim a premium account. "
            f"Currently, you have {user_info['coins']} coins."
        )
        return

    # Check if there are available premium accounts
    if not premium_accounts:
        await message.reply_text("🚫 Sorry, no premium accounts are available right now.")
        return

    # Claim an account
    account = premium_accounts.pop(0)  # Get the first account
    user_info['claimed_accounts'].append(account)  # Store claimed account
    user_info['coins'] -= 20  # Deduct coins
    user_info['last_claim'] = datetime.now().isoformat()  # Update last claim time

    # Save user data back (implement save logic as necessary)
    user_data[user_id] = user_info  

    await message.reply_text(f"✅ Here is your premium account: {account}\nEnjoy! 🎉")

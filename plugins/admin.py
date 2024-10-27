import os
from pyrogram import Client, filters
from pyrogram.types import Message, Document
from accounts_store import premium_accounts, user_data   # Assuming this is where premium_accounts is stored
from config import ADMINS
import shutil


@Client.on_message(filters.command("load_accounts") & filters.private & filters.user(ADMINS))
async def load_accounts_command(client: Client, message: Message):
    if message.reply_to_message and message.reply_to_message.document:
        file: Document = message.reply_to_message.document
        
        if file.mime_type == "text/plain":  # Ensure it's a text file
            file_path = await client.download_media(file)
            await load_accounts_from_file(file_path)
            os.remove(file_path)  # Remove the file after processing
            await message.reply_text("Accounts loaded successfully.")
        else:
            await message.reply_text("Please send a valid text file containing accounts.")
    else:
        await message.reply_text("Please reply to a text file to load accounts.")

async def load_accounts_from_file(file_path):
    # Clear previous accounts
    premium_accounts.clear()

    with open(file_path, 'r') as file:
        accounts = file.readlines()
        for account in accounts:
            premium_accounts.append(account.strip())  # Load each account and strip whitespace

@Client.on_message(filters.command("del_file") & filters.user(ADMINS))
async def del_file(client: Client, message: Message):
    directory = 'downloads'  # Specify the directory to delete

    if os.path.exists(directory):
        shutil.rmtree(directory)  # Remove the directory and all its contents
        await message.reply_text(f"🗑️ Successfully deleted the '{directory}' folder and its contents.")
    else:
        await message.reply_text(f"🚫 The '{directory}' folder does not exist.")

        

from pyrogram import Client, filters
from pyrogram.types import Message
from accounts_store import user_data  # Ensure this points to your user data storage
from config import ADMINS  # List of admin user IDs

@Client.on_message(filters.command('give_coins') & filters.private)
async def give_coins(client: Client, message: Message):
    if message.from_user.id not in ADMINS:
        await message.reply_text("You are not authorized to use this command.")
        return

    try:
        # Split the message text to get parameters
        command_parts = message.text.split(maxsplit=3)
        target = command_parts[1]  # Target user ID or "@all"
        coins_to_give = int(command_parts[2])  # Amount of coins to give
        custom_message = command_parts[3] if len(command_parts) > 3 else f"You have been awarded {coins_to_give} coins!"

        if target == "@all":
            # Give coins to all users
            for user_id in user_data:
                user_data[user_id]['coins'] = user_data.get(user_id, {}).get('coins', 0) + coins_to_give

                # Try to send the custom message to each user
                try:
                    await client.send_message(user_id, f"{custom_message} Your new balance is {user_data[user_id]['coins']} coins!")
                except Exception as e:
                    await message.reply_text(f"Could not notify user {user_id} directly: {e}")

            await message.reply_text(f"Successfully added {coins_to_give} coins to all users.")

        else:
            # Treat target as a single user ID
            user_id = int(target)

            # Check if the user exists in user_data, if not, create a default entry
            if user_id not in user_data:
                user_data[user_id] = {'coins': 0, 'invites': 0, 'claimed_accounts': [], 'last_claim': None, 'claims_today': 0}

            # Update the user's coin balance
            user_data[user_id]['coins'] += coins_to_give
            new_balance = user_data[user_id]['coins']

            # Send confirmation message to the admin and notify the user
            await message.reply_text(f"Successfully added {coins_to_give} coins to user {user_id}. New balance: {new_balance} coins.")

            try:
                await client.send_message(user_id, f"{custom_message} Your new balance is {new_balance} coins!")
            except Exception as e:
                await message.reply_text(f"Could not notify the user directly: {e}")

    except (IndexError, ValueError):
        await message.reply_text("Usage: /give_coins <user_id/@all> <amount_of_coins> [optional_custom_message]")





@Client.on_message(filters.command("remove_coins") & filters.user(ADMINS) & filters.private)
async def remove_coins(client: Client, message: Message):
    # Extract the command parameters
    command_parts = message.text.split()
    
    if len(command_parts) < 3:
        await message.reply_text("❗ Usage: /remove_coins <user_id> <coins>")
        return
    
    try:
        user_id = int(command_parts[1])
        coins_to_deduct = int(command_parts[2])

        # Check if the user exists in user_data
        if user_id not in user_data:
            await message.reply_text("🚫 User not found.")
            return

        # Deduct coins from the user's account
        user_data[user_id]['coins'] = max(0, user_data[user_id].get('coins', 0) - coins_to_deduct)

        await message.reply_text(
            f"✅ Removed {coins_to_deduct} coins from user {user_id}.\n"
            f"💰 New balance: {user_data[user_id]['coins']} coins."
        )

    except ValueError:
        await message.reply_text("❗ Invalid user ID or coin amount.")

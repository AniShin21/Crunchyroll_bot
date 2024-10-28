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
            await message.reply_text("𝙰𝚌𝚌𝚘𝚞𝚗𝚝𝚜 𝚕𝚘𝚊𝚍𝚎𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢.")
        else:
            await message.reply_text("𝙿𝚕𝚎𝚊𝚜𝚎 𝚜𝚎𝚗𝚍 𝚊 𝚟𝚊𝚕𝚒𝚍 𝚝𝚎𝚡𝚝 𝚏𝚒𝚕𝚎 𝚌𝚘𝚗𝚝𝚊𝚒𝚗𝚒𝚗𝚐 𝚊𝚌𝚌𝚘𝚞𝚗𝚝𝚜.")
    else:
        await message.reply_text("𝙿𝚕𝚎𝚊𝚜𝚎 𝚛𝚎𝚙𝚕𝚢 𝚝𝚘 𝚊 𝚝𝚎𝚡𝚝 𝚏𝚒𝚕𝚎 𝚝𝚘 𝚕𝚘𝚊𝚍 𝚊𝚌𝚌𝚘𝚞𝚗𝚝𝚜.")

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
        await message.reply_text(f"🗑️ 𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢 𝚍𝚎𝚕𝚎𝚝𝚎𝚍 𝚝𝚑𝚎 '{directory}' 𝚏𝚘𝚕𝚍𝚎𝚛 𝚊𝚗𝚍 𝚒𝚝𝚜 𝚌𝚘𝚗𝚝𝚎𝚗𝚝𝚜.")
    else:
        await message.reply_text(f"🚫 The '{directory}' folder does not exist.")

          # List of admin user IDs

@Client.on_message(filters.command('give_coins') & filters.private)
async def give_coins(client: Client, message: Message):
    if message.from_user.id not in ADMINS:
        await message.reply_text("𝚈𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍.")
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
                # Update coins for each user
                if user_id in user_data:
                    user_data[user_id]['coins'] = user_data.get(user_id, {}).get('coins', 0) + coins_to_give

                    # Notify each user
                    try:
                        await client.send_message(user_id, f"{custom_message} Your new balance is {user_data[user_id]['coins']} coins!")
                    except Exception as e:
                        print(f"Could not notify user {user_id}: {e}")  # Log the error

            await message.reply_text(f"𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢 𝚊𝚍𝚍𝚎𝚍 {coins_to_give} 𝚌𝚘𝚒𝚗𝚜 𝚝𝚘 𝚊𝚕𝚕 𝚞𝚜𝚎𝚛𝚜.")

        else:
            # Treat target as a single user ID
            user_id = int(target)

            # Check if the user exists in user_data; if not, create a default entry
            if user_id not in user_data:
                user_data[user_id] = {'coins': 0, 'invites': 0, 'claimed_accounts': [], 'last_claim': None, 'claims_today': 0}

            # Update the user's coin balance
            user_data[user_id]['coins'] += coins_to_give
            new_balance = user_data[user_id]['coins']

            # Send confirmation message to the admin and notify the user
            await message.reply_text(f"𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢 𝚊𝚍𝚍𝚎𝚍 {coins_to_give} 𝚌𝚘𝚒𝚗𝚜 𝚝𝚘 𝚞𝚜𝚎𝚛 {user_id}. 𝙽𝚎𝚠 𝚋𝚊𝚕𝚊𝚗𝚌𝚎: {new_balance} 𝚌𝚘𝚒𝚗𝚜.")

            try:
                await client.send_message(user_id, f"{custom_message} 𝚈𝚘𝚞𝚛 𝚗𝚎𝚠 𝚋𝚊𝚕𝚊𝚗𝚌𝚎 𝚒𝚜 {new_balance} 𝚌𝚘𝚒𝚗𝚜!")
            except Exception as e:
                await message.reply_text(f"Could not notify the user directly: {e}")

    except (IndexError, ValueError) as e:
        await message.reply_text("𝚄𝚜𝚊𝚐𝚎: /𝚐𝚒𝚟𝚎_𝚌𝚘𝚒𝚗𝚜 <𝚞𝚜𝚎𝚛_𝚒𝚍/@𝚊𝚕𝚕> <𝚊𝚖𝚘𝚞𝚗𝚝_𝚘𝚏_𝚌𝚘𝚒𝚗𝚜> [𝚘𝚙𝚝𝚒𝚘𝚗𝚊𝚕_𝚌𝚞𝚜𝚝𝚘𝚖_𝚖𝚎𝚜𝚜𝚊𝚐𝚎]")
        print(f"Error in give_coins command: {e}")  




@Client.on_message(filters.command("remove_coins") & filters.user(ADMINS) & filters.private)
async def remove_coins(client: Client, message: Message):
    # Extract the command parameters
    command_parts = message.text.split()
    
    if len(command_parts) < 3:
        await message.reply_text("❗ 𝚄𝚜𝚊𝚐𝚎: /𝚛𝚎𝚖𝚘𝚟𝚎_𝚌𝚘𝚒𝚗𝚜 <𝚞𝚜𝚎𝚛_𝚒𝚍> <𝚌𝚘𝚒𝚗𝚜>")
        return
    
    try:
        user_id = int(command_parts[1])
        coins_to_deduct = int(command_parts[2])

        # Check if the user exists in user_data
        if user_id not in user_data:
            await message.reply_text("🚫 𝚄𝚜𝚎𝚛 𝚗𝚘𝚝 𝚏𝚘𝚞𝚗𝚍.")
            return

        # Deduct coins from the user's account
        user_data[user_id]['coins'] = max(0, user_data[user_id].get('coins', 0) - coins_to_deduct)

        await message.reply_text(
            f"✅ 𝚁𝚎𝚖𝚘𝚟𝚎𝚍 {coins_to_deduct} 𝚌𝚘𝚒𝚗𝚜 𝚏𝚛𝚘𝚖 𝚞𝚜𝚎𝚛 {user_id}.\n"
            f"💰 𝙽𝚎𝚠 𝚋𝚊𝚕𝚊𝚗𝚌𝚎: {user_data[user_id]['coins']} 𝚌𝚘𝚒𝚗𝚜."
        )

    except ValueError:
        await message.reply_text("❗ 𝙸𝚗𝚟𝚊𝚕𝚒𝚍 𝚞𝚜𝚎𝚛 𝙸𝙳 𝚘𝚛 𝚌𝚘𝚒𝚗 𝚊𝚖𝚘𝚞𝚗𝚝.")

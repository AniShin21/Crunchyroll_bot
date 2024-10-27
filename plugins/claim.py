import random
from pyrogram import Client, filters
from pyrogram.types import Message
from accounts_store import user_data  # Assuming user_data is imported
from config import ADMINS  # Make sure ADMINS list is in config.py

# Store for active codes
redeem_codes = {}

@Client.on_message(filters.command("gen") & filters.user(ADMINS))
async def generate_codes(client: Client, message: Message):
    try:
        # Parse command arguments: /gen <coins> <num_of_codes>
        _, coins, num_codes = message.text.split()
        coins = int(coins)
        num_codes = int(num_codes)

        # Generate the specified number of codes
        codes = []
        for _ in range(num_codes):
            code = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
            codes.append(code)
            redeem_codes[code] = {'coins': coins, 'claimed_by': []}

        # Display all generated codes to the admin
        codes_text = "\n".join([f"Code: <code>{code}</code> | Coins: {coins}" for code in codes])
        await message.reply_text(f"{num_codes} redeem code(s) generated!\n\n{codes_text}")

    except ValueError:
        await message.reply_text("Please use the format: /gen <coins> <num_of_codes>.")

@Client.on_message(filters.command("redeem") & filters.private)
async def redeem_code(client: Client, message: Message):
    user_id = message.from_user.id
    code = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not code:
        await message.reply_text("Please provide a code to redeem. Usage: /redeem <code>")
        return

    # Check if the code exists and hasn't been redeemed by this user
    if code in redeem_codes:
        code_info = redeem_codes[code]

        # Check if the user has already redeemed this code
        if user_id in code_info['claimed_by']:
            await message.reply_text("You've already redeemed this code.")
            return

        # Award coins and update user data
        user_data.setdefault(user_id, {'coins': 0})
        user_data[user_id]['coins'] += code_info['coins']

        # Mark code as claimed by this user
        code_info['claimed_by'].append(user_id)
        await message.reply_text(f"Success! You've received {code_info['coins']} coins. Your new balance is {user_data[user_id]['coins']} coins.")
    else:
        await message.reply_text("Invalid code. Please check and try again.")

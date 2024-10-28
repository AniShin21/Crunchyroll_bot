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
        codes_text = "\n".join([f"𝙲𝚘𝚍𝚎: <code>{code}</code> | 𝙲𝚘𝚒𝚗𝚜: {coins}" for code in codes])
        await message.reply_text(f"{num_codes} 𝚛𝚎𝚍𝚎𝚎𝚖 𝚌𝚘𝚍𝚎(𝚜) 𝚐𝚎𝚗𝚎𝚛𝚊𝚝𝚎𝚍!\n\n{codes_text}")

    except ValueError:
        await message.reply_text("𝙿𝚕𝚎𝚊𝚜𝚎 𝚞𝚜𝚎 𝚝𝚑𝚎 𝚏𝚘𝚛𝚖𝚊𝚝: /𝚐𝚎𝚗 <𝚌𝚘𝚒𝚗𝚜> <𝚗𝚞𝚖_𝚘𝚏_𝚌𝚘𝚍𝚎𝚜>.")

@Client.on_message(filters.command("redeem") & filters.private)
async def redeem_code(client: Client, message: Message):
    user_id = message.from_user.id
    code = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not code:
        await message.reply_text("𝙿𝚕𝚎𝚊𝚜𝚎 𝚙𝚛𝚘𝚟𝚒𝚍𝚎 𝚊 𝚌𝚘𝚍𝚎 𝚝𝚘 𝚛𝚎𝚍𝚎𝚎𝚖. 𝚄𝚜𝚊𝚐𝚎: /𝚛𝚎𝚍𝚎𝚎𝚖 <𝚌𝚘𝚍𝚎>")
        return

    # Check if the code exists and hasn't been redeemed by this user
    if code in redeem_codes:
        code_info = redeem_codes[code]

        # Check if the user has already redeemed this code
        if user_id in code_info['claimed_by']:
            await message.reply_text("𝚈𝚘𝚞'𝚟𝚎 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚛𝚎𝚍𝚎𝚎𝚖𝚎𝚍 𝚝𝚑𝚒𝚜 𝚌𝚘𝚍𝚎.")
            return

        # Award coins and update user data
        user_data.setdefault(user_id, {'coins': 0})
        user_data[user_id]['coins'] += code_info['coins']

        # Mark code as claimed by this user
        code_info['claimed_by'].append(user_id)
        await message.reply_text(f"𝚂𝚞𝚌𝚌𝚎𝚜𝚜! 𝚈𝚘𝚞'𝚟𝚎 𝚛𝚎𝚌𝚎𝚒𝚟𝚎𝚍 {code_info['coins']} 𝚌𝚘𝚒𝚗𝚜. 𝚈𝚘𝚞𝚛 𝚗𝚎𝚠 𝚋𝚊𝚕𝚊𝚗𝚌𝚎 𝚒𝚜 {user_data[user_id]['coins']} coins.")
    else:
        await message.reply_text("𝙸𝚗𝚟𝚊𝚕𝚒𝚍 𝚌𝚘𝚍𝚎. 𝙿𝚕𝚎𝚊𝚜𝚎 𝚌𝚑𝚎𝚌𝚔 𝚊𝚗𝚍 𝚝𝚛𝚢 𝚊𝚐𝚊𝚒𝚗.")

from pyrogram import filters
from TgBot import bot, db, lang, utils

@bot.on_message(filters.command('info'))
async def on_info(client, message):
    user_info = await utils.extract_user(client, message)
    tg_info = lang.get(from_user.id, 'tg_info_text').format(first_name, last_name, username, user_id, dc_id, profile_link)
    whisper_info = lang.get(from_user.id, 'whisper_info_text').format()
    info_text = tg_info + whisper_info
    await message.reply(info_text)
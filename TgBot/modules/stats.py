from pyrogram import filters, enums
from TgBot import bot, db, utils

@bot.on_message(group=1)
async def on_new_message(client, message):
    chat = message.chat
    from_user = message.from_user
    if chat.type == enums.ChatType.PRIVATE:
        db.add_user(user_id=from_user.id)

@bot.on_message(filters.command('stats'))
async def on_stats(client, message):
    from_user = message.from_user
    if not from_user:
        return
    if not from_user.id in utils.get_permitted_ids():
        return
    total_users = db.get_users() or []
    text = f'''
<b>• 🤖 Bot Statistics 📊:</b>

<b>Total Users:</b> {len(total_users)}
    '''
    await message.reply(text)
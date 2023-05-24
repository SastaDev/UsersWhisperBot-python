from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from pyrogram import filters
from TgBot import bot, lang

@bot.on_message(filters.command('start'))
async def on_start(client, message):
    from_user = message.from_user
    text = lang.get(from_user.id, 'start_text')
    button_1 = lang.get(from_user.id, 'inline_usage_button_text')
    button_2 = lang.get(from_user.id, 'switch_inline_query_button_text')
    buttons = [
        [InlineKeyboardButton(button_1, callback_data='inline_usage')],
        [InlineKeyboardButton(button_2, switch_inline_query='')]
    ]
    if getattr(message, 'is_callback', False) is True:
        await message.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply(text, reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex(r'^inline_usage'))
async def on_inline_usage(client, callback_query):
    from_user = callback_query.from_user
    text = lang.get(from_user.id, 'inline_usage_text')
    button_1 = lang.get(from_user.id, 'go_back_to_start_menu_button_text')
    buttons = [
        [InlineKeyboardButton(button_1, callback_data='go_back_to_start_menu')]
    ]
    await callback_query.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex(r'^go_back_to_start_menu'))
async def on_go_back_to_start_menu(client, callback_query):
    callback_query.is_callback = True
    await on_start(client, callback_query)
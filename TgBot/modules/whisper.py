from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton)
from pyrogram.types import InlineQueryResult
from TgBot import bot, lang, utils, cache
from pyrogram import filters

whisper_cache = {}

@bot.on_inline_query(group=1)
async def on_inline_query(client, inline_query):
    from_user = inline_query.from_user
    title = lang.get(from_user.id, 'inline_whisper_usage_title')
    description = lang.get(from_user.id, 'inline_whisper_usage_description')
    text = lang.get(from_user.id, 'inline_whisper_usage_text')
    results = [
        InlineQueryResultArticle(
        title=title,
        description=description,
        input_message_content=InputTextMessageContent(text)
        )
    ]
    await inline_query.answer(results, cache_time=0)

@bot.on_inline_query(filters.regex(r'(.+) ?(.+)?'))
async def on_whisper(client, inline_query):
    from_user = inline_query.from_user
    _targets, options, whisper_text = utils.extract_whisper(inline_query.query)
    targets = []
    for target in _targets:
        c = cache.get_cache(str(target))
        if c:
            t = c.get(str(target))
            target_id = c.get('target_id')
            target_full_name = c.get('target_full_name')
            target_username = c.get('target_username')
            target_mention = c.get('target_mention')
        else:
            t = utils.extract_whisper_user(client, target)
            if t is False:
                title = lang.get(from_user.id, 'invalid_target_user_mention_title')
                description = lang.get(from_user.id, 'invalid_target_user_mention_description')
                text = lang.get(from_user.id, 'whisper_target_user_invalid_text')
                results = [
                    InlineQueryResultArticle(
                        title=title,
                        description=description,
                        input_message_content=InputTextMessageContent(text)
                        )
                ]
                await inline_query.answer(results)
                return
            elif t is None:
                if str(target).isalpha():
                    target_full_name = '@' + target if target[0] != '@' else '' + target
                else:
                    target_full_name = target
                if str(target).isalpha():
                    target_id = '@' if target[0] != '@' else '' + target
                else:
                    target_id = target
                if str(target).isalpha():
                    target_username = '@' if target[0] != '@' else '' + target
                else:
                    target_username = target
                if str(target).isdigit():
                    target_mention = f'<a href="tg://user?id={target}">{target}</a>'
                else:
                    target_mention = '@' if target[0] != '@' else '' + target
            else:
                target_id = target.id
                target_full_name = target.first_name + f' {target.last_name}' if target.last_name else ''
                target_username = target.username
                target_mention = target.mention
        data = {
            'target_id': target_id,
            'target_full_name': target_full_name,
            'target_username': target_username,
            'target_mention': target_mention
        }
        cache.add_cache(str(target), data, timeout=120)
        targets.append(data)
    if whisper_text is None:
        title = lang.get(from_user.id, 'write_whisper_text_title')
        description = lang.get(from_user.id, 'write_whisper_text_description')
        text = lang.get(from_user.id, 'write_whisper_text')
        results = [
            InlineQueryResultArticle(
            title=title,
            description=description,
            input_message_content=InputTextMessageContent(text)
            )
        ]
        await inline_query.answer(results)
        return
    for target in targets:
        data = target
        cache.add_cache(str(target['target_id']), data, timeout=120)
    targets_mentions = utils.get_targets_mentions(targets)
    if len(targets) > 1:
        text = lang.get(from_user.id, 'multi_target_users_whisper_open_message_text').format(targets_mentions, from_user.mention, from_user.id)
    else:
        text = lang.get(from_user.id, 'single_target_user_whisper_open_message_text').format(targets[0]['target_mention'], targets[0]['target_id'], from_user.mention, from_user.id)
    data = {
        'targets': targets,
        'options': options,
        'whisper_text': whisper_text,
        'has_been_read': []
    }
    whisper_cache[str(from_user.id)] = data
    targets_full_name = utils.get_targets_full_name(targets)
    title = lang.get(from_user.id, 'whisper_open_message_title')
    description = lang.get(from_user.id, 'whisper_open_message_description').format(targets_full_name)
    button_1 = lang.get(from_user.id, 'open_whisper_button_text')
    reply_markup = [
        [InlineKeyboardButton(button_1, callback_data=f'open_whisper_{from_user.id}')]
    ]
    results = [
        InlineQueryResultArticle(
            title=title,
            description=description,
            input_message_content=InputTextMessageContent(text),
            reply_markup=InlineKeyboardMarkup(reply_markup)
            )
    ]
    await inline_query.answer(results, cache_time=0)

@bot.on_callback_query(filters.regex(r'open_whisper_(.+)'))
async def on_open_whisper(client, callback_query):
    from_user = callback_query.from_user
    by_user = callback_query.matches[0].group(1)
    data = whisper_cache.get(by_user)
    if data is None or from_user.id in data.get('has_been_read'):
        text = lang.get(from_user.id, 'this_whisper_message_was_not_found_text')
        await callback_query.answer(text, show_alert=True)
        return
    not_a_target_user = None
    targets = data['targets']
    target_ids = [x['target_id'] for x in targets]
    for target in targets:
        target_id = target['target_id'].replace('@', '')
        if str(target_id).isdigit() is False:
            if from_user.username.lower() != target_id.lower()  and from_user.id != int(by_user):
                not_a_target_user = True
            else:
                not_a_target_user = False
                break
        else:
            if from_user.id != int(target_id) and from_user.id != int(by_user):
                not_a_target_user = True
            else:
                not_a_target_user = False
                break
    if not_a_target_user is True:
        text = lang.get(from_user.id, 'this_whisper_is_not_for_you_text')
        await callback_query.answer(text, show_alert=True)
        return
    if data is None:
        text = lang.get(from_user.id, 'this_whisper_message_was_not_found_text')
        await callback_query.answer(text, show_alert=True)
        return
    whisper_text = data['whisper_text']
    await callback_query.answer(whisper_text, show_alert=True)
    options = data.get('options') or []
    if '--one-time-open' in options:
        if len(targets) == 0:
            if str(target_id).isdigit() is False:
                _from_user_id = from_user.username
                _target_id = target_id
            else:
                _from_user_id = from_user.id
                _target_id = int(target_id)
            if from_user.id == int(by_user) and _from_user_id == _target_id:
                del whisper_cache[str(by_user)]
            elif from_user.id == int(target_id):
                del whisper_cache[str(by_user)]
        else:
            whisper_cache[str(by_user)]['has_been_read'].append(from_user.id)
        int_target_ids = [int(x['target_id']) for x in targets]
        if int_target_ids == whisper_cache[str(by_user)]['has_been_read']:
            if whisper_cache.get(str(by_user)):
                del whisper_cache[str(by_user)]
    if '--notify-me-on-read' in options:
        if str(target_id).isdigit() is False:
            _from_user_id = from_user.username
            _target_id = target_id
        else:
            _from_user_id = from_user.id
            _target_id = int(target_id)
        if _from_user_id == _target_id:
            text = lang.get(int(by_user), 'target_user_has_read_whisper_text').format(target.get('target_mention'), whisper_text)
            if whisper_cache.get(str(by_user), {}).get('targets'):
                button_1 = lang.get(int(by_user), 'delete_whisper_message_button_text')
                buttons = [
                    [InlineKeyboardButton(button_1, callback_data='delete_whisper{}'.format(*['_' + x.get('target_id') for x in targets]))]
                ]
            else:
                buttons = None
            try:
                await client.send_message(int(by_user), text, reply_markup=InlineKeyboardMarkup(buttons) if buttons else None)
            except:
                pass

@bot.on_callback_query(filters.regex(r'delete_whisper_(.+)'))
async def on_delete_whisper(client, callback_query):
    from_user = callback_query.from_user
    cb_target_ids = str(callback_query.matches[0].group(1)).split('_')
    cb_target_ids = [int(x) for x in cb_target_ids]
    data = whisper_cache.get(str(from_user.id))
    if data is None:
        text = lang.get(from_user.id, 'no_active_whisper_is_avaiable_by_you_text')
        await callback_query.answer(text, show_alert=True)
        return
    target_ids = [int(x['target_id']) for x in data['targets']]
    if len(cb_target_ids) == 0:
        if int(cb_target_ids[0]) not in target_ids:
            text = lang.get(from_user.id, 'no_whisper_was_found_for_this_targeted_user_to_delete_text').format(cb_target_ids[0])
            await callback_query.answer(text, show_alert=True)
            return
        try:
            del whisper_cache[str(from_user.id)]['targets'][int(cb_target_ids[0])]
        except KeyError:
            text = lang.get(from_user.id, 'callback_target_user_was_not_found_text').format(cb_target_ids[0])
            await callback_query.answer(text, show_alert=True)
            return
        text = lang.get(from_user.id, 'callback_delete_whispers_text').format(1, 0)
        await callback_query.answer(text, show_alert=True)
    else:
        deleted_targets = 0
        failed_targets = 0
        for target_id in cb_target_ids:
            if target_id not in target_ids:
                failed_targets += 1
                continue
            index = cb_target_ids.index(target_id)
            try:
                del whisper_cache[str(from_user.id)]['targets'][index]
            except KeyError:
                failed_targets += 1
                continue
            deleted_targets += 1
        text = lang.get(from_user.id, 'callback_delete_whispers_text').format(deleted_targets, failed_targets)
        await callback_query.answer(text, show_alert=True)

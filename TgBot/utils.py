import threading
import random
import json
import time
import os

class Configuration:
    def __init__(self, config_json_path):
        self.config_json_path = config_json_path

    def get_config_json(self):
        with open(self.config_json_path) as f:
            content = f.read()
            j = json.loads(content)
            return j

    def get(self, key):
        config = self.get_config_json()
        return config[key]

class Locale:
    def __init__(self, locale_path, db, default_langs):
        self.locale_path = locale_path
        self.db = db
        self.default_langs = default_langs
        self.load_locale()

    def load_locale(self):
        if not os.path.exists(self.locale_path):
            raise ValueError(f'Locale {self.locale_path} not found')

    def get_random_default_lang(self):
        default_langs = self.default_langs
        result = random.choice(default_langs)
        return result

    def get(self, ID, key):
        lang = self.db.get_lang(ID) or self.get_random_default_lang()
        _lang = 'TgBot.locale' + '.' + lang
        locale = __import__(name=_lang, fromlist=[''])
        result = getattr(locale, key)
        if result:
            result = random.choice(result) if isinstance(result, list) else result
        return result

class Cache:
    def __init__(self):
        pass

    def add_cache(self, cache_name, data, timeout=60):
        setattr(self, cache_name, data)
        t = threading.Thread(
            target=self.delete_from_cache,
            args=(cache_name, timeout)
            )
        t.start()

    def get_cache(self, cache_name):
        return getattr(self, cache_name, None)

    def delete_cache(self, cache_name):
        return delattr(self, cache_name)

    def delete_from_cache(self, cache_name, timeout):
        time.sleep(timeout)
        if getattr(self, cache_name, None):
            delattr(self, cache_name)

def extract_whisper_user(client, entity):
    if str(entity).replace('@', '').replace('_', '').isalnum() or str(entity).isdigit():
        try:
            user = client.get_user(entity)
        except:
            user = None
    else:
        user = False
    return user

def extract_whisper(x):
    x = str(x)
    targets = []
    options = []
    whisper_text = ''
    _x = x.split()
    multi_targets = False
    for t in _x:
        if t.startswith('['):
            multi_targets = True
            if len(t) > 1:
                _t = t[1:] if t[-1] != ']' else t[0:-1]
                targets.append(_t)
                continue
        elif t.endswith(']'):
            targets.append(t[0:-1])
            continue
        if len(_x) > _x.index(t) and not t.startswith('--') and len(targets) in (0, 1) and len(targets) < 1:
            targets.append(t)
        elif t.startswith('--'):
            index = _x.index(t)
            if not _x[index].startswith('--') and len(_x) > index+1:
                options.append(_x[index])
                continue
            else:
                options.append(t)
                continue
        else:
            if _x.index(t) == 0:
                continue
            if len(whisper_text) == 0:
                whisper_text += t
            else:
                whisper_text += ' ' + t
    return targets, options, whisper_text

def get_targets_mentions(targets):
    targets_mentions = ''
    if len(targets) > 0:
        for x in targets:
            if targets_mentions == '':
                targets_mentions += x.get('target_mention')
            else:
                _x = targets.index(x)
                if targets[-1] != targets[_x]:
                    targets_mentions += ' and ' + x.get('target_mention')
                else:
                    targets_mentions += ', ' + x.get('target_mention')
    return targets_mentions

def get_targets_full_name(targets):
    targets_full_name = ''
    if len(targets) > 0:
        for x in targets:
            if targets_full_name == '':
                targets_full_name += x.get('target_full_name')
            else:
                _x = targets.index(x)
                if targets[-1] != targets[_x]:
                    targets_full_name += ' and ' + x.get('target_full_name')
                else:
                    targets_full_name += ', ' + x.get('target_full_name')
    return targets_full_name

def get_permitted_ids():
    with open('config.json') as f:
        content = f.read()
        j = json.loads(content)
        return j['PERMITTED_IDS']

async def extract_user(client, message):
    if message.reply_to_message:
        return await extract_user(client, message.reply_to_message)
    elif message.sender_chat:
        return message.sender_chat
    elif message.from_user:
        return message.from_user
    else:
        return None
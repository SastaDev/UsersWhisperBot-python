from pyrogram import Client, enums
from . import utils, database

config = utils.Configuration(config_json_path='config.json')

API_ID = config.get('API_ID')
API_HASH = config.get('API_HASH')
BOT_TOKEN = config.get('BOT_TOKEN')
MONGODB_URI = config.get('MONGODB_URI')
DEFAULT_LANGS = config.get('DEFAULT_LANGS')

bot = Client(
    'TgBot',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
    )

bot.set_parse_mode(enums.ParseMode.HTML)

db = database.MongoDB(connection_url=MONGODB_URI)

lang = utils.Locale(
    locale_path='TgBot/locale',
    db=db,
    default_langs=DEFAULT_LANGS
    )

cache = utils.Cache()

from . import modules
import pymongo
import json
import dns

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

class MongoDB:
    def __init__(self, connection_url):
        self.connection_url = connection_url
        self.client = pymongo.MongoClient(connection_url)

    def set_lang(self, user_id, lang, chat_id=None):
        db = self.client['UsersWhisperBotDB']
        col = db['LANGS']
        query = {}
        if chat_id:
            update = {
                '_id': str(chat_id),
                str(user_id): {'lang': lang}
            }
        else:
            update = {
                '_id': str(user_id),
                'lang': lang
            }
        col.update_one(query, {'$set': update}, upsert=True)

    def get_lang(self, user_id, chat_id=None):
        db = self.client['UsersWhisperBotDB']
        col = db['LANGS']
        query = {}
        if chat_id:
            query = {
                '_id': str(chat_id),
                str(user_id): {'$exists': True}
            }
        else:
            query = {
                '_id': str(user_id)
            }
        find = col.find_one(query)
        if find:
            return find.get('lang')
        else:
            return None

    def add_user(self, user_id):
        db = self.client['UsersWhisperBotDB']
        col = db['STATS']
        query = {'_id': 'added_users'}
        update = {
            '$push': {
                'user_ids': user_id
            }
        }
        col.update_one(query, update, upsert=True)

    def get_users(self):
        db = self.client['UsersWhisperBotDB']
        col = db['STATS']
        query = {'_id': 'added_users'}
        find = col.find_one(query)
        if find:
            return find['user_ids']
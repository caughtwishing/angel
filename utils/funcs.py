from flask import jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import random, string
import dns.resolver
import cloudscraper

# scraper
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }
)

# dns configuration
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
# dns configuration

uri = "mongodb+srv://angel:jtNJyb7YRWZxoEVk@cluster0.5hbizqi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))


def get_database():
    return client['inject']

def checkKey(key):
    dbname = get_database()
    collection = dbname["users"]
    user = collection.find_one({'key': key})
    if user:
        return True
    else:
        return False

def createKey(userid, adminKey):
    if adminKey != "3kD9aR8tLp7s2jN6wG5hQ1yPxM4cV0iB2oF8uS7nR":
        return jsonify({'msg': 'invalid admin key','errors': ['invalid_admin_key']})

    dbname = get_database()
    collection = dbname["users"]
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    collection.insert_one({'_id': userid, 'key': key})
    return jsonify({"key": key,"msg": "key successfully generated","errors": []})

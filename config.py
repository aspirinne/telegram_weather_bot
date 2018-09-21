"""
Global variables and configurations.
"""

# Token for bot, learn more at:
# https://tlgrm.ru/docs/bots#create-a-new-bot
TOKEN = '625422568:AAHK-vDuGFjPCoiidWKe_X6b7TQpCsX54fg'

# Database
DATABASE = {
    'name': 'weather_bot_db',
    'user': 'postgres',
    'password': 'Kbyljy13',
    'host': 'localhost',
    'port': '5432',
}

# Proxy, if you need...
PROXY = {
    # 'is_need': True,
    'is_need': False,
    'ip': '137.117.227.71',
    'port': '3128',
}

# Weather provider
# TODO: refactor by the new functions requirement.
WEATHER = {
    'provider': 'http://api.openweathermap.org/data/2.5/weather',
    'api_key': 'c3d107b5a0441a124a4686347c8d53da',
}

ADMIN = {
    'name': 'Rafael Galiev',
    'mail': 'rafael.galiev.kazan@gmail.com',
    'chat_id': 227836750,
}

COMMANDS = {
    'start': '/start - begin to use this bot;',
    'help': '/help - get this help message;',
    'settings': '/settings - get list of changeable settings;',
    'now': '/now - get current weather;',
}

SETTINGS = {
    'city': '/city - set/change your city;',
}

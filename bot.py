import config
from users import User

import telebot
import psycopg2
import requests
# import time


# TODO: Separate the different methods in different classes/files. Ato pizdec, chert nogu slomit...
# TODO: "Weather for some hours" function.
if config.PROXY['is_need']:
    telebot.apihelper.proxy = {
      'https': 'https://{}:{}'.format(config.PROXY['ip'], config.PROXY['port'])
    }

bot = telebot.TeleBot(config.TOKEN)


def get_current_weather(city):
    """
    Getting the current weather for city.
    :param city: City or City,COUNTRY_CODE or int(city_id)
    :return: dictionary ( learn more at https://openweathermap.org/current#current_JSON ).
    """

    parametres = {
        'type': 'like',
        'units': 'metric',
        'lang': 'ru',
        'APPID': config.WEATHER['api_key'],
    }

    if type(city) is int:
        parametres.update({'id': city})
    else:
        parametres.update({'q': city})

    res = requests.get(
        config.WEATHER['provider'],
        params=parametres
    )

    data = res.json()
    return data


def set_city(message):
    """
    Method to change the city and country of user in database.
    :param message: Message from user. It looks like JSON ( learn more at https://tlgrm.ru/docs/bots/api#message ).
    :return:
    """
    try:
        chat_id = message.chat.id
        location = message.text.split(',')
        city = location[0]
        country = location[1]
    except Exception as err:
        print(err)
        bot.reply_to(message, 'Try again...')
        bot.register_next_step_handler(message, set_city)
    else:
        user = User()
        user.change_location_for_user(chat_id, city, country)
        # conn = psycopg2.connect(dbname=config.DATABASE['name'], user=config.DATABASE['user'],
        #                         password=config.DATABASE['password'])
        # cur = conn.cursor()
        #
        # try:
        #     cur.execute(
        #         """
        #         UPDATE users
        #         SET city = %(city)s, country = %(country)s, city_id = NULL
        #         WHERE chat_id = %(chat_id)s;
        #         """,
        #         {
        #             'city': city,
        #             'country': country,
        #             'chat_id': chat_id,
        #         }
        #     )
        #
        # except psycopg2.DatabaseError as err:
        #     print(err)
        #     bot.send_message(config.ADMIN['chat_id'], err)
        # else:
        #     conn.commit()
        #     bot.send_message(chat_id, 'Your city updated!')
        # finally:
        #     cur.close()
        #     conn.close()
        bot.send_message(chat_id, 'Your city updated!')


@bot.message_handler(commands=['start', ])
def start_user(message):
    bot.send_message(message.chat.id, 'Hi, {}!\nNice to see you!'.format(message.chat.first_name))

    if message.chat.id != config.ADMIN['chat_id']:
        bot.send_message(config.ADMIN['chat_id'], u'Кто то еще кроме тебя забрался в эту помойку!')

    user = User()

    if not user.is_user_exist(message.chat.id):
        user.set_user(message.chat.id, message.chat.first_name)

    bot.send_message(message.chat.id, 'Please set your city by the\n/city command')


@bot.message_handler(commands=['help', ])
def help_message(message):
    u"""
    '/help' - отображает сообщение с помощью по командам.
    Оно может представлять собой короткое сообщение о вашем боте и список доступных команд.
    :param message:
    :return:
    """

    about_bot = "This bot can send you info about current weather!\n" \
                "Let's try with /now command!"

    commands_list = ';\n'.join(config.COMMANDS.values())
    commands_list += '\n\n' + ';\n'.join(config.SETTINGS.values())

    bot.send_message(message.chat.id, about_bot)
    bot.send_message(message.chat.id, commands_list)


@bot.message_handler(commands=['settings', ])
def settings_message(message):
    u"""
    '/settings' — (по возможности) возвращает список возможных настроек
    и команды для их изменения.
    :param message:
    :return:
    """
    settings_list = ';\n'.join(config.SETTINGS.values())
    bot.send_message(message.chat.id, settings_list)


@bot.message_handler(commands=['city', ])
def change_city(message):
    """
    Method which spelled when user send '/city' command to bot and ask him to send the name of city.
    :param message: Message from user. It looks like JSON ( learn more at https://tlgrm.ru/docs/bots/api#message ).
    :return:
    """
    question_about_city = u'Введи название своего города и буквенный код страны.\n' \
                          u'Например: London,EN'
    bot.send_message(message.chat.id, question_about_city)

    bot.register_next_step_handler(message, set_city)


@bot.message_handler(commands=['now', ])
def send_current_weather(message):
    """
    Method which spelled when user send '/now' command to bot and send him the current weather.
    :param message: Message from user. It looks like JSON ( learn more at https://tlgrm.ru/docs/bots/api#message ).
    :return:
    """

    user = User()
    user_info = user.get_user_by_chat_id(message.chat.id)

    if user_info[-1] is None:
        data = get_current_weather(','.join(user_info[3:5]))
        user.update_city_id_for_user(message.chat.id, data["id"])
    else:
        data = get_current_weather(user_info[-1])

    # TODO: Add more information and some icons.

    response_message = ''
    response_message += u'Описание: ' + data['weather'][0]['description'] + '\n'
    response_message += u'Температура: ' + str(data['main']['temp']) + u'\N{DEGREE SIGN}'
    bot.send_message(message.chat.id, response_message)


if __name__ == '__main__':
    bot.polling(none_stop=True)

    # while True:
    #     try:
    #         bot.polling(none_stop=True)
    #
    #     except Exception as e:
    #         print(e)
    #         time.sleep(15)

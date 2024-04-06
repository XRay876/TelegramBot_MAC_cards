from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import telebot
import os, random
from auth_data import token


bot = telebot.TeleBot(token)


def start_markup():
    markup = types.InlineKeyboardMarkup(row_width=True)
    link_keyboard1 = types.InlineKeyboardButton(text="Думай Дыши Твори", url = "https://t.me/think_breathe_create")
    check_keyboard = types.InlineKeyboardButton(text="Проверить", callback_data= "check")
    markup.add(link_keyboard1, check_keyboard)
    return markup

def cards_markup():
    markup = types.InlineKeyboardMarkup(row_width=True)
    themes_keyboard = types.InlineKeyboardButton(text="Темы", callback_data="themes")
    guide_keyboard = types.InlineKeyboardButton(text="Инструкция", callback_data="guide")
    markup.add(themes_keyboard, guide_keyboard)

    return markup

def themes_markup():
    markup = types.InlineKeyboardMarkup(row_width=True)
    money_n_busButton = types.InlineKeyboardButton(text="Деньги и бизнес", callback_data="money_n_bus")
    relationshipsButton = types.InlineKeyboardButton(text="Отношения", callback_data="relationships")
    selfknowledgeButton = types.InlineKeyboardButton(text="Самопознание", callback_data="selfknowledge")
    startnewButton = types.InlineKeyboardButton(text="Изменения в жизни", callback_data="start_new")
    ur_quesButton = types.InlineKeyboardButton(text="Другое", callback_data="ur_ques")
    markup.add(money_n_busButton, relationshipsButton, selfknowledgeButton, startnewButton, ur_quesButton)
    return markup

def sureness(chat_id, type=None):
    return bot.send_message(chat_id, "Уверены?", reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
        types.InlineKeyboardButton(text="Показать", callback_data="show_card"),
        types.InlineKeyboardButton(text="Назад", callback_data="Back")))


def check(user_id):
    status = ['creator', 'administrator', 'member']
    user_status = bot.get_chat_member(chat_id='-1002053959225', user_id=user_id).status
    return user_status in status


def send_random_photo(chat_id, type, user_id=None, arg=False):
    if check(user_id):

        if type == 1:
            directory = "cards/money_n_business"
        if type == 2:
            directory = "cards/Relationships"
        if type == 3:
            directory = "cards/Selfknowledge"
        if type == 4:
            directory = "cards/start_new"


        if not os.path.exists(directory) or not os.listdir(directory):
            bot.send_message(chat_id, "Извините, изображения в данный момент недоступны.")
            return


        filename = random.choice(os.listdir(directory))
        with open(os.path.join(directory, filename), 'rb') as photo:
            bot.send_photo(chat_id, photo)


    else:
        bot.send_message(chat_id, "Подпишитесь на канал, пожалуйста, для доступа к боту", reply_markup=start_markup())




@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name


    if check(chat_id):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        markup1 = ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.add(KeyboardButton('Темы'), KeyboardButton('Инструкция'),)
        bot.send_message(chat_id, 'Приятного пользования ⬇', reply_markup=markup1)

        bot.send_message(chat_id, '*Найди ответ* с помощью метафорических карт \n \n'
                                  '*__Метафорические ассоциативные карты__* – это инструмент самопознания и ответов на вопросы\, '
                                  'которые волнуют вас\. Они помогают лучше понять ситуацию и найти правильное решение\. '
                                  'Задайте вопрос\, например\, о вас\, текущих отношениях или будущих изменениях\, и карта '
                                  'предложит направление для размышлений\. \n \n'
                                  '*__Выберите тему__*\, которая откликается на ваше текущее состояние '
                                  'или интересы\, и позвольте метафорическим картам дать ответ\.',
                         parse_mode='MarkdownV2',
                         reply_markup=cards_markup())





    else:
        bot.send_message(chat_id, f"Привет {first_name}!\n"
                                  f"Чтобы пользоваться ботом подпишитесь на канал!", reply_markup=start_markup())



@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if check(call.from_user.id):
        if call.data == "check":
            bot.answer_callback_query(call.id, "Вы уже подписаны на канал!")
            start(call.message)
        if call.data == "themes":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Темы")
            bot.send_message(call.message.chat.id, '*К какой теме относится ваш вопрос* ⬇', parse_mode='MarkdownV2', reply_markup=themes_markup())
        if call.data == "guide":
            bot.answer_callback_query(call.id, "Инструкция")
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, '*__Как правильно задать вопрос\?__* \n \n'
                                                   '*_1\._* Выберите из предложенных тем ту\, к которой относится ваш вопрос\. \n'
                                                   'Если ни одна из тем не подходит\, выберите *\"Другое\"* \n'
                                                   '*_2\._* Сосредоточьтесь на вашем вопросе\. Обдумайте его и четко сформулируйте\. \n'
                                                   'Например\: _Почему у меня долги\? '
                                                   'Какие свои ресурсы я не использую\? Что мне поможет начать бизнес\? Какие мои сильные качества\? '
                                                   'Почему у меня сложности в отношениях\? Что мне изменить, чтобы улучшить отношения\?_ \n'
                                                   '*_3\._* Нажмите кнопку *\"Показать\"*\. Посмотрите на карту и опишите\, что вы видите в контексте своего вопроса\. '
                                                   '_Где вы на ней видите себя\, что вас окружает\, что мешает или поддерживает\._ \n'
                                                   '*_4\._* __Один вопрос \- одна карта\.__ Если возникает следующий вопрос\, то концентрируетесь '
                                                   'на нем\, нажимаете на *\"Показать другую\"* и получаете следующую\!', parse_mode='MarkdownV2',
                             reply_markup=types.InlineKeyboardMarkup(row_width=True).add(types.InlineKeyboardButton(text="Выбор темы", callback_data="themes")))


        if call.data == "money_n_bus":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Уверены?")
            bot.send_message(call.message.chat.id, "Уверены?", reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
                types.InlineKeyboardButton(text="Показать", callback_data="show_card_money_n_bus"),
                types.InlineKeyboardButton(text="Назад", callback_data="Back")))
        if call.data == "relationships":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Уверены?")
            bot.send_message(call.message.chat.id, "Уверены?", reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
                types.InlineKeyboardButton(text="Показать", callback_data="show_card_relationships"),
                types.InlineKeyboardButton(text="Назад", callback_data="Back")))
        if call.data == "selfknowledge":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Уверены?")
            bot.send_message(call.message.chat.id, "Уверены?", reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
                types.InlineKeyboardButton(text="Показать", callback_data="show_card_selfknowledge"),
                types.InlineKeyboardButton(text="Назад", callback_data="Back")))
        if call.data == "start_new":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Уверены?")
            bot.send_message(call.message.chat.id, "Уверены?", reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
                types.InlineKeyboardButton(text="Показать", callback_data="show_card_startnew"),
                types.InlineKeyboardButton(text="Назад", callback_data="Back")))
        if call.data == "ur_ques":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Уверены?")
            bot.send_message(call.message.chat.id, "Уверены?", reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
                types.InlineKeyboardButton(text="Показать", callback_data="show_card_ur_ques"),
                types.InlineKeyboardButton(text="Назад", callback_data="Back")))



        if call.data == "show_card_money_n_bus":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Загрузка")
            bot.send_message(call.message.chat.id, 'Ищи ответ ⬇')
            send_random_photo(call.message.chat.id, 1, call.from_user.id)
            bot.send_message(call.message.chat.id, 'Нашли ответ?', reply_markup=types.InlineKeyboardMarkup(row_width=True).
                             add(types.InlineKeyboardButton(text="Показать другую", callback_data="show_card_money_n_bus"),
                             types.InlineKeyboardButton(text="Темы", callback_data="Back")))

        if call.data == "show_card_relationships":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Загрузка")
            bot.send_message(call.message.chat.id, 'Ищи ответ ⬇')
            send_random_photo(call.message.chat.id, 2, call.from_user.id)
            bot.send_message(call.message.chat.id, 'Нашли ответ?', reply_markup=types.InlineKeyboardMarkup(row_width=True).
                             add(types.InlineKeyboardButton(text="Показать другую", callback_data="show_card_relationships"),
                             types.InlineKeyboardButton(text="Темы", callback_data="Back")))

        if call.data == "show_card_selfknowledge":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Загрузка")
            bot.send_message(call.message.chat.id, 'Ищи ответ ⬇')
            send_random_photo(call.message.chat.id, 3, call.from_user.id)
            bot.send_message(call.message.chat.id, 'Нашли ответ?', reply_markup=types.InlineKeyboardMarkup(row_width=True).
                             add(types.InlineKeyboardButton(text="Показать другую", callback_data="show_card_selfknowledge"),
                             types.InlineKeyboardButton(text="Темы", callback_data="Back")))

        if call.data == "show_card_startnew":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Загрузка")
            bot.send_message(call.message.chat.id, 'Ищи ответ ⬇')
            send_random_photo(call.message.chat.id, 4, call.from_user.id)
            bot.send_message(call.message.chat.id, 'Нашли ответ?', reply_markup=types.InlineKeyboardMarkup(row_width=True).
                             add(types.InlineKeyboardButton(text="Показать другую", callback_data="show_card_startnew"),
                             types.InlineKeyboardButton(text="Темы", callback_data="Back")))

        if call.data == "show_card_ur_ques":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Загрузка")
            bot.send_message(call.message.chat.id, 'Ищи ответ ⬇')
            send_random_photo(call.message.chat.id, random.randint(1,4), call.from_user.id)
            bot.send_message(call.message.chat.id, 'Нашли ответ?', reply_markup=types.InlineKeyboardMarkup(row_width=True).
                             add(types.InlineKeyboardButton(text="Показать другую", callback_data="show_card_ur_ques"),
                             types.InlineKeyboardButton(text="Темы", callback_data="Back")))

        if call.data == "Back":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Назад")
            bot.send_message(call.message.chat.id, '*К какой теме относится ваш вопрос* ⬇', parse_mode='MarkdownV2', reply_markup=themes_markup())




    else:
        bot.answer_callback_query(call.id, "Пожалуйста, подпишитесь на канал.")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Подпишитесь на канал, чтобы использовать бота.", reply_markup=start_markup())




@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привки")
    elif message.text.lower() == "деньги и бизнес":
        bot.send_message(message.chat.id, "Уверены?", reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
            types.InlineKeyboardButton(text="Показать", callback_data="show_card_money_n_bus"),
            types.InlineKeyboardButton(text="Назад", callback_data="Back")))
    elif message.text.lower() == "отношения":
        bot.send_message(message.chat.id, "Уверены?", reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
            types.InlineKeyboardButton(text="Показать", callback_data="show_card_relationships"),
            types.InlineKeyboardButton(text="Назад", callback_data="Back")))
    elif message.text.lower() == "cампознание":
        bot.send_message(message.chat.id, "Уверены?", reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
            types.InlineKeyboardButton(text="Показать", callback_data="show_card_selfknowledge"),
            types.InlineKeyboardButton(text="Назад", callback_data="Back")))
    elif message.text.lower() == "изменения в жизни":
        bot.send_message(message.chat.id, "Уверены?", reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
            types.InlineKeyboardButton(text="Показать", callback_data="show_card_startnew"),
            types.InlineKeyboardButton(text="Назад", callback_data="Back")))
    elif message.text.lower() == "cвой вопрос":
        bot.send_message(message.chat.id, "Уверены?", reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
            types.InlineKeyboardButton(text="Показать", callback_data="show_card_ur_ques"),
            types.InlineKeyboardButton(text="Назад", callback_data="Back")))
    elif message.text.lower() == "темы":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(message.chat.id, '*К какой теме относится ваш вопрос* ⬇', parse_mode='MarkdownV2', reply_markup=themes_markup())
    elif message.text.lower() == "инструкция":
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(message.chat.id, '*__Как правильно задать вопрос\?__* \n \n'
                                               '*_1\._* Выберите из предложенных тем ту\, к которой относится ваш вопрос\. \n'
                                               'Если ни одна из тем не подходит\, выберите *\"Другое\"* \n'
                                               '*_2\._* Сосредоточьтесь на вашем вопросе\. Обдумайте его и четко сформулируйте\. \n'
                                               'Например\: _Почему у меня долги\? '
                                               'Какие свои ресурсы я не использую\? Что мне поможет начать бизнес\? Какие мои сильные качества\? '
                                               'Почему у меня сложности в отношениях\? Что мне изменить, чтобы улучшить отношения\?_ \n'
                                               '*_3\._* Нажмите кнопку *\"Показать\"*\. Посмотрите на карту и опишите\, что вы видите в контексте своего вопроса\. '
                                               '_Где вы на ней видите себя\, что вас окружает\, что мешает или поддерживает\._ \n'
                                               '*_4\._* __Один вопрос \- одна карта\.__ Если возникает следующий вопрос\, то концентрируетесь '
                                               'на нем\, нажимаете на *\"Показать другую\"* и получаете следующую\!',
                         parse_mode='MarkdownV2',
                         reply_markup=types.InlineKeyboardMarkup(row_width=True).add(
                             types.InlineKeyboardButton(text="Выбор темы", callback_data="themes")))

    else:
        bot.send_message(message.chat.id, '*К какой теме относится ваш вопрос:* ⬇', parse_mode='MarkdownV2', reply_markup=themes_markup())




bot.infinity_polling()
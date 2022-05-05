import telebot
from telebot import types
import os
import shutil
from func import get_images, get_vectors_from_images, tokenize_text, get_vector_from_tokens, get_result, \
    make_result_funny, make_secret_key
import requests

bot = telebot.TeleBot('')

chats = {}


@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id not in chats:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/clear")
        btn2 = types.KeyboardButton("/end")
        markup.add(btn1, btn2)
        chats[message.chat.id] = {'proc': False, 'txt': '', 'pht': 0}
        bot.send_message(message.chat.id, 'Здравствуйте!'
                                          '\nОтправьте мне данные для анализа.'
                                          '\nДля сброса фото введите\n/clear'
                                          '\nПосле окончания ввода введите\n/end', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, "Команда сейчас не доступна")


@bot.message_handler(commands=["end"])
def end(message):
    if message.chat.id in chats and not chats[message.chat.id]['proc'] and (
            chats[message.chat.id]['txt'] and chats[message.chat.id]['pht']):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/start")
        markup.add(btn1)
        bot.send_message(message.chat.id, "Данные приняты для анализа")
        chats[message.chat.id]['proc'] = True
        images = get_vectors_from_images(get_images(message.chat.id))
        texts = get_vector_from_tokens(*tokenize_text(chats[message.chat.id]['txt']))
        result = float(f"{get_result(images, texts)[0][0] * 100:.3f}")
        for_link = make_secret_key()
        request = requests.post('http://localhost:8080/api/user', json={'chat_id': message.chat.id, 'ident': for_link})
        if request:
            gif = make_result_funny(result)
            if gif:
                bot.send_video(message.chat.id, gif, reply_markup=markup)
            bot.send_message(message.chat.id,
                             f"Результат анализа - {result}%\n\n❗❗❗Результат примерный. Не советуем на него полагаться❗❗❗",
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, '❗❗❗ПРОИЗОШЛА ОШИБКА❗❗❗',
                             reply_markup=markup)
        del chats[message.chat.id]
        shutil.rmtree(f'data/{message.chat.id}')
    elif not (message.chat.id in chats):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/start")
        markup.add(btn1)
        bot.send_message(message.chat.id, "Чтобы бот начал работу, введите /start", reply_markup=markup)
    elif chats[message.chat.id]['proc']:
        bot.send_message(message.chat.id, "Бот занят! Скоро будет предсказание)")
    else:
        bot.send_message(message.chat.id, "Команда сейчас не доступна")


@bot.message_handler(commands=["clear"])
def clear(message):
    if message.chat.id in chats and not chats[message.chat.id]['proc'] and chats[message.chat.id]['pht']:
        chats[message.chat.id]['pht'] = 0
        shutil.rmtree(f'data/{message.chat.id}')
        bot.send_message(message.chat.id, "Фото удалены")
    elif not (message.chat.id in chats):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/start")
        markup.add(btn1)
        bot.send_message(message.chat.id, "Чтобы бот начал работу, введите /start", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Команда сейчас не доступна")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.chat.id in chats and not chats[message.chat.id]['proc']:
        new_text = message.text
        if not chats[message.chat.id]['txt']:
            bot.send_message(message.chat.id, "Текст принят")
        else:
            bot.send_message(message.chat.id, "Текст изменён")
        chats[message.chat.id]['txt'] = new_text
    elif not (message.chat.id in chats):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/start")
        markup.add(btn1)
        bot.send_message(message.chat.id, "Чтобы бот начал работу, введите /start", reply_markup=markup)
    elif chats[message.chat.id]['proc']:
        bot.send_message(message.chat.id, "Бот занят! Скоро будет предсказание)")


@bot.message_handler(content_types=['photo'])
def handle_docs_document(message):
    if message.chat.id in chats and not chats[message.chat.id]['proc'] and chats[message.chat.id]['pht'] < 10:
        chats[message.chat.id]['pht'] += 1
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f"data/{message.chat.id}/{chats[message.chat.id]['pht']}.jpg"
        try:
            os.mkdir('/'.join(src.split('/')[:-1]))
        except OSError:
            pass
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Фото принято")
    elif not (message.chat.id in chats):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/start")
        markup.add(btn1)
        bot.send_message(message.chat.id, "Чтобы бот начал работу, введите /start", reply_markup=markup)
    elif chats[message.chat.id]['proc']:
        bot.send_message(message.chat.id, "Бот занят! Скоро будет предсказание)")
    elif chats[message.chat.id]['pht'] == 10:
        bot.send_message(message.chat.id, "Лимит фотографий превышен")


bot.polling(none_stop=True, interval=0)

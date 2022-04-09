import telebot
import numpy as np
import os
import cv2
import pickle
import tensorflow as tf

bot = telebot.TeleBot('')

chats = {}


@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id not in chats:
        chats[message.chat.id] = {'proc': False, 'txt': '', 'pht': 0}
        bot.send_message(message.chat.id,
                         'Здравствуйте!\nОтправьте мне данные для анализа.\nПосле окончания ввода введите /end')
    else:
        bot.send_message(message.chat.id, "Команда сейчас не доступна")


@bot.message_handler(commands=["end"])
def end(message):
    if message.chat.id in chats and not chats[message.chat.id]['proc'] and (
            chats[message.chat.id]['txt'] or chats[message.chat.id]['pht']):
        bot.send_message(message.chat.id, "Данные приняты для анализа")
        chats[message.chat.id]['proc'] = True
        # нейронка
        del chats[message.chat.id]
    elif not (message.chat.id in chats):
        bot.send_message(message.chat.id, "Чтобы бот начал работу, введите /start")
    elif chats[message.chat.id]['proc']:
        bot.send_message(message.chat.id, "Бот занят! Скоро будет предсказание)")
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
        bot.send_message(message.chat.id, "Чтобы бот начал работу, введите /start")
    elif chats[message.chat.id]['proc']:
        bot.send_message(message.chat.id, "Бот занят! Скоро будет предсказание)")


@bot.message_handler(content_types=['photo'])
def handle_docs_document(message):
    if message.chat.id in chats and not chats[message.chat.id]['proc'] and chats[message.chat.id]['pht'] < 10:
        chats[message.chat.id]['pht'] += 1
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f"data/{message.chat.id}_{chats[message.chat.id]['pht']}.jpg"
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Фото принято")
    elif not (message.chat.id in chats):
        bot.send_message(message.chat.id, "Чтобы бот начал работу, введите /start")
    elif chats[message.chat.id]['proc']:
        bot.send_message(message.chat.id, "Бот занят! Скоро будет предсказание)")
    elif chats[message.chat.id]['pht'] == 10:
        bot.send_message(message.chat.id, "Лимит фотографий превышен")


bot.polling(none_stop=True, interval=0)

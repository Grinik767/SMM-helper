import telebot

bot = telebot.TeleBot('')
idd = ''
coef = 0
txt = False
pht = 0
st = False
b = False


@bot.message_handler(commands=["start"])
def start(m, res=False):
    global txt, pht, idd, st
    st = True
    txt, pht = False, False
    idd = m.chat.id
    bot.send_message(m.chat.id, 'Здравствуйте!\nОтправьте мне данные для анализа.\nПосле окончания ввода введите /end')


@bot.message_handler(commands=["end"])
def end(message, res=False):
    global st, b
    if st:
        if not txt and not pht:
            bot.send_message(message.chat.id, "Данные не введены")
        else:
            b = True
        if b:
            bot.send_message(message.chat.id, "Данные приняты для анализа")
            ##bot.send_message(idd, f"коэфицент равен {coef}")
            st = False
    else:
        bot.send_message(message.chat.id, "Команда сейчас не доступна")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global txt, s
    if st:
        s = message.text
        if not txt:
            txt = True
            bot.send_message(message.chat.id, "Текст принят")
        else:
            bot.send_message(message.chat.id, "Текст изменён")
    elif not st:
        bot.send_message(message.chat.id, "Чтобы бот начал работу, введите /start")


@bot.message_handler(content_types=['photo'])
def handle_docs_document(message):
    global pht
    if st and pht < 10:
        pht += 1
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'C:/works/data/' + message.photo[1].file_id + '.jpg'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Фото принято")
    elif not st:
        bot.send_message(message.chat.id, "Чтобы бот начал работу, введите /start")
    else:
        bot.send_message(message.chat.id, "Лимит фотографий превышен")



bot.polling(none_stop=True, interval=0)

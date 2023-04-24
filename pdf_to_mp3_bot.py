import telegram
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    TypeHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)
from gtts import gTTS
import pdfplumber
from pathlib import Path
import urllib.request

# Здесь нужно указать токен вашего бота
TOKEN = '5764444819:AAEUpn_tHlvB_Dv4aqOCUTlB8LrkV9fG9Vw'
bot = telegram.Bot(token=TOKEN)

# Перечень кнопок
button1 = KeyboardButton('Отправить pdf файл')
button2 = KeyboardButton('Выбрать русский язык')
button3 = KeyboardButton('Выбрать английский язык')
markup = ReplyKeyboardMarkup([[button1], [button2], [button3]], resize_keyboard=True)
language = 'ru'


def ask_what_to_do(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Что сделать?', reply_markup=markup)


def button1(update, context):
    update.message.reply_text('Отправьте мне pdf файл')


def button2(update, context):
    global language
    language = 'ru'
    print(f'Выбран {language} язык')


def button3(update, context):
    global language
    language = 'en'
    print(f'Выбран {language} язык')


def ask_what_to_do(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Что сделать?', reply_markup=markup)


# Получение и сохранение файла от пользователя
def handle_pdf(update, context):
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    file = bot.getFile(file_id)
    file_url = file.file_path
    urllib.request.urlretrieve(file_url, f'{file_name}')

    # update.message.reply_text(
    #     "Если текст на русском языке, напиши 'ru', если на английском - 'en' ")

    print('Файл получен и сохранен')


# # Обработчик команды /pdf_to_mp3
# def pdf_to_mp3(update: Update, context: CallbackContext) -> None:
#     file = update.message.document.file_id
#     file_name = update.message.document.file_name
#     language = context.args[0] if context.args else 'en'
#
#     print('Файл почучен')
#
#     update.message.reply_text('[+] Working in progress...')
#
#     # Скачиваем PDF-файл с помощью bot.get_file и pdfplumber
#     pdf_file = context.bot.get_file(file)
#     with pdf_file.download() as f:
#         with pdfplumber.open(f) as pdf:
#             pages = []
#             for page in pdf.pages:
#                 pages.append(page.extract_text())
#
#     # Конвертируем текст из PDF в аудио
#     text = ''.join(pages).replace('\n', '')
#     audio = gTTS(text=text, lang=language, slow=False)
#
#     # Сохраняем MP3-файл и отправляем пользователю
#     audio_file_name = f'{Path(file_name).stem}.mp3'
#     audio.save(audio_file_name)
#     update.message.reply_audio(audio=open(audio_file_name, 'rb'))


# Обработчик команды /start
# def start(update: Update, context: CallbackContext) -> None:
#     keyboard = [[InlineKeyboardButton('Отправить pdf', callback_data='1'),
#                  InlineKeyboardButton('Русский язык', callback_data='2'),
#                  InlineKeyboardButton('Английский язык', callback_data='3')]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text('Пожалуйста, выберите: ', reply_markup=reply_markup)


def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    # Добавляем обработчики команд
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Отправить pdf файл'), button1))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Выбрать русский язык'), button2))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Выбрать английский язык'), button3))
    updater.dispatcher.add_handler(MessageHandler(Filters.document.pdf, handle_pdf))
    updater.dispatcher.add_handler(TypeHandler(Update, ask_what_to_do))

    # Запускаем бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()



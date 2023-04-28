import telegram
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
from gtts import gTTS
import pdfplumber
import settings

# Токен
TOKEN = settings.TOKEN
bot = telegram.Bot(token=TOKEN)
language = ''


# Кнопка "Отправить файл"
def button1(update, context):
    global language
    if language == '':
        update.message.reply_text('Сначала выберите язык, потом отправьте pdf файл')
    else:
        update.message.reply_text('Отправьте мне pdf файл')


# Кнопка "Выбрать русский язык"
def button2(update, context):
    global language
    language = 'ru'
    print(f'Выбран {language} язык')
    update.message.reply_text('Выбран русский язык, теперь отправьте pdf файл')


# Кнопка "Выбрать английский язык"
def button3(update, context):
    global language
    language = 'en'
    print(f'Выбран {language} язык')
    update.message.reply_text('Выбран английский язык, теперь отправьте pdf файл')


# Получение и сохранение файла от пользователя
def pdf_to_mp3(update, context):
    global language
    if language == '':
        update.message.reply_text('Сначала выберите язык, потом отправьте pdf файл')
    else:
        # Скачиваем файл пдф
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name
        file_path = f'download_pdf/{file_name}'
        file = bot.get_file(file_id)
        downloaded_file = file.download(file_path)
        print('Файл загружен')

        # Считываем пдф и переводим в текст
        with pdfplumber.PDF(open(downloaded_file, 'rb')) as pdf:
            pages = []
            for page in pdf.pages:
                pages.append(page.extract_text())
            text = ''.join(pages).replace('\n', '')

        update.message.reply_text('Идет процесс конвертации файла...\nВремя конвертации зависит от размера файла...')

        # Конвертируем текст из PDF в аудио
        audio = gTTS(text=text, lang=language, slow=False)

        # Сохраняем MP3-файл и отправляем пользователю
        audio_file_name = str(file_name)
        n = 4
        audio_file_name = audio_file_name[:-n]
        audio_file_name = f'{audio_file_name}.mp3'
        audio.save(f'download_audio/{audio_file_name}')
        update.message.reply_audio(audio=open(f'download_audio/{audio_file_name}', 'rb'))

        update.message.reply_text('Конвертация завершена. Приятного прослушивания.\n'
                                  'Для конвертации другого файла нажмите /start')

        # Обнуляем язык
        language = ''


# Если в чат отправляется не pdf файл
def not_pdf(update, context):
    update.message.reply_text('Данный формат не поддерживается.\nОтправьте файл в формате pdf')


# Обработчик команды /start
def start(update, context):
    button1 = KeyboardButton('Отправить pdf файл')
    button2 = KeyboardButton('Выбрать русский язык')
    button3 = KeyboardButton('Выбрать английский язык')
    markup = ReplyKeyboardMarkup([[button2, button3], [button1]], resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Сначала выберите язык, потом отправьте pdf файл', reply_markup=markup)


def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    # Добавляем обработчики команд
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Отправить pdf файл'), button1))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Выбрать русский язык'), button2))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Выбрать английский язык'), button3))
    updater.dispatcher.add_handler(MessageHandler(Filters.document.pdf, pdf_to_mp3))
    updater.dispatcher.add_handler(MessageHandler(~Filters.document.pdf, not_pdf))

    # Запускаем бота
    updater.start_polling()
    print('Бот запущен')
    updater.idle()


if __name__ == '__main__':
    main()

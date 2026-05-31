import os
import tempfile
import requests
import telebot

yolo_api = "http://model_products:5000/detect"   
easyocr_api = "http://model_receipts:5000/ocr"     
TOKEN_BOT = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN_BOT)
itog = {}

@bot.message_handler(commands=['start'])
def start(message):
    itog.pop(message.chat.id, None)
    bot.reply_to(message, 'Пришлите фото/видео продуктов (овощи/фрукты)')

@bot.message_handler(content_types=['photo', 'video'])
def sort_product_or_check(message):
    chat_id = message.chat.id
    if chat_id in itog:
        detect_check(message, chat_id)
    else:
        detect_product(message, chat_id)

def detect_product(message, chat_id):

    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        suffix = '.jpg'
    else:   
        file_id = message.video.file_id
        suffix = '.mp4'

    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(downloaded)
        tmp_name = tmp.name

    with open(tmp_name, 'rb') as f:
        resp = requests.post(yolo_api, files={'file': f})
        data = resp.json()
        detected = data['products']

    os.unlink(tmp_name)

    itog[chat_id] = detected
    object_detected = " ".join(f"{item['name']}: {item['count']} шт." for item in detected)
    bot.reply_to(message, f"Найдено: {object_detected}\nПришлите фото чека.")

def detect_check(message, chat_id):

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)

    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        tmp.write(downloaded)
        tmp_name = tmp.name

    with open(tmp_name, 'rb') as f:
        resp = requests.post(easyocr_api, files={'file': f})
        items = resp.json()['check'] 

    os.unlink(tmp_name)

    detected = itog.pop(chat_id, [])
    result = sravnenie_for_check(detected, items)

    bot.reply_to(message, result)

def sravnenie_for_check(detected, items):
    detected_products = [item['name'].lower().strip() for item in detected]
    detected_check = [name.lower().strip() for name in items]

    try_det_and_false_check = []
    for prod in detected_products:
        if not any(prod.startswith(ch) or ch.startswith(prod) for ch in detected_check):
            try_det_and_false_check.append(prod)

    false_det_and_try_check = []
    for ch in detected_check:
        if not any(ch.startswith(prod) or prod.startswith(ch) for prod in detected_products):
            false_det_and_try_check.append(ch)

    result = ""
    if try_det_and_false_check:
        result += f"Не хватает в чеке: {', '.join(try_det_and_false_check)}\n"
    if false_det_and_try_check:
        result += f"Лишнее в чеке: {', '.join(false_det_and_try_check)}\n"
    if not result:
        result = 'совпадает'
    return result

if __name__ == '__main__':
    bot.polling(non_stop=True)

import requests
from states import load
# Load environment variables from .env file
from dotenv import load_dotenv
import os
import model

# Load environment variables from .env file
load_dotenv('.env', override=True)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()


def send_photo(photo_path, caption=None, cctv=None, object_id=None):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
    with open(photo_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': TELEGRAM_CHAT_ID}
        if caption:
            data['caption'] = caption
        response = requests.post(url, files=files, data=data)
        # save to db
        model.save_to_db(photo_path, cctv, object_id)
    return response.json()

# res = send_message('sudah update')
# print(res)


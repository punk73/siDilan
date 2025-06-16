import requests
from states import load
# Load environment variables from .env file


env = load('env.json')
# Replace with your actual Telegram Bot Token
TELEGRAM_BOT_TOKEN = env['TELEGRAM_BOT_TOKEN']
# Replace with your chat ID or the chat ID to which messages should be sent
TELEGRAM_CHAT_ID = env['TELEGRAM_CHAT_ID']  # You can also make this dynamic

def send_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()


# res = send_message('Hello world')
# print(res)


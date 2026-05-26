import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '886769'
API_KEY = '863bb56ef29bf0f48d3ae70a759a5463'

URL_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'

EMOJI_CODE = {
    200: '⛈️',
    800: '☀️',
    801: '🌤️',
    802: '⛅',
    803: '🌥️',
    804: '☁️'
}

bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_weather = KeyboardButton('Получить погоду 🌍', request_location=True)
button_about = KeyboardButton('О проекте ℹ️')
keyboard.add(button_weather)
keyboard.add(button_about)


def get_weather(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'lang': 'ru',
        'units': 'metric',
        'appid': API_KEY
    }
    try:
        response = requests.get(url=URL_WEATHER_API, params=params).json()
        if response.get('cod') != 200:
            return " Не удалось получить данные о погоде."

        city_name = response['name']
        description = response['weather'][0]['description']
        code = response['weather'][0]['id']
        temp = response['main']['temp']
        temp_feels_like = response['main']['feels_like']
        humidity = response['main']['humidity']

        emoji = EMOJI_CODE.get(code, '🌡️')

        message = f'📍 Погода в: {city_name}\n'
        message += f'{emoji} {description.capitalize()}.\n'
        message += f'🌡️ Температура: {temp}°C.\n'
        message += f'🤔 Ощущается как: {temp_feels_like}°C.\n'
        message += f'💧 Влажность: {humidity}%.'
        return message
    except:
        return "⚠️ Произошла ошибка при обработке запроса."


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = '👋 Привет! Отправь мне свое местоположение с помощью кнопки, и я отправлю тебе текущую погоду. 🌤️'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.message_handler(regexp='О проекте')
def send_about(message):
    text = (
        "🤖 О боте: Это простой погодный ассистент.\n"
        "📍 Он умеет определять погоду по вашей геолокации.\n\n"

    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon = message.location.longitude
    lat = message.location.latitude
    bot.send_chat_action(message.chat.id, 'find_location')
    result = get_weather(lat, lon)
    if result:
        bot.send_message(message.chat.id, result, reply_markup=keyboard)


if name == 'main':
    bot.infinity_polling()
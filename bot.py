import telebot
import random

TOKEN = "8821361661:AAFFDe3E4-5Mj6ganw_Bh1vfySOuFcv4z9k"
bot = telebot.TeleBot(TOKEN)

users = {}

# Проверка связи при запуске
print("Бот запущен!")
print("Проверяю связь с Telegram...")

try:
    me = bot.get_me()
    print(f"✅ Бот @{me.username} подключён и работает!")
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
    print("Проверь интернет и токен!")

@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.chat.id
    users[user_id] = {
        'number': random.randint(1, 100),
        'attempts': 10
    }
    print(f"📩 Получена команда /start от {user_id}")
    bot.send_message(user_id, "🎮 Я загадал число от 1 до 100. У тебя 10 попыток! Введи число:")

@bot.message_handler(func=lambda message: message.text.isdigit())
def guess_number(message):
    user_id = message.chat.id
    guess = int(message.text)
    print(f"📩 Получено число {guess} от {user_id}")

    if user_id not in users:
        bot.send_message(user_id, "Сначала напиши /start")
        return

    user_data = users[user_id]
    user_data['attempts'] -= 1
    remaining = user_data['attempts']
    secret = user_data['number']

    if guess < 1 or guess > 100:
        user_data['attempts'] += 1
        bot.send_message(user_id, "🚫 Число от 1 до 100! Попытка не засчитана.")
        return

    if guess == secret:
        bot.send_message(user_id, f"🎉 Угадал! Это число {secret}. Сыграем ещё? /start")
        del users[user_id]
        return

    if remaining == 0:
        bot.send_message(user_id, f"😞 Попытки закончились. Я загадал {secret}. /start")
        del users[user_id]
        return

    if guess < secret:
        hint = "📉 Больше!"
    else:
        hint = "📈 Меньше!"

    bot.send_message(user_id, f"{hint} Осталось попыток: {remaining}")

@bot.message_handler(func=lambda message: True)
def other(message):
    user_id = message.chat.id
    print(f"📩 Получено другое сообщение от {user_id}: {message.text}")
    bot.send_message(user_id, "🎮 Введи число от 1 до 100 или /start")

print("Ожидаю сообщения...")
bot.infinity_polling()

import telebot
import random
from telebot import types

TOKEN = "8821361661:AAFFDe3E4-5Mj6ganw_Bh1vfySOuFcv4z9k"
bot = telebot.TeleBot(TOKEN)

users = {}

# Список слов (все 5 букв, 105 слов)
WORDS = [
    "АРБУЗ", "БАНАН", "БЕЛКА", "БУКВА", "ВЕТЕР",
    "ВИЛКА", "ВОЛНА", "ВОРОН", "ГИТАР", "ГОРОД",
    "ГРУША", "ДВЕРЬ", "ДОЖДЬ", "ДОСКА", "ЗАМОК",
    "ЗЕБРА", "КАБАН", "КАРТА", "КНИГА", "КОМАР",
    "КОШКА", "ЛАМПА", "ЛЕНТА", "ЛИМОН", "ЛОДКА",
    "ЛОЖКА", "МАСКА", "МОЛОТ", "МЫШКА", "НОСОК",
    "ОБЛАК", "ПАРТА", "ПИЛОТ", "ПИРОГ", "ПЛИТА",
    "ПОЕЗД", "ПТИЦА", "ПЧЕЛА", "РАМКА", "РОБОТ",
    "РУЧКА", "САЛАТ", "САПОГ", "СВЕЧА", "СУМКА",
    "ТИГРЫ", "ТОЧКА", "ТРАВА", "ТРУБА", "ТЫКВА",
    "ФАКЕЛ", "ФОКУС", "ХВОСТ", "ЦАПЛЯ", "ЧАШКА",
    "ШАПКА", "ШКОЛА", "ШТОРМ", "ЩЕНОК", "ЭКРАН",
    "ЯБЛОК", "ЯГОДА", "ЯКОРЬ", "ГОЛОС", "ДОМИК",
    "КРУЖК", "ЛУНКА", "МОСТЫ", "НОЖИК", "ПЕЧКА",
    "РЫБКА", "СКАЛА", "СОСНА", "БРОВЬ", "ВЕТКА",
    "ГОРКА", "ДЫРКА", "ЖАБКА", "ЗЕРНО", "ИГРУШ",
    "КАМЫШ", "ЛЕСКА", "МАРКА", "БАНКА", "ВИШНЯ",
    "ГАЙКА", "ДРАКА", "ЖИЗНЬ", "ЗАЙКА", "ИСКРА",
    "КАСКА", "КЕПКА", "КОЗАК", "КРУПА", "ЛАВКА",
    "ЛИПКА", "МЕТЛА", "МИСКА", "НАСОС", "ОПОРА",
    "ПАПКА", "ПЕНАЛ", "ПЕТЛЯ", "ПЛИТК", "ПОЛКА",
    "ПРОБА", "РАМПА", "САХАР", "СЕМЬЯ", "СКОТЧ",
    "СМОЛА", "СТЕНА", "СТОПА", "ТАКСА", "ТОСКА"
]

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add("🎯 Угадай число", "✊✋✌️ Камень-ножницы-бумага", "📝 Угадай слово")
    return markup

# Кнопка возврата
def back_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙 В меню")
    return markup

# ============ ИГРА 1: УГАДАЙ ЧИСЛО ============
def start_guess(chat_id):
    users[chat_id] = {'game': 'guess', 'number': random.randint(1, 100), 'attempts': 10}
    bot.send_message(chat_id, "🎯 Я загадал число от 1 до 100. У тебя 10 попыток!\nВведи число:", reply_markup=back_button())

def play_guess(chat_id, guess, user_data):
    user_data['attempts'] -= 1
    rem = user_data['attempts']
    secret = user_data['number']

    if guess < 1 or guess > 100:
        user_data['attempts'] += 1
        bot.send_message(chat_id, "🚫 Число от 1 до 100! Попытка не засчитана.")
        return

    if guess == secret:
        bot.send_message(chat_id, f"🎉 Поздравляю! Ты угадал число {secret}!", reply_markup=main_menu())
        del users[chat_id]
        return

    if rem == 0:
        bot.send_message(chat_id, f"😞 Попытки закончились! Я загадал число {secret}.", reply_markup=main_menu())
        del users[chat_id]
        return

    hint = "📉 Больше!" if guess < secret else "📈 Меньше!"
    bot.send_message(chat_id, f"{hint}\nОсталось попыток: {rem}")

# ============ ИГРА 2: КАМЕНЬ-НОЖНИЦЫ-БУМАГА ============
RPS_EMOJI = {'камень': '✊', 'ножницы': '✌️', 'бумага': '✋'}

def rps_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add("✊ Камень", "✌️ Ножницы", "✋ Бумага", "🔙 В меню")
    return markup

def start_rps(chat_id):
    users[chat_id] = {'game': 'rps'}
    bot.send_message(chat_id, "✊✋✌️ Выбери: камень, ножницы или бумага!", reply_markup=rps_keyboard())

def play_rps(chat_id, choice):
    options = ['камень', 'ножницы', 'бумага']
    bot_choice = random.choice(options)
    
    bot.send_message(chat_id, f"Я выбрал: {RPS_EMOJI[bot_choice]} {bot_choice}")
    bot.send_message(chat_id, f"Ты выбрал: {RPS_EMOJI[choice]} {choice}")

    if choice == bot_choice:
        result = "🤝 Ничья!"
    elif (choice == 'камень' and bot_choice == 'ножницы') or \
         (choice == 'ножницы' and bot_choice == 'бумага') or \
         (choice == 'бумага' and bot_choice == 'камень'):
        result = "🎉 Ты победил!"
    else:
        result = "😞 Я победил!"

    bot.send_message(chat_id, result, reply_markup=main_menu())
    del users[chat_id]

# ============ ИГРА 3: УГАДАЙ СЛОВО ============
def start_word(chat_id):
    word = random.choice(WORDS)
    users[chat_id] = {'game': 'word', 'word': word, 'attempts': 8}
    bot.send_message(chat_id, f"📝 Я загадал слово из 5 букв. У тебя 8 попыток!\nВведи слово:", reply_markup=back_button())

def get_hint(secret_word, guessed_word):
    hint = []
    secret_letters = list(secret_word)
    guess_letters = list(guessed_word)
    used = [False] * len(secret_word)
    
    for i in range(len(guess_letters)):
        if guess_letters[i] == secret_letters[i]:
            hint.append(f"🟢{guess_letters[i]}")
            used[i] = True
        else:
            hint.append(None)
    
    for i in range(len(guess_letters)):
        if hint[i] is None:
            found = False
            for j in range(len(secret_letters)):
                if not used[j] and guess_letters[i] == secret_letters[j]:
                    hint[i] = f"🟡{guess_letters[i]}"
                    used[j] = True
                    found = True
                    break
            if not found:
                hint[i] = f"⚫{guess_letters[i]}"
    
    return " ".join(hint)

def play_word(chat_id, word, user_data):
    secret = user_data['word']
    user_data['attempts'] -= 1
    rem = user_data['attempts']
    
    guess_word = word.upper()
    
    if len(guess_word) != 5:
        user_data['attempts'] += 1
        bot.send_message(chat_id, "🚫 Слово должно быть из 5 букв! Попытка не засчитана.")
        return
    
    if guess_word == secret:
        bot.send_message(chat_id, f"🎉 Поздравляю! Ты угадал слово: {secret}", reply_markup=main_menu())
        del users[chat_id]
        return
    
    hint = get_hint(secret, guess_word)
    legend = "\n🟢 — буква на своём месте\n🟡 — буква есть, но на другом месте\n⚫ — такой буквы нет"
    
    if rem == 0:
        bot.send_message(chat_id, f"😞 Попытки закончились! Слово: {secret}", reply_markup=main_menu())
        del users[chat_id]
        return
    
    bot.send_message(chat_id, f"{hint}\n{legend}\nОсталось попыток: {rem}")

# ============ ОБРАБОТЧИКИ ============
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(message.chat.id, "👋 Привет! Выбери игру:", reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if text == "🔙 В меню":
        if chat_id in users:
            del users[chat_id]
        bot.send_message(chat_id, "Выбери игру:", reply_markup=main_menu())
        return

    if text == "🎯 Угадай число":
        start_guess(chat_id)
        return
    if text == "✊✋✌️ Камень-ножницы-бумага":
        start_rps(chat_id)
        return
    if text == "📝 Угадай слово":
        start_word(chat_id)
        return

    if chat_id not in users:
        bot.send_message(chat_id, "Выбери игру из меню:", reply_markup=main_menu())
        return

    user_data = users[chat_id]
    game = user_data.get('game')

    if game == 'guess':
        if text.isdigit():
            play_guess(chat_id, int(text), user_data)
        else:
            bot.send_message(chat_id, "Введи число от 1 до 100:")

    elif game == 'rps':
        clean = text.lower().replace("✊", "").replace("✌️", "").replace("✋", "").strip()
        if clean in ['камень', 'ножницы', 'бумага']:
            play_rps(chat_id, clean)
        else:
            bot.send_message(chat_id, "Используй кнопки или напиши: камень, ножницы, бумага")

    elif game == 'word':
        play_word(chat_id, text.upper(), user_data)

print("Бот запущен!")
bot.infinity_polling()

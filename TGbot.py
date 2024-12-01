import telebot
from telebot import types

# Ваш токен Telegram API
TOKEN = "8100213011:AAFSoqbfRn8OatYW6CFo8B1r3EpQr1QilY0"

bot = telebot.TeleBot(TOKEN)

# Хранилище для продуктов и состояния пользователей
user_products = {}
user_states = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_products[user_id] = []  # Инициализация пустого списка продуктов для пользователя
    
    # Создание клавиатуры с кнопками для команд
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Добавить продукт"),
        types.KeyboardButton("Список продуктов"),
        types.KeyboardButton("Получить рецепт"),
        types.KeyboardButton("Удалить все продукты")
    )

    bot.send_message(user_id, 
        "Привет! Я кулинарный бот, который поможет тебе управлять списком продуктов и находить рецепты.\n"
        "Выбери нужную команду с помощью кнопок ниже.", 
        reply_markup=markup
    )

# Обработчик для кнопок
@bot.message_handler(func=lambda message: message.text in ["Добавить продукт", "Список продуктов", "Получить рецепт", "Удалить все продукты"])
def handle_buttons(message):
    user_id = message.chat.id
    text = message.text.lower()

    if text == "добавить продукт":
        user_states[user_id] = 'adding_product'
        bot.send_message(user_id, "Напишите название продукта, чтобы добавить его в список.")
    elif text == "список продуктов":
        list_products(message)
    elif text == "получить рецепт":
        get_recipes(message)
    elif text == "удалить все продукты":
        remove_all_products(message)

# Обработчик для добавления продукта после нажатия кнопки "Добавить продукт"
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'adding_product')
def add_product(message):
    user_id = message.chat.id
    product_name = message.text.lower()

    if user_id not in user_products:
        user_products[user_id] = []
    user_products[user_id].append(product_name)
    user_states[user_id] = None  # Сбрасываем состояние после добавления
    bot.send_message(user_id, f"Продукт '{product_name}' добавлен.")

# Команда для показа списка продуктов
def list_products(message):
    user_id = message.chat.id
    products = user_products.get(user_id, [])
    
    if products:
        bot.send_message(user_id, "Ваши продукты:\n" + "\n".join(products))
    else:
        bot.send_message(user_id, "Ваш список продуктов пуст.")

# Команда для удаления всех продуктов
def remove_all_products(message):
    user_id = message.chat.id
    if user_id in user_products:
        user_products[user_id].clear()  # Очищаем весь список продуктов
        bot.send_message(user_id, "Все продукты удалены.")
    else:
        bot.send_message(user_id, "Ваш список продуктов уже пуст.")

# База данных с рецептами
recipes = {
    frozenset(["яйца", "молоко", "масло"]): (
        "Рецепт яичного омлета:\n\n"
        "- Яйца — 3 шт.\n"
        "- Молоко — 2 столовые ложки\n"
        "- Соль и перец по вкусу\n"
        "- Масло для жарки\n\n"
        "1. Взбейте яйца с молоком, добавьте соль и перец.\n"
        "2. Разогрейте сковороду с маслом и вылейте смесь.\n"
        "3. Готовьте, пока омлет не станет золотистым. Приятного аппетита!"
    ),
    frozenset(["помидоры", "огурцы", "перец", "маслины", "фета", "оливковое масло", "лук"]): (
    "Рецепт Греческого салата:\n\n"
    "- Помидоры — 2 шт.\n"
    "- Огурцы — 1 шт.\n"
    "- Сладкий перец — 1 шт.\n"
    "- Маслины — 10–15 шт.\n"
    "- Сыр фета — 150 г\n"
    "- Лук красный — 1/2 шт.\n"
    "- Оливковое масло — 3 ст.л.\n"
    "- Соль, орегано — по вкусу\n\n"
    "1. Нарежьте помидоры крупными дольками, огурцы — полукольцами, сладкий перец — полосками.\n"
    "2. Лук нарежьте тонкими кольцами.\n"
    "3. Выложите овощи в миску, добавьте маслины и нарезанный кубиками сыр фета.\n"
    "4. Заправьте салат оливковым маслом, добавьте соль и орегано по вкусу.\n"
    "5. Аккуратно перемешайте и подавайте. Приятного аппетита!"
    ),
    frozenset(["яйца", "молоко", "масло", "сыр"]): (
        "Рецепт Чезабреты:\n\n"
        "- Мука — 300 г\n"
        "- Тертый сыр (чеддер или гауда) — 150 г\n"
        "- Яйцо — 1 шт.\n"
        "- Сметана — 100 мл\n"
        "- Разрыхлитель — 1 ч.л.\n"
        "- Соль — по вкусу\n"
        "- Масло для жарки\n\n"
        "1. В миске смешайте муку, соль, разрыхлитель и тертый сыр.\n"
        "2. Добавьте яйцо и сметану, замесите мягкое тесто.\n"
        "3. Разделите тесто на кусочки, раскатайте в лепешки.\n"
        "4. Разогрейте сковороду с маслом, обжаривайте лепешки до золотистой корочки с двух сторон.\n"
        "5. Подавайте горячими с любимым соусом. Приятного аппетита!"
    ),
    frozenset(["перец", "какашки"]): "Муха сосал хуи.",
}

# Команда для поиска рецептов на основе продуктов (частичное совпадение)
def get_recipes(message):
    user_id = message.chat.id
    products = set(user_products.get(user_id, []))  # Продукты пользователя как множество

    # Порог минимального совпадения
    min_matches = 2

    # Список найденных рецептов
    found_recipes = []

    for ingredients, recipe in recipes.items():
        # Подсчет совпадающих ингредиентов
        matches = len(ingredients & products)  # Пересечение множеств
        if matches >= min_matches:
            found_recipes.append((matches, recipe))

    # Если найдены рецепты, отправляем их пользователю, отсортированные по количеству совпадений
    if found_recipes:
        found_recipes.sort(reverse=True, key=lambda x: x[0])  # Сортировка по количеству совпадений
        for _, recipe in found_recipes:
            bot.send_message(user_id, recipe)
    else:
        bot.send_message(user_id, "На основе ваших продуктов пока нет подходящих рецептов. Ждите апдейта.")

    


# Запуск бота
bot.polling()

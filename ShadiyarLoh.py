import telebot
from telebot import types
from Gemini import get_response_from_gemini
from user import mycursor, db

# Your bot token (keep this secure!)
TOKEN = '7447014134:AAEIDJfDEqI8iA_POXnRhPPc4_LZXbG9Tf0'
bot = telebot.TeleBot(TOKEN)
topics = ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]

user_data = {}

class User:
    def __init__(self):
        self.name = None
        self.phone = None
        self.countries = None
        self.school = None
        self.grade = None


input = "Hi"
# Assume user_input is obtained from somewhere, e.g., user input in your Telegram bot


# Get the response from Gemini API

# Now user_output contains the response from Gemini API
# You can use it as needed, e.g., send back to the user via the Telegram bot


def generate_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton('Menu')
    markup.add(menu_button)
    return markup

@bot.message_handler(func=lambda message: message.text == 'Menu')
def handle_menu(message):
    markup = generate_submenu()  # Assuming you have a 'generate_submenu' function.
    bot.send_message(message.chat.id, 'Choose an option:', reply_markup=markup)


user_text = ""
# Start command
def generate_submenu():
    global user_text
    user_text = ""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Question')
    btn2 = types.KeyboardButton('Consultation')
    btn3 = types.KeyboardButton('Support')
    btn4 = types.KeyboardButton('Traction')
    btn5 = types.KeyboardButton('Menu')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

# Send main menu message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = User()
    msg = bot.reply_to(message, "This is Voke's Chat Bot. What's your name?")
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    chat_id = message.chat.id
    name = message.text
    user = user_data[chat_id]
    user.name = name
    msg = bot.reply_to(message, "What's your phone number?")
    bot.register_next_step_handler(msg, process_phone_step)

def process_phone_step(message):
    chat_id = message.chat.id
    phone = message.text
    user = user_data[chat_id]
    user.phone = phone
    msg = bot.reply_to(message, "Which countries are you interested in applying to?")
    bot.register_next_step_handler(msg, process_countries_step)

def process_countries_step(message):
    chat_id = message.chat.id
    countries = message.text
    user = user_data[chat_id]
    user.countries = countries
    msg = bot.reply_to(message, "What is the name of your school?")
    bot.register_next_step_handler(msg, process_school_step)

def process_school_step(message):
    chat_id = message.chat.id
    school = message.text
    user = user_data[chat_id]
    user.school = school
    msg = bot.reply_to(message, "Which grade are you in?")
    bot.register_next_step_handler(msg, process_grade_step)

def process_grade_step(message):
    chat_id = message.chat.id
    grade = message.text
    user = user_data[chat_id]
    user.grade = grade
    
    # Store in the database
    store_user_data(chat_id, user.name, user.phone, user.countries, user.school, user.grade)
    
    bot.send_message(chat_id, "Thank you, we have received your information. Now choose option from the menu", reply_markup=generate_submenu())

# Mock database storage function
def store_user_data(chat_id, name, phone, countries, school, grade):
    # Here you would connect to your database and store the details
    mycursor.execute("INSERT INTO Users_final (name, countries, school, phone, grade) VALUES (%s,%s,%s,%s,%s)",(name, phone, countries, school, grade))
    db.commit()





@bot.message_handler(func=lambda message: True)
def menu_handler(message):
    if message.text == 'Question':
        # Send the question as before, or just send a manual message
        # by using `bot.send_message` instead of `bot.reply_to`
        handle_question(message)
    elif message.text == 'Consultation':
        handle_consultation(message)
    elif message.text == 'Support':
        handle_support(message)
    elif message.text == 'Traction':
        handle_traction(message)
    elif message.text == "Menu":
        # Return to the main menu
        send_welcome(message)

# Handle 'Question' button
@bot.message_handler(func=lambda message: message.text == "Question")
def handle_question(message):
    msg = bot.reply_to(message, "Please write your question.")
    bot.register_next_step_handler(msg, process_question_step)
   
def process_question_step(message):
    user_input = message.text
    user_output = get_response_from_gemini(user_input)
    # Here you can handle the message containing the question
    # For example, save it or send it to an admin
    bot.reply_to(message, user_output)
    bot.send_message(message.chat.id, "if you want to ask another question. Press question button in the menu", reply_markup=generate_submenu())


def more_question(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Yes')
    btn2 = types.KeyboardButton('No')
    markup.add(btn1)
    markup.add(btn2)
    if message.text=="Yes":
        handle_question()
    if message.text=="No":
        bot.send_message(message.chat.id, "Do you want to return to main menu?", reply_markup=generate_main_menu())


# Handle 'Consultation' button
@bot.message_handler(func=lambda message: message.text == "Consultation")
def handle_consultation(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # Here you would dynamically generate the consultation topics
    for i in range(5):
        btn = types.KeyboardButton(f'{topics[i]}')
        markup.add(btn)
    msg = bot.reply_to(message, "Choose a topic for consultation:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_consultation_step)

@bot.message_handler(func=lambda message: message.text == "Consultation")
def handle_consultation(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # Here you would dynamically generate the consultation topics
    msg = bot.reply_to(message, "Now we need your contact details. Please write your full name in Russian or English:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_consultation_step)

def process_consultation_step(message):
    # Here you would handle the chosen consultation topic
    bot.reply_to(message, f"You've selected {message.text}, we will respond to you shortly.")
    bot.send_message(message.chat.id, "Do you want to return to the menu?", reply_markup=generate_main_menu())

# Handle 'Support' button
@bot.message_handler(func=lambda message: message.text == "Support")
def handle_support(message):
    msg = bot.reply_to(message, "What is your concern?")
    bot.register_next_step_handler(msg, process_support_step)

def process_support_step(message):
    # Here you would handle the message containing the support request
    bot.reply_to(message, "Thank you for contacting support, we will get back to you soon!")
    bot.send_message(message.chat.id, "Do you want to return to the menu?", reply_markup=generate_main_menu())
    

# Handle 'Traction' button
@bot.message_handler(func=lambda message: message.text == "Traction")
def handle_traction(message):
    msg = bot.reply_to(message, "Please share your name or nickname and the goals or exams you want to prepare for.")
    #цель, класс, школа. 
    #
    bot.register_next_step_handler(msg, process_traction_step)

def process_traction_step(message):
    # Here you would handle the message containing the traction request
    # Presumably, you'll set up some kind of reminder system
    bot.reply_to(message, "Thanks! We've recorded your details and will send you daily reminders.")
    bot.send_message(message.chat.id, "Do you want to return to the menu?", reply_markup=generate_main_menu())


# Polling
bot.polling(none_stop=True)    



import telebot
from telebot import types
from Gemini import get_response_from_gemini
from user import mycursor, db
import schedule
import time
import threading
from datetime import datetime, timedelta, time
import mysql.connector
import random

# Your bot token (keep this secure!)
TOKEN = '7447014134:AAEIDJfDEqI8iA_POXnRhPPc4_LZXbG9Tf0'
bot = telebot.TeleBot(TOKEN)
topics = ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
reminder_time = time(18, 53, 00).strftime("%H:%M")
user_data = {}

class User:
    def __init__(self):
        self.chat_id= None
        self.name = None
        self.phone = None
        self.countries = None
        self.school = None
        self.grade = None
        self.consultation = None
        self.consultation_details = None
        self.traction_started = False
        self.streak = 0
        self.goals = None

def generate_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton('Menu')
    markup.add(menu_button)
    return markup

@bot.message_handler(func=lambda message: message.text == 'Menu')
def handle_menu(message):
    try:
        markup = generate_submenu()  # Assuming you have a 'generate_submenu' function.
        bot.send_message(message.chat.id, 'Choose an option:', reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

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
    try:
        chat_id = message.chat.id
        user_data[chat_id] = User()
        user = user_data[chat_id]
        msg = bot.reply_to(message, "This is Voke's Chat Bot. What's your name?")
        bot.register_next_step_handler(msg, process_name_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = user_data[chat_id]
        user.chat_id = chat_id
        user.name = name
        msg = bot.reply_to(message, "What's your phone number?")
        bot.register_next_step_handler(msg, process_phone_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def process_phone_step(message):
    try:
        chat_id = message.chat.id
        phone = message.text
        user = user_data[chat_id]
        user.phone = phone
        msg = bot.reply_to(message, "Which countries are you interested in applying to?")
        bot.register_next_step_handler(msg, process_countries_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def process_countries_step(message):
    try:
        chat_id = message.chat.id
        countries = message.text
        user = user_data[chat_id]
        user.countries = countries
        msg = bot.reply_to(message, "What is the name of your school?")
        bot.register_next_step_handler(msg, process_school_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def process_school_step(message):
    try:
        chat_id = message.chat.id
        school = message.text
        user = user_data[chat_id]
        user.school = school
        msg = bot.reply_to(message, "Which grade are you in?")
        bot.register_next_step_handler(msg, process_grade_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def process_grade_step(message):
    try:
        chat_id = message.chat.id
        grade = message.text
        user = user_data[chat_id]
        user.grade = grade
        
        # Store in the database
        store_user_data(user.chat_id, user.name, user.phone, user.countries, user.school, user.grade)
        
        bot.send_message(chat_id, "Thank you, we have received your information. Now choose option from the menu", reply_markup=generate_submenu())
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def store_user_data(chat_id, name, phone, countries, school, grade):
    try:
        # Here you would connect to your database and store the details
        mycursor.execute("INSERT INTO Users_final (chat_id, name, countries, school, phone, grade, traction_started, streak) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(chat_id, name, countries, school, phone, grade, False, 0))
        db.commit()
    except Exception as e:
        print(f"An error occurred while storing user data: {str(e)}")

@bot.message_handler(func=lambda message: True)
def menu_handler(message):
    try:
        if message.text == 'Question':
            handle_question(message)
        elif message.text == 'Consultation':
            handle_consultation(message)
        elif message.text == 'Support':
            handle_support(message)
        elif message.text == 'Traction':
            handle_traction(message)
        elif message.text == "Menu":
            send_welcome(message)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(func=lambda message: message.text == "Question")
def handle_question(message):
    try:
        msg = bot.reply_to(message, "Please write your question.")
        bot.register_next_step_handler(msg, process_question_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
   
def process_question_step(message):
    try:
        user_input = message.text
        user_output = get_response_from_gemini(user_input)
        bot.reply_to(message, user_output)
        bot.send_message(message.chat.id, "If you want to ask another question, press the question button in the menu", reply_markup=generate_submenu())
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")


def more_question(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton('Yes')
        btn2 = types.KeyboardButton('No')
        markup.add(btn1)
        markup.add(btn2)
        if message.text=="Yes":
            handle_question()
        if message.text=="No":
            bot.send_message(message.chat.id, "Do you want to return to main menu?", reply_markup=generate_main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
@bot.message_handler(func=lambda message: message.text == "Consultation")
def handle_consultation(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        mycursor.execute("SELECT topic from topics")
        topics_db = mycursor.fetchall()
        # Here you would dynamically generate the consultation topics using the fetched topics
        for topic in topics_db:
            btn = types.KeyboardButton(topic[0])
            markup.add(btn)
        msg = bot.reply_to(message, "Choose a topic for consultation:", reply_markup=markup)
        bot.register_next_step_handler(msg, process_consultation_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def process_consultation_step(message):
    try:
        chat_id = message.chat.id
        user = user_data[chat_id]
        user.consultation_details = message.text
        bot.reply_to(message, f"You've selected {message.text}, we will respond to you shortly.")
        bot.send_message(message.chat.id, "Do you want to return to the menu?", reply_markup=generate_main_menu())
        
        mycursor.execute("""
            UPDATE Users_final 
            SET consultation = %s, consultation_details = %s 
            WHERE chat_id = %s
        """, (1, user.consultation_details, chat_id))
        
        db.commit()
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(func=lambda message: message.text == "Support")
def handle_support(message):
    try:
        msg = bot.reply_to(message, "Please write all your concerns to @vokecom telegram and we will answer you")
        bot.send_message(message.chat.id, "Do you want to return to the menu?", reply_markup=generate_main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}") 

@bot.message_handler(func=lambda message: message.text == "Traction")
def handle_traction(message):
    try:
        msg = bot.reply_to(message, "Please share your long-term goals or exams you want to prepare for. Then you will divide it to small steps for every day")
        chat_id = message.chat.id
        user = user_data[chat_id]
        user.traction_started = True

        mycursor.execute("""
            UPDATE Users_final 
            SET traction_started = %s
            WHERE chat_id = %s
        """, (user.traction_started, chat_id))
        
        db.commit()
        bot.register_next_step_handler(msg, process_traction_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def process_traction_step(message):
    try:
        chat_id = message.chat.id
        user = user_data[chat_id]
        user.goals = message.text

        mycursor.execute("""
            UPDATE Users_final 
            SET goals = %s
            WHERE chat_id = %s
        """, (user.goals, chat_id))
        
        db.commit()
        bot.reply_to(message, f"Thanks! We've recorded your details about {user.goals} and will send you daily reminders.")
        bot.send_message(message.chat.id, "Do you want to return to the menu?", reply_markup=generate_main_menu())
        schedule_first_reminder(message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")


def check():
    print("I am working...")

def schedule_first_reminder(chat_id):
    try:
        reminder_time = time(18, 10, 00).strftime("%H:%M")
        schedule.every().day.at(reminder_time).do(check)
        schedule.every().day.at(reminder_time).do(send_reminder, chat_id)
    except Exception as e:
        print(f"An error occurred while scheduling reminder: {str(e)}")

def send_reminder(chat_id):
    try:
        bot.send_message(chat_id, "Have you done something today to achieve your goal? Reply with Yes or No.")
    except Exception as e:
        print(f"An error occurred while sending reminder: {str(e)}")

@bot.message_handler(func=lambda message: message.text.lower() in ['yes', 'no'])
def handle_activity_response(message):
    try:
        chat_id = message.chat.id
        user = user_data[chat_id]
        
        if message.text.lower() == 'yes':
            msg = bot.reply_to(message, "Please describe what you did today.")
            bot.register_next_step_handler(msg, save_activity_description)
            user.streak +=1
        else:       
            schedule_single_reminder(3, message.chat.id)
            user.streak = 0

        mycursor.execute("""
            UPDATE Users_final 
            SET streak = %s
            WHERE chat_id = %s
        """, (user.streak, chat_id))

        db.commit()
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def save_activity_description(message):
    try:
        activity_id = random.randint(10000, 99999)  # Generate a random activity ID
        chat_id = message.chat.id
        add_activity = ("INSERT INTO useractivity "
                    "(activity_id, chat_id, activity_date, activity_done, activity_description) "
                    "VALUES (%s, %s, %s, %s, %s)")
        data_activity = (activity_id, chat_id, datetime.now(), True, message.text)
        mycursor.execute(add_activity, data_activity)
        
        db.commit()
        schedule_first_reminder(message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def schedule_single_reminder(hours, chat_id):
    try:
        reminder_time = datetime.now() + timedelta(hours=3)
        schedule.every().at(reminder_time.strftime("%H:%M")).do(send_reminder, chat_id).tag(f"reminder_{chat_id}")
        schedule.clear(f"reminder_{chat_id}")
    except Exception as e:
        print(f"An error occurred while scheduling single reminder: {str(e)}")

# Run the scheduler in a separate thread
def run_scheduler():
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f"An error occurred in the scheduler: {str(e)}")

schedule_thread = threading.Thread(target=run_scheduler)
schedule_thread.start()
bot.polling(none_stop=True)
   



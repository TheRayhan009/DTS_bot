import telebot
import random
TOKEN = 'YOUR_TOKEN'
bot = telebot.TeleBot(TOKEN)

def generate_special_code():
    return str(random.randint(100000, 999999))

def store_data(username, password):
    special_code = generate_special_code()
    with open('stored_data.txt', 'a') as file:
        file.write(f"username: {username}\npassword: {password}\nspecial_code: {special_code}\n")
    return special_code

def retrieve_data(special_code):
    with open('stored_data.txt', 'r') as file:
        global  dna
        data_lines = file.readlines()
        dna=0
        for i in range(0, len(data_lines), 3):
            if data_lines[i + 2].strip() == f"special_code: {special_code}":
                dna=1
                return f"Username: {data_lines[i].split(': ')[1].strip()}\nPassword: {data_lines[i + 1].split(': ')[1].strip()}"
        if dna == 0:
            return f"ops! We have no data."

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    user = message.from_user.last_name
    link = message.from_user.username
    with open("user.txt", "r") as file:
        global found
        found = False
        data_lines2 = file.readlines()
        for line in data_lines2:
            if line.strip() == link:
                found = True
                break
        if found == False:
            with open("user.txt", "a") as file:
                file.write(f"{link}\n")
    bot.send_message(message.chat.id, f"Hello {user}. I am DTS. I am a data storage bot. \n\n"
                                      "To store data: up\n"
                                      "To retrieve data: sd\n"
                                      "To delete data: /delete\n"
                                      f"\n \n TheRayhan PY made me. ")
    print(link)

@bot.message_handler(commands=['delete'])
def delete_information(message):
    bot.send_message(message.chat.id, "Enter special code to confirm deletion:")
    bot.register_next_step_handler(message, delete_checker)

def delete_checker(message):
    chat_id = message.chat.id
    special_code = message.text
    result = retrieve_data(special_code)
    if result:
        bot.send_message(chat_id, f"Are you sure you want to delete the following data?\n\n{result}\n\n"
                                  f"Type 'confirm' to proceed.")
        bot.register_next_step_handler(message, lambda s: delete_confirmation(s, special_code))
    else:
        bot.send_message(chat_id, "Invalid special code. Deletion aborted.")

def delete_confirmation(message, special_code):
    chat_id = message.chat.id
    confirmation = message.text.lower()

    if confirmation == 'confirm':
        with open("stored_data.txt", "r") as file:
            data_lines = file.readlines()
        with open("stored_data.txt", "w") as file:
            for i in range(0, len(data_lines), 3):
                if data_lines[i + 2].strip() != f"special_code: {special_code}":
                    file.write(data_lines[i])
                    file.write(data_lines[i + 1])
                    file.write(data_lines[i + 2])

        bot.send_message(chat_id, "Data deleted successfully.")
    else:
        bot.send_message(chat_id, "Deletion aborted.")

@bot.message_handler()
def handle_messages(message):
    chat_id = message.chat.id
    user_input = message.text.lower()

    if user_input == "/start":
        handle_start_help(message)

    elif user_input == "/help":
        handle_start_help(message)

    elif user_input == "up":
        bot.send_message(chat_id, "Enter username:")
        bot.register_next_step_handler(message, process_username_step)

    elif user_input == "sd":
        bot.send_message(chat_id, "Enter special code:")
        bot.register_next_step_handler(message, process_special_code_step)

    else:
        bot.send_message(chat_id, "Invalid input. Please try again.")

def process_username_step(message):
    chat_id = message.chat.id
    username = message.text
    bot.send_message(chat_id, "Enter password:")
    bot.register_next_step_handler(message, lambda s: process_password_step(s, username))

def process_password_step(message, username):
    chat_id = message.chat.id
    password = message.text
    special_code = store_data(username, password)
    bot.send_message(chat_id, "Data stored successfully. Special Code: " + "" + special_code + """
                                                                          -------------""")

def process_special_code_step(message):
    chat_id = message.chat.id
    special_code = message.text
    result = retrieve_data(special_code)
    bot.send_message(chat_id, result)

bot.polling()

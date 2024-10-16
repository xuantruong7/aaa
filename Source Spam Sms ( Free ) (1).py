import telebot
import bs4,  base64
import os
import subprocess
import psutil
import sqlite3
import hashlib
import threading
import time
import requests
import datetime
api_bot = "6578917837:AAE_aFNfulvYw3clA94XZigAG0jdBQJZ48Y" #Nhập api Bot Của Telegram
processes = []
bot = telebot.TeleBot(api_bot)
allowed_users = []
ADMIN_ID = 5884057707 # id Admin để sử dụng quyền hành
Group_Id_Chat = -1002170354953  # Lấy Id Group Mà Bạn Muốn Bot Hoạt Động Trên Đó


connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Tạo bảng người dùng nếu chưa tồn tại
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()

def TimeStamp():
    now = str(datetime.date.today())
    return now

def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.datetime.now():
            allowed_users.append(user_id)

def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()
@bot.message_handler(commands=['add'])
def add_user(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    message_parts = message.text.split()
    if len(message_parts) == 1:
        bot.reply_to(message, 'Vui lòng nhập ID người dùng.')
        return
    if len(message_parts) < 3:
        bot.reply_to(message, 'Vui lòng nhập đủ thông tin.')
        return

    user_id = message_parts[1]
    ngay = int(message_parts[2])

    allowed_users.append(user_id)
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=int(ngay))
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    bot.reply_to(message, 'Add Success Vip\nId_User : {user_id}\nDay : {ngay}\n')

load_users_from_database()
@bot.message_handler(commands=['vipspam'])
def lqm_sms(message):
    user_id = message.from_user.id
    if user_id not in allowed_users:
        bot.reply_to(message, text='Bạn không có quyền sử dụng lệnh này!')
        return
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Enter Phone Number')
        return

    phone_number = message.text.split()[1]
    if not phone_number.isnumeric():
        bot.reply_to(message, 'Phone Number Not Working')
        return

    if phone_number in ['113','911','114','115','1800']:
        # Số điện thoại nằm trong danh sách cấm
        bot.reply_to(message,"LOL ! NO SPAM")
        return        
        bot.reply_to(message, f'''┏━━━━━━━━━━━━━━━━━━━━┓
┣➤ ⊂🚀⊃Attack Success⊂🚀⊃
┣➤Commands : VIP
┣➤Attack By : 
┣➤Bot : 
┣➤Attack Type : SMS
┣➤Phone Number : {phone_number} 📱
┣➤Attack Delay : 200 Delay
┣➤Admin : 
┗━━━━━━━━━━━━━━━━━━━━➤
''')

@bot.message_handler(commands=['spam'])
def sms(message):
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Please Enter Phone Number') 
        return
      
    phone_number = message.text.split()[1]       
    if not phone_number.isdigit() or len(phone_number) != 10:
        bot.reply_to(message, 'Please Enter 10 Digits Phone Number')         
        return

    file_path = os.path.join(os.getcwd(), "smsfree.py")
    process = subprocess.Popen(["python", file_path, phone_number, "50"])
    processes.append(process)

    bot.reply_to(message, f'''┏━━━━━━━━━━━━━━━━━━━━┓
┣➤Bot : @truongdeptrai7
┣➤Attack Type : SMS
┣➤Phone Number : {phone_number} 📱
┣➤Attack Deply : 50 Deply
┣➤Admin :  @truongdeptrai7
┗━━━━━━━━━━━━━━━━━━━━➤
''')



    
    





    
@bot.message_handler(func=lambda message: message.chat.id != Group_Id_Chat)
def handle_message(message):
    # Gửi thông báo nếu bot nhận được tin nhắn từ một nhóm khác
    bot.reply_to(message, "Bot Working in Group[https://t.me/concunha] AD @truongdeptrai7 ")









    
bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'User Does Not Have Authority To Use This Command.')
        return
    if user_id not in allowed_users:
        bot.reply_to(message, text='User Does Not Have Authority To Use This Command!')
        return
    process_count = len(processes)
    bot.reply_to(message, 'Number of running processes {process_count}.')

@bot.message_handler(commands=['restart'])
def restart(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'User Does Not Have Authority To Use This Command.')
        return

    bot.reply_to(message, 'Please Wait Bot Reset....')
    time.sleep(2)
    python = sys.executable
    os.execl(python, python, *sys.argv)

@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'User Does Not Have Authority To Use This Command.')
        return

    bot.reply_to(message, 'Please Wait Bot Stop....')
    time.sleep(2)
    bot.stop_polling()
@bot.message_handler(commands=['help','start'])
def help(message):
    help_text = '''
┏━━━━━━━━━━━━━━┓
┣➤ Commands Spam
┗━━━━━━━━━━━━━━➤
┏━━━━━━━━━━━━━━┓
┣➤ /spam : [ Commands Free] /spam + phone 
┣➤ /vipspam : [ Commands Vip ] /vipspam + phone.
┗━━━━━━━━━━━━━━➤
┏━━━━━━━━━━━━━━┓
┣➤ Command Admin
┗━━━━━━━━━━━━━━➤
┣➤/status : 
┣➤/restart : Reset Bot
┣➤/stop : Stop Run Bot
┗━━━━━━━━━━━━━━➤
'''
    bot.reply_to(message, help_text)
    
    
    
    
# Khởi tạo bot ứng dụng của bạn

# Lệnh "/start" để bắt đầu theo dõi thời gian


    

bot.polling()

    
    
    
    
    


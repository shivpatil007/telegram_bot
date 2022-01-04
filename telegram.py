import telebot
import os 
import pyqrcode
from pyqrcode import QRCode
import base64
import string
import random
  

 


'''===========================DB CONNECTION==============================='''
import psycopg2
conn = psycopg2.connect(
    host=os.getenv("host"),
    database=os.getenv("database"),
    user=os.getenv("user"),
    password=os.getenv("password")
)

cursor = conn.cursor()
'''=========================TELEGRAM==============================='''



API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot('5051244909:AAENSR45-6Vi25dOQrpRWeSfL5TvBub0SnE',parse_mode='None') 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, """
    /text followed by message upto 4000 words to be converted in QR code of type png
    /image followed by image to be converted in QR code of type png
    """)


@bot.message_handler(commands=['text'], content_types=['text'])
def send_welcome(message):
    msg=message.text
    if len(msg)<=4000:
        img = pyqrcode.create(msg[6:])
        img.png('myqr.png', scale = 6)
        bot.send_photo(message.chat.id, open('myqr.png', 'rb'))
        os.remove('myqr.png')
    else:
        print(len(msg))
        bot.reply_to(message, "Message too long")
    print(message.text)

@bot.message_handler(func=lambda message: True, commands=['image'])
def test(message):
   text_message = 'Upload a photo' 
   bot.send_message(message.chat.id,text_message) 
   bot.register_next_step_handler(message, test2) 

def randomizer():
    return ''.join(random.choices(string.ascii_uppercase+string.ascii_lowercase +string.digits, k = 12)) 



def test2(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    print(file_info)
    data =bot.download_file(file_info.file_path)
    
    name=file_info.file_path.split('/')[-1]
    unique_id=randomizer()
    
    try:
        cursor.execute("INSERT INTO photos (unique_id ,image,name) VALUES (%s,%s,%s)", (unique_id,data,name))
        conn.commit()
        link='https://qr-code-generator.herokuapp.com/?image='+unique_id
        img = pyqrcode.create(link)
        img.png('myqr.png', scale = 6)
        bot.send_photo(message.chat.id, open('myqr.png', 'rb'))
        os.remove('myqr.png')


    except Exception as e:
        bot.reply_to(message, "ERROR!!! not supported with this format")
        print(e)
    



bot.polling()
    




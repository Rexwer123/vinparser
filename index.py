import telebot
import re
from vininfo import Vin
from db import DB
from colors import colors


try:
    db = DB()
    print(colors.OKGREEN + 'Connected to the database' + colors.BOLD + ' CARS ' + colors.ENDC + colors.OKGREEN + 'at http://localhost:27017\n' + colors.ENDC)
except Exception as e:
    print(e)

bot = telebot.TeleBot('1818558003:AAG1o9g-tGdc-uPcUDl1RAqWh7Vnrce5k7M')

def checkVIN(vinNumber):
    try:
        return Vin(vinNumber).verify_checksum()
    except Exception:
        return False

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if(message.text == '/help' or message.text == '/start'):
        bot.send_message(message.from_user.id, "Введите VIN, чтобы получить информацию об автомобиле\n")   
    else:
        if checkVIN(message.text) == True:
            carInfo = db.getCarByVIN(message.text)
            if(carInfo == False):
                bot.send_message(message.from_user.id, "Нет информации о машине с этим VIN")
            else:
                bot.send_message(message.from_user.id, carInfo)
        else:
            bot.send_message(message.from_user.id, "Чексумма VIN не совпала, попробуйте другой")

bot.polling(none_stop=False, interval=0)
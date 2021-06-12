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
    exit()

bot = telebot.TeleBot('1807234639:AAE4pAHjWfnLhzb6vVIPgytyQVvk62haBy0')

def parseInfo(vin):
    result = "VIN: " + vin.num + "\n"
    vin = vin.annotate()
    for attr, value in vin.items():
        result += "-" + attr + ": " + value + "\n" 

    return result

def checkVIN(vinNumber):
    return Vin(vinNumber).verify_checksum()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if(message.text == '/help'):
        bot.send_message(message.from_user.id, "Введите VIN, чтобы получить информацию об автомобиле\nЛибо введите /add, чтобы добваить автомобиль по VIN")   
    if(message.text == '/get'):
        bot.send_message(message.from_user.id, "Вот, что я смог найти:\n\n" + db.getAllCars())
    else:
        try:
            if checkVIN(message.text) == True:
                vin = Vin(message.text)
                db.addNewCar(vin)
                vin.annotate()
                bot.send_message(message.from_user.id, "Вот, что я смог найти:\n\n{0}".format(parseInfo(vin)))
            else:
                bot.send_message(message.from_user.id, "Чексумма VIN не совпала, попробуйте другой")
        
        except Exception as e:
            bot.send_message(message.from_user.id, str(e))

bot.polling(none_stop=False, interval=0)
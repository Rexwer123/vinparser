#Импортируем библиотеки
import telebot
import re
from vininfo import Vin
from db import DB
from colors import colors

#Пытаемся создать соединение с базой, инициализируя объект класса DB
try:
    db = DB()
    print(colors.OKGREEN + 'Connected to the database' + colors.BOLD + ' CARS ' + colors.ENDC + colors.OKGREEN + 'at http://localhost:27017\n' + colors.ENDC)
except Exception as e:
    print(e)
    exit()

#Инициализируем инстант бота по API ключу от @botfather
bot = telebot.TeleBot('API KEY')

#Функция для парса объекта Vin для отправки пользователю
def parseInfo(vin):
    result = "VIN: " + vin.num + "\n"
    vin = vin.annotate()
    for attr, value in vin.items():
        result += "-" + attr + ": " + value + "\n" 

    return result

#Проверяем валидность VIN
def checkVIN(vinNumber):
    return Vin(vinNumber).verify_checksum()

#Создаём обработчик сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if(message.text == '/help'):
        bot.send_message(message.from_user.id, "Введите VIN, чтобы получить информацию об автомобиле\nЛибо введите /add, чтобы добваить автомобиль по VIN")   
    if(message.text == '/get'):
        #Отправка всех машин из базы
        bot.send_message(message.from_user.id, "Вот, что я смог найти:\n\n" + db.getAllCars())
    else:
        try:
            #Проверка чексуммы VIN
            if checkVIN(message.text) == True:
                #Инициализация объекта класса VIN
                vin = Vin(message.text)
                #Добавляем машину в базу
                db.addNewCar(vin)
                #Получаем детали о машине исходя из сегментов VIN
                vin.annotate()
                #Отправляем пользователю полученные детали
                bot.send_message(message.from_user.id, "Вот, что я смог найти:\n\n{0}".format(parseInfo(vin)))
            else:
                #Если чексумма не совпала - отправяем соответствующий ответ
                bot.send_message(message.from_user.id, "Чексумма VIN не совпала, попробуйте другой")
        
        except Exception as e:
            #Если с базой что-то пошло не так
            bot.send_message(message.from_user.id, str(e))

#Включаем режим работы бота без задержек
bot.polling(none_stop=False, interval=0)

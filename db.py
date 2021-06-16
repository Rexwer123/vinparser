#Импортируем библиотеки
import pymongo
from colors import colors
from vininfo import Vin

#Модель для работы с базой данных
class DB:
    def __init__(self):
        #Создаём соединение с монго при инициализации объекта класса
        self.conn = pymongo.MongoClient('localhost', 27017)
    
    def addNewCar(self, vin):
        #Парсим vin объект и сохраняем в базу данных
        try:
            car = {"vin": vin.num, "country": vin.country, "region": vin.region, "manufacturer": vin.manufacturer, "years": vin.years}
            if(self.conn.cars.cars.find_one(car) == None): #Проверка: существует ли машина с таким VIN в базе?
                self.conn.cars.cars.save(car)
        except Exception as e:
            #Обработка ошибок записи
            print(e)
            return False
            
        return True
    
    def getAllCars(self):
        #Функция для вывода всех сохранённых в базе машин
        result = ""
        for car in self.conn.cars.cars.find({}):
            result += "VIN: " + car["vin"] + "\n" + "-Country: " + car["country"] + "\n" + "-Region: " + car["region"] + "\n" + "-Years: " + str(car["years"][0])
        if len(result) == 0: #Если машин в базе нет, то вернуть ошибку
            return False
        return result

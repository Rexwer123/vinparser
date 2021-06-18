#Импортируем библиотеки
import pymongo
from colors import colors
from vininfo import Vin

# #ВОТ ОТСЮДА

testList = [
    {
        "VIN": "JN1CV6FE3BM983517",
        "crashes": [
            "Наезд на стоящие ТС – 2 августа 2016, Япония",
            "Столкновение – 10 ноября 2018, Япония"
        ] 
    },
    {
        "VIN": "1GCCS19W6Y8200480",
        "crashes": [
            "Опрокидывание транспортных средств – 8 сентября 2017, Соединенные Штаты Америки"
        ] 
    },
    {
        "VIN": "WBAPH7C51BE656105",
        "crashes": [
           "Наезд на препятствие – 14 марта 2017, Германия"
        ] 
    },
    {
        "VIN": "JKAZRBC11YA058549",
        "crashes": [
           "Наезд на пешехода – 13 августа 2003, Япония",
           "Столкновение – 4 апреля 2013, Япония"
        ] 
    },
    {
        "VIN": "5GAKVBKD2EJ144030",
        "crashes": [
           "Наезд на велосипедиста – 27 июня 2007, Соединенные Штаты Америки",
        ] 
    },
    {
        "VIN": "1FBSS31L89DA67372",
        "crashes": [
           "Наезд на стоящее транспортное средства – 8 октября 2018, Соединенные Штаты Америки",
        ] 
    },
    {
        "VIN": "WD2PD644945698571",
        "crashes": [
           "Наезд на гужевой транспорт – 13 ноября 2012, Германия", 
           "Наезд на стоящий ТС – 25 ноября 2012, Германия"
        ] 
    },
    {
        "VIN": "WBADN6349YGM50573",
        "crashes": [
           "Наезд на животных и прочие – 3 июля 2013, Германия", 
           "Наезд на препятствие – 5сентября 2015, Германия"
        ] 
    },
    {
        "VIN": "2T2HA31U46C075426",
        "crashes": [
           "Удар оторвавшимся колесом – 6 июня 2006, Канада",
           "(Столкновение – 6 июня 2006, Канада"
        ] 
    },
    {
        "VIN": "1G1ZC5E06CF303007",
        "crashes": [
           "Наезд на стоящее транспортное средство – 14 мая 2008, Соединенные Штаты Америки"
        ] 
    },
    {
        "VIN": "1G2JB12F837380467",
        "crashes": [
           "Столкновение – 23 декабря 2017, Соединенные Штаты Америки"
        ] 
    },
    {
        "VIN": "2C4RDGCG5FR570605",
        "crashes": [
           "Столкновение – 13 января 2016, Канада"
        ] 
    },
    {
        "VIN": "2B3CA8CT6AH256754",
        "crashes": [
           "Столкновение – 13 января 2016, Канада"
        ] 
    },
    {
        "VIN": "1GC4K0E89FF131170",
        "crashes": [
           "Опрокидывание транспортных средств – 14 мая 2019, Соединенные Штаты Америки"
        ] 
    },
    {
        "VIN": "3FADP4BJ0EM266283",
        "crashes": [
           "Наезд на пешехода – 3 июля 2011, Мексика"
        ] 
    }
]

# #ДО СЮДА ПОТОМ УДАЛИТЬ

class DB:
    def __init__(self):
        #Создаём соединение с монго при инициализации объекта класса
        self.conn = pymongo.MongoClient('localhost', 27017)
        #УДАЛИТЬ ОТСЮДА
        try:
            self.conn.cars.cars.insert_many(testList)
        except Exception as e:
            #Обработка ошибок записи
            print(e)
        #КОНЕЦ

    def assembleResult(self, responseString, crashes):
        for crash in crashes:
            responseString += "- " + crash + "\n"
        return responseString

    def getCarByVIN(self, vinNumber):
        responseHeader = "VIN: " + vinNumber + "\n" + "Аварии:\n"
        queryResult = self.conn.cars.cars.find_one({"VIN": vinNumber})
        if(queryResult):
            if(len(queryResult["crashes"]) == 0):
                return False
            else:
                return self.assembleResult(responseHeader, queryResult["crashes"])
        else:
            return False
            
                

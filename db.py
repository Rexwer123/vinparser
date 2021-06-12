import pymongo
from colors import colors
from vininfo import Vin

class DB:
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
    
    def addNewCar(self, vin):
        try:
            car = {"vin": vin.num, "country": vin.country, "region": vin.region, "manufacturer": vin.manufacturer, "years": vin.years}
            if(self.conn.cars.cars.find_one(car) == None):
                self.conn.cars.cars.save(car)
        except Exception as e:
            print(e)
            return False
            
        return True
    
    def getAllCars(self):
        result = ""
        for car in self.conn.cars.cars.find({}):
            result += "VIN: " + car["vin"] + "\n" + "-Country: " + car["country"] + "\n" + "-Region: " + car["region"] + "\n" + "-Years: " + str(car["years"][0])
        if len(result) == 0:
            return False
        return result

from abc import ABC, abstractmethod


class Transport(ABC):
    def __init__(self, brand, speed, year, price):
        self.brand = brand
        self.__speed = speed
        self.year = year
        self.price = price

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        if value >= 0:
            self.__speed = value

    @staticmethod
    def is_fast(value):
        return value > 200

    def __str__(self):
        return (f"{self.brand}")

    def __eq__(self, other):
        return self.speed == other.speed and self.price == other.price

    def __len__(self):
        return len(self.brand)

    def __lt__(self, other):
        return self.price < other.price


class Engine:
    def __init__(self, engine_type, horsepower):
        self.engine_type = engine_type
        self.horsepower = horsepower

    @classmethod
    def from_string(cls, data):
        engine_type, horsepower = data.split(",")
        return cls(engine_type, float(horsepower))

    def start_engine(self):
        print(f"Engine {self} is running")

    def __add__(self, other):
        return self.horsepower + other.horsepower

    def __sub__(self, other):
        return self.horsepower - other.horsepower


class Car(Transport, Engine):
    def __init__(self, brand, speed, year, price, engine_type, horsepower):
        Transport.__init__(self, brand, speed, year, price)
        Engine.__init__(self, engine_type, horsepower)

    def move(self):
        print(f"{self}  has gone")

    def stop(self):
        print(f"{self}  has stopped")


class Bike(Transport):
    def __init__(self, brand, speed, year, price, horsepower, wheels):
        Transport.__init__(self, brand, speed, year, price)
        self.horsepower = horsepower
        self.wheels = wheels

    def move(self):
        print(f"{self} bike has gone")

    def stop(self):
        print(f"{self} bike has stopped")


class Plane(Transport, Engine):
    def __init__(self, brand, speed, year, price, engine_type, horsepower, size):
        Transport.__init__(self, brand, speed, year, price)
        Engine.__init__(self, engine_type, horsepower)
        self.size = size

    def move(self):
        print(f"{self} took off")

    def stop(self):
        print(f"{self} has landed")


class Ship(Transport, Engine):
    def __init__(self, brand, speed, year, price, engine_type, horsepower, able_distance):
        Transport.__init__(self, brand, speed, year, price)
        Engine.__init__(self, engine_type, horsepower)
        self.able_distance = able_distance

    def move(self):
        print(f"{self} ship sailed away")

    def stop(self):
        print(f"{self} has swum up")

def main():
    car1 = Car("Toyota", 250, 2020, 30000, "бензин", 120)
    car2 = Car("BMW", 250, 2022, 30000, "бензин", 200)
    print(car1)
    print(car1 == car2)
    print(car1 < car2)
    print(car1 + car2)
    print(car1 - car2)
    
if __name__ == '__main__':
    main()

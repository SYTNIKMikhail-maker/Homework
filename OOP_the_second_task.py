from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, id, name, phone, email, salary, hire_date):
        self._id = id
        self.name = name
        self.__phone = phone
        self.__email = email
        self.__salary = salary
        self.hire_date = hire_date

    @abstractmethod
    def work(self):
        pass

    def login(self):
        print(f"{self.name} logged in")

    def logout(self):
        print(f"{self.name} logged out")

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        if value > 0:
            self.__salary = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self._id == other._id


class Waiter(Person):
    def __init__(self, id, name, phone, email, salary, hire_date, table_number, experience_years):
        super().__init__(id, name, phone, email, salary, hire_date)
        self.table_number = table_number
        self.__tips = 0.0
        self.experience_years = experience_years

    def work(self):
        print(f"{self} is serving tables")

    def take_order(self, order):
        print(f"{self} took the order")

    def serve_food(self):
        print(f"{self} is serving food")

    def request_bill(self):
        print(f"{self} brought the bill")

    @property
    def tips(self):
        return self.__tips

    def add_tip(self, amount):
        self.__tips += amount


class Chef(Person):
    def __init__(self, id, name, phone, email, salary, hire_date, specialty, years_experience):
        super().__init__(id, name, phone, email, salary, hire_date)
        self.specialty = specialty
        self.years_experience = years_experience

    def work(self):
        print(f"{self} is cooking {self.specialty}")

    def cook_dish(self, dish_name):
        print(f"{self} is cooking: {dish_name}")


class DeliveryPerson(Person):
    def __init__(self, id, name, phone, email, salary, hire_date, vehicle_type):
        super().__init__(id, name, phone, email, salary, hire_date)
        self.vehicle_type = vehicle_type
        self.__current_location = None

    def work(self):
        print(f"{self} is delivering orders on {self.vehicle_type}")

    def deliver_order(self, delivery):
        print(f"{self} is delivering to: {delivery.address}")

    @property
    def current_location(self):
        return self.__current_location

    @current_location.setter
    def current_location(self, location):
        self.__current_location = location


class Customer:
    def __init__(self, name, phone, address):
        self.name = name
        self.__phone = phone
        self.address = address

    def make_payment(self, payment):
        print(f"{self.name} is paying: {payment.amount}")

    def track_delivery(self, delivery):
        print(f"{self.name} is tracking delivery. Status: {delivery.status}")

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = value

    def __str__(self):
        return self.name


class MenuItem:
    def __init__(self, name, price, is_available = True):
        self.name = name
        self.__price = price
        self.is_available = is_available

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value > 0:
            self.__price = value

    def __str__(self):
        return self.name


class Menu:
    total_menus = 0

    def __init__(self, name):
        self.name = name
        self.__items = []
        Menu.total_menus += 1

    @property
    def items(self):
        return self.__items

    def add_item(self, item):
        self.__items.append(item)

    def remove_item(self, item):
        self.__items.remove(item)

    @staticmethod
    def get_total_menus():
        return Menu.total_menus


class Order:
    order_count = 0

    def __init__(self, is_delivery = False):
        Order.order_count += 1
        self.__order_id = Order.order_count
        self.__status = "pending"
        self.__total_price = 0.0
        self.is_delivery = is_delivery
        self.__items = []

    @property
    def order_id(self):
        return self.__order_id

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def total_price(self):
        return self.__total_price

    def add_item(self, item):
        self.__items.append(item)
        self.__total_price += item.price
        print(f"Added: {item} ({item.price})")

    def remove_item(self, item):
        self.__items.remove(item)
        self.__total_price -= item.price

    def __len__(self):
        return len(self.__items)

    def __lt__(self, other):
        return self.__total_price < other.__total_price


class Payment:
    def __init__(self, amount):
        self.__amount = amount
        self.__status = "unpaid"

    @property
    def amount(self):
        return self.__amount

    @property
    def status(self):
        return self.__status

    def process_payment(self):
        self.__status = "paid"
        print(f"Payment of {self.__amount} was successful")

    def __str__(self):
        return f"Payment: {self.__amount} - {self.__status}"


class Delivery:
    def __init__(self, address):
        self.address = address
        self.__status = "preparing"

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_status):
        self.__status = new_status
        print(f"Delivery status updated: {new_status}")

    def __str__(self):
        return f"Delivery to {self.address} - {self.__status}"



waiter1 = Waiter(1, "John", "123", "john@email.com", 2000, "2023-01-01", 5, 3)
chef1 = Chef(2, "Mike", "456", "mike@email.com", 3000, "2023-01-01", "Italian", 5)
customer1 = Customer("Alice", "789", "Main St 10")

menu = Menu("Main Menu")
item1 = MenuItem("Pizza", 15.99)
item2 = MenuItem("Pasta", 12.99)
menu.add_item(item1)
menu.add_item(item2)

order1 = Order(is_delivery=True)
order1.add_item(item1)
order1.add_item(item2)

print(f"Order total: {order1.total_price}")
print(f"Order ID: {order1.order_id}")
print(f"Order status: {order1.status}")
order1.status = "completed"
print(f"New status: {order1.status}")
print(f"Total menus created: {Menu.get_total_menus()}")
print(f"Waiter salary: {waiter1.salary}")
waiter1.salary = 2500
print(f"New salary: {waiter1.salary}")
print(f"Item price: {item1.price}")
item1.price = 18.99
print(f"New price: {item1.price}")
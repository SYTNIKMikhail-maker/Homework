from abc import ABC


class Person(ABC):
    def __init__(self, person_id, name, phone, email, salary, hire_date):
        self._id = person_id
        self.name = name
        self.__phone = phone
        self.__email = email
        self.__salary = salary
        self.__hire_date = hire_date

    def get_info(self):
        return f"{self.name}"

    def login(self):
        print(f"{self.name} logged in")

    def logout(self):
        print(f"{self.name} logged out")

    @property
    def get_Salary(self):
        return self.__salary


class Waiter(Person):
    def __init__(self, person_id, name, phone, email, salary, hire_date,
                 table_number, tips, experience_years):
        super().__init__(person_id, name, phone, email, salary, hire_date)
        self.table_number = table_number
        self.tips = tips
        self.experience_years = experience_years

    def take_Order(self):
        print(f"{self.name} takes the order")

    def serve_Food(self):
        print(f"{self.name} serves the food")

    def request_Bill(self):
        print(f"{self.name} brings the bill")


class Chef(Person):
    def __init__(self, person_id, name, phone, email, salary, hire_date,
                 specialty, certifications, years_experience):
        super().__init__(person_id, name, phone, email, salary, hire_date)
        self.specialty = specialty
        self.certifications = certifications
        self.years_experience = years_experience

    def cook_Dish(self):
        print(f"{self.name} cooks a dish")


class DeliveryPerson(Person):
    def __init__(self, person_id, name, phone, email, salary, hire_date,
                 vehicle_type, current_location):
        super().__init__(person_id, name, phone, email, salary, hire_date)
        self.vehicle_type = vehicle_type
        self.current_location = current_location

    def deliver_Order(self):
        print(f"{self.name} delivers the order")


class MenuItem:
    def __init__(self, name, price, is_available):
        self.name = name
        self.price = price
        self.is_available = is_available

    def get_Price(self):
        return self.price


class Menu:
    def __init__(self, name, items):
        self.name = name
        self.items = items

    def get_items(self):
        return self.items


class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.__phone = phone
        self.orders = []

    def make_Payment(self):
        print(f"{self.name} makes payment")

    def track_Delivery(self):
        print(f"{self.name} tracks delivery")


class Payment:
    def __init__(self, amount, status):
        self.__amount = amount
        self.status = status

    def process_Payment(self):
        print(f"Processing payment of {self.__amount}")

    def get_Status(self):
        return self.status


class Delivery:
    def __init__(self, address, status):
        self.address = address
        self.status = status

    def get_Status(self):
        return self.status

    def update_Status(self, new_status):
        self.status = new_status
        print(f"Delivery status updated: {self.status}")


class Order:
    def __init__(self, status, total_price, is_delivery,
                 customer, payment, delivery, menu):
        self.status = status
        self.total_price = total_price
        self.is_delivery = is_delivery

        self.customer = customer
        self.payment = payment
        self.delivery = delivery
        self.menu = menu

        self.items = []

        customer.orders.append(self)

    def add_Item(self, item):
        self.items.append(item)
        print(f"Added: {item.name}")

    def remove_Item(self, item):
        self.items.remove(item)
        print(f"Removed: {item.name}")


burger = MenuItem("Burger", 9.99, True)
pizza = MenuItem("Pizza", 12.50, True)
soda = MenuItem("Soda", 2.00, True)
menu = Menu("Main Menu", [burger, pizza, soda])

waiter = Waiter(1, "Alice", "111", "a@a.com", 2000, "2022-01-01", 3, 50.0, 2)
chef = Chef(2, "Bob", "222", "b@b.com", 3000, "2020-05-01", "Italian", "Pro", 5)
delivery_person = DeliveryPerson(3, "Carl", "333", "c@c.com", 1800, "2023-03-01",
                                 "Bicycle", "Downtown")

customer = Customer("John", "555-1234")

payment = Payment(22.49, "pending")
delivery = Delivery("5th Avenue 10", "on the way")

order = Order(
    status="new",
    total_price=22.49,
    is_delivery=True,
    customer=customer,
    payment=payment,
    delivery=delivery,
    menu=menu
)

order.add_Item(burger)
order.add_Item(pizza)

waiter.take_Order()
chef.cook_Dish()
delivery_person.deliver_Order()

payment.process_Payment()
delivery.update_Status("delivered")

print(f"{customer.name} has {len(customer.orders)} orders")
print(f"Menu items: {[item.name for item in menu.get_items()]}")
print(f"Order items: {[item.name for item in order.items]}")
print(f"Waiter info: {waiter.get_info()}")
print(f"Chef salary: {chef.get_Salary}")

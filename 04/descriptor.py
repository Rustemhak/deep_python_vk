class FloatValue:
    @classmethod
    def verify_value(cls, value):
        if not isinstance(value, float):
            raise TypeError("Присваивать можно только вещественный тип данных.")

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self.verify_value(value)
        instance.__dict__[self.name] = value


class StringValue:
    def verify_value(self, value):
        if not isinstance(value, str):
            raise TypeError("Присваивать можно только строковый тип данных")
        elif not (self.min_length <= len(value) <= self.max_length):
            raise ValueError("Присваивать можно только длиной от 2 до 50 символов.")

    def __init__(self, min_length=2, max_length=50):
        self.min_length = min_length
        self.max_length = max_length

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self.verify_value(value)
        instance.__dict__[self.name] = value


class PriceValue:
    def verify_value(self, value):
        if not isinstance(value, int):
            raise TypeError("Присваивать можно только целое число")
        elif not (0 <= value <= self.max_value):
            raise ValueError("Присваивать можно только положительное число до 10_000 включительно.")

    def __init__(self, max_value=10_000):
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self.verify_value(value)
        instance.__dict__[self.name] = value


class Product:
    name = StringValue()
    price = PriceValue()
    weight = FloatValue()

    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight

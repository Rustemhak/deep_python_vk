def add_custom_prefix(name):
    return name if name.startswith('__') and name.endswith('__') \
        else 'custom_' + name


class CustomMeta(type):

    def __new__(mcs, name, bases, dct):
        custom_attrs = {
            add_custom_prefix(name): value
            for name, value in dct.items()
        }
        return type.__new__(mcs, name, bases, custom_attrs)

    def __custom_setattr__(cls, key, val):
        cls.__dict__[add_custom_prefix(key)] = val

    def __call__(cls, *args, **kwargs):
        cls.__setattr__ = CustomMeta.__custom_setattr__

        self = type.__call__(cls, *args, **kwargs)
        custom_dict = {}
        for key, val in self.__dict__.items():
            custom_dict['custom_' + key] = val
        self.__dict__ = custom_dict

        return self


class CustomClass(metaclass=CustomMeta):
    x = 50

    @classmethod
    def multiply_x(cls, n):
        return cls.custom_x * n

    def __init__(self, val=99):
        self.val = val

    @staticmethod
    def line():
        return 100

    def __str__(self):
        return "Custom_by_metaclass"

    def square(self):
        return self.custom_val ** 2

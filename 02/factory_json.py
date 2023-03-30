import string
import factory


class JSONFactory(factory.Factory):
    """JSON Generator"""
    fields = []
    keywords = []

    @classmethod
    def generate(cls, strategy: list, **kwargs) -> str:
        """Method for generating json string with strategy[0] elements
                 and strategy[1] values for each element """
        cls.fields = []
        cls.keywords = []
        result = "{\n"
        for i in range(strategy[0]):
            result += '  "' + string.ascii_letters[i] + '"' + ": "
            cls.fields.append(string.ascii_letters[i])
            if strategy[1] > 1:
                result += "["
            for j in range(strategy[1]):
                if j > len(string.ascii_uppercase):
                    j = 0
                result += '"' + string.ascii_uppercase[j + i] + '"'
                cls.keywords.append(string.ascii_uppercase[j + i])
                if j != strategy[1] - 1:
                    result += ", "
            if strategy[1] > 1:
                result += "]"
            if i != strategy[0] - 1:
                result += ","
            result += "\n"
        result += "}\n"
        return result

    @classmethod
    def get_fields(cls):
        return cls.fields

    @classmethod
    def get_keywords(cls):
        return cls.keywords

"""module profile decorator"""
import cProfile
import pstats
import io


def profile_deco(function):
    """profile_deco"""

    class Wrapper:
        """wrapper class"""

        def __init__(self, function):
            self.function = function
            self.content = []

        def __call__(self, *args, **kwargs):
            profile = cProfile.Profile()
            profile.enable()
            self.function(*args, **kwargs)
            profile.disable()
            string = io.StringIO()
            pstat = pstats.Stats(profile, stream=string)
            pstat.print_stats()
            self.content.append(string.getvalue())

        def print_stat(self):
            """print stat"""
            print("\n".join(self.content))

    return Wrapper(function)


@profile_deco
def add(value_a, value_b):
    """add"""
    return value_a + value_b


@profile_deco
def sub(value_a, value_b):
    """sub"""
    return value_a - value_b


if __name__ == "__main__":
    add(1, 2)
    add(4, 5)

    add.print_stat()

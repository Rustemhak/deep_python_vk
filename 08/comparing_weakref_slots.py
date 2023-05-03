"""Comparing ref module"""

import io
import weakref
import cProfile
import pstats

from time import time
from memory_profiler import profile


class CommonClass:
    def __init__(self, value_1, value_2):
        self.attribute_1 = value_1
        self.attribute_2 = value_2


class SlotClass:
    __slots__ = "attribute_1", "attribute_2"


class WeakClass:
    def __init__(self, value_1, value_2):
        self.attribute_1 = weakref.ref(value_1)
        self.attribute_2 = weakref.ref(value_2)


class Plug1:
    pass


class Plug2:
    pass


@profile
def common_create():
    commons = []
    for _ in range(100500):
        com = CommonClass(Plug1(), Plug2())
        commons.append(com)

    return commons


@profile
def slot_create():
    slots = []

    for _ in range(100500):
        slot = SlotClass()
        slot.attribute_1 = Plug1()
        slot.attribute_2 = Plug2()
        slots.append(slot)

    return slots


@profile
def weaks_create():
    weaks = []

    for _ in range(100500):
        weak = WeakClass(Plug1(), Plug2())
        weaks.append(weak)

    return weaks


@profile
def df_access(list_classes):
    result = 0
    for element in list_classes:
        if element.attribute_1 and element.attribute_2:
            result += 1


@profile
def df_change(list_classes):
    for element in list_classes:
        element.attribute_1, element.attribute_2 = (
            element.attribute_2,
            element.attribute_1,
        )


@profile
def df_delete(list_classes):
    for element in list_classes:
        del element.attribute_2
        del element.attribute_1


def get_result(func, *args):
    start_time = time()
    result = func(*args)
    end_time = time()
    return result, end_time - start_time


def main():
    comms, com_time = get_result(common_create)
    slots, slot_time = get_result(slot_create)
    weaks, weak_time = get_result(weaks_create)

    print("Time create common", com_time)
    print("Time create slots", slot_time)
    print("Time create weaks", weak_time)
    print()
    print("Time access common", get_result(df_access, comms)[1])
    print("Time access slots", get_result(df_access, slots)[1])
    print("Time access weaks", get_result(df_access, weaks)[1])
    print()
    print("Time change common", get_result(df_change, comms)[1])
    print("Time change slots", get_result(df_change, slots)[1])
    print("Time change weaks", get_result(df_change, weaks)[1])
    print()
    print("Time delete common", get_result(df_delete, comms)[1])
    print("Time delete slots", get_result(df_delete, slots)[1])
    print("Time delete weaks", get_result(df_delete, weaks)[1])


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    main()
    pr.disable()
    s = io.StringIO()
    SORT_BY = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(SORT_BY)
    ps.print_stats()
    print(s.getvalue())

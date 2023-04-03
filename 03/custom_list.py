class CustomList(list):
    def operation_lists(self, second, add=True, right=False):
        new_list = []
        max_length = max(len(self), len(second))
        for i in range(max_length):
            left_el = self[i] if i < len(self) else 0
            right_el = second[i] if i < len(second) else 0
            if add:
                new_list.append(left_el + right_el)
            else:
                if right:
                    new_list.append(right_el - left_el)
                else:
                    new_list.append(left_el - right_el)
        return new_list

    def __add__(self, other):
        result = self.operation_lists(other)
        return CustomList(result)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        result = self.operation_lists(other, add=False, right=False)
        return CustomList(result)

    def __rsub__(self, other):
        result = self.operation_lists(other, add=False, right=True)
        return CustomList(result)

    def __eq__(self, other):
        return sum(self[:]) == other

    def __ne__(self, other):
        return sum(self[:]) != other

    def __lt__(self, other):
        return sum(self[:]) < other

    def __le__(self, other):
        return sum(self[:]) <= other

    def __ge__(self, other):
        return sum(self[:]) >= other

    def __gt__(self, other):
        return sum(self[:]) > other

    def __str__(self):
        return f"{self[:]}, {sum(self[:])}"

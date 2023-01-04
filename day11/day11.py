# Advent of Code: Day 11
__author__ = "Matteo Golin"

# Imports
from typing import Self, Callable
import operator
from progress.bar import Bar

# Constants
INPUT_FILE = "./input.txt"


# Main
class Monkey:

    jungle: dict[int, Self] = {}
    big_num: int = 1

    def __init__(
            self,
            _id: int,
            starting_items: list[int],
            operation: Callable,
            test: int,
            pass_id: int,
            fail_id: int,
    ):
        self.id = _id
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.pass_id = pass_id
        self.fail_id = fail_id
        self.inspections: int = 0

        self.__class__.jungle[_id] = self  # Store the monkey in a searchable way
        self.__class__.big_num *= test  # Store the big num for reducing worry

    @staticmethod
    def parse_operation(operation: str, test: int) -> Callable:

        """Returns a lambda that performs the operation."""

        # Create operation
        operation = operation.split(" ")

        # Get operator
        match operation[1]:
            case "*":
                op = operator.mul
            case "/":
                op = operator.truediv
            case "+":
                op = operator.add
            case "-":
                op = operator.sub
            case _:
                raise ValueError("Invalid operator.")

        def operation_lambda(old: int, relief: bool) -> tuple[bool, int]:

            # Get second value
            second = None
            if operation[2] != "old":
                second = int(operation[2])

            # Two old values
            if not second:
                second = old

            new = op(old, second)
            new = new // 3 if relief else new
            return new % test == 0, new

        return operation_lambda

    @classmethod
    def from_input(cls, input_str: str) -> Self:

        """Creates a Monkey instance from a chunk of input text."""

        information = input_str.split("\n")

        # Parse ID
        id = int(information[0][7])

        # Parse items
        items = information[1].replace(",", " ").split()[2:]
        items = [int(item) for item in items]

        # Parse test
        test_num = int(information[3].split(" ")[-1])
        pass_num = int(information[4].split(" ")[-1])
        fail_num = int(information[5].split(" ")[-1])

        # Parse operation
        operation = information[2].split("=")[-1].strip()
        operation = cls.parse_operation(operation, test_num)

        return Monkey(
            _id=id,
            starting_items=items,
            test=test_num,
            pass_id=pass_num,
            fail_id=fail_num,
            operation=operation
        )

    def take_turn(self, relief: bool = True):

        """The monkey inspects and throws items to other monkeys."""

        for item in self.items:

            # Perform operation
            test_passed, new_worry = self.operation(item, relief)
            self.inspections += 1

            # Reduce worry non-destructively
            new_worry %= self.big_num

            # Select monkey to throw to
            if test_passed:
                next_id = self.pass_id

            else:
                next_id = self.fail_id

            monkey = self.__class__.jungle[next_id]
            monkey.items.append(new_worry)

        self.items = []  # Reset items as they have all been thrown

    def __repr__(self):
        return f"Monkey {self.id}: {self.items} {self.inspections}"


def main():

    # Unload input
    with open(INPUT_FILE, "r") as file:
        raw_monkeys = file.read().split("\n\n")

    # Create monkeys
    for monkey in raw_monkeys:
        Monkey.from_input(monkey)

    # Part 1
    # Which two monkeys inspected the most items

    # Perform rounds
    for _ in range(20):

        # Loop through monkeys
        for monkey in Monkey.jungle.values():
            monkey.take_turn()

    two_highest = sorted(Monkey.jungle.values(), key=lambda x: x.inspections, reverse=True)[:2]
    monkey_business = two_highest[0].inspections * two_highest[1].inspections
    print(f"The level of monkey business is: {monkey_business}.")

    # Part 2
    # What is the monkey business if worry levels are no longer divided by three after inspection

    # Reset monkeys
    Monkey.jungle = {}
    Monkey.big_num = 1
    for monkey in raw_monkeys:
        Monkey.from_input(monkey)

    # 1000 Rounds
    bar = Bar("Rounds", max=10_000)
    for _ in range(10_000):

        # Loop through monkeys
        for monkey in Monkey.jungle.values():
            monkey.take_turn(relief=False)

        # print(f"Round {_ + 1} results: ")
        # for print_monkey in Monkey.jungle.values():
        #     print(print_monkey)
        # print()

        bar.next()
    bar.finish()

    two_highest = sorted(Monkey.jungle.values(), key=lambda x: x.inspections, reverse=True)[:2]
    monkey_business = two_highest[0].inspections * two_highest[1].inspections
    print(f"The level of monkey business without reducing worry is: {monkey_business}.")


if __name__ == '__main__':
    main()

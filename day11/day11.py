# Advent of Code: Day 11
__author__ = "Matteo Golin"

# Imports
from typing import Self, Callable

# Constants
INPUT_FILE = "./input.txt"


# Main
class Monkey:

    jungle = {}

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

    @staticmethod
    def parse_operation(operation: str, test: int) -> Callable:

        """Returns a lambda that performs the operation."""

        def operation_lambda(old: int) -> tuple[bool, int]:
            newop = operation.replace("old", str(old))
            new = eval(newop) // 3
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

    def take_turn(self):

        """The monkey inspects and throws items to other monkeys."""

        for item in self.items:

            # Perform operation
            test_passed, new_worry = self.operation(item)
            self.inspections += 1

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

        # Show after each round
        # print(f"Round {_ + 1} results: ")
        # for print_monkey in Monkey.jungle.values():
        #     print(print_monkey)
        # print()

    two_highest = sorted(Monkey.jungle.values(), key=lambda x: x.inspections, reverse=True)[:2]
    monkey_business = two_highest[0].inspections * two_highest[1].inspections
    print(f"The level of monkey business is: {monkey_business}.")


if __name__ == '__main__':
    main()

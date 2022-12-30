# Advent of Code: Day 6
__author__ = "Matteo Golin"

# Imports

# Constants
INPUT_FILE = "./input.txt"


def index_of_packet_header(stream: str, unique_chars: int) -> int:

    """Returns the index of the packet header in the signal stream."""

    packet_header: list[str] = [""] * unique_chars
    for character in stream:

        if len(packet_header) == unique_chars and len(set(packet_header)) == unique_chars and "" not in packet_header:
            packet_header = "".join(packet_header)
            return stream.index(packet_header) + unique_chars

        # Store last 4 characters
        packet_header.append(character)
        packet_header.pop(0)


# Main
def main():

    # Unpacking input
    with open(INPUT_FILE, 'r') as file:
        signal = file.read()

    # Part 1
    # Detect the beginning of the packet stream and report the index at which it ends
    header_loc = index_of_packet_header(signal, 4)
    print(f"The packet header begins after character #{header_loc}, and it is {signal[header_loc - 4: header_loc]}")

    # Part 2
    # Detect the start-of-message marker and report the index at which it ends
    header_loc = index_of_packet_header(signal, 14)
    print(f"The packet header begins after character #{header_loc}, and it is {signal[header_loc - 14: header_loc]}")


if __name__ == '__main__':
    main()

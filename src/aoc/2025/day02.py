"""https://adventofcode.com/2025/day/2"""

from aoc_utils import get_input_data, print_time_taken

actual_input = get_input_data(2025, 2)


example_input = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""


@print_time_taken
def solve(inputs: str):
    ranges = inputs.split(",")

    part1, part2 = 0, 0
    for start_end in ranges:
        start, end = map(int, start_end.split("-"))
        for number in range(start, end + 1):
            str_num = str(number)
            number_length = len(str_num)
            for num_chunks in range(2, number_length + 1):
                chunk_l, r = divmod(number_length, num_chunks)
                if r != 0:
                    continue
                is_invalid = True
                for i in range(0, number_length - chunk_l, chunk_l):
                    next_i = i + chunk_l
                    if str_num[i : i + chunk_l] != str_num[next_i : next_i + chunk_l]:
                        is_invalid = False
                        break
                if is_invalid:
                    part2 += number
                    if num_chunks == 2:
                        part1 += number
                    break

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}\n")


solve(example_input)
solve(actual_input)

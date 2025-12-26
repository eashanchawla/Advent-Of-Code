import argparse
import timeit
from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int


def load_file(filepath: str) -> tuple[list[Range], list[int]]:
    """Load file into a list of Range objects and a list of input values."""
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f]

    ranges = []
    values = []
    empty_line_found = False

    for line in lines:
        if line == '':
            empty_line_found = True
            continue

        if not empty_line_found:
            # Parse range (e.g., "3-5")
            start, end = line.split('-')
            ranges.append(Range(int(start), int(end)))
        else:
            # Parse input values
            values.append(int(line))

    return ranges, values

def check_if_in_range(range: Range, value: int) -> bool:
    return True if value >= range.start and value <= range.end else False
        

def part1(ranges: list[Range], values: list[int]) -> int:
    """Solve part 1 of the puzzle."""
    fresh_ingredients = 0
    for value in values:
        for range in ranges:
            if check_if_in_range(range, value):
                fresh_ingredients += 1
                break
    return fresh_ingredients

def calculate_overlap(range1: Range, range2: Range) -> bool:
    # range1 is before range 2 and completely out 
    if range1.end < range2.start or range2.end < range1.start:
        return False
    return True

def find_max(ranges: list[Range]) -> int:
    return max([current_range.end for current_range in ranges])
    

def find_power_of_2(max: int) -> int:
    pow = 1
    while True:
        if 2 ** pow >= max:
            return 2 ** pow
        pow += 1

def is_overlapping(range_left: Range, range_right: Range) -> bool:
    return range_right.start <= range_left.end + 1

def merge_overlap(range_left: Range, range_right: Range) -> Range:
    start = min(range_left.start, range_right.start)
    end = max(range_left.end, range_right.end)
    return Range(start, end)

def part2(ranges: list[Range]) -> int:
    """Solve part 2 of the puzzle."""
    sorted_ranges = sorted(ranges, key=lambda r: r.start)
    merged_ranges = [sorted_ranges[0]]

    for i in range(1, len(sorted_ranges)):
        current_range = sorted_ranges[i]
        if is_overlapping(merged_ranges[-1], current_range):
            merged_ranges[-1] = merge_overlap(merged_ranges[-1], current_range)
        else:
            merged_ranges.append(current_range)

    return sum([(current_range.end - current_range.start + 1)for current_range in merged_ranges])


def solve_part1(filepath: str) -> int:
    """Wrapper to solve part 1."""
    ranges, values = load_file(filepath)
    return part1(ranges, values)


def solve_part2(filepath: str) -> int:
    """Wrapper to solve part 2."""
    ranges, values = load_file(filepath)
    return part2(ranges)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2025 Day 5")
    parser.add_argument("filepath", help="Path to input file")
    args = parser.parse_args()

    # Load the data
    ranges, values = load_file(args.filepath)

    print(f"Loaded {len(ranges)} ranges and {len(values)} input values")

    # Part 1
    print("\n=== Part 1 ===")
    try:
        result1 = part1(ranges, values)
        print(f"Answer for part 1: {result1}")
        time1 = timeit.timeit(lambda: solve_part1(args.filepath), number=100)
        print(f"Average CPU time (100 runs): {time1/100:.6f} seconds")
    except NotImplementedError as e:
        print(f"Part 1: {e}")

    # Part 2
    print("\n=== Part 2 ===")
    try:
        result2 = part2(ranges)
        print(f"Answer for part 2: {result2}")
        time2 = timeit.timeit(lambda: solve_part2(args.filepath), number=100)
        print(f"Average CPU time (100 runs): {time2/100:.6f} seconds")
    except NotImplementedError as e:
        print(f"Part 2: {e}")
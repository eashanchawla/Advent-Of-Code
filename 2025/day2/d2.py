from pathlib import Path
from util import Range, load_file
from typing import List

def detect_repeat(number: str) -> bool:
    if len(number) % 2 == 0:
        mp = len(number) // 2
        return True if number[:mp] == number[mp:] else False
    else:
        return False

def part1(parsed_ranges: Range):
    final_ans = 0
    for ranges in parsed_ranges:
        start, end = ranges.start, ranges.end
        for number in range(start, end + 1):
            if detect_repeat(str(number)):
                final_ans += number
    return final_ans


def detect_repeat_updated(number: str) -> bool:
    for i in range(2, len(number) + 1):
        if len(number) % i == 0:
            div = len(number) // i
            if number[:div] * i == number:
                return True


def detect_max_in_limit(ranges: List[Range]) -> int:
    return max(r.end for r in ranges)
    
def is_contained_in_ranges(ranges: List[Range], number: int) -> bool:
    for range in ranges:
        if number >= range.start and number <= range.end:
            return True
    return False


def part2_reverse_max(parsed_ranges: List[Range]) -> int:
    seed = 1
    solution = 0
    limit = detect_max_in_limit(parsed_ranges)
    considered_set = set()
    while True:
        if int(str(seed) * 2) > limit:
            break
        repeat = 2
        while True:
            candidate_str = str(seed) * repeat
            candidate_val = int(candidate_str)
            
            if candidate_val > limit:
                break
            
            if is_contained_in_ranges(parsed_ranges, candidate_val):
                considered_set.add(candidate_val)
            repeat += 1
            
        seed += 1
    return sum(considered_set)



def part2(parsed_ranges: List[Range]):
    final_ans = 0
    for ranges in parsed_ranges:
        start, end = ranges.start, ranges.end
        for number in range(start, end + 1):
            if detect_repeat_updated(str(number)):
                final_ans += number
    return final_ans


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load ranges from a file")
    parser.add_argument("path", nargs="?", help="Path to ranges file (default: trial.txt next to this script)")
    parser.add_argument("-t", "--time", type=int, default=0, help="If >0, run each part this many times and report timing stats")
    args = parser.parse_args()

    if args.path:
        path = Path(args.path)
    else:
        path = Path(__file__).resolve().parent / "trial.txt"

    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")

    parsed = load_file(path)
    print(f"Loaded {len(parsed)} ranges")

    # If timing requested, run each part multiple times and print stats
    if args.time and args.time > 0:
        import time
        import statistics

        def time_runs(func, *fargs, repeats: int = 5):
            times: list[float] = []
            last = None
            for _ in range(repeats):
                t0 = time.perf_counter()
                last = func(*fargs)
                t1 = time.perf_counter()
                times.append(t1 - t0)
            return last, times

        _, times1 = time_runs(part1, parsed, repeats=args.time)
        _, times2 = time_runs(part2, parsed, repeats=args.time)
        _, times3 = time_runs(part2_reverse_max, parsed, repeats=args.time)

        print(f"part1: runs={args.time} min={min(times1):.6f}s mean={statistics.mean(times1):.6f}s std={statistics.pstdev(times1):.6f}s")
        print(f"part2: runs={args.time} min={min(times2):.6f}s mean={statistics.mean(times2):.6f}s std={statistics.pstdev(times2):.6f}s")
        print(f"part2 pro: runs={args.time} min={min(times3):.6f}s mean={statistics.mean(times3):.6f}s std={statistics.pstdev(times3):.6f}s")
    else:
        print(f'Solution for part 1: {part1(parsed)}')
        print(f'Solution for part 2: {part2(parsed)}')
        print(f'Solution for part 2: {part2_reverse_max(parsed)}')
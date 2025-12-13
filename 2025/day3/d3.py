from pathlib import Path
from typing import List
import timeit

def load_grid(path: str | Path, to_int: bool = True) -> List[List[int]]:
	"""Load a file into a grid (list of lists).

	Each line becomes a row. By default each character is converted to int.

	Args:
		path: path to the input file.
		to_int: if True, convert each character to int; otherwise keep as str.

	Returns:
		List of rows, where each row is a list of ints (or strings).
	"""
	p = Path(path)
	text = p.read_text(encoding="utf-8").strip()
	if not text:
		return []

	grid: List[List[int]] = []
	for line in text.splitlines():
		row = [ch for ch in line.rstrip("\n")]
		if to_int:
			try:
				grid.append([int(ch) for ch in row])
			except ValueError as exc:
				raise ValueError(f"Non-integer character found in line: {line!r}") from exc
		else:
			grid.append(row)

	return grid

def solve(grid):
    return part1(grid)

def find_max(row, limit):
	max_val, max_index = float("-inf"), -1
	for i in range(limit):
		if row[i] == max_val:
			# don't change index
			continue
		elif row[i] > max_val:
			max_val, max_index = row[i], i
	return max_val, max_index

def part1(grid: List[List[int]]) -> int:
	solution = 0
	for row in grid:
		search_limit = len(row)

		while True:
			max_val, max_index = find_max(row, search_limit)
			if max_index == len(row) - 1:
				search_limit -= 1
			else:
				break
		remainder = row[max_index + 1:]
		second_max, _ = find_max(remainder, len(remainder))
		
		current_sol = int(str(max_val) + str(second_max))
		solution += current_sol
	return solution

def part2(grid: List[List[int]]) -> int:
	pass

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description="Load a grid file into a list-of-lists")
	parser.add_argument("path", nargs="?", help="Path to grid file (default: trial.txt next to this script)")
	parser.add_argument("--no-int", dest="to_int", action="store_false", help="Leave characters as strings instead of converting to int")
	parser.add_argument("-n", type=int, default=5, help="Number of rows to print as sample")
	args = parser.parse_args()

	if args.path:
		path = Path(args.path)
	else:
		path = Path(__file__).resolve().parent / "trial.txt"

	if not path.exists():
		raise SystemExit(f"Input file not found: {path}")

	grid = load_grid(path, to_int=args.to_int)
	print(f'Answer for part 1: {part1(grid)}')
	
	setup_code = "from __main__ import solve; from __main__ import grid"
	stmt = "solve(grid)"
	results = timeit.repeat(
        stmt=stmt, 
        setup=setup_code, 
        repeat=5, 
        number=5000 
    )
	min_time = min(results) / 5000 # Divide by number of runs to get time per call
	print(f"\nTimeit Results (best of 5 runs, 5000 loops each):")
	print(f"  Best time per call: {min_time * 1e6:.3f} microseconds") # Display in microseconds for small times
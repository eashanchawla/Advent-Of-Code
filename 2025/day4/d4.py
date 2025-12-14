import argparse
import timeit
from collections import deque

adjacent = [
    [-1, -1], [0, -1], [1, -1],
    [-1, 0], [1, 0], [-1, 1], 
    [0, 1], [1, 1]
]

def load_file(filepath: str) -> list[list[str]]:
    """Load file into a list of lists where each value is a character."""
    with open(filepath, 'r') as f:
        return [list(line.strip()) for line in f]

def check_adjacent_positions(i: int, j: int, grid: list[list[str]]) -> bool:
    num_adj = 0
    for x, y in adjacent:
        updated_x, updated_y = x + i, y + j
        if updated_x < 0 or updated_x >= len(grid):
            continue
        if updated_y < 0 or updated_y >= len(grid[0]):
            continue

        if grid[updated_x][updated_y] == '@':
            num_adj += 1
    
    return True if num_adj < 4 and grid[i][j] == '@' else False


def part1(grid: list[list[str]]) -> int:
    """Solve part 1 of the puzzle."""
    eligible_rolls = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if check_adjacent_positions(i, j, grid):
                eligible_rolls += 1
    return eligible_rolls

def part2(grid: list[list[str]]) -> int:
    """Solve part 2 using a queue and your original helper."""
    rows = len(grid)
    cols = len(grid[0])
    
    # Use a queue for efficiency (O(1) pops)
    queue = deque()

    # 1. Initial Scan: Find everything currently removable
    for r in range(rows):
        for c in range(cols):
            # We use your function here
            if check_adjacent_positions(r, c, grid):
                queue.append((r, c))

    removed_count = 0
    
    # 2. Process the queue
    while queue:
        r, c = queue.popleft()

        # If this spot was already processed/removed, skip it
        if grid[r][c] == '.':
            continue

        # Remove the roll
        grid[r][c] = '.'
        removed_count += 1

        # Check the 8 neighbors of the spot we just cleared
        for dr, dc in adjacent:
            nr, nc = r + dr, c + dc
            
            # Bounds check
            if 0 <= nr < rows and 0 <= nc < cols:
                # If the neighbor is a paper roll, check if it is NOW removable
                if grid[nr][nc] == '@':
                    # We use your function on the neighbor
                    if check_adjacent_positions(nr, nc, grid):
                        queue.append((nr, nc))

    return removed_count


def solve_part1(filepath: str) -> int:
    """Wrapper to solve part 1."""
    grid = load_file(filepath)
    return part1(grid)


def solve_part2(filepath: str) -> int:
    """Wrapper to solve part 2."""
    grid = load_file(filepath)
    return part2(grid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2025 Day 4")
    parser.add_argument("filepath", help="Path to input file")
    args = parser.parse_args()

    # Load the grid
    grid = load_file(args.filepath)

    print(f"Loaded grid: {len(grid)} rows x {len(grid[0])} cols")

    # Part 1
    print("\n=== Part 1 ===")
    result1 = part1(grid)
    print(f"Answer for part 1: {result1}")
    time1 = timeit.timeit(lambda: solve_part1(args.filepath), number=100)
    print(f"Average CPU time (100 runs): {time1/100:.6f} seconds")

    # Part 2 (reload grid since part2 modifies it)
    print("\n=== Part 2 ===")
    grid = load_file(args.filepath)
    result2 = part2(grid)
    print(f"Answer for part 2: {result2}")
    time2 = timeit.timeit(lambda: solve_part2(args.filepath), number=100)
    print(f"Average CPU time (100 runs): {time2/100:.6f} seconds")
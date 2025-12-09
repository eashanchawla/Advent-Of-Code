from pathlib import Path
from typing import List
from move import Move

def load_moves(path: str | Path) -> List[Move]:
    """Load moves from a file where each line is like 'L68' or 'R30'.

    Args:
        path: Path to the input file.

    Returns:
        A list of Move objects parsed from the file.
    """
    p = Path(path)
    moves: List[Move] = []
    with p.open("r", encoding="utf-8") as fh:
        for raw in fh:
            s = raw.strip()
            if not s:
                continue
            # First character is direction (L/R), rest is integer distance
            direction = s[0]
            try:
                distance = int(s[1:])
            except ValueError as exc:
                raise ValueError(f"Invalid move line: {s!r}") from exc
            moves.append(Move(direction=direction, move=distance))
    return moves

def is_zero(rolling_sum: int):
    '''simple did we hit a 0?'''
    return True if rolling_sum % 100 == 0 else False

def calculate_final_position(start: int, move: Move):
    '''what is the final position based on the current position and the move being made'''
    return (start + move.move) % 100 if move.direction == 'R' else (start - move.move) % 100

def calculate_number_zeros_hit(start: int, move: Move) -> int:
    '''calculate number of zeros hit by this move, considering that a move can lead to crossing multiple zeros'''
    if move.direction == 'L': 
        distance_to_first_0 = 100 if start == 0 else start
    else:
        distance_to_first_0 = 100 - start
    number_moves = 0 if move.move < distance_to_first_0 else 1 + ((move.move - distance_to_first_0) // 100)
    return number_moves

def part1(moves: List[Move]):
    rolling_sum, pwd = 50, 0
    for move in moves:
        direction_multiplier = 1 if move.direction == 'R' else -1
        rolling_sum += (move.move * direction_multiplier)
        rolling_sum = rolling_sum % 100
        if is_zero(rolling_sum):
            pwd += 1
    return pwd

def part2(moves: List[Move]): 
    start, pwd = 50, 0
    for move in moves:
        new_start = calculate_final_position(start, move)
        count_moves = calculate_number_zeros_hit(start, move)
        start = new_start
        pwd += count_moves
    return pwd

if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Load moves from a file")
    parser.add_argument("path", nargs="?", help="Path to moves file (default: trial.txt next to this script)")
    args = parser.parse_args()

    if args.path:
        demo_path = Path(args.path)
    else:
        demo_path = Path(__file__).resolve().parent / "trial.txt"

    if not demo_path.exists():
        raise SystemExit(f"Input file not found: {demo_path}")

    parsed = load_moves(demo_path)
    print(f"Loaded {len(parsed)} moves")
    print(f'Answer: {part1(parsed)}')
    print(f'Answer: {part2(parsed)}')
    
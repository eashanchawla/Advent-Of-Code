from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Range:
    start: int
    end: int


def load_file(path: str | Path) -> List[Range]:
    """Load comma-separated ranges like '11-22,95-115' into List[Range].

    Each range is 'start-end'. Returns start and end as ints.
    """
    p = Path(path)
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        return []

    ranges: List[Range] = []
    for seg in (s.strip() for s in text.split(",") if s.strip()):
        try:
            start_s, end_s = seg.split("-", 1)
            ranges.append(Range(start=int(start_s), end=int(end_s)))
        except ValueError as exc:
            raise ValueError(f"Invalid range segment: {seg!r}") from exc

    return ranges

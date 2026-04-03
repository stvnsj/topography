from dataclasses import dataclass
import common.numeric as numeric

@dataclass(frozen=True)
class HeightEntry:
    dm_raw: str
    height_raw: str

    @property
    def dm_float(self):
        return numeric.to_rounded_float(self.dm_raw)

    @property
    def height_float(self):
        return numeric.to_float(self.height_raw)


class LongitudinalProfile:
    def __init__(self, entries: list[HeightEntry]):
        self._entries = entries
        self._by_dm_raw = {entry.dm_raw: entry.height_raw for entry in entries}

    @classmethod
    def from_matrix(cls, matrix):
        if matrix is None:
            return cls([])
        entries = [HeightEntry(dm_raw=row[0], height_raw=row[1]) for row in matrix]
        return cls(entries)

    def to_legacy_dict(self):
        return dict(self._by_dm_raw)

    def contains(self, dm_raw: str) -> bool:
        return dm_raw in self._by_dm_raw

    def get_height_raw(self, dm_raw: str, default="0"):
        return self._by_dm_raw.get(dm_raw, default)

    def guess_dm(self, dm_raw: str, tolerance=0.01):
        dm_float = numeric.to_rounded_float(dm_raw)
        if dm_float is None:
            return None

        for entry in self._entries:
            entry_dm = entry.dm_float
            if entry_dm is None:
                continue
            if numeric.are_close(dm_float, entry_dm, tolerance=tolerance):
                return entry.dm_raw

        return None
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class CrossSectionRow:
    dm_raw: str
    x_raw: str
    y_raw: str
    z_raw: str
    label_raw: str

    @classmethod
    def from_array_row(cls, row):
        return cls(
            dm_raw=row[0],
            x_raw=row[1],
            y_raw=row[2],
            z_raw=row[3],
            label_raw=row[4],
        )

    def to_array(self):
        return np.array(
            [self.dm_raw, self.x_raw, self.y_raw, self.z_raw, self.label_raw],
            dtype=str,
        )

    @property
    def axis_raw(self):
        return np.array([self.x_raw, self.y_raw], dtype=str)
    
    @property
    def dm_is_blank(self):
        return self.dm_raw == ""
    

    
class CrossSectionBlock:
    def __init__(self, rows: list[CrossSectionRow]):
        if not rows:
            raise ValueError("CrossSectionBlock requires at least one row")
        self.rows = rows

    @property
    def dm_raw(self):
        return self.rows[0].dm_raw

    @property
    def default_height_raw(self):
        return self.rows[0].z_raw

    @property
    def axis_raw(self):
        return self.rows[0].axis_raw

    def matrix_raw(self):
        return np.array([row.to_array() for row in self.rows], dtype=str)

    def codes_raw(self):
        return np.array([row.label_raw for row in self.rows], dtype=str)
    

class CrossSectionFile:

    def __init__(self, blocks):
        # This is a list of CrossSectionBlock
        self.blocks = blocks

    @classmethod
    def from_matrix(cls, matrix):
        # If matrix is empty, the file is returned empty.
        if matrix is None or len(matrix) == 0:
            return cls([])

        # List of all CrossSectionRow of the data file.
        rows = [CrossSectionRow.from_array_row(row) for row in matrix]
        # Final list of all CrossSectionBlock
        blocks = []

        # CrossSectionRow's in each CrossSectionBlock
        current_rows = [rows[0]]

        # Iterate over all CrossSectionRows's, starting 
        # from the second row.
        for row in rows[1:]:
            # If row is not the start of a block, append to the 
            # current block
            if row.dm_is_blank:
                current_rows.append(row)
            # otherwise...
            else:
                # build a CrossSectionBlock with current_rows, and...
                blocks.append(CrossSectionBlock(current_rows))
                # make row the first element of the next CrossSectionBlock
                current_rows = [row]

        # build the last CrossSectionBlock with current_rows
        blocks.append(CrossSectionBlock(current_rows))

        # build the CrossSectionFile with the list of CrossSectionBlock's
        return cls(blocks)
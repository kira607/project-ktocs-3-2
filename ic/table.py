class Cell:
    def __init__(self, value: str):
        self.value = str(value)

    def __len__(self):
        return len(self.value) + 2

    def render(self, width: int) -> str:
        result = ' '
        result += self.value
        result += ' ' * (width - len(self.value) - 2)
        result += ' '
        return result


class Row:
    def __init__(self, cols: int):
        self._cols = cols
        self._cells = []

    def __iter__(self):
        return iter(self._cells)

    def __getitem__(self, key):
        return self._cells[key]

    def set(self, *cells: str):
        if len(cells) != self._cols:
            raise ValueError(f'Too {"much" if len(cells) < self._cols else "few"} values for row!')
        for cell_val in cells:
            cell = Cell(cell_val)
            self._cells.append(cell)

    def get_len(self):
        length = 0
        for cell in self._cells:
            length += len(cell)
        return length

    def render(self, cols_widths) -> str:
        result = '|'
        for i, cell in enumerate(self._cells):
            result += cell.render(cols_widths[i]) + '|'
        result += '\n'
        return result


class Header(Row):
    pass


class Table:
    def __init__(self, cols: int):
        self._cols = cols
        self._header = None
        self._rows = []

    def set_header(self, *cells):
        self._header = Header(self._cols)
        self._header.set(*cells)

    def add_row(self, *cells: str):
        row = Row(self._cols)
        row.set(*cells)
        self._rows.append(row)

    def render(self) -> str:
        cols_widths = self.get_cols_widths()
        result = ''
        sep_row = '+' + '+'.join('-' * n for n in cols_widths) + '+\n'
        if self._header:
            result += sep_row
            result += self._header.render(cols_widths)
            result += sep_row
        for row in self._rows:
            result += row.render(cols_widths)
        result += sep_row
        return result

    def get_cols_widths(self):
        if self._header:
            cols_widths = [len(self._header[i]) for i in range(self._cols)]
        else:
            cols_widths = [0 for _ in range(self._cols)]
        for row in self._rows:
            for i, cell in enumerate(row):
                cols_widths[i] = max(cols_widths[i], len(cell))
        return tuple(cols_widths)

def main():
    grid = open('15b.txt').read().splitlines()
    grid = [list(row) for row in grid]

    n = 0
    while '.' in str(grid):
        step(grid)
        n += 1
    print(n)


def step(grid):
    to_oxygenate = []
    for pos, value in enumerate2d(grid):
        if value == 'O':
            for nei in get_neighbors(pos):
                if getindex(grid, nei) == '.':
                    to_oxygenate.append(nei)

    for pos in to_oxygenate:
        setindex(grid, pos, 'O')


def getindex(grid, pos):
    r, c = pos
    return grid[r][c]


def setindex(grid, pos, value):
    r, c = pos
    grid[r][c] = value


def get_neighbors(pos):
    r, c = pos
    return [
        (r - 1, c),
        (r + 1, c),
        (r, c - 1),
        (r, c + 1),
    ]



def enumerate2d(grid):
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            yield (r, c), value


main()

"""the maze"""

import random
from collections import deque
WALL = "#"
FLOOR = "."
DIRS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
def make_maze(width: int, height: int) -> list[list[str]]:
    """random maze"""
    grid = [[WALL] * width for _ in range(height)]
    grid[1][1] = FLOOR
    stack = [(1, 1)]
    while stack:
        x, y = stack[-1]
        options = []
        for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and grid[ny][nx] == WALL:
                options.append((dx, dy))
        if options:
            dx, dy = random.choice(options)
            grid[y + dy // 2][x + dx // 2] = FLOOR
            grid[y + dy][x + dx] = FLOOR
            stack.append((x + dx, y + dy))
        else:
            stack.pop()
    return grid
def find_path(grid, start, goal, blocked=frozenset()):
    """shortest path as a list of tiles"""
    parents = {start: None}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parents[(x, y)]
            path.reverse()
            return path
        for dx, dy in DIRS.values():
            nxt = (x + dx, y + dy)
            if nxt in parents or nxt in blocked or grid[nxt[1]][nxt[0]] == WALL:
                continue
            parents[nxt] = (x, y)
            queue.append(nxt)
    return None
def line_clear(grid, x0, y0, x1, y1) -> bool:
    """true if no wall sits between the two tiles"""
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while (x, y) != (x1, y1):
        if (x, y) != (x0, y0) and grid[y][x] == WALL:
            return False
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return True
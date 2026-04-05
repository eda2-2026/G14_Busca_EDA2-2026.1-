import random
import time
from collections import deque
import matplotlib.pyplot as plt

def generate_maze(rows, cols):
    rows = rows if rows % 2 == 1 else rows + 1
    cols = cols if cols % 2 == 1 else cols + 1

    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve(r, c):
        maze[r][c] = 0
        directions = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(directions)

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 < nr < rows and 0 < nc < cols and maze[nr][nc] == 1:
                maze[r + dr//2][c + dc//2] = 0
                carve(nr, nc)

    carve(1, 1)
    return maze

def bfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])

    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    while queue:
        current = queue.popleft()

        if current == end:
            break

        for dr, dc in directions:
            r = current[0] + dr
            c = current[1] + dc

            if (0 <= r < rows and 0 <= c < cols and
                maze[r][c] == 0 and (r, c) not in visited):

                queue.append((r, c))
                visited.add((r, c))
                parent[(r, c)] = current

    if end not in parent:
        return None

    path = []
    node = end

    while node:
        path.append(node)
        node = parent[node]

    path.reverse()
    return path

def draw_maze(maze, path, start, end):
    display = [row[:] for row in maze]

    if path:
        for r, c in path:
            display[r][c] = 2

    display[start[0]][start[1]] = 3
    display[end[0]][end[1]] = 4

    plt.imshow(display)
    plt.title("Labirinto com BFS")
    plt.show()

if __name__ == "__main__":
    maze = generate_maze(21, 21)

    start = (1, 1)
    end = (19, 19)

    # ⏱️ medir tempo do BFS
    start_time = time.perf_counter()
    path = bfs(maze, start, end)
    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    print(f"Tempo de execução do BFS: {elapsed_time:.6f} segundos")

    if path:
        print("Caminho encontrado!")
    else:
        print("Não há caminho.")

    print(f"Tempo de execução do BFS: {elapsed_time:.6f} segundos")

    draw_maze(maze, path, start, end)
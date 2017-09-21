from collections import deque
from heapq import heappop, heappush

def input_to_array(file):
    lines = []
    for line in open(file):
        appendable = list(line.rstrip('\n'))
        lines.append(appendable)
    return lines

def find_starting_position(maze):
    for line in maze:
        for item in line:
            if item=='P':
                pIndex=line.index('P')
                lineIndex = maze.index(line)
                maze[lineIndex][pIndex]=' '
                return(lineIndex,pIndex)
def find_goal_position(maze):
    for line in maze:
        for item in line:
            if item=='.':
                pIndex=line.index('.')
                lineIndex = maze.index(line)
                maze[lineIndex][pIndex]=' '
                return(lineIndex,pIndex)

def maze2graph(maze):
    height = len(maze)
    print(height)
    width = len(maze[0]) if height else 0
    print(width)
    graph = {(i, j): [] for j in range(width) for i in range(height) if  maze[i][j]==' '}
    for row, col in graph.keys():
        if row < height - 1 and maze[row + 1][col]==' ':
            graph[(row, col)].append(("S", (row + 1, col)))
            graph[(row + 1, col)].append(("N", (row, col)))
        if col < width - 1 and maze[row][col + 1]==' ':
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
    return graph

def find_path_bfs(maze,start,goal):
    queue = deque([("", start)])
    visited = set()
    graph = maze
    while queue:
        path, current = queue.popleft()
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            queue.append((path + direction, neighbour))
    return "NO WAY!"

def find_path_dfs(maze,start,goal):
    stack = deque([("", start)])
    visited = set()
    graph=maze
    while stack:
        path, current = stack.pop()
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            stack.append((path + direction, neighbour))
    return "NO WAY!"

def manhattan_distance_heuristic(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def find_path_astar(maze,start,goal):
    pr_queue = []
    heappush(pr_queue, (0 + manhattan_distance_heuristic(start, goal), 0, "", start))
    visited = set()
    graph = maze
    while pr_queue:
        _, cost, path, current = heappop(pr_queue)
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            heappush(pr_queue, (cost + manhattan_distance_heuristic(neighbour, goal), cost + 1,
                                path + direction, neighbour))
    return "NO WAY!"

if __name__ == "__main__":
    medium_maze = input_to_array('./Inputs/mediumMaze.txt')
    for line in medium_maze:
        print(line)
    start = find_starting_position(medium_maze)
    goal = find_goal_position(medium_maze)
    graph = maze2graph(medium_maze)
    print(graph)
    x=find_path_bfs(graph,start,goal)
    print(x)
    x=find_path_dfs(graph,start,goal)
    print(x)
    x = find_path_astar(graph, start, goal)
    print(x)
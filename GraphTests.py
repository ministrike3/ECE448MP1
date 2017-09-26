from collections import deque
from heapq import heappop, heappush
import glob
import copy


def get_list_of_1dot_files():
    return glob.glob("./Inputs/1dot/*")


def input_to_array(file):
    lines = []
    for line in open(file):
        appendable = list(line.rstrip('\n'))
        lines.append(appendable)
    return lines


def find_starting_position(maze):
    for line in maze:
        for item in line:
            if item == 'P':
                p_index = line.index('P')
                line_index = maze.index(line)
                maze[line_index][p_index] = ' '
                return line_index, p_index


def find_goals_position(maze):
    list_of_goals = []
    for line in maze:
        for item in line:
            if item == '.':
                p_index = line.index('.')
                line_index = maze.index(line)
                maze[line_index][p_index] = ' '
                list_of_goals.append((line_index, p_index))
    return list_of_goals


def maze2graph(maze):
    height = len(maze)
    width = len(maze[0]) if height else 0
    graph = {(i, j): [] for j in range(width) for i in range(height) if  maze[i][j] == ' '}
    for row, col in graph.keys():
        if row < height - 1 and maze[row + 1][col] == ' ':
            graph[(row, col)].append(("S", (row + 1, col)))
            graph[(row + 1, col)].append(("N", (row, col)))
        if col < width - 1 and maze[row][col + 1] == ' ':
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
    return graph


def find_path_bfs(graph, start, goal):
    queue = deque([("", start)])
    visited = set()
    while queue:
        path, current = queue.popleft()
        if current == goal:
            return path, len(visited)
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            queue.append((path + direction, neighbour))
    return "NO WAY!", len(visited)


def find_path_dfs(graph, start, goal):
    stack = deque([("", start)])
    visited = set()
    while stack:
        path, current = stack.pop()
        if current == goal:
            return path, len(visited)
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            stack.append((path + direction, neighbour))
    return "NO WAY!",len(visited)


def find_path_astar(graph, start, goal):
    def manhattan_distance_heuristic(cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])
    pr_queue = []
    heappush(pr_queue, (0 + manhattan_distance_heuristic(start, goal), 0, "", start))
    visited = set()
    while pr_queue:
        _, cost, path, current = heappop(pr_queue)
        if current == goal:
            return path, len(visited)
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            heappush(pr_queue, (cost + manhattan_distance_heuristic(neighbour, goal), cost + 1,
                                path + direction, neighbour))
    return "NO WAY!", len(visited)


def print_solved_maze(start, maze, solution, goals, expanded_nodes, file):
    output_maze = open(file, 'w')
    solved_maze = copy.deepcopy(maze)
    solved_maze[start[0]][start[1]] = 'P'
    current_node = [start[0], start[1]]
    path_cost = len(solution)
    for letter in solution:
        if letter == 'E':
            current_node[1] += 1
            solved_maze[current_node[0]][current_node[1]] = '.'
        if letter == 'W':
            current_node[1] -= 1
            solved_maze[current_node[0]][current_node[1]] = '.'
        if letter == 'S':
            current_node[0] += 1
            solved_maze[current_node[0]][current_node[1]] = '.'
        if letter == 'N':
            current_node[0] -= 1
            solved_maze[current_node[0]][current_node[1]] = '.'
    for row in solved_maze:
        for item in row:
            output_maze.write("%s" % item)
        output_maze.write('\n')
    output_maze.write('Path Cost = ')
    output_maze.write(str(path_cost))
    output_maze.write('\n')
    output_maze.write('Nodes_expanded = ')
    output_maze.write(str(expanded_nodes))


if __name__ == "__main__":
    inputs = get_list_of_1dot_files()
    for raw_input in inputs:
        maze = input_to_array(raw_input)
        names = raw_input.split('/')
        name = names[3]
        name, trash = name.split('.')
        print(name)
        #for line in maze:
        #    print(line)

        start = find_starting_position(maze)

        goals = find_goals_position(maze)

        graph = maze2graph(maze)

        solution, expanded_nodes = find_path_bfs(graph, start, goals[0])
        #print(solution)
        #print(expanded_nodes)
        file_name = './Outputs/1dot/BFS/' + name + '.txt'
        print(file_name)
        print_solved_maze(start, maze, solution, goals, expanded_nodes, file_name)

        solution, expanded_nodes = find_path_dfs(graph, start, goals[0])
        # print(solution)
        # print(expanded_nodes)
        file_name = './Outputs/1dot/DFS/' + name + '.txt'
        print(file_name)
        print_solved_maze(start, maze, solution, goals, expanded_nodes, file_name)

        solution, expanded_nodes = find_path_astar(graph, start, goals[0])
        #print(solution)
        #print(expanded_nodes)
        file_name = './Outputs/1dot/Astar/' + name + '.txt'
        print(file_name)
        print_solved_maze(start, maze, solution, goals, expanded_nodes, file_name)

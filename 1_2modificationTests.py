from collections import deque
from heapq import heappop, heappush
from itertools import combinations
import glob
import copy
import time

class Node:
    def __init__(self,coords,cost,path,goals):
        self.coords=coords
        self.cost=cost
        self.path=path
        self.goals = goals


def neil_hash(coordinates,goals):
    #word = str(coordinates[0] ** 3) + str(coordinates[1] ** 3) + str(len(goals))
    word= str(coordinates[0] * 1000 + coordinates[1])
    goalstring = ''
    for goal in goals:
        goalstring += (str(goal[0]) + str(goal[1]))
    word += goalstring
    return word


def find_path_greedy(graph, start, goals):
    def manhattan_distance_heuristic(cell, goal):
        return abs(cell[0] - goal[0][0]) + abs(cell[1] - goal[0][1])


    # states is a duplicate of goals
    states=list(goals)
    #declare a hashmap for all the nodes that are going to be created
    nodes_hash={}
    #this sequence creates a unique hash based on the coordinates,the number of remaining goals, and the goals
    name = neil_hash(start,states)
    #Create the initial starting node and initialize it with a cost 0 and a blank path
    nodes_hash[name] = Node(start, 0, '', states)


    pr_queue = []
    heappush(pr_queue, (0 + manhattan_distance_heuristic(start, goals),name))
    visited = set()

    while pr_queue:
        _, node_name = heappop(pr_queue)

        current_node = nodes_hash[node_name]
        # get the list of goals left for a node in this state
        goals_targeted = list(current_node.goals)
        # if this node is a goal
        if current_node.coords in goals_targeted:
            # remove the goal from list of goals
            goals_targeted.remove(current_node.coords)
        # if the node has 0 goals left its a solution, return its path
        if len(goals_targeted) == 0:
            return current_node.path, len(visited)
        # if this node has been visited already, dont do anything
        if (node_name) in visited:
            continue
        # make a new copy of the (possibly) modified list
        goals = list(goals_targeted)
        # Add this node to the visited set
        visited.add(node_name)

        for direction, neighbor in graph[current_node.coords]:
            name = neil_hash(neighbor,goals)
            if name not in nodes_hash:
                nodes_hash[name]=Node(neighbor, current_node.cost+1,current_node.path+direction, goals)

            heappush(pr_queue, (manhattan_distance_heuristic(neighbor, goals),name))
    return "NO WAY!", len(visited)


def print_solved_maze(start, maze, solution, goals, expanded_nodes, file, time):
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
    output_maze.write('The Number of Nodes Expanded = ')
    output_maze.write(str(expanded_nodes))
    output_maze.write('Seconds Used = ')
    output_maze.write(str(time))


def get_list_of_multi_dot_files():
    return glob.glob("./Inputs/Search/*")


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
                dot_index = line.index('.')
                line_index = maze.index(line)
                maze[line_index][dot_index] = ' '
                list_of_goals.append((line_index, dot_index))
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

def find_path_dfs(graph, start, goalinput):
    # states is a duplicate of goalinput
    states=list(goalinput)
    #declare a hashmap for all the nodes that are going to be created
    nodes_hash={}
    #this sequence creates a unique hash based on the coordinates,the number of remaining goals, and the goals
    name = neil_hash(start,states)
    #Create the initial starting node and initialize it with a cost 0 and a blank path
    nodes_hash[name] = Node(start, 0, '', states)
    #print(nodes_hash[name])
    #print(name)
    #push the initial node onto the queue
    stack = deque([name])
    visited = set()

    while stack:
        #pop the nodes name off the queue
        node_name = stack.pop()
        #print(node_name)
        #get the info about the node from the hashmap
        current_node = nodes_hash[node_name]
        #get the list of goals left for a node in this state
        goals_targeted=list(current_node.goals)
        #if this node is a goal
        #print(current_node.coords)
        #print(current_node.goals)
        if current_node.coords in goals_targeted:
            #remove the goal from list of goals
            goals_targeted.remove(current_node.coords)
        # if the node has 0 goals left its a solution, return its path
        if len(goals_targeted) == 0:
            return current_node.path,len(visited)
        # if this node has been visited already, dont do anything
        if (node_name) in visited:
            continue
        # make a new copy of the (possibly) modified list
        goals = list(goals_targeted)
        # Add this node to the visited set
        visited.add(node_name)
        for direction, neighbor in graph[current_node.coords]:
            #print(direction,neighbor)
            #print(visited)

            name = neil_hash(neighbor,goals)
            #print(name)
            if name not in nodes_hash:
                #print('I\'m appended!')
                nodes_hash[name]=Node(neighbor, current_node.cost+1,current_node.path+direction, goals)
            stack.append(name)

    return "NO WAY!", len(visited)


def find_path_astar(graph, start, goals):
    def manhattan_distance_heuristic(cell, goal):
        return abs(cell[0] - goal[0][0]) + abs(cell[1] - goal[0][1])


    # states is a duplicate of goals
    states=list(goals)
    #declare a hashmap for all the nodes that are going to be created
    nodes_hash={}
    #this sequence creates a unique hash based on the coordinates,the number of remaining goals, and the goals
    name = neil_hash(start,states)
    #Create the initial starting node and initialize it with a cost 0 and a blank path
    nodes_hash[name] = Node(start, 0, '', states)


    pr_queue = []
    heappush(pr_queue, (0 + manhattan_distance_heuristic(start, goals),name))
    visited = set()

    while pr_queue:
        _, node_name = heappop(pr_queue)

        current_node = nodes_hash[node_name]
        # get the list of goals left for a node in this state
        goals_targeted = list(current_node.goals)
        # if this node is a goal
        if current_node.coords in goals_targeted:
            # remove the goal from list of goals
            goals_targeted.remove(current_node.coords)
        # if the node has 0 goals left its a solution, return its path
        if len(goals_targeted) == 0:
            return current_node.path, len(visited)
        # if this node has been visited already, dont do anything
        if (node_name) in visited:
            continue
        # make a new copy of the (possibly) modified list
        goals = list(goals_targeted)
        # Add this node to the visited set
        visited.add(node_name)

        for direction, neighbor in graph[current_node.coords]:
            name = neil_hash(neighbor,goals)
            if name not in nodes_hash:
                nodes_hash[name]=Node(neighbor, current_node.cost+1,current_node.path+direction, goals)

            heappush(pr_queue, (current_node.cost+1+manhattan_distance_heuristic(neighbor, goals),name))
    return "NO WAY!", len(visited)


def find_path_astar_multi(graph, start, goal_input):
    def heuristic(start,goal_list):
        def manhattan_distance(cell, goal):
            return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

        if len(goal_list)==0:
            return(0)
        elif len(goal_list)==1:
            return(manhattan_distance(start, goal_list[0]))
        else:
            max_distance=0
            for pair in combinations(goal_list, 2):
                if manhattan_distance(pair[0],pair[1]) > max_distance:
                    max_distance = manhattan_distance(pair[0],pair[1])
                    max_pair=pair
            d=min(manhattan_distance(start, max_pair[0]),manhattan_distance(start, max_pair[1]))
            return(max_distance+d)

    #heuristic(start,goals)
    state = set(goal_input)
    pr_queue = []
    heappush(pr_queue, (0 + heuristic(start, state), 0, "", start,state))
    visited = set()
    while pr_queue:
        _, cost, path, current,goals_left = heappop(pr_queue)
        goals_targeted=list(goals_left)
        if current in goals_targeted:
            goals_targeted.remove(current)
            #    print('GOAL')

        if len(goals_targeted) == 0:
            return path, len(visited)

        if (current, frozenset(goals_targeted)) in visited:
            # print('Already In Visited')
            # print(visited)
            continue

        goals = list(goals_targeted)
        visited.add((current, frozenset(goals)))
        for direction, neighbour in graph[current]:
            heappush(pr_queue, (cost + heuristic(neighbour, goals), cost + 1, path + direction, neighbour,goals))


def find_path_bfs(graph, start, goalinput):
    # states is a duplicate of goalinput
    states=list(goalinput)
    #declare a hashmap for all the nodes that are going to be created
    nodes_hash={}
    #this sequence creates a unique hash based on the coordinates,the number of remaining goals, and the goals
    name = neil_hash(start,states)
    #Create the initial starting node and initialize it with a cost 0 and a blank path
    nodes_hash[name] = Node(start, 0, '', states)
    #print(nodes_hash[name])
    #print(name)
    #push the initial node onto the queue
    queue = deque([name])
    visited = set()

    while queue:
        #pop the nodes name off the queue
        node_name = queue.popleft()
        #print(node_name)
        #get the info about the node from the hashmap
        current_node = nodes_hash[node_name]
        #get the list of goals left for a node in this state
        goals_targeted=list(current_node.goals)
        #if this node is a goal
        #print(current_node.coords)
        #print(current_node.goals)
        if current_node.coords in goals_targeted:
            #remove the goal from list of goals
            goals_targeted.remove(current_node.coords)
        # if the node has 0 goals left its a solution, return its path
        if len(goals_targeted) == 0:
            return current_node.path,len(visited)
        # if this node has been visited already, dont do anything
        if (node_name) in visited:
            continue
        # make a new copy of the (possibly) modified list
        goals = list(goals_targeted)
        # Add this node to the visited set
        visited.add(node_name)
        for direction, neighbor in graph[current_node.coords]:
            #print(direction,neighbor)
            #print(visited)

            name = neil_hash(neighbor,goals)
            #print(name)
            if name not in nodes_hash:
                #print('I\'m appended!')
                nodes_hash[name]=Node(neighbor, current_node.cost+1,current_node.path+direction, goals)
            queue.append(name)
    return "NO WAY!", len(visited)


if __name__ == "__main__":
    inputs = get_list_of_1dot_files()
    #inputs = ['./Inputs/1dot/mediumMaze.txt']
    #inputs = ['./Inputs/Search/tinySearch.txt']

    for raw_input in inputs:
        maze = input_to_array(raw_input)
        names = raw_input.split('/')
        name = names[3]
        name, trash = name.split('.')
        print(name)

        start = find_starting_position(maze)
        initial_goals = find_goals_position(maze)
        graph = maze2graph(maze)
        start_time=time.time()
        solution, expanded_nodes = find_path_bfs(graph, start, initial_goals)
        end_time=time.time()
        print(end_time-start_time)
        print(solution)
        print(expanded_nodes)
        file_name = './Outputs/1dot/BFS/' + name + '.txt'
        print(file_name)
        print_solved_maze(start, maze, solution, initial_goals, expanded_nodes, file_name,end_time-start_time)
        #
        start_time=time.time()
        solution, expanded_nodes = find_path_dfs(graph, start, initial_goals)
        end_time=time.time()
        print(end_time-start_time)
        print(solution)
        print(expanded_nodes)
        file_name = './Outputs/1dot/DFS/' + name + '.txt'
        print(file_name)
        print_solved_maze(start, maze, solution, initial_goals, expanded_nodes, file_name,end_time-start_time)

        start_time=time.time()
        solution, expanded_nodes = find_path_greedy(graph, start, initial_goals)
        end_time=time.time()
        print(end_time-start_time)
        print(solution)
        print(expanded_nodes)
        file_name = './Outputs/1dot/Greedy/' + name + '.txt'
        print(file_name)
        print_solved_maze(start, maze, solution, initial_goals, expanded_nodes, file_name,end_time-start_time)

        start_time=time.time()
        solution, expanded_nodes = find_path_astar(graph, start, initial_goals)
        end_time=time.time()
        print(end_time-start_time)
        print(solution)
        print(expanded_nodes)
        file_name = './Outputs/1dot/Astar/' + name + '.txt'
        print(file_name)
        print_solved_maze(start, maze, solution, initial_goals, expanded_nodes, file_name,end_time-start_time)

    inputs = ['./Inputs/Search/tinySearch.txt']

    for raw_input in inputs:
        maze = input_to_array(raw_input)
        names = raw_input.split('/')
        name = names[3]
        name, trash = name.split('.')
        print(name)

        start = find_starting_position(maze)
        initial_goals = find_goals_position(maze)
        graph = maze2graph(maze)
        start_time=time.time()
        solution, expanded_nodes = find_path_bfs(graph, start, initial_goals)
        end_time=time.time()
        print(end_time-start_time)
        print(solution)
        print(expanded_nodes)
        file_name = './Outputs/Search/BFS/' + name + '.txt'
        print(file_name)
        print_solved_maze(start, maze, solution, initial_goals, expanded_nodes, file_name,end_time-start_time)

        # start_time=time.time()
        # solution, expanded_nodes = find_path_astar_multinodes(graph, start, initial_goals)
        # end_time=time.time()
        # print(end_time-start_time)
        # print(solution)
        # print(expanded_nodes)
        # file_name = './Outputs/Search/Astar/' + name + '.txt'
        # print(file_name)
        # print_solved_maze(start, maze, solution, initial_goals, expanded_nodes, file_name,end_time-start_time)

        # print('New Loop')
        # print('Current Node Coordinates',current_node.coords)
        # print('Current Node Goals',current_node.goals)
        # print('PR Queue',pr_queue)
        # print('Visited Set',visited)
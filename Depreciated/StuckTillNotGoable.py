from anytree import Node, RenderTree
import sys
def input_to_array(file):
    lines = []
    for line in open(file):
        appendable = list(line.rstrip('\n'))
        lines.append(appendable)
    return lines

def find_starting_position(maze):
    pIndex=0
    for line in maze:
        for item in line:
            if item=='P':
                pIndex=line.index('P')
                lineIndex = maze.index(line)
                return(lineIndex,pIndex,)

def explore_frontier(node,direction):
    location=node.name[1:-1]
    yCord,xCord=location.split(',')
    xCord=int(xCord)
    yCord=int(yCord)

    top = medium_maze[yCord - 1][xCord]
    if top == ' ' and direction!='Top':
        modifycord=yCord
        while medium_maze[modifycord][xCord]==' ':
            modifycord-=1
        print('top')
        next_node = Node('('+str(modifycord)+','+str(xCord)+')', parent = node)
        explore_frontier(next_node,'Bot')

    bot = medium_maze[yCord + 1][xCord]
    if bot == ' ' and direction!='Bot':
        i=1
        while medium_maze[yCord + i][xCord]==' ':
            i+=1
        print('bot')
        next_node = Node('('+str(yCord + i)+','+str(xCord)+')', parent = node)
        explore_frontier(next_node,'Top')

    left = medium_maze[yCord][xCord-1]
    if left == ' ' and direction !='Left':
        modifycord=xCord
        while medium_maze[yCord][modifycord]==' ':
            modifycord-=1
        print('left')
        next_node = Node('('+str(yCord)+','+str(modifycord)+')', parent = node)
        explore_frontier(next_node,'Right')

    right = medium_maze[yCord][xCord + 1]
    if right == ' ' and direction !='Right':
        i=1
        while medium_maze[yCord][xCord+i]==' ':
            i+=1
        print('right')
        next_node = Node('('+str(yCord)+','+str(xCord+i-1)+')', parent = node)
        print(next_node.name)
        explore_frontier(next_node,'Left')



if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    medium_maze = input_to_array('./Inputs/mediumMaze.txt')
    for line in medium_maze:
        print(line)
    start=find_starting_position(medium_maze)
    print(start)
    start_node=Node(str(start))
    explore_frontier(start_node,'None')
    for pre, fill, node in RenderTree(start_node):
        print("%s%s" % (pre, node.name))
from anytree import Node, RenderTree
from anytree.dotexport import RenderTreeGraph
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
    if location not in visitedNodes:
        visitedNodes.append(location)
        yCord,xCord=location.split(',')
        yCord=int(yCord)
        xCord=int(xCord)
        top = medium_maze[yCord - 1][xCord]
        bot = medium_maze[yCord + 1][xCord]
        left = medium_maze[yCord][xCord-1]
        right = medium_maze[yCord][xCord + 1]

        if top == '.' or bot == '.' or left == '.' or right == '.':
            next_node = Node('(' + str(yCord - 1) + ',' + str(xCord) + '.............)', parent=node)
            print('DONEDOENDOENDONE',next_node.name)
        if top == ' ' and direction!='Top':
            next_node = Node('('+str(yCord - 1)+','+str(xCord)+')', parent = node)
            print('top',next_node.name)
            explore_frontier(next_node,'Bot')

        if bot == ' ' and direction!='Bot':
            next_node = Node('('+str(yCord + 1)+','+str(xCord)+')', parent = node)
            print('bot',next_node.name)
            explore_frontier(next_node,'Top')

        if left == ' ' and direction !='Left':
            next_node = Node('('+str(yCord)+','+str(xCord-1)+')', parent = node)
            print('left',next_node.name)
            explore_frontier(next_node,'Right')

        if right == ' ' and direction !='Right':
            next_node = Node('('+str(yCord)+','+str(xCord+1)+')', parent = node)
            print('right',next_node.name)
            explore_frontier(next_node,'Left')



if __name__ == "__main__":
    #sys.setrecursionlimit(1000)
    medium_maze = input_to_array('./Inputs/mediumMaze.txt')
    for line in medium_maze:
        print(line)
    start=find_starting_position(medium_maze)
    print(start)
    start_node=Node(str(start))
    visitedNodes=[]
    explore_frontier(start_node,'None')
    for pre, fill, node in RenderTree(start_node):
        print("%s%s" % (pre, node.name))
    RenderTreeGraph(start_node).to_picture("tree.png")

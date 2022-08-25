import random

def generateGraph(nodeNum, root = 1, splitRate = 0.5, connectRate = 0.5):
    # generate a random graph
    # Parameters:
    # nodeNum - the amount of nodes
    # spliteRate - the split probability of a tree, which is used to generate the graph
    # connectRate - the connect probability of nodes (besides the construction of the tree)
    # Phase 1: randomize a tree
    # Initialize
    graph = {}
    nodeList = []
    for i in range(0, nodeNum-1):
        if i + 1 != root:
            nodeList.append(i + 1)
        graph[i + 1] = []
    # Define a queue (first come last leave) to store father nodes
    fatherList = []
    # Initialize this queue with root
    fatherList.insert(0, root)
    # Define a list (leave only) to store child nodes
    childList = nodeList.copy()
    while childList:
        child = random.choice(childList)
        childList.remove(child)
        # choose a child, and it might become new father
        fatherList.insert(0,child)
        # get the father
        father = fatherList.pop()
        # use "SplitRate" to control the number of children of each node in the tree
        if random.random() < splitRate:
            # put the used father back, so as to own more children
            fatherList.append(father)
        # link it
        graph[father].append(child)
    # Phase 2: add extra links besides the tree (for the sink)
    sink = nodeNum
    graph[sink] = []
    fatherList = nodeList.copy()
    fatherList.append(root)
    probFatherList = []
    while fatherList:
        father = fatherList.pop()
        if len(graph[father]) == 0:
            graph[father].append(sink)
        else:
            probFatherList.append(father)
    while probFatherList:
        father = random.choice(probFatherList)
        graph[father].append(sink)
        probFatherList.remove(father)
        if random.random() > connectRate:
            break
    return graph

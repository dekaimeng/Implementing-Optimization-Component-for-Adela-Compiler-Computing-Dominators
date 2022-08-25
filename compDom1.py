import numpy as np
import random
import randomGraph
from copy import deepcopy
class newNode:
    # create a node structure
    def __init__(self, indicator, children, id):
       self.indicator = indicator
       self.children = children
       self.id = id

def getAllImmediateSuccessor(graph, node, idToIndicatorGraph):
    # compute all the successor for the target node
    successorList = []
    # for all the child in our target node, that will be successors
    for child in graph[node.indicator]:
        nodeItem = newNode(child, graph[child], getKeys(idToIndicatorGraph, child))
        successorList.append(nodeItem)
    return successorList

def getAllImmediatePredecessors(graph, node, idToIndicatorGraph):
    # computer all the immediate predecessors for the target node
    immediatePredecessorsList = []
    # if node is a member of someone's child, that will be a immediate predecessor to the node
    for x, y in graph.items():
        if node.indicator in y:
            imNode = newNode(x, y, getKeys(idToIndicatorGraph, x))
            immediatePredecessorsList.append(imNode)
    return immediatePredecessorsList

def getAllNodes(graph, idToIndicatorGraph):
    # get all the nodes in the given graph
    nodeList = []
    for x, y in graph.items():
        nodeItem = newNode(x, y, id = getKeys(idToIndicatorGraph, x))
        nodeList.append(nodeItem)
    return nodeList 

def createDom(graph):
    # create the initial dom, which are all zeros
    dom = np.zeros([len(graph), len(graph)])
    return dom

def printInfor(graph, dom, nodeList):
    print('-'*30)
    print(f'The graph given is {graph}')
    print('-'*30)
    print(f'The node list is:')
    for node in nodeList:
        print(f'node indicator: {node.indicator}, node children: {node.children}')
    print('-'*30)
    print(f'The dominator matrix is:')
    print(dom)
    print('-'*30)

def dfsJustifyGraph(graph, source,path = []):
    # find all path from given graph, in order to justify is graph valid or not
    # print(f'source is {source}, path is {path}')
    if source not in path:
        path.append(source)
        if source not in graph:
            return path
        for neighbour in graph[source]:
            path = dfsJustifyGraph(graph, neighbour, path)
    return sorted(path)

def justifyGraph(graph, paths):
    # justify is this Graph valid by dfs
    allIndicator = []
    for x, y in graph.items():
        allIndicator.append(x)
    print(f'all indicator is: {allIndicator}')
    # if all the nodes will be visited, which means the input graph is exactly one graph, which is valid
    return sorted(allIndicator) == paths

def bfs(start, end, graph):
    # use breadth first search to find all the path from start to end
    q = [[start]]
    paths = []
    target = end
    while q:
        temp = q.pop(0)
        if temp[-1] == target:
            paths.append(temp)
        else:
            for children in graph[temp[-1]]:
                if children in temp:
                    continue
                q.append(temp + [children])
    return paths

def dominateFirst(paths, start, end):
    # all the path to the node must pass the dominator first, so we need:
    # check is dominator always occurs first before the node for all the possible path
    indexStart, indexEnd = 0, 0
    for path in paths:
        find1 = False
        find2 = False
        for index in range(len(path)):
            if path[index] == start:
                indexStart = index
                find1 = True
            elif path[index] == end:
                indexEnd = index
                find2 = True
        if indexStart > indexEnd or (not find1) or (not find2):
            return False
    return True

def testingDom(dom, graph):
    # create an empty new test dom
    testDom = np.zeros([len(graph), len(graph)])
    for i in range(len(dom)):
        for j in range(len(dom[0])):
            # node itself must dominate itself
            if i == j:
                testDom[i][j] = dom[i][j]
                continue
            # find path by bfs
            paths = bfs(1, j + 1, graph)
            # check is our dominator occurs first before our node
            result = dominateFirst(paths, i + 1, j + 1)
            if dom[i][j] == 1:
                # assign 1 to the new test dom
                if result:
                    testDom[i][j] = 1
                # if not result, means our node occurs first than dominator, then our output will be wrong
                else:
                    print('Wrong Dom output!')
                    return
            else:
                if result:
                    print('Wrong Dom output!')
                    return
    # check if test dom is the same with our output dom
    if (testDom == dom).all():
        print('Correct Dom output!')
    return

def testByNewDom(dom, graph):
    # create an empty new test dom
    testDom = np.zeros([len(graph), len(graph)])
    for i in range(len(dom)):
        for j in range(len(dom[0])):
            if i == j:
                testDom[i][j] = dom[i][j]
                continue
            paths = bfs(1, j + 1, graph)
            # check is our dominator occurs first before our node
            result = dominateFirst(paths, i + 1, j + 1)
            # assign 1 to the new test dom
            if result:
                testDom[i][j] = 1
            # if not result, means our node occurs first than dominator, then our output will be wrong
            else:
                testDom[i][j] = 0
    if (testDom == dom).all():
        print('Correct dom!')
    else:
        print('Wrong dom!')
        print(f'Correct dom should be: \n{testDom}')

def findId(graph, s):
    visited = [] # List for visited nodes.
    queue = []     #Initialize a queue
    visited.append(s)
    queue.append(s)
    idList = []
    while queue:          # Creating loop to visit each node
        m = queue.pop(0) 
        idList.append(m)
        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
    return idList

def assignIdIndicator(graph, idList):
    idToIndicatorGraph = {}
    for i in range(len(idList)):
        idToIndicatorGraph[idList[i]] = i + 1
    return idToIndicatorGraph

def changeGraphToNumFormat(graph, idToIndicatorGraph):
    tempGraph = {}
    for x, y in graph.items():
        tempGraph[idToIndicatorGraph[x]] = []
        for item in y:
            tempGraph[idToIndicatorGraph[x]].append(idToIndicatorGraph[item])
    tempGraph = sorted(tempGraph.items())
    newGraph = {}
    for i in tempGraph:
        newGraph[i[0]] = sorted(i[1])
    return newGraph

def changeToDomGraph(graph, dom, idToIndicatorGraph):
    resultDomGraph = {}
    for i in range(len(dom)):
        key = getKeys(idToIndicatorGraph, i + 1)
        resultDomGraph[key] = []
        for j in range(len(dom[0])):
            if dom[i][j] == 1:
                value = j + 1
                resultDomGraph[key].append(getKeys(idToIndicatorGraph, value))
    print('The Dominator relatioship for dom : node is:')
    for x, y in resultDomGraph.items():
        print(f'{x} dominate: {y}')
    return resultDomGraph

def getKeys(idToIndicatorGraph, value):
    for x, y in idToIndicatorGraph.items():
        if y == value:
            return x
    return None

def CompDom(graph, node, dom, idToIndicatorGraph):
    if dom[node.indicator - 1][node.indicator - 1] == 1: # been here before
        return
    # node itself dominate itself
    dom[node.indicator - 1][node.indicator - 1] = 1
    #Let M1 .. Mk be all immediate predecessors of Node
    immediatePredecessorsList = getAllImmediatePredecessors(graph, node, idToIndicatorGraph)
    for mi in immediatePredecessorsList:
        #compute all dominators of mi
        CompDom(graph, mi, dom, idToIndicatorGraph)
    # now check which dominators of predecessors dominate node as well
    nodeList = getAllNodes(graph, idToIndicatorGraph)
    for n in nodeList:
        if n.indicator != node.indicator:# we must ensure n and node must not be the same
            if len(immediatePredecessorsList) > 0: # we must ensure it has immediate predecessor
                for mi in immediatePredecessorsList:
                    dom[n.indicator - 1][node.indicator - 1] = dom[n.indicator - 1][mi.indicator - 1] # n dominate node if n dominate the immediate predecessor of node
                    # if n does not dominate mi
                    if dom[n.indicator - 1][node.indicator - 1] == 0:# n does not dominate mi, so it does not dominate the node
                        break
            # if not immediate predecessor list, means that nodes dominate all the other nodes
            else:
                dom[node.indicator - 1][n.indicator - 1] = 1
    # we have all dominators of node
    successorList = getAllImmediateSuccessor(graph, node, idToIndicatorGraph)
    for successor in successorList:
        if dom[successor.indicator - 1][successor.indicator - 1] == 0:
            # recursive call depth-first traversal
            CompDom(graph, successor, dom, idToIndicatorGraph)

def CompDomSupport(graph, dom):
    allpaths = []
    for x, y in graph.items():
        for i in range(x + 1, len(graph) + 1):
            allpaths = FindAllPaths(graph, 1, i)
            result = dominateFirst(allpaths, x, i)
            print(f'{x} dom {i} with path {allpaths} is {result}')
            if result:
                dom[x - 1][i - 1] = 1
    return dom

def FindAllPaths(graph, src, dst):
    allpaths = []
    path = []
    path.append(src)
    DFS(graph, src, dst, path, allpaths)
    return allpaths
    
def DFS(graph, src, dst, path, allpaths):
    if (src == dst):
        allpaths.append(deepcopy(path))
    else:
        for adjnode in graph[src]:
            if adjnode not in path:
                path.append(adjnode)
                DFS(graph, adjnode, dst, path, allpaths)
                path.pop()


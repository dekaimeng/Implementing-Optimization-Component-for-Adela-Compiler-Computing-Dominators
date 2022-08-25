import numpy as np

def findId(graph, s):
    visited = [] # List for visited nodes.
    queue = []   # Initialize a queue
    visited.append(s)
    queue.append(s)
    idList = []
    while queue: # Creating loop to visit each node
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
    numGraph = {}
    for i in range(len(dom)):
        key = getKeys(idToIndicatorGraph, i + 1)
        resultDomGraph[key] = []
        numGraph[i + 1] = []
        for j in range(len(dom[0])):
            if dom[i][j] == 1:
                value = j + 1
                numGraph[i + 1].append(value)
                resultDomGraph[key].append(getKeys(idToIndicatorGraph, value))
    print('The Dominator relatioship for dom : node is:')
    for x, y in resultDomGraph.items():
        print(f'{x} dominate: {sorted(y)}')
    return resultDomGraph, numGraph

def getKeys(idToIndicatorGraph, value):
    for x, y in idToIndicatorGraph.items():
        if y == value:
            return x
    return None

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

def checkResultList(graph, resultDomGraph, idToIndicatorGraph):
    for x, y in resultDomGraph.items():
        for m, n in graph.items():
            if x == m: continue
            paths = bfs(1, m, graph)
            result = dominateFirst(paths, x, m)
            if result:
                if m not in y:
                    print(f'The result of {getKeys(idToIndicatorGraph, x)} dominate {getKeys(idToIndicatorGraph, m)}, dom is incorrect')
            else:
                if m in y:
                    print(f'The result of {getKeys(idToIndicatorGraph, x)} does not dominate {getKeys(idToIndicatorGraph, m)}, dom is incorrect')
    print('The result dominator graph is correct!')


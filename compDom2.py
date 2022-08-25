from copy import deepcopy
import numpy as np
from functools import reduce

import randomGraph
class newNode:
    # create node structure for doubly linked list, with children, previoud and next pointer
    # the first column of the matrix is being dominated by the entry node
    # if found Enter, insert Enter when create new nodeFirstList
    ENTER = None
    def __init__(self, indicator, children, id):
        self.indicator = indicator
        self.children = children
        self.prev = None
        self.next = None
        self.id = id

class doublyLinkedList:
    # create doubly linked list indicator structure with head and tail
    def __init__(self):
        self.head = None
        self.tail = None

    def addNode(self, indicator, children, id):
        # add node function
        new = newNode(indicator, children, id)
        # if doubly linked list is None, inserted node as head
        if self.head == None:
            self.head = new
            self.tail = new
            self.head.prev = None
            self.tail.next = None
        # add node to the tail, update tail
        else:
            self.tail.next = new
            new.prev = self.tail
            self.tail = new
            self.tail.next = None

    def remove(self, node):
        # remove function
        # if doubly linked list is None, nothing to remove
        if not self.head or not node:
            print('No element to remove')
        curr = self.head
        prev = None
        # loop the doubly linked list, find the target node
        while curr and curr.indicator != node.indicator:
            prev = curr
            curr = curr.next
        # node not find, nothing to remove
        if not curr:
            print('Node not found!')
            return
        # node is the head, update the head
        if curr == self.head:
            self.head = self.head.next
        # node is tail, update the tail
        elif curr == self.tail:
            self.tail = self.tail.prev
            self.tail.next = None
        # node is in the middle
        else:
            curr.prev.next = curr.next
            curr = curr.next
        return node.indicator

    def findKey(self, value):
        if not self.head or not value:
            return False
        curr = self.head
        find = False
        while curr and curr.indicator != value:
            curr = curr.next
            if curr and curr.indicator == value:
                find = True
                break
        return find

def nodeFirstList(node):
    # create an empty doubly linked list, add the node as the head
    domNodeList = doublyLinkedList()
    domNodeList.addNode(node.indicator, node.children, node.id)
    return domNodeList

def getImmediatePredecessors(graph, node, idToIndicatorGraph):
    # get the immediate predecessors for target node in doubly linked list structure
    immediatePredecessorsList = doublyLinkedList()
    for x, y in graph.items():
        if node.indicator in y:
            immediatePredecessorsList.addNode(x, y, getKeys(idToIndicatorGraph, x))
    return immediatePredecessorsList

def intersection(graph, dom, immediatePredecessorsList, idToIndicatorGraph):
    # find the intersection of nodes in immediate predecessor by doubly linked list structure
    # create the empty doubly linked list
    newNodeList = doublyLinkedList()
    curr1 = immediatePredecessorsList.head
    # create an empty list to store each indicator for each immediate predecessor in dom
    indicatorList = []
    # loop the immediate predecessor doubly linked list
    while curr1:
        # loop the dom by immedpate predecessor doubly linked list
        curr2 = dom[curr1.indicator - 1].head
        temp = []
        # store the indicator for each nodes in dom[curr2] to indicatorList
        while curr2:
            temp.append(curr2.indicator)
            curr2 = curr2.next
        curr1 = curr1.next
        indicatorList.append(temp)
    # get the intersection for 2d list of indicator List
    a = reduce(np.intersect1d, (indicatorList))
    # add the node into our empty doubly linked list, which is the intersection
    for d in a:
        newNodeList.addNode(d, graph[d], getKeys(idToIndicatorGraph ,d))
    return newNodeList

def CompDom(graph, node, dom, visit, idToIndicatorGraph):
    # loop until the visit is None
    while visit:
        if dom[node.indicator - 1].head and dom[node.indicator - 1].head.indicator != 0: # been here before
            return
        domNodeList = nodeFirstList(node) # find the linkedList which starts with the node
        # if have Enter already, add the Enter into our current linked list which starts with the node
        if newNode.ENTER:
            domNodeList.addNode(newNode.ENTER.indicator, newNode.ENTER.children, getKeys(idToIndicatorGraph, newNode.ENTER.indicator))
        dom[node.indicator - 1] = domNodeList # list with node as its first node
        visit.remove(node) # remove the node from visit
        # get the immediate predecessors linkedList for the node
        immediatePredecessorsList = getImmediatePredecessors(graph, node, idToIndicatorGraph)
        # if node does not have immediate predecessors, means node is the Enter, so that dominate all other nodes
        # give dom the Enter dominate the others, then return
        if not immediatePredecessorsList.head:
            # define the Enter in newNode structure
            newNode.ENTER = deepcopy(node)
            # add the node(which is Enter, dominate all the other nodes in graph) into dom 
            for i in dom:
                # if i is not None, add the Enter node, which dominate all other nodes
                if i.head and i.head.indicator != 0 and i.head.indicator != node.indicator:
                    i.addNode(node.indicator, node.children, node.id)
            return
        # loop all immediate predecessors, recursive call the function
        mi = immediatePredecessorsList.head
        while mi:
            CompDom(graph, mi, dom, visit, idToIndicatorGraph) # compute all dominators of mi
            mi = mi.next
        # find the intersection of dom[m1] ... dom[mk]
        intersectionLinkedList = intersection(graph, dom, immediatePredecessorsList, idToIndicatorGraph)
        curr = intersectionLinkedList.head
        # add the intersection into the dom
        while curr:
            dom[node.indicator - 1].addNode(curr.indicator, curr.children, curr.id)
            curr = curr.next

def getAllLinkedNodesList(graph, idToIndicatorGraph):
    # get a doubly linked list with all the occurs nodes
    allLinkedList = doublyLinkedList()
    for x,y in graph.items():
        allLinkedList.addNode(x, y, getKeys(idToIndicatorGraph, x))
    return allLinkedList

def initialDom(graph, visit):
    # initialize a dom, which is a list of doubly linked list
    dom = []
    curr = visit.head
    while curr:
        dom.append(doublyLinkedList())
        curr = curr.next
    return dom

def printDom(graph, dom):
    # because Dom[node] stores the node which are dominate the node, but not the node which was dominated by the node
    # so the first dom is the matrix transpose, second dom is the 2d matrix result, first dom is the dominator relationship result
    count = 0
    newDom = np.zeros([len(graph), len(graph)])
    for linkedNode in dom:
        curr = linkedNode.head
        while curr:
            newDom[count][curr.indicator - 1] = 1
            # print(curr.indicator)
            curr = curr.next
        count += 1
    print('-'*30)
    print(f'The input Graph is: {graph}')
    print('-'*30)
    print('The relationship for the dominators of the node is: ')
    print(newDom)
    # change to the dom matrix relationsiop, which is the traversal of our matrix
    twoDimMatrix = np.zeros([len(newDom), len(newDom)])
    for col in range(len(newDom[0])):
        for row in range(len(newDom)): 
            twoDimMatrix[col][row] = newDom[row][col]
    print('-'*30)
    print('The relationship for two dimensional array is:')
    print(twoDimMatrix)
    print('-'*30)
    return twoDimMatrix

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
    # all the path to the node must pass the dominator first, so we need
    # check is dominator always occurs first before the node for all the possible path, 
    # which means every path to the node must pass the dominator
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
        # if the dominator occurs after node, then our result will be false
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

def dfsJustifyGraph(graph, source,path = []):
    # find all path from given graph, in order to justify is graph valid or not
    if source not in path:
        path.append(source)
        if source not in graph:
            return path
        for neighbour in graph[source]:
            path = dfsJustifyGraph(graph, neighbour, path)
    return sorted(path)

def justifyGraph(graph, paths):
    # justify is this Graph valid by dfs
    allindicator = []
    for x, y in graph.items():
        allindicator.append(x)
    # if all the nodes will be visited, which means the input graph is exactly one graph, which is valid
    return sorted(allindicator) == paths

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
    newGraph = {}
    for x, y in graph.items():
        newGraph[idToIndicatorGraph[x]] = []
        for item in y:
            newGraph[idToIndicatorGraph[x]].append(idToIndicatorGraph[item])
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

def CompDomSupport(graph, dom, idToIndicatorGraph):
    allpaths = []
    for x, y in graph.items():
        for i in range(x + 1, len(graph) + 1):
            allpaths = FindAllPaths(graph, 1, i)
            result = dominateFirst(allpaths, x, i)
            if result:
                find = dom[i - 1].findKey(x)
                if not find:
                    dom[i - 1].addNode(x, graph[x], getKeys(idToIndicatorGraph, x))
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

if __name__ == '__main__':
    # graph = {1: [2], 2: [3, 4, 6], 3: [5], 4: [5], 5: [2], 6: []}
    # graph = {'a': ['b'], 'b': ['c', 'd', 'f'], 'c': ['e'], 'd': ['e'], 'e': ['b'], 'f': []}
    # graph = {1: [2], 2: [3, 4], 3: [5], 4: [5], 5: [2]}
    # graph = {1: [2], 2: [3, 4], 3: [], 4: [5, 6], 5: [7, 8], 6: [8], 7: [9], 8: [10], 9: [10], 10: []}
    # graph = {1: [2, 3], 2: [4], 3: [4], 4: [5, 6], 5: [4], 6: []}
    # graph = {1: [3, 4], 2: [5], 3: [4, 5], 4: [2, 3, 5], 5: [2, 3, 4], 6: [2, 5, 1]}
    # graph = {1: [2], 2: [3, 4], 3: [4, 5], 4: [6], 5: [], 6: [2, 5, 3]}
    graph = randomGraph.generateGraph(10, root = 1, splitRate = 0.5, connectRate = 0.5)
    ENTER = list(graph.keys())[0]
    idList = findId(graph, ENTER)
    idToIndicatorGraph = assignIdIndicator(graph, idList)
    print(f'idToIndicatorGraph is {idToIndicatorGraph}')
    newGraph = changeGraphToNumFormat(graph, idToIndicatorGraph)
    print(f'newGraph is {newGraph}')
    print('-'*30)
    path = dfsJustifyGraph(newGraph, 1)
    print(f'The path for given graph is: {path}')
    if justifyGraph(newGraph, path):
        visit = getAllLinkedNodesList(newGraph, idToIndicatorGraph)
        dom = initialDom(newGraph, visit)
        curr = deepcopy(visit).head 
        while curr:
            CompDom(newGraph, curr, dom, visit, idToIndicatorGraph)
            curr = curr.next
        dom = CompDomSupport(newGraph, dom, idToIndicatorGraph)
        twoDimMatrix = printDom(newGraph, dom)
        testDom = testingDom(twoDimMatrix, newGraph)
        print('-'*30)
        resultDomGraph = changeToDomGraph(newGraph, twoDimMatrix, idToIndicatorGraph)
        print('-'*30)
        testByNewDom(twoDimMatrix, newGraph)
    else:
        print('ERROR: Invalid Graph!')

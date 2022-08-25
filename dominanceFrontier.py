import randomGraph
import compDom1
class newNode:
    # create a node structure
    def __init__(self, indicator, children, id):
       self.indicator = indicator
       self.children = children
       self.id = id

def justifyImmediateDominateOrNot(dom, node1, node2):
    if dom[node1.indicator - 1][node2.indicator - 1] == 1:
        if node2.indicator in node1.children:
            return True
    return False

def printDF(node, nodeArray):
    # print the domiance frontier for current node
    if nodeArray:
        print(f'node ID {node.id} dominance frontier is:')
        for n in nodeArray:
            print(n.id)
    return

def DF(graph, node, idToIndicatorGraph, dom, visit, currentWValue, W = []):
    nodeW = []
    # visit set for avoiding auplicated and infinity recursion
    if node.id in visit: return W
    # add current node to visit
    visit.add(node.id)
    # compute the DF local
    immediateSuccessor = compDom1.getAllImmediateSuccessor(graph, node, idToIndicatorGraph)
    for successor in immediateSuccessor:
        if dom[node.indicator - 1][successor.indicator - 1] == 1:
            immediateSSuccessor = compDom1.getAllImmediateSuccessor(graph, successor, idToIndicatorGraph)
            for ssuccessor in immediateSSuccessor:
                if dom[node.indicator - 1][ssuccessor.indicator - 1] == 0 and ssuccessor.id not in currentWValue:
                    W.append(ssuccessor)
                    nodeW.append(ssuccessor)
                    currentWValue.append(ssuccessor.id)
    printDF(node, nodeW)
    nodeW = []
    # compute the DF up
    for child in immediateSuccessor:
        S = DF(graph, child, idToIndicatorGraph, dom, visit, currentWValue, W)
        for nodeD in S:
            # combine DF local and up together
            if (dom[node.indicator - 1][nodeD.indicator - 1] == 0 and nodeD.id not in currentWValue):
                nodeW.append(nodeD)
                W.append(nodeD)
                currentWValue.append(nodeD.id)
        printDF(node, nodeW)
    return W

def justifyResult(W, graph, dom, idToIndicatorGraph, nodeList):
    listResult = []
    listW = []
    for w in W:
        listW.append(w.id)
    for node in nodeList:
        for n in nodeList:
            # check condition 1, does node not strictly dominate w
            if n.indicator != node.indicator and dom[node.indicator - 1][n.indicator - 1] == 0:
                # check condition 2, node dominate one of a predecessor of n
                # get all the immediate predecessor of the current node n
                allImmediatePredecessor = compDom1.getAllImmediatePredecessors(graph, n, idToIndicatorGraph) 
                for predecessor in allImmediatePredecessor:
                    # satisfied condition 2, then break
                    if node.indicator != predecessor.indicator and n.id not in listResult and dom[node.indicator - 1][predecessor.indicator - 1] == 1:
                        listResult.append(n.id)
                        break
    # pass all the condition, return True
    if sorted(listW) == sorted(listResult):
        print('Correct dominance frontier!')
        print(f'The dominate frontier: {listW}')
    else:
        print(f'Wrong dominance frontier, your output is {listW}, correct output should be {listResult}.')

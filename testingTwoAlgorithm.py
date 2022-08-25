import compDom1
import compDom2
import testingDominator
import randomGraph
from copy import deepcopy
if __name__ == '__main__':
    graph = randomGraph.generateGraph(100, root = 1, splitRate = 0.5, connectRate = 0.5) 
    print(f'The input graph is {graph}')
    ENTER = list(graph.keys())[0]
    idList = testingDominator.findId(graph, ENTER)
    idToIndicatorGraph = testingDominator.assignIdIndicator(graph, idList)
    print(f'idToIndicatorGraph is {idToIndicatorGraph}')
    newGraph = testingDominator.changeGraphToNumFormat(graph, idToIndicatorGraph)
    print(f'The newGraph with ascending order list is {newGraph}')
    print('-'*30)
    path = testingDominator.dfsJustifyGraph(newGraph, 1)
    print(f'The path for given graph is: {path}')
    if testingDominator.justifyGraph(newGraph, path):
        dom1 = compDom1.createDom(newGraph)
        nodeList = compDom1.getAllNodes(newGraph, idToIndicatorGraph)
        compDom1.CompDom(newGraph, nodeList[0], dom1, idToIndicatorGraph)
        testingDominator.printInfor(newGraph, dom1, nodeList)
        resultDomGraph = testingDominator.changeToDomGraph(newGraph, dom1, idToIndicatorGraph)
        print('-'*30)
        visit = compDom2.getAllLinkedNodesList(newGraph, idToIndicatorGraph)
        dom2 = compDom2.initialDom(newGraph, visit)
        curr = deepcopy(visit).head 
        while curr:
            compDom2.CompDom(newGraph, curr, dom2, visit, idToIndicatorGraph)
            curr = curr.next
        twoDimMatrix = compDom2.printDom(newGraph, dom2)
        print('-'*30)
        resultDomGraph, numGraph = testingDominator.changeToDomGraph(newGraph, twoDimMatrix, idToIndicatorGraph)
        print('-'*30)
        print('Algorithm1 dom:')
        print(dom1)
        testDom = testingDominator.testingDom(dom1, newGraph)
        testingDominator.testByNewDom(dom1, newGraph)
        print('-'*30)
        print('Algorithm2 dom:')
        print(twoDimMatrix)
        testingDominator.testingDom(twoDimMatrix, newGraph)
        testingDominator.testByNewDom(twoDimMatrix, newGraph)
        print('-'*30)
    print(f'Compare two dom from two algorithms: {(dom1 == twoDimMatrix).all()}')
    print(f'numGraph: {numGraph}')
    print(f'resultDomGraph: {resultDomGraph}')
    testingDominator.checkResultList(newGraph, numGraph, idToIndicatorGraph)
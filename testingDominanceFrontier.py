import dominanceFrontier as df
import compDom1
import compDom2
import randomGraph
if __name__ == '__main__':
    # graph = randomGraph.generateGraph(100, root = 1, splitRate = 0.5, connectRate = 0.5)
    graph = {0:[1,10], 1:[2,3,7,10],2:[4,5,7],3:[6,10],4:[7],5:[8],6:[9],7:[],8:[],9:[],10:[]}
    ENTER = list(graph.keys())[0]
    idList = compDom1.findId(graph, ENTER)
    idToIndicatorGraph = compDom1.assignIdIndicator(graph, idList)
    print(f'idToIndicatorGraph is {idToIndicatorGraph}')
    newGraph = compDom1.changeGraphToNumFormat(graph, idToIndicatorGraph)
    print(f'newGraph is {newGraph}')
    dom = compDom1.createDom(newGraph)
    nodeList = compDom1.getAllNodes(newGraph, idToIndicatorGraph)
    print('-'*30)
    path = compDom1.dfsJustifyGraph(newGraph, 1)
    print(f'The path for given graph is: {path}')
    if compDom1.justifyGraph(newGraph, path):
        compDom1.CompDom(newGraph, nodeList[0], dom, idToIndicatorGraph)
        dom = compDom1.CompDomSupport(newGraph, dom)
        compDom1.printInfor(newGraph, dom, nodeList)
        resultDomGraph = compDom1.changeToDomGraph(newGraph, dom, idToIndicatorGraph)
        print('-'*30)
        compDom1.testingDom(dom, newGraph)
        compDom1.testByNewDom(dom, newGraph)
        print('*'*30)
        node = nodeList[0]
        W = df.DF(newGraph, node, idToIndicatorGraph, dom, visit = set(), currentWValue = [], W = [])
        listW = []
        for w in W:
            listW.append(w.id)
        listW = sorted(listW)
        df.justifyResult(W, newGraph, dom, idToIndicatorGraph, nodeList)
from pygraphviz import *
import sys
import os

def generateDotFile(content, fname, index):
	dot = AGraph()
	nodes = []
	edges = []

	for x in content:
		firstNode, secondNode = x.split('>')[0], x.split('>')[1]
		firstIndex, secondIndex = firstNode.split(':')[0], secondNode.split(':')[0]
		nodeToEdge = firstNode.split('&')[1]
		nodeToEdgeLabel = nodeToEdge.split('@')[0]
		nodes.append(firstNode)
		nodes.append(secondNode)
		edges.append((firstIndex, secondIndex, nodeToEdgeLabel))

	firstNode = (nodes[0].split('&'))[0]
	labelTemp = firstNode[firstNode.find("(")+1:firstNode.find(")")]
	labels = labelTemp.split(',')
	getNames = input("Enter the variable names for the graph number " + str(index) + " seperated by comma: ")
	labelNames = getNames.split(',')

	for tempNode in nodes:
		temp = tempNode.split(':')
		secondTemp = (temp[1].split('&'))[0]
		forLabels = secondTemp[secondTemp.find("(")+1:secondTemp.find(")")]
		forLabelsList = forLabels.split(',')
		labelText = 'State number: ' + temp[0] + '\n'
		for i in range(len(forLabelsList)):
			labelText =  labelText + labelNames[i] + '=' + forLabelsList[i] + ', '

		probString = secondTemp[secondTemp.find("[")+1:secondTemp.find("]")]
		probInt = [round(float(x), 3) for x in probString.split(',')]
		labelText = labelText + '\n' + str(probInt)
		dot.add_node(temp[0], label=labelText)

	for tempEdge in edges:
		tempEdgeLabel = tempEdge[2]
		fixPoint = round(float(tempEdgeLabel.split('/')[1]), 3)
		edgeLabel = tempEdgeLabel.split('/')[0] + '/' + str(fixPoint)
		dot.add_edge(tempEdge[0], tempEdge[1],label=edgeLabel)

	dot.layout(prog='dot')
	dot.write(path = directoryName + '%s'%('/' if directoryName != '' else '') + fname + '.gv')
	dot.draw(path = directoryName + '%s'%('/' if directoryName != '' else '') + fname + '.gv.pdf')

directoryName = input("Enter directory name (blank if current): ")

if (directoryName != ''):
	os.mkdir(directoryName)

for i in range(1, len(sys.argv)):
	content = ''
	fname= sys.argv[i]

	with open(fname) as f:
		content = f.readlines()
	content = [x.strip() for x in content]
	content = [x.replace(" ", "") for x in content]
	generateDotFile(content, fname, i)

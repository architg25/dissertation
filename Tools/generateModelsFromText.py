import sys
import os
import generateModelBase

fname= sys.argv[1]

with open(fname) as f:
    content = f.readlines()
content = [x.strip() for x in content]
content = [x.replace(" ", "") for x in content]

directory = input("Enter directory name (blank if current): ")

if (directory != ''):
	os.mkdir(directory)
	os.chdir(directory)

data = []
for x in content:
	temp = x.split('=')
	data.append((temp[0], temp[1]))
	
dataDict = dict(data)
	
numberOfModels = int(dataDict["numberOfModels"])
modelName = dataDict["model"]	
numberOfBandits = dataDict["numberOfBandits"].split(',')
probabilities = []
fileNames = dataDict["fileNames"].split(',')

def getProbabilities(modelNumber):
	probModel = 'probModel' + str(modelNumber)
	tempProbabilities = dataDict[probModel].split('],')
	probabilities = []
	for x in tempProbabilities:
		x = x.replace('[', "")
		x = x.replace(']', "")
		probabilities.append(x)
		
	banditData = ''
	for x in probabilities:
			bandit = probabilities.index(x)
			banditNumber = str(bandit+1)
			banditData += '\n\nmodule bandit' + banditNumber
			banditVariable = 'b' + banditNumber
			banditData += '\n\n\t' + banditVariable + ' : [0..1];'
			probability = x.split(',')
			banditData += '\n\t[initial] true -> 0.5 : (' + banditVariable + '\'=0) + 0.5 : (' + banditVariable + '\'=1);'
			banditData += '\n\t[a1] ' + banditVariable + '=0 -> ' + probability[0] + ':(' + banditVariable + '\'=0) + ' + probability[1] + ':(' + banditVariable + '\'=1);'
			banditData += '\n\t[a1] ' + banditVariable + '=1 -> ' + probability[2] + ':(' + banditVariable + '\'=0) + ' + probability[3] + ':(' + banditVariable + '\'=1);'
			banditData += '\n\nendmodule'
		
	return banditData
	
for x in range(numberOfModels):
	generateModelBase.generateModels(modelName, int(numberOfBandits[x]), getProbabilities(x), fileNames[x])
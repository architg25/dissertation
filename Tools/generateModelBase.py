def getProbabilities(noOfbandits):
	banditData = ''
	for bandit in range(noOfbandits):
			banditNumber = str(bandit+1)
			banditData += '\n\nmodule bandit' + banditNumber
			banditVariable = 'b' + banditNumber
			banditData += '\n\n\t' + banditVariable + ' : [0..1];'
			probabilities = input("Enter probabilities for " + banditVariable + "(0->0), (0->1), (1->0), (1->1): ").split(',')
			banditData += '\n\t[initial] true -> 0.5 : (' + banditVariable + '\'=0) + 0.5 : (' + banditVariable + '\'=1);'
			banditData += '\n\t[a1] ' + banditVariable + '=0 -> ' + probabilities[0] + ':(' + banditVariable + '\'=0) + ' + probabilities[1] + ':(' + banditVariable + '\'=1);'
			banditData += '\n\t[a1] ' + banditVariable + '=1 -> ' + probabilities[2] + ':(' + banditVariable + '\'=0) + ' + probabilities[3] + ':(' + banditVariable + '\'=1);'
			banditData += '\n\nendmodule'
	return banditData
	
def getFileName():
	fname = input("Enter the file name to be saved: ")
	return fname
	
def generateModels(modelName, noOfbandits, getProbFunction, fileNameFunction):
		fileData = modelName
		if(modelName == 'pomdp'):
			observables = '\n\nobservables \n\ts, turn, k'
			for number in range(noOfbandits):
				observables += ', v' + str(number+1)
			fileData += observables + '\n\nendobservables'

		banditData = getProbFunction
		fileData += banditData

		scheduler = '\n\nmodule scheduler \n\n\ts : [0..' + str(noOfbandits) + '];\n\tturn : [-1..1];'
		for bandit in range(noOfbandits):
			banditNumber = str(bandit+1)
			if(modelName=='pomdp'):
				observeVariable = 'v' + banditNumber
				scheduler += '\n\t' + observeVariable + ' : [0..1];'
		scheduler += '\n\t[initial] turn=-1 -> (turn\'=0); \n\t[a1] turn=0 -> (turn\'=1);'
		
		if(modelName=='dtmc'):
			scheduler += '\n\t[choose] turn=1 -> 1/' + str(noOfbandits) + ':(s\'=1)&(turn\'=0)'
			for bandit in range(1,noOfbandits):
				banditNumber = str(bandit+1)
				scheduler += ' + 1/' + str(noOfbandits) + ':(s\'=' + banditNumber + ')&(turn\'=0)'
			scheduler += ';'
		
		elif(modelName=='mdp'):
			banditNumber = str(bandit+1)
			banditVariable = 'b' + banditNumber
			scheduler += '\n\t[choose' + banditNumber + '] turn=1 -> (s\'=' + banditNumber + ')&(turn\'=0);'
		
		else:
			for bandit in range(noOfbandits):
				banditNumber = str(bandit+1)
				banditVariable = 'b' + banditNumber
				observeVariable = 'v' + banditNumber
				scheduler += '\n\t[choose' + banditNumber + '] turn=1 -> (s\'=' + banditNumber + ')&(turn\'=0)&(' + observeVariable +'\'=' + banditVariable + ');'
		
		scheduler += '\n\nendmodule'
		fileData += scheduler
	
		counter = '\n\nconst int kmax; \n\nmodule counter \n\n\tk : [0..kmax+1];\n\t[a1] k<kmax -> true;'
		if(modelName=='dtmc'):
			counter += '\n\t[choose] k<kmax -> (k\'=min(kmax,k+1));'
			
		else:	
			for bandit in range(noOfbandits):
				banditNumber = str(bandit+1)
				counter += '\n\t[choose'+ banditNumber +'] k<kmax -> (k\'=min(kmax,k+1));'
				
		counter += '\n\t[] k=kmax -> (k\'=k+1);\n\nendmodule'
		fileData += counter

		rewards = '\n\nrewards "correct_guess"\n'
		for bandit in range(noOfbandits):
			banditNumber = str(bandit+1)
			banditVariable = 'b' + banditNumber
			rewards += '\n\tturn=0 & s=' + banditNumber + ' & ' + banditVariable + '=1 : 1;'
		rewards += '\n\nendrewards'
		fileData += rewards

		fname = fileNameFunction
		with open(fname, 'w') as filehandle:
			filehandle.write(fileData)
	
import generateModelBase as gmb
import os

directory = input("Enter directory name (blank if current): ")
if (directory != ''):
	os.mkdir(directory)
	os.chdir(directory)

numberOfBandits = int(input("Enter how many bandits: "))
probs = gmb.getProbabilities(numberOfBandits)

for x in (['dtmc','']):
	gmb.generateModels(model, numberOfBandits, gmb.getProbabilities(numberOfBandits), gmb.getFileName())

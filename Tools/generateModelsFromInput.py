import generateModelBase as gmb
import os

directory = input("Enter directory name (blank if current): ")
if (directory != ''):
	os.mkdir(directory)
	os.chdir(directory)

multipleFiles = int(input("Enter how many models would you like to generate? "))
for x in range(multipleFiles):
	model = input("Enter model name: ")
	numberOfBandits = int(input("Enter how many bandits: "))
	gmb.generateModels(model, numberOfBandits, gmb.getProbabilities(numberOfBandits), gmb.getFileName())
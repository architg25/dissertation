import matplotlib.pyplot as plt
import sys, os, math

dtmc = []
mdp = []
pomdp = []
k = []

def generateDotFile(content, i):
    del(content[0])
    for x in content:
        temp = x.split('\t')
        temp[0] , temp[1] = float(temp[0]), float(temp[1])
        if i == 1:
            k.append(temp[0])
            dtmc.append(temp[1])
        elif i == 2:
            mdp.append(temp[1])
        else:
            pomdp.append(temp[1])


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
        generateDotFile(content, i)

plt.plot(k, dtmc, color='g',)
plt.plot(k, mdp, color='orange')
plt.plot(k, pomdp, color='b')

for var in (dtmc, mdp, pomdp):
    plt.annotate('%0.2f' % max(var), xy=(1, max(var)), xytext=(8, 0),
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

plt.gca().legend(('DTMC','MDP','POMDP'))
plt.ylim(0, math.ceil(max(mdp)) + 1)
plt.xlabel('k iterations')
plt.ylabel('Rewards')

plt.grid()
fileName = input("Enter file name: ")
plt.savefig(fileName)

import datetime
import glob
import ntpath
import os
import sys

import matplotlib.pyplot as plt


#move files to test directory
files = glob.glob('../Environment/RealEnvironment/StepsVsGoal_Task*.txt')
newPath = '../Environment/RealEnvironment/FilesGoalVsSteps/'

for filename in files:
    newFilename = ntpath.basename(filename) + '_' + str(datetime.datetime.now())+ ".txt"
    os.rename(filename, newPath + newFilename)
    

# open and plot all files in test directory
files = glob.glob(newPath + '*.txt')

fig, ax1 = plt.subplots()

for filename in files:
    try:
        print "trying to open: ", filename
        f = open(filename, 'rb')
        lines = f.readlines()
        splitInto = lines[0].strip().count(";") + 1
        data = [line.strip().split(";",splitInto) for line in lines]
        f.close()
    except:
        print "Could not open file: ", filename
        sys.exit()
     
    # xLst, yLst = zip(*data)
    x = [float(d[0]) for d in data]
    y1 = [float(d[1]) for d in data]

    ax1.plot(x, y1, '-')
     
    if splitInto > 2:
        y2 = [float(d[2]) for d in data]
        ax2 = ax1.twinx()
        ax2.plot(x, y2, 'r-')
  
#plt.scatter(x, y)
ax1.legend([ntpath.basename(f) for f in files],loc='best')
plt.show()
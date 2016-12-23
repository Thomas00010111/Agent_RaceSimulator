import sys

import matplotlib.pyplot as plt


# f = open('StepsVsGoal.txt', 'rb')
# lines = f.readlines()
# splitInto = lines[0].strip().count(";") + 1
# data = [line.strip().split(";",splitInto) for line in lines]
# f.close()
# 
# print data
# #add a plot
# y = [float(y)+10 for y in yLst] 
# plt.scatter(x, y)
filename = 'StepsVsGoal_Task2.txt'
try:
    f = open(filename, 'rb')
    lines = f.readlines()
    splitInto = lines[0].strip().count(";") + 1
    data = [line.strip().split(";",splitInto) for line in lines]
    f.close()
except:
    print "Could not open file: ", filename
    sys.exit()
    
print data

# xLst, yLst = zip(*data)
x = [float(d[0]) for d in data]
y1 = [float(d[1]) for d in data]
fig, ax1 = plt.subplots()
ax1.plot(x, y1, 'b-')

if splitInto > 2:
    y2 = [float(d[2]) for d in data]
    ax2 = ax1.twinx()
    ax2.plot(x, y2, 'r-')
 
#plt.scatter(x, y)
plt.show()
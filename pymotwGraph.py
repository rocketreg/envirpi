#!/usr/bin/python
# http://pymotw.com/2/csv/

import glob
import os
import csv
import sys
import matplotlib.pyplot as plt

# Get csv column number given column header tag
def getColumn(row, colId):
    cell = 0
    Col = 0
    while cell < len(row):
        if row[cell] == colId:
            Col = cell
        cell += 1
    return Col

# Convert Datetime format to seconds elapsed this year
def timeToInt(t):
    if int(t[:2])%4 == 0:  # Leap year
        months = [31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        months = [31,28,31,30,31,30,31,31,30,31,30,31]
    # Sum of previous months this year
    monthSum = 0
    monthCount = 0
    while monthCount < int(t[3:5])-1:
        monthSum += months[monthCount]
        monthCount += 1
    tInt = (monthSum*86400)+(86400*(int(t[6:8])-1))+(3600*int(t[9:11]))+(60*int(t[12:14]))+ int(t[15:17])
    return tInt

rowLen = 0
yCol = 0
xaxis = 'tmpr'
chId = 'ch1'
sensorId = '0'
chNum = 0
sensNum = 0
listTime = []
listWatts = []


input_path = '/home/steve/EnviR/joiner/tojoin'
outputFile = open('energy.csv', 'a')

fileCounter = 0
for inputFile in sorted(glob.glob(os.path.join(input_path,'*.csv'))):

    f = open(inputFile, 'rt')
    try:
        reader = csv.reader(f)

        if fileCounter < 1:
            for row in reader:
                if row[0] == 'time':
                    rowLen = len(row)
                    chNum = getColumn(row, chId)
                    sensNum = getColumn(row, 'sensor')
                    print 'chNum',chNum,'sensNum',sensNum
                if rowLen == len(row):
                    if row[sensNum] == sensorId:
                    #    print timeToInt(row[0]),row[chNum]
                        listTime.append(str(timeToInt(row[0])))
                        listWatts.append(row[chNum])
        else:
            header = next(reader,None)
            for row in reader:
                if rowLen == len(row):
                    if row[sensNum] == sensorId:
                     #   print timeToInt(row[0]),row[chNum]
                        listTime.append(str(timeToInt(row[0])))
                        listWatts.append(row[chNum])

    finally:
        f.close()
        
    fileCounter += 1
xMax = max(listTime)
yMax = max(listWatts)
plt.plot(listTime, listWatts)
plt.show()

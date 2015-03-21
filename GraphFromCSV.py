#!/usr/bin/python
import matplotlib.pyplot as plt

csvObj = open("energy.csv", 'r')

# Convert hr:min:sec string to seconds as integer
def timeToInt(t):
    tInt = (3600*int(t[:2]))+(60*int(t[3:5]))+ int(t[6:8])
 #   print tInt
    return tInt

channel = raw_input("channel? ")

#gPlot = open("usage.csv", 'a')

tagList = ["time","tmpr","sensor","id","type", "watts", "focus"]
dictOfValues = {}

listTime = []
listWatts = []

line = 0
while 1:
    reading = csvObj.readline()
    if not reading:       # detect end of file
        break
    commas = 0
    j = 0
    l = 0
    while j < len(reading):
        if reading[j] == ',':
            val = reading[l:j]
            dictOfValues[tagList[commas]] = val
            l = j+1
            commas += 1
        j+=1
    if line == 0:
        xOffset = timeToInt(dictOfValues['time'])
    if dictOfValues['sensor'] == channel:
        listTime.append((timeToInt(dictOfValues['time'])-xOffset))
        listWatts.append(dictOfValues['watts'])
    line += 1

xMax = max(listTime)
yMax = max(listWatts)
plt.plot(listTime, listWatts)
plt.show()

#gPlot.close()
csvObj.close()


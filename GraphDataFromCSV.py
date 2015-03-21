#!/usr/bin/python

csvObj = open("energy.csv", 'r')

def timeToInt(t):
    tInt = (3600*int(t[:2]))+(60*int(t[3:5]))+ int(t[6:8])
    return tInt

channel = raw_input("channel? ")

tagList = ["time","tmpr","sensor","id","type", "watts", "focus"]
dictOfValues = {}
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
        tStr = dictOfValues['time']
        print (timeToInt(tStr)-xOffset),':', int(dictOfValues['watts']);
    line += 1
#print 'line',line
csvObj.close()


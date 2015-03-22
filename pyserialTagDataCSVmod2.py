#!/usr/bin/python

import serial, time
import datetime
ser = serial.Serial()

#------ Extract data from a line of XML ------------
def extractData(readstr):
    n = 0
    while n < len(readstr):
        # get start of tag in readstr
        if readstr[n] == "<":  
            tagStart = n
        # get length of tagName
        if readstr[n] == ">":
            tagLen = n - tagStart
            # Trim <> from tagName
            tagName = readstr[tagStart+1:-(len(readstr)-n)]
            # Register current string position '>' with tagName
            dictOfTags[tagName] = n
            # Is this a closing tag?
            if tagName[0] == "/":
                # mark end of data substring
                dataEnd = tagStart
                # recall start point of data substring
                # and remove '/' from tagName
                dataStart = dictOfTags[tagName[1:]]+1;
                dataStr = readstr[dataStart:-(len(readstr)-dataEnd)]
                if dataStr[0] == "<":
                    break
                dictOfData[tagName[1:]] = dataStr
                print dataStr
        n+=1
    return dataStr
            
#------

ser.port = "/dev/ttyUSB0"

#ser.port = "/dev/ttyS2"

ser.baudrate = 57600

ser.bytesize = serial.EIGHTBITS #number of bits per bytes

ser.parity = serial.PARITY_NONE #set parity check: no parity

ser.stopbits = serial.STOPBITS_ONE #number of stop bits

ser.timeout = None          #block read

ser.xonxoff = False     #disable software flow control

ser.rtscts = False     #disable hardware (RTS/CTS) flow control

ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control

ser.writeTimeout = 2     #timeout for write
def openCsv():
    #----- Create CSV file with start time as title ----------
    titleStr = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")# + "\n"
    fileObj = open(titleStr + '.csv' , 'a')
    return fileObj
    #----- 

minuteCount = 0
while minuteCount<3:

    try: 

        ser.open()

    except Exception, e:

        print "error open serial port: " + str(e)

        exit()

    tagList = ["time","tmpr","sensor","id","type", "watts", "focus"]

    if ser.isOpen():

        try:

            ser.flushInput() #flush input buffer, discarding all its contents

            ser.flushOutput()#flush output buffer, aborting current output 

                 #and discard all that is in buffer
        
            numOfLines = 0
            # set length of CSV file to close on turn of minute
            now = datetime.datetime.now().strftime("%M")
            print datetime.datetime.now(), "waiting for time out"
            later = now # initialise later
            csvObj = openCsv()
            #print "CSVOBJ=", csvObj
            while int(now) == int(later):
                #test for stop signal - todo
                later = datetime.datetime.now().strftime("%M")

                response = ser.readline()

                readStr = ""+response # a line of xml data
            
                tagLen = 0
                tagTally = 0
                dictOfTags = {} #Make a tag dictionary
                dictOfData = {} #Make a data dictionary
                for ti in tagList:
                    dictOfData[ti] = " "
                extractData(readStr)

                record = ""
                for tn in tagList:
                    record += dictOfData[tn] + ","
                recordStr = record + datetime.datetime.now().strftime("%y-%m-%d-%H-%M") + "\n"  # lose final comma
                print recordStr
                csvObj.write(recordStr)

                numOfLines += 1

            ser.close()
            csvObj.close()
            print "Name of the file: ", csvObj.name
            print "Closed or not : ", csvObj.closed
    #       print "Opening mode : ", fileObj.mode
    #       print "Softspace flag : ", fileObj.softspace

        except Exception, e1:

            print "error communicating...: " + str(e1)

    else:

        print "cannot open serial port "

    minuteCount += 1

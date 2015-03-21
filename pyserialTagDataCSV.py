#!/usr/bin/python

import serial, time

#initialization and open the port

#possible timeout values:

#    1. None: wait forever, block call

#    2. 0: non-blocking mode, return immediately

#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()

#ser.port = "/dev/ttyUSB0"

ser.port = "/dev/ttyUSB0"

#ser.port = "/dev/ttyS2"

ser.baudrate = 57600

ser.bytesize = serial.EIGHTBITS #number of bits per bytes

ser.parity = serial.PARITY_NONE #set parity check: no parity

ser.stopbits = serial.STOPBITS_ONE #number of stop bits

ser.timeout = None          #block read

#ser.timeout = 1            #non-block read

#ser.timeout = 2              #timeout block read

ser.xonxoff = False     #disable software flow control

ser.rtscts = False     #disable hardware (RTS/CTS) flow control

ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control

ser.writeTimeout = 2     #timeout for write

try: 

    ser.open()

except Exception, e:

    print "error open serial port: " + str(e)

    exit()
fileObj = open("energy.csv", 'a')
tagList = ["time","tmpr","sensor","id","type", "watts", "focus"]
title = ""
for tn in tagList:
    title += tn + ","
titleStr = title[:-1] + "\n"
print titleStr
#fileObj.write(titleStr)

if ser.isOpen():

    try:

        ser.flushInput() #flush input buffer, discarding all its contents

        ser.flushOutput()#flush output buffer, aborting current output 

                 #and discard all that is in buffer
        
        numOfLines = 0
        while True:

            response = ser.readline()

            readstr = ""+response
#            print readstr
            n = 0
            tagLen = 0
            tagTally = 0
            dictOfTags = {} #Make a tag dictionary
            dictOfData = {} #Make a data dictionary
            for ti in tagList:
                dictOfData[ti] = " "
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

            record = ""
            for tn in tagList:
        #        if dictOfData[tn] == " ":
        #            continue
                record += dictOfData[tn] + ","
            recordStr = record[:-1] + "\n"  # lose final comma
            print recordStr
            fileObj.write(recordStr)


            numOfLines += 1
            #print "\n";

            if (numOfLines >= 30):

                break

        ser.close()
        fileObj.close()
    #    print "Name of the file: ", fileObj.name
        print "Closed or not : ", fileObj.closed
     #   print "Opening mode : ", fileObj.mode
      #  print "Softspace flag : ", fileObj.softspace

    except Exception, e1:

        print "error communicating...: " + str(e1)

else:

    print "cannot open serial port "

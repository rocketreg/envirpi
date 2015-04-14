#!/usr/bin/python
# Introducing rank to distinguish xml layers
# todo - link ch1 and ch2 in rank 1 to data in rank 3

import serial, time
import datetime
import smtplib
import mimetypes
import string
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

def sendmail(csvName):
    emailfrom = "env1rdata@gmail.com"
    emailto = "env1rdata@gmail.com"
    fileToSend = csvName
    username = "env1rdata"
    password = "currentCost"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Energy data by email"
    msg.preamble = "Here's the CSV file"

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
    
ser = serial.Serial()

#------ Extract Tags from a line of XML ------------
def extractTags(readstr):
    charNum = 0
    tList = []
    while charNum < len(readstr):
        # get start of tag in readstr
        if readstr[charNum] == "<":
            tagStart = charNum
        # get length of tagName
        if readstr[charNum] == ">":
            tagLen = charNum - tagStart
            # Trim <> from tagName
            tagName = readstr[tagStart:-(len(readstr)-(charNum+1))]
            tList.append(tagName)
        charNum += 1
    return tList            

#---Establish Tag ranking--------------------------
                
def ranking(tagList):                
    rank = 0
    rankList = []
    tagNum = 0
    while tagNum < len(tagList):
        if tagList[tagNum][0] == '<' and tagList[tagNum][1] != '/':
            rank += 1
            rankList.append(rank)
        if tagList[tagNum][:2] == '</':
            rank -= 1
            rankList.append(rank)
                        
        tagNum += 1
    return rankList
                
#----------------------------------------------                


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
    titleStr = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")# + "\n"
    fileObj = open(titleStr + '.csv' , 'a')
    return fileObj
    #----- 

minuteCount = 0
while 1:

    try: 

        ser.open()

    except Exception, e:

        print "error open serial port: " + str(e)

        exit()

    tagList = []

    if ser.isOpen():

        try:

            ser.flushInput() #flush input buffer, discarding all its contents

            ser.flushOutput()#flush output buffer, aborting current output 

                 #and discard all that is in buffer
        
            numOfLines = 0
            # set length of CSV file to close on turn of minute
            now = datetime.datetime.now().strftime("%H")
            print datetime.datetime.now(), "waiting for time out"
            later = now # initialise later
            csvObj = openCsv()
            csvHeader = 'time,tmpr,sensor,ch1,ch2\n'
            csvObj.write(csvHeader)
            while int(now) == int(later):
                #test for stop signal - todo
                later = datetime.datetime.now().strftime("%H")
                # Fetch a line of XML
                response = ser.readline()
                tagRank = {} #Create dictionary for tags and ranks
                tagList = extractTags(response) #Fetch tags from response
                
                #print tagList

                # extract data from tagList using response
                rankList = ranking(tagList)
                tNum = 0
                record = []
                tagData = {} #Create dictionary for tags and data
                csvList = []
                # make time the first column
                csvList.append(datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S"))
                while tNum < len(tagList):
                    # Get rank of opening tag
                    if rankList[tNum] == 2 and tagList[tNum][1] != '/':
                        #Get start point of data
                        dataStart = response.find(tagList[tNum]) + len(tagList[tNum])
                        #Get end of block bounded by matching closing tag
                        dataEnd = response.find('</'+tagList[tNum][1:])
                        dataStr = response[dataStart:dataEnd];
                        #Is data held by redundant tags
                        if dataStr[0] != '<':
                            tagData[tagList[tNum]] = dataStr
                            #print 'tagData[tagList[tNum]]', tagData[tagList[tNum]]
                        else:
                            # strip tags from dataStr
                            dc = 0
                            while dc < len(dataStr):
                                dStart = dataStr.find('>', 1)+1
                                dEnd = dataStr.find('</')
                                tagData[tagList[tNum]] = dataStr[dStart:dEnd]
                                    
                                dc += 1
                    tNum += 1
                    
                #Print tagData dictionary
                for key in tagData:
                    print key, tagData[key],':',
                
                #Create user-interface to select tags to include in CSV flie !!!

                csvTags = ['<tmpr>','<sensor>','<ch1>','<ch2>']
                col = 0
                while col < len(csvTags):
                    if csvTags[col] in tagData: # if selected
                        csvList.append(',')
                        csvList.append(tagData[csvTags[col]])
                    else:
                        csvList.append('') # a blank cell
                        
                    col += 1
                csvList.append('\n')

                csvLine = ''.join(csvList)
                print 'csvLine=', csvLine
    
                csvObj.write(csvLine)
                print '---------------------';
     
                numOfLines += 1

            ser.close()
            csvObj.close() #csv file is completed
            try:
                sendmail(csvObj.name)
            except Exception:
                print "Error: unable to send email"
            
            print "Name of the file: ", csvObj.name
            print "Closed or not : ", csvObj.closed
    #       print "Opening mode : ", fileObj.mode
    #       print "Softspace flag : ", fileObj.softspace

        except Exception, e1:

            print "error communicating...: " + str(e1)

    else:

        print "cannot open serial port "


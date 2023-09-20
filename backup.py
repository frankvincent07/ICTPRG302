#!/usr/bin/python3

import os 
import math
import sys
from backupcfg import jobs, backupDir, backupLog, smtp
from datetime import datetime 

import smtplib
import pathlib
import shutil

def writeLogMessage(logMessage, dateTimeStamp, isSuccess):
    try:
        file = open(backupLog, "a")
        
        if isSuccess:
            file.write(f"SUCCESS {dateTimeStamp} {logMessage}\n")
        else:
            file.write(f"FAILURE {dateTimeStamp} {logMessage}\n")
            
        file.close()
            
       
        
        
    except FileNotFoundError:
        print("ERROR: File does not exist.")
    except IOError:
        print("ERROR: File is not accessible.")
        
def errorHandler(errorMessage, dateTimeStamp):
    print(errorMessage) 
    writeLogMessage(errorMessage, dateTimeStamp, False)
    sendEmail(errorMessage)
    

    
# append all error messages to email and send
def sendEmail(message):

    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject: Backup Error\n\n' + message + '\n'

    # connect to email server and send email
    try:
        smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(smtp["user"], smtp["password"])
        smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
        smtp_server.close()
    except Exception as e:
        print("ERROR: An error occurred.")
    
    
    
def main():
    try:
        dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S") 
        
        """ i imported smtplib and entered lines 48-50
        
        """
        argCount = len(sys.argv)
        
        if argCount < 2:
            errorHandler("ERROR: job not specified",  dateTimeStamp)     
        else:
            #jobName = sys.argv[1]
            for jobName in sys.argv[1:]:
                if not jobName in jobs:
                    errorHandler(f"ERROR: job {jobName} is not in job list", dateTimeStamp)
                else:        
                    jobsPath=jobs[jobName]
                   
                    if not os.path.exists(jobsPath):
                        errorHandler("ERROR: file " + jobsPath + " does not exist.", dateTimeStamp)
                    else:
                        Destination = backupDir  
          
                        if not os.path.exists(Destination):
            
                            errorHandler("ERROR: Dir" + (Destination) + "does not exist", dateTimeStamp)
                        else:
                            
                            srcPath = pathlib.PurePath(jobsPath)
                            dstLoc = Destination + "/" + srcPath.name + "-" + dateTimeStamp
                            
                            if pathlib.Path(jobsPath).is_dir():
                               shutil.copytree(jobsPath, dstLoc) 
                            else:    
                                shutil.copy2(jobsPath, dstLoc)
                            
                            writeLogMessage(f"Backed up {jobsPath} to {dstLoc}", dateTimeStamp, True)    
                               # if file = open("dir1/file1.txt", "a")
                                
                                # connect to email server and send email
                        """    try:
                                smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
                                smtp_server.ehlo()
                                smtp_server.starttls()
                                smtp_server.ehlo()
                                smtp_server.login(smtp["user"], smtp["password"])
                                smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
                                smtp_server.close()
                                except Exception as e:
                                print("ERROR: An error occurred.")
                
                                
                                
                        
                                
                              #  if smtplib = {"sender": "30024901@students.sunitafe.edu.au",
                              #  "recipient": "etrichvfrank@gmail.com",
                              #  "server": "smtp.gmail.com", "port": 587,
                             """  
                               
                             
                        
                    
    except:
        print("ERROR: general error occured.")
                    
if __name__ == '__main__':
     main()
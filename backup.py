#!/usr/bin/python3
""" always enter the shebang 
program: backup.py
Author: frank etrich
Version: 1.0
Copyright 2023 frank etrich
Program to Backup sequence of one or more files and/or directories.
"""
import os 
import math
import sys
from backupcfg import jobs, backupDir, backupLog, smtp
from datetime import datetime 

import smtplib
import pathlib
import shutil

def writeLogMessage(logMessage, dateTimeStamp, isSuccess):
    """ write the log message to the backup.log file. With TimeDateStamp
    and outcome Success/Failure
    
    Arguments
    
    logMessage - string - message to be written to the file
    dateTimeStamp  string -current date time stamp to be written to the file
    isSuccess -Boolean true if success else false
    """
    try:
        file = open(backupLog, "a")
        # send message of outcome SUCCESS/FAILURE, include datetimestamp, logfile
        if isSuccess:
            file.write(f"SUCCESS {dateTimeStamp} {logMessage}\n")
        else:
            file.write(f"FAILURE {dateTimeStamp} {logMessage}\n")
            
        file.close()
            
       
        
        
    except FileNotFoundError:
        print("ERROR: File does not exist.")
    except IOError:
        print("ERROR: File is not accessible.")
    # sends error message    
def errorHandler(errorMessage, dateTimeStamp):
    print(errorMessage) 
    writeLogMessage(errorMessage, dateTimeStamp, False)
    sendEmail(errorMessage)
    # 

    
# append all error messages to email and send
def sendEmail(message):
    """send an email to and account
    
    Arguments
    
    message string email message
    """
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
    """ perform backups for one or more jobs specified on the command line.
    The file or directory to be backed up for a job is specified in the backup.
    """
    try:
        dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S") 
        
        argCount = len(sys.argv)
        # check at least one CLI argument
        if argCount < 2:
            errorHandler("ERROR: job not specified",  dateTimeStamp)     
        else:
            
            for jobName in sys.argv[1:]:
                #check for valid job name in directory
               
                if not jobName in jobs:
                    errorHandler(f"ERROR: job {jobName} is not in job list", dateTimeStamp)
                else:        
                    jobsPath=jobs[jobName]
                    #check source is a valid file/directory
                    if not os.path.exists(jobsPath):
                        errorHandler("ERROR: file " + jobsPath + " does not exist.", dateTimeStamp)
                    else:
                        Destination = backupDir  
                        # check Destination is valid
                        if not os.path.exists(Destination):
            
                            errorHandler("ERROR: Dir" + (Destination) + "does not exist", dateTimeStamp)
                        else:
                            
                            srcPath = pathlib.PurePath(jobsPath)
                            dstLoc = Destination + "/" + srcPath.name + "-" + dateTimeStamp
                            
                            #copys file/ directory to a backup directory
                            if pathlib.Path(jobsPath).is_dir():
                               shutil.copytree(jobsPath, dstLoc) 
                            else:    
                                shutil.copy2(jobsPath, dstLoc)
                            
                            writeLogMessage(f"Backed up {jobsPath} to {dstLoc}", dateTimeStamp, True)    

                    
    except:
        print("ERROR: general error occured.")
                    
if __name__ == '__main__':
     main()
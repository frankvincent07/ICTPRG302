#!/usr/bin/python3

import os 
import math
import sys
from backupcfg import jobs, backupDir
from datetime import datetime

import pathlib
import shutil
def main():
    try:
        argCount = len(sys.argv)
        
        if argCount != 2:
            print("ERROR: job not specified")     
        else:
            jobName = sys.argv[1]
            if not jobName in jobs:
                print(f"ERROR: job {job} is not in job list")
            else:        
                jobsPath=jobs[jobName]
               
                if not os.path.exists(jobsPath):
                    print("ERROR: file " + jobsPath + " does not exist.")
                else:
                    Destination = backupDir  
      
                    if not os.path.exists(Destination):
        
                        print("ERROR: Dir" + (Destination) + "does not exist")
                    else:
                        dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                        srcPath = pathlib.PurePath(jobsPath)
                        dstLoc = Destination + "/" + srcPath.name + "-" + dateTimeStamp
                        
                        if pathlib.Path(jobsPath).is_dir():
                           shutil.copytree(jobsPath, dstLoc) 
                        else:    
                             shutil.copy2(jobsPath, dstLoc)
                             
                        pass
                    
    except:
        print("ERROR: general error occured.")
                    
if __name__ == '__main__':
     main()
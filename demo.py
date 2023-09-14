#!/usr/bin/python3

n = int(input("Enter a number"))


v = 1
while v < n+1:
    print("The number is "+ str(v)+" its spuare is "+ str(v*v)+ " and its cube is "+ str (v**3))
    
    v += 1
    
   #!/usr/bin/python3

import math#!/usr/bin/python3

import sys

def main():
    """
    This Python code demonstrates the following features:
    
    * accessing command line arguments.
    
    """
    try:
        argCount = len(sys.argv)
        program = sys.argv[0]
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        
        print("The program name is " + program + ".")
        print("The number of command line items is " + str(argCount) + ".")
        print("Command line argument 1 is " + arg1 + ".")
        print("Command line argument 2 is " + arg2 + ".")
        
    except:
        print("ERROR: An error occurred.")
    
if __name__ == "__main__":
    main()
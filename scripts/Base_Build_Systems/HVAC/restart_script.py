
#################################-- restart Script --#################################
## This section tries for arduino connection on a specified port                    ##
######################################################################################


#! /bin/env python3
import os
import sys

def like_cheese():
    var = input("Hi! I like cheese! Do you like cheese?").lower()
    if var == "yes":
        print("That's awesome!")

if __name__ == '__main__':
    like_cheese()
    os.execv(__file__, sys.argv)  # Run a new iteration of the current script, providing any command line args from the current iteration.

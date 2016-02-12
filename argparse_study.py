import sys

if len(sys.argv) > 1:
    print ("~ Script: " + sys.argv[0])
    # print ("~ Arg   : " + sys.argv[1])
    print "~ args :"
    print " \n".join(sys.argv[1:])
else:
    print (" No arguments")

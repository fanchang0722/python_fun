import argparse

parser = argparse.ArgumentParser(description='Demo')
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help='verbose flag')
parser.add_argument('filename')
parser.add_argument('parameter')

args = parser.parse_args()

print "~ Filename: {}".format(args.filename)
print "~ Parameter: {}".format(args.parameter)
if args.verbose:
    print ("~ Verbose!")
# else:
#     print ("~ Not so verbose!")

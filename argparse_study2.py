import argparse

parser = argparse.ArgumentParser(description='Demo')
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help='verbose flag')
parser.add_argument('--filename')
parser.add_argument('--nums', nargs=2)
parser.add_argument('--limit', default=5, type=int)

args = parser.parse_args()

print "~ Filename: {}".format(args.filename)
print "~ Nums: {}".format(args.nums)
print "~ Limit: {}".format(args.limit)
if args.verbose:
    print ("~ Verbose!")
# else:
#     print ("~ Not so verbose!")

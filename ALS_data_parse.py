#!/anaconda/bin/python
import json

fp = open(r'/Users/fanchang/Downloads/results-20170718-161548.json', 'r')
count = 0
for line in fp:
	line = json.loads(line)
	count += 1
	if line['serialNumbers']:
		if line['serialNumbers'][0]['value']:
			if len(line['arguments']) > 15:
				# if line['arguments'][11]['value']:
				# if line['arguments'][13]['value']:
				# if line['arguments'][11]['value']:
				# if line['arguments'][13]['value']:
				print '{:>4}, {}, {}, {}'.format(count, line['serialNumbers'][0]['value'], line['arguments'][11]['value'],
				                                 line['arguments'][13]['value'])
# for element in line['arguments']:
#    print element
# print line.keys()

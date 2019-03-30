import os

folder = r'/Users/fanchang/Downloads/a50_fatp2/temp'

fout = open('a50_fatp2_stat.csv', 'w')

for filename in os.listdir(folder):
	if filename.endswith('csv'):
		print filename
		fp = open(os.path.join(folder, filename), 'r')
		fp.readline()
		lines = fp.readline()
		fout.writelines(lines)
		fp.close()

fout.close()

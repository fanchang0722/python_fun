# outputFile = r'/Users/fanchang/Download/fanchang'
fp = open(r'/Users/fanchang/Downloads/fanchang', 'w')
temp=''
for index in range(10):
    temp += str(index)+','

print temp
fp.write(temp)
fp.close()

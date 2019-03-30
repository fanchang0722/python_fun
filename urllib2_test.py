import urllib2
try:
    response=urllib2.urlopen('http://lauw0.mtv.corp.google.com:13373/api/md5?serial_number=6520018801BPRXNANA16150158')
    data = response.read()
    print "NVM filename is %s" % data.split(',')[0].split(':')[1]
    print "NVM checksum is %s" % data.split(',')[1].split(':')[1].rstrip('}')
except urllib2.HTTPError:
    print 'No such NVM file to download'
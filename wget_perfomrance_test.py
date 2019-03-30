import time
import urllib2
import subprocess
import hashlib


def timeo(fun, n=1000):
    def void():
        pass

    start = time.clock()

    for i in range(n):
        void()

    stend = time.clock()
    overhead = stend-start

    start = time.clock()
    for i in range(n):
        fun()

    stend = time.clock()
    thetime = stend-start
    return fun.__name__, thetime-overhead


def urlget_function(project, SID, destination):
    response = urllib2.urlopen([r'http://lauw0.mtv.corp.google.com:13373/api/files?project=', project, ';name=', SID])
    data = response.read()
    with open(destination, 'wb') as fp:
        fp.write(data)


def subprcess_function():
    subprocess.check_output(['wget', '-O', 'final_otp.nvm',
                             r'http://lauw0.mtv.corp.google.com:13373/api/files?project=indigo;name=final_otp.nvm'])


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as fp:
        for chunk in iter(lambda: fp.read(1024), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))


if __name__ == '__main__':
    # for f in urlget_function, subprcess_function:
    #     print "%s: %.2f\n" % timeo(f, 1)

    # destination = r'/Users/fanchang/Downloads/google-python-exercises/basic/test.ovm'
    # urlget_function('indigo', 'final_opt.nvm', destination)
    string1 = md5(r'/Users/fanchang/Downloads/google-python-exercises/basic/test.ovm')
    subprcess_function()
    # string2 = md5(r'/Users/fanchang/Downloads/google-python-exercises/basic/list1.py')
    string2 = md5(r'/Users/fanchang/Downloads/google-python-exercises/basic/final_otp.nvm')
    # print string1
    # print string2
    test(string1, string2)
    # while True:
    #     try:
    #         print string1 == string2
    #         break
    #     except ValueError:
    #         print "Checksum fail.  Try upload file again..."


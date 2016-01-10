print range(0, 30, 5)
print 1.0/complex(1,2)
dict1=\
    {'jack': 4098, 'sjoerd': 4127} #or {4098: 'jack', 4127: 'sjoerd'}
print dict1

# from contextlib import closing
# import urllib
#
# with closing(urllib.urlopen('http://www.python.org')) as page:
#     for line in page:
#         print line

# import contextlib
# import time

# @contextlib.contextmanager
# def time_print(task_name):
#     t = time.time()
#     try:
#         yield
#     finally:
#         print task_name, "took", time.time() - t, "seconds."
#
# with time_print("processes"):
#     [doproc() for _ in range(500)]
#
# # processes took 15.236166954 seconds.
#
# with time_print("threads"):
#     [dothread() for _ in range(500)]

# class Mgr(object):
#     def __enter__(self): pass
#     def __exit__(self, ext, exv, trb):
#         if ext is not None: print "no not possible"
#         print "OK I caught you"
#         return True
#
# with Mgr():
#     name='rubicon'/2 #to raise an exception


# from contextlib import contextmanager
# @contextmanager
# def handler():
#     # Put here what would ordinarily go in the `__enter__` method
#     # In this case, there's nothing to do
#     print 1
#     try:
#         yield
#         # print 3
#         # print "I am here"
#         # yield # You can return something if you want, that gets picked up in the 'as'
#     except Exception as e:
#         print 4
#         print "no not possible"
#     finally:
#         print 5
#         print "Ok I caught you"

# with handler():
#     print 2
#     name='rubicon'/2 #to raise an exception


with open('temp.txt', 'w') as f:
    f.write("Hi!")


from contextlib import contextmanager
@contextmanager
def single_use():
    print("Before")
    # pass
    yield
    print("After")

cm = single_use()
with cm:
    print 'test start'

# import logging
# import time
# # loggingimport auxiliary_module
#
# # create logger with 'spam_application'
# logger = logging.getLogger('spam_application')
# logger.setLevel(logging.DEBUG)
# # create file handler which logs even debug messages
# fh = logging.FileHandler('spam.log')
# fh.setLevel(logging.DEBUG)
# # create console handler with a higher log level
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
# # create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
# # add the handlers to the logger
# logger.addHandler(fh)
# logger.addHandler(ch)
#
# logger.info('creating an instance of auxiliary_module.Auxiliary')
# # a = auxiliary_module.Auxiliary()
# logger.info('created an instance of auxiliary_module.Auxiliary')
# logger.info('calling auxiliary_module.Auxiliary.do_something')
# # a.do_something()
# logger.info('finished auxiliary_module.Auxiliary.do_something')
# logger.info('calling auxiliary_module.some_function()')
# # auxiliary_module.some_function()
# logger.info('done with auxiliary_module.some_function()')

import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')

# import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
fh2 = logging.FileHandler('spam2.log')
fh2.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh2.setFormatter(formatter)
logger.addHandler(fh2)
logger.info('Start reading database')
# read database here

records = {'john': 55, 'tom': 66}
logger.debug('Records: %s', records)
logger.info('Updating records ...')
# update records here

logger.info('Finish updating records')
import threading
import time

def do_this():
	global x
	while (x < 300):
		x += 1
		pass
	print x
	# time.sleep(5)

def do_after():
	global x
	while (x < 600):
		x += 1
		pass
	print x

def main():
	'''
	global x
	x = 0
	
	our_thread = threading.Thread(target=do_this, name='myname')
	our_thread.start()
	print our_thread.ident
	our_thread.join()
	our_thread2 = threading.Thread(target=do_after, name='myname2')
	our_thread2.start()
	print our_thread2.ident
	'''
	main_thread= threading.enumerate()[0]
	print main_thread.isDaemon() 

if __name__ == "__main__":
	main()
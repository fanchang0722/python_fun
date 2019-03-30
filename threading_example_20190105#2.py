import threading
import time

def do_this():
	global dead
	print "This is our thread!"
	x = 0
	while (not dead):
		x += 1
		pass
	print x
	# time.sleep(5)
 
def main():
	global dead
	dead = False
	our_thread = threading.Thread(target=do_this, name='myname')
	our_thread.start()
	print threading.active_count()
	print threading.enumerate()
	print threading.current_thread()
	print our_thread.is_alive()
	raw_input("Hit enter to quit")
	dead = True
	raw_input("Hit enter to quit")
	print our_thread.is_alive()

	

if __name__ == "__main__":
	main()
#  Copyright 2014 Google Inc. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import threading
import time

exitFlag = 0


class MyThread(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		print "Starting " + self.name
		print_time(self.name, self.counter, 1)
		print "Exiting " + self.name


def print_time(threadName, counter, delay):
	while counter:
		if exitFlag:
			threadName.exit()
		time.sleep(delay)
		print "%s: %s" % (threadName, time.ctime(time.time()))
		counter -= 1
		# print counter
		# print '\n'


# Create new threads
thread1 = MyThread(1, "Thread-1", 3)
thread2 = MyThread(2, "Thread-2", 6)

# Start new Threads
thread1.start()
thread2.start()

print "Exiting Main Thread"

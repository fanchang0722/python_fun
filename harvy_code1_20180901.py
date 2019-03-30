import numpy as np


def gcd(in1, in2):
	if in1 < in2:
		in1, in2 = in2, in1
	temp = in1 % in2
	if temp == 0:
		return 0
	if temp == 1:
		return 1
	if temp > 1:
		in1, in2 = in2, temp
		return gcd(in1, in2)


count = 1
for a in np.arange(1, 101, 1):
	for b in np.arange(1, 101, 1):
		if b >= a:
			if np.sqrt(a**2+b**2).is_integer() and np.sqrt(a**2+b**2) < 100:
				if gcd(a, b):
					print([count,  a, b, np.sqrt(a**2+b**2)])
					count += 1

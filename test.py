from kodemon import kodemon
import time
import threading
import random

@kodemon
def test1():
	pass

@kodemon
def test2():
	time.sleep(random.choice(range(2)))

@kodemon(smack=5.0)
def test3():
	pass

def tests():
	i = 0
	while i < 5:
		test1()
		test2()
		test3()
		i += 1
	
if __name__ == '__main__':
	tests()
		
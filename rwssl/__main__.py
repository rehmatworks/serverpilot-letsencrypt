import sys
if sys.version_info < (3, 5):
    sys.exit('Error: rwssl only works in Python 3.x.')

from rwssl.rwssl import *
if __name__ == '__main__':
	main()

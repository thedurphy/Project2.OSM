import string
import logging
import sys

def mapper():
	
	for line in sys.stdin:
		
		data = line.strip().split(',')
        if len(data) != 22 or data[1] == 'UNIT':
            continue

        out = "{0}\t{1}\t{2}\t{3}".format(data[1], data[6], data[2], data[3])
        print out


mapper()
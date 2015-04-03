import sys
import logging


def reducer():

	def format_key(fog, rain):
		return '{}fog-{}rain'.format(
			'' if fog else 'no',
			'' if rain else 'no'
		)

	riders = 0
	num_hours = 0
	last_key = None

	for line in sys.stdin:
		data = line.strip().split("\t")
		if len(data) != 2:
			continue
		this_unit, count = data

		if last_key and last_key != this_unit:
			print '{0}\t{1}'.format(last_key, (riders/float(num_hours)))
			riders = 0

		last_key = this_unit
		riders += float(count)
		num_hours += 1

	if last_key != None:
		print '{0}\t{1}'.format(last_key, (riders/float(num_hours)))
reducer()


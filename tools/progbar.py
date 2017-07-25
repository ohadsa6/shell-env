#!/usr/bin/python

import sys

class Progress_bar(object):
	def __init__(self, units_full):
		self.stdout_len = 100
		self.units_full = units_full
		self.units_done = 0
		self.printed_bars = 0;
		print '|{}|'.format('-' * self.stdout_len)
		sys.stdout.write('|')

	def refresh(self, inc):
		if (inc < 0):
			print 'progress backwards- exit'
			exit(1)

		self.units_done += inc
		if (self.units_done == self.units_full):
			finalize = True
			add = self.stdout_len - self.printed_bars
		else:
			finalize = False
			add = int((100 * self.units_done) / self.units_full) - self.printed_bars
		for i in xrange(add):
			sys.stdout.write('=')

		if (finalize):
			sys.stdout.write('|')
			print ''
			print 'Complete'
		self.printed_bars += add
		sys.stdout.flush()

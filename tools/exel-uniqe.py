#!/usr/bin/python
import sys
import getopt
import time
import hashlib
import time
import bisect
import toolz
import xlwt
from xlrd import open_workbook
		
class Entry(object):
	def __init__(self, fields):
		self.id = fields[0]
		self.jnul = fields[1]
		self.bar_sys = fields[2]
		self.notes = ''.join(fields[3:])

	def __cmp__(self, other):
		return cmp(self.jnul, other.jnul)

	def __eq__(self, other):
		return self.jnul == other.jnul
		
	def print_line(self, fd):
		line = '{},{},{},{}\n'.format(self.id, self.jnul, self.bar_sys, self.notes)
		fd.write(line)

def main(argv):
	book = xlwt.Workbook(encoding="utf-8")
	sheet1 = book.add_sheet("Sheet 1")
	
	bookdup = xlwt.Workbook(encoding="utf-8")
	dupsheet1 = bookdup.add_sheet("DupSheet 1")
	
	
	jn_array = []
	wb = open_workbook(argv[0])
	for sheet in wb.sheets():
		number_of_rows = sheet.nrows
		number_of_columns = sheet.ncols
	
	last_jnul = 0.0
	new_row = 0
	dup_row = 0
	full_rows = 0
	for row in range(1, number_of_rows):
		full_rows += 1
		jnul = sheet.cell(row, 1).value
		id = sheet.cell(row, 0).value		
		bar_sys = sheet.cell(row, 2).value
		notes = sheet.cell(row, 3).value
		if type(jnul) is not float:
			continue
		jn = float(jnul)
		if jn in jn_array:
			dupsheet1.write(dup_row, 0, id)
			dupsheet1.write(dup_row, 1, jnul)
			dupsheet1.write(dup_row, 2, bar_sys)
			dupsheet1.write(dup_row, 3, notes)
			dup_row += 1
		else:
			sheet1.write(new_row, 0, id)
			sheet1.write(new_row, 1, jnul)
			sheet1.write(new_row, 2, bar_sys)
			sheet1.write(new_row, 3, notes)
			new_row += 1
			jn_array.append(jn)

		#extract fields
		#id = sheet.cell(row, 1).value		
		#bar_sys = sheet.cell(row, 3).value
		#notes = sheet.cell(row, 4).value
		#dc1 = sheet.cell(row, 5).value
		#dc2 = sheet.cell(row, 6).value
		
		#write values to new sheet
		#sheet1.write(new_row, 0, id)
		#sheet1.write(new_row, 1, jnul)
		#sheet1.write(new_row, 2, bar_sys)
		#sheet1.write(new_row, 3, notes)
		#sheet1.write(new_row, 4, dc1)
		#sheet1.write(new_row, 5, dc2)
		
		#modify
		#new_row += 1
			
	print 'full: {}, rd: {} dup: {}'.format(full_rows, new_row, dup_row)
	book.save("remove-dups.xls")
	bookdup.save("only-dups.xls")

if __name__ == "__main__":
    main(sys.argv[1:])

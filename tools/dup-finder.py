#!/usr/bin/python

from sys import argv
import os
import sys
import bisect
import re
import getopt
import filecmp
from progbar import Progress_bar

def print_err(msg, *params):
    msg += '\n'
    sys.stderr.write(msg.format(*params))
		
class File(object):
	def __init__(self, name, size):
		self.size = size
		self.name = name
		
	def is_size_eq(self, other):
		return self.size == other.size

	def __cmp__(self, other):
		return cmp(self.size, other.size)

	def __eq__(self, other):
		return filecmp.cmp(self.name, other.name)

def group_match_operation(group):
	global state_handler
	
	state_handler.duplicate_groups.append(g)
	print 'File group'
	for i in group:
		print '    {}'.format(i)
	print '----------------------------------------------------'
	print ''
    
def group_find_dup():
	global state_handler

	while len(state_handler.filesize_group) > 1:
		anchor = state_handler.filesize_group[0]
		match_list = [anchor]
		del_idx = [0]
		for idx, i in enumerate(state_handler.filesize_group[1:]):
			if filecmp.cmp(anchor, i) == True:
				match_list.append(i)
				del_idx.append(idx)
		# check if we got matches
		if len(del_idx) > 1:
			group_match_operation(match_list)
		state_handler.filesize_group = [v for i, v in enumerate(state_handler.filesize_group) if i not in del_idx]

def handle_file(sfile):
	global state_handler
	global progbar
	
	# group files by byte size
	if sfile.is_size(state_handler.last_byte_size):
		# in case of match size- add to size group
		state_handler.filesize_group.append(file_name)
		# change state to MATCH
		state_handler.state_update(StateHandler.MATCH)
	else:
		# check if match sequence ends
		if state_handler.state == StateHandler.MATCH:
			group_find_dup()
		state_handler.filesize_group = [file_name]
		state_handler.state_update(StateHandler.IDLE)
			
	state_handler.last_file_name = file_name
	
	g_former_file_name = file_name
	state_handler.last_byte_size = size

def sizeof_fmt(num, suffix='B'):
	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)

#get number of lines in file
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def help():
	print '''
Usage: ./dupf.py SORTED_FILES_FILE
Finds files duplication in directories
Options:
	-h        Prints this help and exit
'''
	sys.exit(2)

class MatchGroup(object):
	def __init__(self, size, files):
		self.size = size;
		self.files = files

class DuplicateFinder(object):
	STATE_IDLE, STATE_MATCH, STATE_MAX = range(3)
	def __init__(self, dir1, dir2):
		#create zero-length file object
		zero_file = '/tmp/zero-file'
		fd = open(zero_file, 'w')
		fd.close()
		zero_file_obj = File(zero_file, 0)
		
		self.files = []
		
		#create sorted File objects list
		for path, subdirs, files in os.walk(dir1):
			for name in files:
				f = os.path.join(path, name)
				sz = os.path.getsize(f)
				bisect.insort(self.files, File(f, sz))
		
		#create sorted File objects list
		for path, subdirs, files in os.walk(dir2):
			for name in files:
				f = os.path.join(path, name)
				sz = os.path.getsize(f)
				bisect.insort(self.files, File(f, sz))

		self.progbar = Progress_bar(len(self.files))
		
		self.last_file = zero_file_obj
		self.state = DuplicateFinder.STATE_IDLE
		self.filesize_group = [zero_file_obj]
		self.duplicate_groups = []
		
		#statistics
		self.stat_grp_num = 0
		self.stat_redundant_files = 0
		self.stat_redundant_byte_size = 0
		
		#operation flags
		self.flag_delete_dups = False
		self.flag_prefix = False
		self.prefix_str = ''
		
	def handle_binary_match_group(self, bm_group):
		size = bm_group[0].size
		flist = [v.name for v in bm_group]
		self.duplicate_groups.append(MatchGroup(size, flist))
		
		#update statistics
		self.stat_grp_num += 1
		rfiles = len(flist) - 1
		self.stat_redundant_files += rfiles
		self.stat_redundant_byte_size += rfiles * size
	
	def dups_in_sizegroup(self):
		while len(self.filesize_group) > 1:
			anchor = self.filesize_group[0]
			match_list = [anchor]
			del_idx = [0]
			for idx, i in enumerate(self.filesize_group[1:]):
				if anchor == i:
					match_list.append(i)
					del_idx.append(idx)
			# check if we got matches
			if len(del_idx) > 1:
				self.handle_binary_match_group(match_list)
			self.filesize_group = [v for i, v in enumerate(self.filesize_group) if i not in del_idx]
		
	def handle_file_object(self, f):
		# group files by byte size
		if f.is_size_eq(self.last_file):
			# in case of match size- add to size group
			self.filesize_group.append(f)
			# change state to MATCH
			self.state = DuplicateFinder.STATE_MATCH
		else:
			# check if match sequence ends
			if self.state == DuplicateFinder.STATE_MATCH:
				self.dups_in_sizegroup()
			self.filesize_group = [f]
			self.state == DuplicateFinder.STATE_IDLE
				
		self.last_file = f
		
	def print_match_groups(self):
		for mg in self.duplicate_groups:
			print 'File Group ({})'.format(mg.size)
			for f in mg.files:
				print '    {}'.format(f)
			print '----------------------------------------------------'
		
	def delete_groups_dups(self):
		for mg in self.duplicate_groups:
			for f in mg.files[1:]:
				print 'delete -{}-'.format(f)
				sys.stdout.flush()
				os.remove(f)
		
	def delete_prefix(self):
		for mg in self.duplicate_groups:
			idx = next((i for i, v in enumerate(mg.files) if not v.startswith(self.prefix_str)), -1)
			if idx == -1:
				return
			#swap indexes so the first will be preserved
			mg.files[0], mg.files[idx] = mg.files[idx], mg.files[0]
			for f in mg.files[1:]:
				if f.startswith(self.prefix_str):
					print 'delete -{}-'.format(f)
					sys.stdout.flush()
					os.remove(f)

	def delete_prefix_verify(self):
		for mg in self.duplicate_groups:
			if mg.files[0].startswith(self.prefix_str):
				return
			for f in mg.files[1:]:
				if f.startswith(self.prefix_str) and os.path.isfile(f):
					print 'DeleteError -{}-'.format(f)
		
		
	def print_statistics(self):
		print 'Number of Match Groups: {}'.format(self.stat_grp_num)
		print 'Number of Redundant Files: {}'.format(self.stat_redundant_files)
		print 'Number of Redundant Sapce: {}'.format(sizeof_fmt(self.stat_redundant_byte_size))
		
	def execute(self):
		for f in self.files:
			#advance the progress bar
			self.progbar.refresh(1)
			#handle current file
			self.handle_file_object(f)
		self.print_match_groups()
		self.print_statistics()
		if self.flag_delete_dups == True:
			if self.flag_prefix == True:
				self.delete_prefix()
				self.delete_prefix_verify()
			else:
				self.delete_groups_dups()

def help():
	print '''Usage: dup-finder.py <DIRECTORY1> <DIRECTORY2> [OPTIONS]

Finds binary same files on both directories
    Options:
        -h:    get the help menu and exit
        -d:    delete redundant files
        -p:    supply path prefix. only files whos prefix matches
               the supplied one could be deleted'''
	exit(1)

# Get arguments from user and send to log parser
def main(argv):
	delete_duplicate = False
	prefix_flag = False
	try:
		opts, args = getopt.getopt(argv, "hdp:")
	except getopt.GetoptError:
		help()

	for opt, arg in opts:
		if opt == '-h':
			help()
		if opt == '-d':
			delete_duplicate = True
		if opt == '-p':
			prefix_flag = True
			prefix = arg
			
	
	if len(args) != 2:
		help()
	dir1  = args[0]
	dir2  = args[1]
	dup_finder = DuplicateFinder(dir1, dir2)
	if delete_duplicate:
		dup_finder.flag_delete_dups = True
	if prefix_flag:
		dup_finder.flag_prefix = True
		dup_finder.prefix_str = prefix
	dup_finder.execute()
	

if __name__ == "__main__":
	main(sys.argv[1:])

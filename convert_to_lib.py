import re
import os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='''Convert .dll to .lib
	Warning!
	You need dumpexport.exe and lib.exe tools from msvc or something else. 

	''')

parser.add_argument('filename', help = 'Name of dll file.')

args = parser.parse_args()

filename = args.filename
filename_noext = os.path.splitext(filename)[0]

if len(os.path.splitext(filename)[1]) < 1:
	filename = filename + ".dll"


def _check_is_valid_file(str):
	if os.path.isfile(str):
		if os.path.splitext(str)[1] == ".dll":
			return True
		else:
			print "error: passed not a dll"

	return False

def _extract_imports(out):
	return re.findall("(\d+)\s+[\dA-F]+\s+[0-9A-F]+\s+([^\s]+)",out)

def _process_lib(filename_def):
	if os.path.isfile(filename_def):
		print(filename_noext)
		os.system("lib /DEF:%s /OUT:%s" % (filename_def, os.path.abspath(filename_noext + '.lib')))

		proc = subprocess.Popen( ['lib', '/DEF:%s' % os.path.abspath(filename_def), '/OUT:%s' % os.path.abspath(filename_noext + '.lib')] )
		(out, error) = proc.communicate()
		print out
	else:
		print "error: no such filename %s" % filename_def

if _check_is_valid_file(filename):
	proc = subprocess.Popen(['dumpbin', '/exports', filename], stdout=subprocess.PIPE, shell=True)
	(out, error) = proc.communicate()
	filename_def = filename_noext + ".def"
	list = _extract_imports(out)
	with open(filename_def, "w") as f:
		f.write('EXPORTS\n')
		for obj in list:
			f.write(obj[1] + "\n")

		_process_lib(filename_def)


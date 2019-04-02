#!/usr/lib/python
'''
usage: python runMonophy.py

Lucy Tran
Department of Ecology and Evolutionary Biology
University of Michigan, Ann Arbor
Written June 11, 2010
'''


import subprocess as sp
import glob
import re

gtfname_re = re.compile(r'(.*?ind)')

for file in glob.iglob('*ind'):
	gtfsearch = gtfname_re.findall(file)
	gtfilename = gtfsearch[0]
	filename_re = re.compile(r'(.*?)_[A-Z]_[0-9]*?ind')
	filesearch = filename_re.findall(gtfilename)
	filename = filesearch[0]
	cmd = 'python monophy.py %s %s.node %s.split' % (gtfilename,filename,filename)
	process = sp.Popen(cmd, shell = True)
	process.wait()
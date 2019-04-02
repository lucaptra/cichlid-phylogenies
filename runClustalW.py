#!/usr/bin/python
'''
usage: python runClustalW.py

Lucy Tran
Department of Ecology and Evolutionary Biology
University of Michigan, Ann Arbor
April 17, 2010 (modified May 3, 2010)
'''

import subprocess as sp
import glob
import re

filename_re = re.compile(r'(.*?).fasta')	#compile regex to search for gene names in fasta file names

#for all fasta files in working directory, run ClustalW2 to align sequences
for infileName in glob.iglob('*_2.fasta'):
	search = filename_re.findall(infileName)
	filename = search[0]
	cmd = './clustalw2 -infile=%s -align -type=DNA -outorder=input -outfile=%sa.fasta -output=fasta' % (infileName,filename)
	process = sp.Popen(cmd, shell = True)
	process.wait()
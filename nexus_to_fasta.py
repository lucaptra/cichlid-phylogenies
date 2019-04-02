#!/usr/bin/python
'''
usage: python nexus_to_fasta.py

Run script in directory of nexus files to convert. Need text file of species names separated from corresponding sequences by tab.

E.g.,
Canis familiaris\tACTG...\n
Felis catus\tACTG...\n
Mus musculus\tACTG...

Lucy Tran
Department of Ecology and Evolutionary Biology
University of Michigan, Ann Arbor
May 3, 2010
'''

import glob
import re

for file in glob.iglob('*.fasta'):
	openfile = open(file, 'r')
	text = openfile.readlines()
	filename_re = re.compile(r'(.*?).fasta')
	search = filename_re.findall(file)
	filename = search[0]
	openfile.close()
	speciesname_re = re.compile(r'(.*?)\r')
	seq_re = re.compile(r'\r([a-zA-Z]*?(?:\n|$))')
	newitemlist = []
	for item in text:
		item2 = item.replace('\t','\r')
		speciesname = speciesname_re.findall(item2)
		seq = seq_re.findall(item2)
		seq2 = seq[0].replace('\n','\r')
		newitem = '>' + speciesname[0] + '\r' + seq2
		newitemlist.append(newitem)
	newtext = ''.join(newitemlist)
	template = '%s_2.fasta'
	outfilename = template % (filename)
	outfile = open(outfilename, 'w')
	outfile.write(newtext.encode('utf-8'))
	outfile.close()
	print 'File writing complete!'
#!/usr/bin/python
'''
usage: python fasta_to_nexus.py

Run script in directory of fasta files to convert. Creates text file of species names separated from corresponding sequences by tab.

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

for x in glob.iglob('*_2a.fasta'):
	infile = x
	outfilename_re = re.compile(r'(.*?)_2a.fasta')
	outfilename = outfilename_re.findall(x)
	outfilename2 = outfilename[0]
	file = open(infile, 'r')
	text = file.readlines()
	text2 = ''.join(text)
	file.close()
	#compile regular expressions to search for headers and sequences
	header_re = re.compile(r'(>.*?)\n(?:-|[A-Z]{10})')
	seq_re = re.compile(r'>[a-zA-Z0-9_]*?\n([A-Z\n\-]{10,60000})')
	header = header_re.findall(text2)
	seq = seq_re.findall(text2)
	#construct list of corresponding headers and sequences
	headseqlist = []
	for i in range(len(header)):
		headeritem = header[i]
		seqitem = seq[i]
		seqitem2 = seqitem.replace('\n','')
		headseq = headeritem + '\t' + seqitem2 + '\n'
		headseqlist.append(headseq)
	#print nexus file
	newtext = ''.join(headseqlist)
	template = '%s_2a.nex'
	outfilename3 = template % (outfilename2)
	outfile = open(outfilename3, 'w')
	outfile.write(newtext.encode('utf-8'))
	print 'Fasta file writing complete!'
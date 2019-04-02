#!/usr/bin/python
'''
usage: python readSeq.py infile outfilename

e.g., python readSeq.py Nagl_et_al._2000_Fig3_NJ_2.fasta Nagl_et_al._2000_Fig3_NJ

Compare sequences to standard sequence, replacing nucleotide placemarker (e.g., '-') with nucleotide present in standard and keeping segregating nucleotide.

Lucy Tran
Department of Ecology and Evolutionary Biology
University of Michigan, Ann Arbor
May 3, 2010
'''

import sys
import re

infile = sys.argv[1]
outfilename = sys.argv[2]
file = open(infile, 'r')
text = file.readlines()
text2 = ''.join(text)
file.close()

#compile regular expressions to search for headers and sequences
header_re = re.compile(r'(>.*?)\n')
seq_re = re.compile(r'>[a-zA-Z0-9_]*?\n([A-Z\n\-*]{10,60000})')
header = header_re.findall(text2)
seq = seq_re.findall(text2)

#construct list of corresponding headers and sequences
firstseq = seq[0].strip()
headerlist = []
seqlist = []
for i in range(1,len(header)):
	headeritem = header[i]
	headerlist.append(headeritem)
	seqitem = seq[i]
	seqitem2 = seqitem.replace('\n','')
	seqlist.append(seqitem2)

charlist = []
for sequence in seqlist:
	for i in range(len(firstseq)):
		if sequence[i] == '-':
			newchar = firstseq[i]
		else: newchar = sequence[i]
		charlist.append(newchar)
charlist2 = ''.join(charlist)

newseqfirst = charlist2[0:len(firstseq)]
newseqlist = [firstseq, newseqfirst]
for i in range(1,len(header)-1):
	newseq = charlist2[len(firstseq)*i:len(firstseq)+len(firstseq)*i]
	newseqlist.append(newseq)

headseqlist = []
for i in range(len(header)):
	header2 = header[i]
	seq2 = newseqlist[i]
	newseq2 = seq2.replace('*','-')
	headseq = header2 + '\t' + newseq2 + '\n'
	headseqlist.append(headseq)

#print nexus file
newtext = ''.join(headseqlist)
template = '%s_2a.nex'
outfilename2 = template % (outfilename)
outfile = open(outfilename2, 'w')
outfile.write(newtext.encode('utf-8'))
print 'Fasta file writing complete!'
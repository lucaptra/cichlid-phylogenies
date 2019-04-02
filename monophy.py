#!/usr/bin/python
'''
usage: python monophy.py gtfilename nodefilename splitfilename

e.g., python monophy.py Booton1999_con_sp1_L_5ind Booton1999_con_sp1.node Booton1999_con_sp1.split

Lucy Tran
Department of Ecology and Evolutionary Biology
University of Michigan, Ann Arbor
Written June 9, 2010
'''

import sys
import re

gtfilename = sys.argv[1]
nodefilename = sys.argv[2]
splitfilename = sys.argv[3]

gtfile = open(gtfilename,'r')
nodefile = open(nodefilename,'r')
splitfile = open(splitfilename,'r')

gt = gtfile.readlines()
sp = nodefile.read()
split = splitfile.readlines()

gtfile.close()
nodefile.close()
splitfile.close()

#find taxa in clades of zero node depth
keep_re = re.compile(r'(?:^|\n)([a-zA-Z.]*?),')	#first taxon in clade of zero node depth
discard_re = re.compile(r',([a-zA-Z.]*?)(?:,\t\||,[a-zA-Z.]*?,\t\|)')	#other taxa in clade of zero node depth
keeplist = []
discardlist = []
for line in split:
	if '\t0\n' in line:
		keep = keep_re.findall(line)
		discard = discard_re.findall(line)
		keeplist.append(keep[0])
		for i in range(len(discard)):
			discardlist.append(discard[i])

#find number and name of each taxon
spnum_re = re.compile(r'(?:^|\n)([0-9]*?)\s')
spname_re = re.compile(r'[0-9]*?\s([A-Za-z\.0-9]*?)\s[0-9.]*?\n')
spnum = spnum_re.findall(sp)
spname = spname_re.findall(sp)

spdict = {}
for i in range(len(spnum)):
	spdict[spname[i]] = spnum[i]

#remove taxa other than first one in clades of zero node depth from dictionary
for item in discardlist:
	del spdict[item]

spdictvals = spdict.values()	#species numbers of remaining taxa

headerlist = [str(len(spname))]
for i in range(len(spname)):
	spnameheader = spname[i]
	headerlist.append(spnameheader)
header = '\t'.join(headerlist)

gtlist = [header]
for i in range(len(gt)):
	gtree = gt[i]
	gtnum = str(i+1)
	gtrow = ['None'] * (len(spnum) + 1)	#species denoted by 'None' are those that belong to clades of zero node depth and which are ignored
	gtrow[0] = str(i+1)
	for val in spdictvals:
		findsp_re = re.compile(r'(?:\(|,)(%s)(?:\:|_[0-9]*?\:)' % (val))
		findsp = findsp_re.findall(gtree)
		numind = len(findsp)
		if numind==1:
			gtrow[int(val)] = '1'	#value is 1 if species is monophyletic, otherwise is 0
		else:
			findseg_re = re.compile(r'(?:^|,)([^0-9]*?%s_[0-9]*?.*[^0-9]%s_[0-9]*?.*?(?:,|;))' % (val,val))	#find segment with all individuals of given species
			findseg = findseg_re.findall(gtree)
			findsp2_re = re.compile(r'(?:[^0-9]|^)([0-9]*?)_')	#find all species numbers in segment
			findsp2 = findsp2_re.findall(findseg[0])
			if len(findsp2) == numind:
				findpolyphy_re = re.compile(r',\({2,100}')
				findpolyphy = findpolyphy_re.findall(findseg[0])
				if findpolyphy == []:
					gtrow[int(val)] = '1'
				else:
					findpar1_re = re.compile(r'[)]')
					findpar1 = findpar1_re.findall(findseg[0])
					findpar2_re = re.compile(r'[(]')
					findpar2 = findpar2_re.findall(findseg[0])
					if len(findpar2) >= numind - 1:
						gtrow[int(val)] = '1'	
						if len(findpar1) > numind - 1:
							if ';' in findseg[0]:
								gtrow[int(val)] = '1'
						if len(findpar1) < numind - 1:
							gtrow[int(val)] = '0'
					else:
						gtrow[int(val)] = '0'
			else:
				findpolytom_re = re.compile(r'\(%s_[0-9]*?:[0-9\.]*?,[0-9]*?_[0-9]*?:[0-9\.]*?\):0.000,%s_[0-9]*?' % (val,val))
				findpolytom = findpolytom_re.findall(findseg[0])
				if findpolytom == []:
					gtrow[int(val)] = '0'
				elif len(findpoly) == len(findsp2)-numind:
					gtrow[int(val)] = '1'
				else:
					gtrow[int(val)] = 'error'
	newgtrow = '\t'.join(gtrow)
	gtlist.append(newgtrow)

newtext = '\n'.join(gtlist)	#each row corresponds to one gene tree
outfile = open('%s_monophyly.txt' % (gtfilename),'w')
outfile.write(newtext)
print '%s_monophyly.txt written' % (gtfilename)
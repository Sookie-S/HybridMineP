#!/usr/bin/python3

__author__ = "Soukaina Timouma"
__credits__ = ["Soukaina Timouma", "Daniela Delneri", "Jean-Marc Schwartz"]
__version__ = "1.0.1"
__maintainer__ = "Soukaina Timouma"
__email__ = "soukaina.timouma@manchester.ac.uk"




import argparse
import re
#import sys

"""
Identify 1:1 orthologs
"""
parser = argparse.ArgumentParser(description='Filenames')
parser.add_argument('--name', required=True, help='Output filename')
parser.add_argument('--ortho1', required=True, help='Orthologies filename')
parser.add_argument('--ortho2', required=True, help='Orthologies filename')

args = parser.parse_args()
name = args.name

params = vars(parser.parse_args())
params.pop("name",None)

# print("\n\nparameters: "+str(params))
# print("Name is: "+str(name))
#sys.exit("Testing")



global hybrid_name
hybrid_name = name.split("_")[0]
global parent_name
parent_name = name.split("_")[1]
print(hybrid_name)
print(parent_name)



class Sequence(object):
	"""Sequence graph-node like class to contain adjacency lists for relationships between sequences."""
	def __init__(self, id):
		self.id = id
		self.BH = None
		self.BH_eval = None
		self.BBH = None
		self.BBH_eval = None

	def __str__(self):
		return "id:%s" %(self.id)

	def addHit(self, seq, score):
		self.BH = [seq,score]
			
			
			
def evalue_to_float(evalue):
	tmp = re.match('(\d*)e(-\d*)', evalue)
	# print("e-value before conversion: "+str(evalue))
	if tmp:
		# print(tmp.group(1))
		# print(tmp.group(2))
		#res = float(tmp.group(1)) * 10**float(tmp.group(2))
		# print(float(res))
		# print("e-value before conversion: "+str(tmp)+"--> "+str(float(tmp.group(1)) * 10**float(tmp.group(2))))
		return float(float(tmp.group(1)) * (10**float(tmp.group(2))))
	else:
		try:
			return float(evalue)
		except:
			pass
	


seqById = {}

def loadCSVs():
	"""
	Loads all files given in arguments.
	"""
	for filename in params.values():
		# print("\nFilenames: "+str(filename))
		global tmp0
		tmp0 = re.findall('../Results/2_Best_hits/(\w+-\w+).csv', str(filename))
		# print("tmp0: "+str(tmp0))
		tmp0 = list(tmp0[0])
		#print("tmp0: "+str(tmp0))
		tmp0 = "".join(str(tmp0[0]))
		# print("tmp0: "+str(tmp0))
		# print(type(tmp0))
		tmp = filename.split("../Results/2_Best_hits/")[1]
		# print("tmp: "+str(tmp))
		tmp = tmp.split('.')[0]
		# print("tmp: "+str(tmp))
		with open(filename) as file:
			line = file.readline().rstrip() #Line 0 = title
			line = file.readline().rstrip() #Line 1
			while(line):
				# print("\n")
				# print(line)
				cols = line.split(',')
				# print("cols: "+str(cols))
				seq1 = Sequence(cols[0])
				# print("seq1: "+str(seq1.id))
				if(seq1.id not in seqById.keys()):
					seqById[seq1.id] = seq1
				else:
					seq1 = seqById[seq1.id]
				seq2 = Sequence(cols[1])
				# print("seq2: "+str(seq2.id))
				if(seq2.id not in seqById.keys()):
					seqById[seq2.id] = seq2
				else:
					seq2 = seqById[seq2.id]


				seq1.BH = seq2
				seq1.BH_eval = evalue_to_float(cols[2])
				line = file.readline().rstrip()
		
		file.close()

def findOrthologs(filename):
	i = 0
	k = 0
	liste = []
	for s in seqById.values():
		if s.BH:
			if s.BH.BH:
				# print(s.id + ' | ' + s.BH.id + ' | ' + s.BH.BH.id)
				if s.id == s.BH.BH.id: #Reciprocal best hit
					s.BBH = s.BH
					s.BBH_eval = s.BH_eval
					# print("BBH found")
	with open(filename, 'w') as file:
		file.write(str(hybrid_name)+","+str(parent_name)+"\n")
		for s in seqById.values():
			if s.BBH:
				i +=1
				if s.id not in [elmt for elmt in liste]:
					liste.append(s.id)
					liste.append(s.BBH.id)
					# print("OK")
					k +=1 
					sid = s.id
					sid = sid.split(".")
					sBBHid = s.BBH.id
					sBBHid = sBBHid.split(".")
					if sid[0] == hybrid_name:
						file.write(sid[1] + ',' + sBBHid[1] + '\n')
					else:
						file.write(sBBHid[1] + ',' + sid[1] + '\n')
	file.close()
    
loadCSVs()
findOrthologs("../Results/3_Orthologs_Paralogs/"+str(name)+"_orthologies.csv")
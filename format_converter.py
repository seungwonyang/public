# Date: 1/27/2013
# Seungwon Yang <seungwon@vt.edu>
# Description: This scripts reads in data file and converts it to SVM light 
#			   (also applicable for LibSVM, Liblinear) format. A dictionary file
#			   'words' is created as well.
# Note: a stopword list is in 'stopwords.txt' file
# Use: ?> python format_converter.py  <input_filename>  <output_filename>

import sys
from collections import Counter

class ConvFormat:
	def __init__(self, stop_path):
		stop_li = open(stop_path, "r").read().split()
		self.stoplist = set(stop_li)
		self.dict_li = []

	def findDictIndex(self, item):
		try:
			return self.dict_li.index(item)
		except ValueError:
			return -1

	def makeWdict(self, input_filename):
		fi = open(input_filename, 'r')
		for each in fi:
			for item in each.split()[1:]:
				if item not in self.stoplist:
					self.dict_li.append(item)
			self.dict_li = list(set(self.dict_li))
		(self.dict_li).sort()
		# write a dictionary file
		fo_dict = open("words", "w+")
		for word in self.dict_li:
			fo_dict.write(word)
			fo_dict.write("\n")
		
	def convertInput(self, input_filename, output_filename):
		fi = open(input_filename, 'r')
		fo = open(output_filename, "w+")
		for each in fi:
			# string to hold converted format
			new_str = ""
			tokens = each.split()
			label = tokens[0]
			new_str += label
			svm_index_li = []
			item_count = []
			for item in sorted(tokens[1:]):
				index = self.findDictIndex(item)
				if index != -1:
					svm_index_li.append(index+1)  

			# print svm_index_li
			tuple_li = sorted(dict(Counter(svm_index_li)).items())
			for tup in tuple_li:
				new_str += " %d:%d" % (tup[0], tup[1])
			fo.write(new_str)
			fo.write("\n")

def main():
	conv = ConvFormat("stopwords.txt")
	conv.makeWdict(sys.argv[1])
	conv.convertInput(sys.argv[1], sys.argv[2])
	
if __name__ == "__main__":
	main()
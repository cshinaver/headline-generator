#!./bin/python3

import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('bllip_wsj_no_aux')
import json

class Verb_Parse():
	def __init__(self,filename):
		self.article_list = self.read_data(filename) #list of json article data
		self.token_list = self.make_tokens() #each entry is a document, with a list of entries for each line
		print(self.token_list[0][1])
		self.take_verbs()

	def read_data(self,filename):
		print("reading in data...")
		article_list = []
		fp = open(filename) #open the doc
		for line in fp.readlines()[0:100]:
			article_list.append(json.loads(line)) #load the json of each article and add it to the list
		return article_list

	def tag_line(self,line):
		tokens = nltk.word_tokenize(line)
		tagged = nltk.pos_tag(tokens)
		return tagged

	def make_tokens(self):
		print("making tokens...")
		tagged_list = [] #this is the master list of tagged documents
		for article in self.article_list:
			#find important sentences here!
			content = article['content'].split("\n \n")
			tagged_line_list = [] #this keeps track of each tagged line
			for line in content:
				tagged_line_list.append(self.tag_line(line))
			tagged_list.append(tagged_line_list) #at the end append the whole document
		return tagged_list

	def take_verbs(self):
		for doc in self.token_list[0:1]:
			for line in doc:
				for word in line:
					if word[1][0] == 'V':
						print(word)

if __name__ == "__main__":
	verb_parse = Verb_Parse('train.json')
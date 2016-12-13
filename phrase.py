class Phrase():
	def __init__(self,pv_wd,wd,nx_wd):
		self.prev_word_list = pv_wd
		self.word = wd
		self.next_word_list = nx_wd
		self.phrase = self.create_phrase()
		
	def __str__(self):
		return 'object' + str(self.word)

	def __repr__(self):
		return self.phrase

	def create_phrase(self):
		phrase_string = ''
		if self.prev_word_list != None:
			for word in self.prev_word_list:
				phrase_string += word[0] + ' '
		phrase_string += self.word[0] + ' '
		if self.next_word_list != None:
			for word in self.next_word_list:
				phrase_string += word[0] + ' '
		return phrase_string

	def get_list_words(self):
		word_list = []
		if self.prev_word_list != None:
			for word in self.prev_word_list:
				word_list.append(word[0])
		word_list.append(self.word[0])
		if self.next_word_list != None:
			for word in self.next_word_list:
				word_list.append(word[0])
		return word_list

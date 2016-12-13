#!./bin/python3

import itertools
import nltk
import json
import sys
from sentence_extraction import SentenceExtractor
from phrase import Phrase

class Verb_Parse():
    def __init__(self):
        self.num_important = 2 #top two sentences
        self.docs = self.get_doc_generator(sys.argv[1])
        self.sentence_extractor = SentenceExtractor()
        self.initiate()
        self.titles = self.run()
        print(self.titles)
        #self.get_title_generator()
    def initiate(self):
        print("training...")
        self.sentence_extractor.fit_tfidf(itertools.islice(
            self.docs,
            0,
            300
            )
        )

    def get_doc_generator(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                doc = json.loads(line)
                content = doc['content']
                yield content

    def get_title_generator(self):
        with open(sys.argv[1]) as f:
            for line in f.readlines()[0:10]:
                doc = json.loads(line)
                content = doc['title']
                print(content)

    def tag_line(self,line): #takes a line of text, tokenizes and returns a list with word tag tuples
        tokens = nltk.word_tokenize(line)
        tagged = nltk.pos_tag(tokens)
        return tagged

    def run(self):
        print("running...")
        phrases_list = []
        docs = itertools.islice(
            self.get_doc_generator(sys.argv[2]),
            0,
            10
            )
        for article in docs:
            #order sentences
            important_list, sentences = self.get_important_sentences(article)
            #pull verbs from these sentences here!
            verbs = self.take_verbs_from_list(important_list,sentences)
            #find important verb phrases
            important_phrases = self.get_important_phrases(verbs,sentences)

            phrases_list.append(important_phrases)

        return phrases_list

    def get_important_sentences(self,article):
        sentences = self.sentence_extractor.get_sentences_from_doc(article) #seperate lines of document
        important_list = self.sentence_extractor.get_most_important_sentences(sentences) #important list for the document
        return important_list, sentences

    def take_verbs_from_list(self,index_list,sentences):
        verb_list = []
        for i in range(0,len(sentences)):
            if i >= self.num_important:
                break #already searched the important sentences
            else:
                important_sentence = index_list[i][0] #get the index of the sentence
                tagged_line = self.tag_line(sentences[important_sentence])
                verb_list.extend(self.get_verbs(tagged_line,important_sentence))
        return verb_list

    def get_verbs(self,tagged_line,sentence_index):
        verb_list = []
        for i in range(0,len(tagged_line)):
            #right now just grab a word before and one after, this can use some improvement
            prev_word = None
            if i > 0:
                prev_word = self.find_prev_noun(i,tagged_line)
                #prev_word = tagged_line[i-1]
            word = tagged_line[i]
            if i == len(tagged_line) - 1:
                next_word = None
            else:
                next_word = self.find_next_noun(i,tagged_line)
                #next_word = tagged_line[i+1]
            if word[1][0] == 'V':
                verb_list.append((word,sentence_index,Phrase(prev_word,word,next_word)))
        return verb_list

    def find_prev_noun(self,index,sentence):
        prev_noun_list = []
        count = 0
        extra_words = 2
        while index >= 0:
            prev_word = sentence[index]
            if prev_word[1][0] == 'N' or prev_word[1][0] == 'P': #if first letter of tag is N
                prev_noun_list.append(prev_word)
                #print('Found noun:', prev_noun, 'index:', index)
                count += 1
                if count >= extra_words:
                    break
            index -= 1
        return prev_noun_list
    def find_next_noun(self,index,sentence):
        extra_words = 2
        count = 0
        next_noun_list = []
        while index < len(sentence):
            next_word = sentence[index]
            if next_word[1][0] == 'N' or next_word[1][0] == 'P':
                next_noun_list.append(next_word)
                count += 1
                #print('Found noun:', next_noun, 'index:', index)
                if count >= extra_words:
                    break
            index += 1
        return next_noun_list

    def get_important_phrases(self,verbs,sentences):
        phrases_list = []
        prob_list = []
        important_list = []
        if not self.sentence_extractor.tfidf:
            raise RuntimeError(
                "Must have called fit_tfidf before trying to calculate tfidf"
            )
        lines_matrix = self.sentence_extractor.tfidf.transform(sentences)
        inverse_matrix = self.sentence_extractor.tfidf.inverse_transform(lines_matrix)
        for verb_group in verbs:
            prob_phrase = 0
            #word = verb_group[0][0] #pull the verb
            line_number = verb_group[1]
            inverse_list = inverse_matrix[line_number].tolist()
            for word in verb_group[2].get_list_words():
                if word in inverse_list:
                    prob_phrase += self.get_prob_for_word(line_number,word,inverse_list,lines_matrix)

            prob_list.append((verb_group,prob_phrase))
        #prob_list contains verb_group and prob for that verb
        #print(prob_list[:2])
        sorted_list = sorted(prob_list,key=lambda x: x[1],reverse=True)
        best_list = sorted_list[:3]
        ordered_best_list = sorted(best_list,key=lambda x: x[0][1])
        for group in ordered_best_list:
            verb_phrase = group[0][2]
            important_list.append(verb_phrase)

        return important_list

    def get_prob_for_word(self,line_number,word,inverse_list,lines_matrix):
        nonzero_index = inverse_list.index(word)
        matrix_index = lines_matrix[line_number].nonzero()[1][nonzero_index]
        prob = lines_matrix.toarray().tolist()[line_number][matrix_index]

        return prob


    def calculate_tfidf_for_verbs(self):
            if not self.sentence_extractor.tfidf:
                raise RuntimeError(
                    "Must have called fit_tfidf before trying to calculate tfidf"
                )
            doc_num = self.verbs[0][1]
            print(self.token_list[doc_num])
            lines = self.sentence_extractor.get_sentences_from_doc(self.doc_list[doc_num])
            lines_matrix = self.sentence_extractor.tfidf.transform(lines)
            inverse = self.sentence_extractor.tfidf.inverse_transform(lines_matrix)
            print(len(lines_matrix.toarray().tolist()))
            print(lines_matrix[17].nonzero()[1][8])
            print(lines_matrix.toarray().tolist()[17][1857]) #[line number][position] TODO find out how to get the position
            print(inverse[17])
            print(inverse[17].tolist().index('said')) #find index of given word!
            print(lines_matrix[17])

            sums = lines_matrix.sum(axis=1)
            flattened_sums = [
                item for sublist in sums.tolist() for item in sublist
            ]
            sorted_scores = sorted(
                zip(range(0, len(flattened_sums)), flattened_sums),
                key=lambda x: x[1],
                reverse=True,
            )
            return sorted_scores

if __name__ == "__main__":
    verb_parse = Verb_Parse()

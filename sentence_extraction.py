#!/usr/bin/env python
# sentence_extraction.py
# Charles Shinaver and Nick Lombardo
# Module for sentence extraction

import itertools
import json
import nltk
import sys
from sklearn.feature_extraction.text import TfidfVectorizer


class SentenceExtractor:
    def tokenize(self, line):
        tokens = nltk.word_tokenize(line)
        return tokens

    def calculate_tfidf(self, docs):
        tfidf = TfidfVectorizer(tokenizer=self.tokenize)
        frequencies = tfidf.fit_transform(docs)
        return frequencies


def get_doc_generator():
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            doc = json.loads(line)
            content = doc['content']
            yield content

if __name__ == '__main__':
    docs = get_doc_generator()
    sentence_extractor = SentenceExtractor()
    print(sentence_extractor.calculate_tfidf(itertools.islice(docs, 0, 5)))

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
    def __init__(self):
        self.tfidf = None

    def tokenize(self, line):
        tokens = nltk.word_tokenize(line)
        return tokens

    def fit_tfidf(self, docs):
        """ Calculates all weights for words in tfidf matrix. "Trains" it """
        self.tfidf = TfidfVectorizer(tokenizer=self.tokenize)
        tfidf_matrix = self.tfidf.fit_transform(docs)
        return tfidf_matrix

    def calculate_tfidf_for_lines(self, lines):
        if not self.tfidf:
            raise RuntimeError(
                "Must have called fit_tfidf before trying to calculate tfidf"
            )
        lines_matrix = self.tfidf.transform(lines)
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

    def get_most_important_sentences(self, lines):
        sorted_scores = self.calculate_tfidf_for_lines(lines)
        sorted_lines = [lines[t[0]] for t in sorted_scores]
        return sorted_lines

    def get_sentences_from_doc(self, doc):
        sentences = nltk.sent_tokenize(doc)
        return sentences


def get_doc_generator():
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            doc = json.loads(line)
            content = doc['content']
            yield content

if __name__ == '__main__':
    docs = get_doc_generator()
    sentence_extractor = SentenceExtractor()
    tfidf_matrix = sentence_extractor.fit_tfidf(itertools.islice(
            docs,
            0,
            5
        )
    )
    sentences = sentence_extractor.get_sentences_from_doc(
        next(get_doc_generator())
    )
    print(sentence_extractor.get_most_important_sentences(sentences))

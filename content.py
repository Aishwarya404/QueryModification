# Aishwarya Sivakumar - as6418
# Sairam Haribabu - sh4188

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict
import math

# Class Content which stores the processed result, query, bigrams,
# vocab of words, relevant and irrelevant term frequency vectors.
# Contains member methods to perform bigram calculation, tf-idf calculations.
class Content:

    # Constructor for class Content
    def __init__(self, result, query, original_query, no_of_relevant):
        self.data = result
        self.original_query = original_query.lower().split(' ')
        self.query = query.lower().split(' ')
        self.relevant_count = no_of_relevant
        self.vocab = set()
        self.bigrams = defaultdict(int)
        self.relevant = []
        self.irrelevant = []
        self.populate_vocab_bigrams()
        self.calculate_tf_idf()

    # Method that takes terms in a doc, doc as input
    # finds possible bigrams and updates self.bigrams
    def get_bigrams(self, terms, doc):
        for bigram in nltk.bigrams(terms):
            if doc["relevancy"]:
                self.bigrams[bigram] = self.bigrams.get(bigram, 0) + 1
            else:
                self.bigrams[bigram] = self.bigrams.get(bigram, 0) - 1

    # Method that uses nltk libraries to tokenize and get all terms
    # Removes stop words, symbols and numbers
    def get_terms(self, doc_words):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(doc_words)
        terms = [w.lower() for w in word_tokens if not w.lower() in stop_words and w.isalpha()]
        return terms

    # Method to traverse through processed data, get terms and populate bigrams and vocab of words
    def populate_vocab_bigrams(self):
        for i in range(len(self.data)):
            doc = self.data[i]
            terms_title = self.get_terms(str(doc["title"]))
            terms_snippet = self.get_terms(str(doc["snippet"]))
            for term in terms_title + terms_snippet:
                self.vocab.add(term)
            self.get_bigrams(terms_snippet, doc)
            self.get_bigrams(terms_title, doc)
        self.vocab = list(self.vocab)
        self.bigrams = sorted(self.bigrams.items(), key=lambda item: item[1], reverse=True)
        self.bigrams = list(filter(lambda x: x[1] > 0, self.bigrams))

    # Method to iterate through processed data and calculate the term freq, doc freq and tf-idf
    def calculate_tf_idf(self):
        doc_freq = defaultdict(set)
        for i in range(len(self.data)):
            doc = self.data[i]
            term_freq = dict.fromkeys(self.vocab, 0)
            terms = self.get_terms(str(doc["title"]) + " " + str(doc["snippet"]))
            for term in terms:
                term_freq[term] = term_freq.get(term, 0) + 1
                doc_freq[term].add(i)
            if doc["relevancy"]:
                self.relevant.append(term_freq)
            else:
                self.irrelevant.append(term_freq)
        for doc in self.relevant:
            for term in doc:
                if doc[term] != 0:
                    doc[term] = (1 + math.log10(doc[term])) * math.log10(len(self.data)/ len(doc_freq[term])) * 10
        for doc in self.irrelevant:
            for term in doc:
                if doc[term] != 0:
                    doc[term] = (1 + math.log10(doc[term])) * math.log10(len(self.data)/ len(doc_freq[term])) * 10

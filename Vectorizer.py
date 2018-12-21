#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
import numpy as np
import math
from collections import Counter

class Vectorizer:
    def __init__(self, min_word_length=3, max_df=1.0, min_df=0.0):
        self.min_word_length = min_word_length
        self.max_df=max_df
        self.min_df=min_df
        self.term_df_dict = {}
        self.vocabulary = []
        np.set_printoptions(threshold=np.nan)
        
    def fit(self, raw_documents):
        """Generates vocabulary for feature extraction. Ignores words shorter than min_word_length and document frequency
        not between max_df and min_df.

        :param raw_documents: list of string for creating vocabulary
        :return: None
        """
        self.document_count = len(raw_documents)
        # TODO: Implement this method
        cnt = Counter()
        for document in raw_documents:
            document = document.split()#document = nltk.tokenize.word_tokenize(document)
            passed = Counter()
            for word in document:
                if  passed[word] == 0:#word not in passed:
                    passed[word] = 1#passed.append(word)
                    cnt[word] +=1
        for (key,_) in cnt.items():
            temp = cnt[key]/float(self.document_count)
            if len(key)>=self.min_word_length and temp >= self.min_df and temp <= self.max_df and key not in self.vocabulary:
                self.vocabulary.append(key)
                self.term_df_dict[key] = temp


    def _transform(self, raw_document, method):
        """Creates a feature vector for given raw_document according to vocabulary.

        :param raw_document: string
        :param method: one of count, existance, tf-idf
        :return: numpy array as feature vector
        """
        # TODO: Implement this method
        #temp = nltk.tokenize.word_tokenize(raw_document)
        temp = raw_document.split()
        count_words = Counter()
        for word in temp:
            count_words[word] += 1
        result = np.zeros((len(self.vocabulary)))
        if method == "existance":
            for word in temp:
                if word in self.vocabulary:
                    result[self.vocabulary.index(word)] = 1
        elif method == "count":
            for word in temp:
                if word in self.vocabulary:
                    result[self.vocabulary.index(word)] +=1
        elif method == "tf-idf":
            for word in temp:
                if word not in self.vocabulary:
                    continue
                freq = self.term_df_dict[word]*self.document_count
                idf = math.log((1+self.document_count)/(1+freq)) + 1
                tf = count_words[word]/float(self.document_count)
                result[self.vocabulary.index(word)] = tf*idf
            n = np.linalg.norm(result)
            for i in range(len(result)):
                if n == 0:
                    continue
                result[i] = result[i]/n    
        return result

    def transform(self, raw_documents, method="tf-idf"):
        """For each document in raw_documents calls _transform and returns array of arrays.

        :param raw_documents: list of string
        :param method: one of count, existance, tf-idf
        :return: numpy array of feature-vectors
        """
        # TODO: Implement this method
        result = np.zeros((len(raw_documents),len(self.vocabulary)),float)
        for i in range(len(raw_documents)):
            result[i] = self._transform(raw_documents[i],method)
        return result

    def fit_transform(self, raw_documents, method="tf-idf"):
        """Calls fit and transform methods respectively.

        :param raw_documents: list of string
        :param method: one of count, existance, tf-idf
        :return: numpy array of feature-vectors
        """
        # TODO: Implement this method
        self.fit(raw_documents)
        return self.transform(raw_documents,method)

    def get_feature_names(self):
        """Returns vocabulary.

        :return: list of string
        """
        try:
            self.vocabulary
        except AttributeError:
            print "Please first fit the model."
            return []
        return self.vocabulary

    def get_term_dfs(self):
        """Returns number of occurances for each term in the vocabulary in sorted.

        :return: array of tuples
        """
        return sorted(self.term_df_dict.iteritems(), key=lambda (k, v): (v, k), reverse=True)

if __name__=="__main__":
    v = Vectorizer(min_df=0.25, max_df=0.75)
    contents = [
     "this is the first document",
     "this document is the second document",
     "and this is the third one",
     "is this the first document",
 ]
    v.fit(contents)
    print v.get_feature_names()
    existance_vector = v.transform(contents, method="existance")        
    print existance_vector
    count_vector = v.transform(contents, method="count")        
    print count_vector
    tf_idf_vector = v.transform(contents, method="tf-idf")
    print tf_idf_vector

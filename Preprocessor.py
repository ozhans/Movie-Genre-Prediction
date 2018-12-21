#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
import os
from nltk.corpus import stopwords
import codecs
import errno
import string

class Preprocessor:
    def __init__(self, dataset_directory="Dataset", processed_dataset_directory= "ProcessedDataset"):
        self.dataset_directory = dataset_directory
        self.processed_dataset_directory=processed_dataset_directory
        nltk.download("stopwords")
        nltk.download("punkt")
        self.stop_words = set(stopwords.words('english'))

    def _remove_puncs_numbers_stop_words(self, tokens):
        """Remove punctuations in the words, words including numbers and words in the stop_words list.

        :param tokens: list of string
        :return: list of string with cleaned version
        """
        # TODO: Implement this method
        #punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        result = []
        size = len(tokens)
        i=0
        while i < size:
            s = len(tokens[i])
            j = 0
            flag = True
            while j < s:
                if tokens[i][j] in string.punctuation:
                    tokens[i] = tokens[i][:j] + tokens[i][j+1:]
                    s-=1
                    flag = False
                else:
                    flag = True
                if flag:
                    j+=1
            i+=1
                    
        result2 = []
        result2 = [x for x in tokens if x.isalpha()]
        result = [x for x in result2 if x not in self.stop_words]
        return result

    def _tokenize(self, sentence):
        """Tokenizes given string.

        :param sentence: string to tokenize
        :return: list of string with tokens
        """
        # TODO: Implement this method
        return nltk.tokenize.word_tokenize(sentence)

    def _stem(self, tokens):
        """Stems the tokens with nltk SnowballStemmer

        :param tokens: list of string
        :return: list of string with words stems
        """
        # TODO: Implement this method
        stemmer = nltk.stem.snowball.SnowballStemmer("english")
        i = 0
        size = len(tokens)
        while i<size:
            tokens[i] = stemmer.stem(tokens[i])
            if tokens[i] == "":
                tokens.remove(tokens[i])
                size-=1
                i-=1
            i+=1
        return tokens

    def preprocess_document(self, document):
        """Calls methods _tokenize, _remove_puncs_numbers_stop_words and _stem respectively.

        :param document: string to preprocess
        :return: string with processed version
        """
        # TODO: Implement this method
        temp = self._tokenize(document.lower())
        temp = self._remove_puncs_numbers_stop_words(temp)
        temp = ' '.join(self._stem(temp))
        return temp


    def preprocess(self):
        """Walks through the given directory and calls preprocess_document method. The output is
        persisted into processed_dataset_directory by keeping directory structure.

        :return: None
        """
        for root, dirs, files in os.walk(self.dataset_directory):
            if os.path.basename(root) != self.dataset_directory:
                print "Processing", root, "directory."
                dest_dir = self.processed_dataset_directory+"/"+root.lstrip(self.dataset_directory+"/")
                if not os.path.exists(dest_dir):
                    try:
                        os.makedirs(dest_dir)
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise
                for file in files:
                    file_path = root + "/" + file
                    with codecs.open(file_path, "r", "ISO-8859-1") as f:
                        data = f.read().replace("\n", " ")
                    processed_data = self.preprocess_document(data)
                    output_file_path = dest_dir + "/" + file
                    with codecs.open(output_file_path, "w", "ISO-8859-1") as o:
                        o.write(processed_data)

if __name__=="__main__":
    text =  """ Greetings,
                shall I sit or stand?
                - Tell us.
                - Tell us.
                I'll tell. We bought the goods
                from Black Faik.
                We reloaded the truck
                in Karabuk.
                I was driving the truck
                till Adana.
                - What are you talking about?
                - And you?!
                You've abducted me,
                you'll do the talking.
                I'm confused anyway.
                - Aggressive.
                - Aggressive...
                Yeah, aggressive.
                Is that it?"""
    """p = Preprocessor()
    p.preprocess()"""
    p = Preprocessor()
    print p.preprocess_document(text)
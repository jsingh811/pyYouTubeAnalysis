#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 7 17:08:31 2020

@author: jsingh
"""
import nltk

from itertools import groupby
from unicodedata import category as unicat

from nltk.chunk import tree2conlltags
from nltk.chunk.regexp import RegexpParser

from pyYouTubeAnalysis import cleaner

GRAMMAR = r"KT: {<NNP.*?>+|((<JJ>|<NN.*?>|<RB>) (<NN>|<NNS>))}"
STOPWORDS = set(nltk.corpus.stopwords.words("english"))


class KeyPhraseGenerator():
    """
    Extracts keyphrases from input list of strings.
    """
    def __init__(self, grammar=GRAMMAR, stopwords=STOPWORDS):

        self.chunker = RegexpParser(grammar)
        self.stopwords = stopwords

    def clean_text(self, txt):
        """
        Removes emoji and urls from text.
        """
        cleaned = cleaner.remove_emojis(txt)
        cleaned = cleaner.remove_urls(cleaned)
        return cleaned

    def clean_tagged_text(self, tagged_text):
        """
        Remove punctuation from tagged text.
        """
        punct_tagged = lambda word: all(
            unicat(char).startswith("P") and char != "," for char in word
        )
        cleaned = filter(lambda t: not punct_tagged(t[0]), tagged_text)
        return list(cleaned)

    def extract_keyphrases_single(self, txt):
        """
        Yields keyphrases for one piece of text.
        """
        for sent in txt:
            sent = self.clean_tagged_text(sent)
            if not sent:
                continue
            chunks = tree2conlltags(self.chunker.parse(sent))
            phrases = [
                " ".join(word for word, pos, chunk in group).lower()
                for key, group in groupby(chunks, lambda term: term[-1] != "O")
                if key
            ]
            for phrase in phrases:
                if phrase.lower() not in self.stopwords and len(phrase) > 2:
                    yield phrase

    def extract_keyphrases(self, txt_list):
        """
        Returns keyphrases for input list of strings.
        """
        key_docs = []
        for txt in txt_list:
            tagged_doc = []
            txt = self.clean_text(txt)
            for sent in nltk.sent_tokenize(txt):
                tagged_doc.append(nltk.pos_tag(nltk.word_tokenize(sent)))
            key_docs.append(list(self.extract_keyphrases_single(tagged_doc)))
        return key_docs


if __name__ == "__main__":

    kp = KeyPhraseGenerator()
    print(
        kp.extract_keyphrases(
            ["""
            Did you know about this conference in Miami? It is about Natural
            Language Processing techniques as applied to messy data.""",
            """
            I really enjoyed the chocolate cheesecake yesterday!"""]
        )
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 1 18:38:32 2021

@author: jsingh
"""

import re

URL_PATTERN = re.compile(
    r"https?://\S+|www\.\S+",
    re.X
)
EMOJI_PATTERN = re.compile(
    "[\U00010000-\U0010ffff]",
    flags=re.UNICODE
)


def remove_emojis(txt):
     """
     Remove emojis from input text
     """
     clean_txt = EMOJI_PATTERN.sub(" ", txt)
     return clean_txt

def remove_urls(txt):
     """
     Remove urls from input text
     """
     clean_txt = URL_PATTERN.sub(" ", txt)
     return clean_txt

if __name__ == "__main__":

    print(remove_emojis(" emoji was here -> 😃"))
    print(remove_urls(" urls was here -> https://google.com"))

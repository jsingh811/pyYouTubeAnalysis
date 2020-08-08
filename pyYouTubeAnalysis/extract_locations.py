#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 7 17:08:31 2020

@author: jsingh
"""
####    Imports
import argparse
import json
import spacy
from collections import Counter

#### Globals
NLP = spacy.load("en_core_web_sm")

#### Functions
def read_comment_text(filepath):
    """
    Read comments file
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    comment_text = []
    for video_id in data:
        if data[video_id]:
            for cmt in data[video_id]:
                if (
                    cmt
                    and "snippet" in cmt
                    and "topLevelComment" in cmt["snippet"]
                    and "snippet" in cmt["snippet"]["topLevelComment"]
                    and "textOriginal" in cmt["snippet"]["topLevelComment"]["snippet"]
                ):
                    comment_text.append(
                        cmt["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                    )
    return comment_text

def extract_locations(comments_list):
    """
    Extract location strings for the input list of strings
    """
    locs = []
    for cmt in comments_list:
        doc = NLP(cmt)
        locs += [
            x.text.lower()
            for x in doc.ents
            if x.label_ in ["GPE", "LOC"] and len(x.text.lower().strip())>0
        ]
    return locs

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Fetch YouTube data")
        parser.add_argument(
            "-filepath", "--filepath", type=str, required=True,
            help="Path to the file you have saved comments data in"
        )
        args = parser.parse_args()
        comments = read_comment_text(args.filepath)
        locations = extract_locations(comments)
        with open("".join([
            "/".join(args.filepath.split("/")[0:-1] + [""]),
            "locations_",
            args.filepath.split("/")[-1]
        ]), "w") as f:
            json.dump(Counter(locations), f, indent=2)

        print("Locations saved in {}".format("".join([
            "/".join(args.filepath.split("/")[0:-1] + [""]), "locations_",
            args.filepath.split("/")[-1]
        ])))

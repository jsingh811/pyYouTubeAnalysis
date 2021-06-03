#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 3 17:03:21 2021

@author: jsingh
"""

from pyYouTubeAnalysis.extract_locations import extract_locations


def test_extract_locations():
    """
    Tests extraction of location strings
    """
    good_input = ["Enjoying the sunny weather in Washington DC.",
                  "I moved from Los Angeles to Washington DC."]
    bad_input = ["This does not mention any location.",
                  "Just another random piece of text"]
    good_locs = extract_locations(good_input)
    bad_locs = extract_locations(bad_input)

    assert good_locs == [
        "washington dc",
        "los angeles",
        "washington dc"
    ]
    assert bad_locs == []

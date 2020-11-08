#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 7 17:08:31 2020

@author: jsingh
"""
### Imports
import argparse
import json

from googleapiclient.errors import HttpError

from pyYouTubeAnalysis import crawler

### Functions
def get_videos(api, keyword, start_date, end_date):
    """
    Fetch videos from YouTube API
    """
    return api.search_videos(
        keyword=keyword,
        start_date=start_date,
        end_date=end_date
    )

def get_comments(api, video_id, limit=50):
    """
    Fetch commets for inpurt video ID from YouTube API
    """
    try:
        comments = api.fetch_comments(
            video_id,
            limit=limit
        )
    except HttpError:
        comments = None
    return comments

def get_videos_and_comments(
    api,
    keyword=None,
    start_date="2005-01-01T00:00:00Z",
    end_date="2020-12-01T00:00:00Z",
    comment_limit=50
):
    """
    Search for videos between start and end dates and fetch their comments from YouTube API
    """
    video_data = get_videos(
        api,
        keyword=keyword,
        start_date=start_date,
        end_date=end_date
    )
    comments = {}
    ids = list(set([itm["id"] for itm in video_data]))
    for video_id in ids:
        comments[video_id] = get_comments(api, video_id, limit=comment_limit)
    return video_data, comments

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch YouTube data")
    parser.add_argument(
        "-path", "--path", type=str, required=True,
        help="Path to the directory you want to save the data in"
    )
    parser.add_argument(
        "-k", "--keyword", type=str, default=None,
        help="Keyword to search data for"
    )
    parser.add_argument(
        "-sd",
        "--start-date",
        type=str,
        default=None,
        help="Starting publish date of video to search. Format YYYY-MM-DDThh:mm:ssZ",
    )
    parser.add_argument(
        "-ed",
        "--end-date",
        type=str,
        default=None,
        help="Ending publish date of video to search. Format YYYY-MM-DDThh:mm:ssZ",
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        required=True,
        help="YouTube API access token",
    )
    parser.add_argument(
        "-cmts",
        "--comments",
        type=str,
        default="false",
        help="Whether you want to fetch comment text for the videos",
    )
    parser.add_argument(
        "-climit",
        "--comment-limit",
        type=int,
        default=50,
        help="Per video comment limit to fetch.",
    )

    args = parser.parse_args()
    api = crawler.YouTubeCrawler(key=args.token)

    comments = {}
    video_data = get_videos(
        api,
        keyword=args.keyword,
        start_date=args.start_date,
        end_date=args.end_date
    )
    with open("/".join([
        args.path,
        "_".join([
            args.keyword,
            args.start_date.replace(":", ""),
            args.end_date.replace(":", ""),
            "video_details.json"
        ])
    ]), "w") as f:
        json.dump(video_data, f, indent=2)
    print("Searched and loaded video details into {}".format(
        "/".join([
            args.path,
            "_".join([
                args.keyword,
                args.start_date.replace(":", ""),
                args.end_date.replace(":", ""),
                "video_details.json"
            ])
        ])
    ))
    if args.comments:
        comments = {}
        ids = list(set([itm["id"] for itm in video_data]))
        for video_id in ids:
            comments[video_id] = get_comments(api, video_id, limit=args.comment_limit)

        with open("/".join([
            args.path,
            "_".join([
                args.keyword,
                args.start_date.replace(":", ""),
                args.end_date.replace(":", ""),
                "comment_details.json"
            ])
        ]), "w") as f:
            json.dump(comments, f, indent=2)

        print("Fetched and loaded comments into {}".format(
            "/".join([
                args.path,
                "_".join([
                    args.keyword,
                    args.start_date.replace(":", ""),
                    args.end_date.replace(":", ""),
                    "comment_details.json"
                ])
            ])
        ))

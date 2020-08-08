#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 7 17:08:31 2020

@author: jsingh
"""
### Imports
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

### Globals and Variables
YOUTUBE_VERSION = "v3"
SERVICE_NAME = "youtube"

### Class
class YouTubeCrawler(object):
    """
    YouTube Crawler object queries the YouTube Data API
    """
    def __init__(self, key):
        self.key = key
        self.service_name = SERVICE_NAME
        self.youtube_version = YOUTUBE_VERSION
        self.api = self.build_connection()

    def build_connection(self):
        """
        Construct the API connection
        """
        return build(
            self.service_name,
            self.youtube_version,
            developerKey = self.key,
            cache_discovery = False
        )

    def search_videos(
        self,
        topic=None,
        keyword=None,
        start_date="2010-01-01T00:00:00Z",
        end_date="2020-01-01T00:00:00Z"
    ):
        """
        Searches for videos containing the keyword or topic between start and end dates.
        Also fetches details and stats for every resulting video.
        """
        res = []
        q = self.api.search().list(
                type="video",
                q=keyword,
                topicId=topic,
                maxResults=50,
                part="snippet",
                publishedAfter=start_date,
                publishedBefore=end_date
        ).execute()
        page_token = q.get("nextPageToken")
        res += q["items"]
        while page_token and len(q["items"])>0:
            q = self.api.search().list(
                type="video",
                q=keyword,
                topicId=topic,
                part="snippet",
                maxResults=50,
                publishedAfter=start_date,
                publishedBefore=end_date,
                pageToken=page_token
            ).execute()
            page_token = q.get("nextPageToken")
            res += q["items"]
        vidids = [i["id"]["videoId"] for i in res]
        dets = self.fetch_video_details(vidids)
        return dets

    def fetch_video_details(self, ids, part="snippet,statistics"):
        """
        Fetches details and stats for input video IDs.
        """
        video_details = []
        for inx in range(0, len(ids), 50):
            try:
                video_details += self.api.videos().list(
                    part=part,
                    maxResults=50,
                    id=",".join(ids[inx: inx + 50])
                ).execute()["items"]
            except HttpError:
                pass

        return video_details

    def fetch_comments(self, video_id, part="snippet", limit=50):
        """
        Fetches comments for input video ID.
        """
        coms = []
        if limit <= 50:
            try:
                q = self.api.commentThreads().list(
                        part=part,
                        maxResults=limit,
                        videoId=video_id
                    ).execute()
            except HttpError:
                return None
            return q["items"]
        elif limit > 50:
            q = self.api.commentThreads().list(
                    part=part,
                    maxResults=50,
                    videoId=video_id
                ).execute()
            coms += q["items"]
            while len(q["items"])>0 and "nextPageToken" in q and len(coms) < limit:
                try:
                    q = self.api.commentThreads().list(
                            part=part,
                            maxResults=50,
                            pageToken=q["nextPageToken"],
                            videoId=video_id
                        ).execute()
                    coms += q["items"]
                except HttpError:
                    break

        return coms

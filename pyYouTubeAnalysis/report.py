#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 7 18:12:23 2021

@author: jsingh
"""

import argparse
import json
from collections import Counter

from matplotlib import pyplot as plt
from wordcloud import WordCloud
from fpdf import FPDF

from pyYouTubeAnalysis import run_crawl, crawler, extract_locations


class ReportGenerator:
    """
    Generate a report from YouTube
    """

    def __init__(self, path, keyword, start_date, end_date, analysis_type):
        self.path = path
        self.keyword = keyword
        self.start_date = start_date
        self.end_date = end_date
        self.analysis_type = analysis_type

    def get_wordcloud(
        self, word_frequencies, file_name="word_cloud.png", max_words=100
    ):
        """
        Generates and saves word cloud for the input word word frequencies.
        """
        # TODO: Add stopwords
        wordcloud = WordCloud(
            max_font_size=50,
            max_words=100,
            mode="RGBA",
            background_color="white",
            normalize_plurals=True,
            min_word_length=2,
        ).generate_from_frequencies(word_frequencies)
        wordcloud.to_file("/".join([self.path, file_name]))

    def extract_month(self, date):
        """
        Extracts month from "YYYY-MM-DDTHH:MM:SSZ" format.
        """
        return int(date[5:7])

    def extract_year(self, date):
        """
        Extracts year from "YYYY-MM-DDTHH:MM:SSZ" format
        """
        return int(date[0:4])

    def agg_stats(self, stats, by_year=True, by_month=True):
        """
        Aggregates statistics overall, by year, and by month.
        """
        sum_total = sum([int(i[0]) for i in stats])
        month_total = None
        yr_total = None

        if by_month:
            month_total = {i: 0 for i in range(1, 13)}
            for i in stats:
                month_total[i[1]] += int(i[0])
        if by_year:
            yr_total = {int(k): 0 for k in set([i[2] for i in stats])}
            for i in stats:
                yr_total[i[2]] += int(i[0])

        return sum_total, month_total, yr_total

    def plot_bar(self, x, y, title, file_path):
        """
        Saves a bar plot to file_path specified by user.
        """
        plt.figure()
        plt.bar(x, y)
        plt.suptitle(title)
        plt.savefig(file_path)

    def plot_monthly_stats(self, stats, stat_name, file_name="monthly_stats.png"):
        """
        Plot monthly statistics.
        """
        y = [stats.get(i, 0) for i in range(1, 13)]
        x = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        self.plot_bar(
            x, y, "{} per month".format(stat_name), "/".join([self.path, file_name])
        )

    def plot_yearly_stats(self, stats):
        """
        Get x and y for plotting yearly statistics.
        """
        x = list(stats.keys())
        x.sort()
        y = [stats.get(i, 0) for i in x]
        x = [str(i) for i in x]
        return x, y

    def get_all_stats(self, videos):
        """
        Get all video stats.
        """
        views = [
            [
                i.get("statistics", {}).get("viewCount", None),
                i.get("snippet", {}).get("publishedAt", None),
            ]
            for i in videos
        ]
        views = [
            [i[0], self.extract_month(i[1]), self.extract_year(i[1])]
            for i in views
            if i[0] is not None and i[1] is not None
        ]
        likes = [
            [
                i.get("statistics", {}).get("likeCount", None),
                i.get("snippet", {}).get("publishedAt", None),
            ]
            for i in videos
        ]
        likes = [
            [i[0], self.extract_month(i[1]), self.extract_year(i[1])]
            for i in likes
            if i[0] is not None and i[1] is not None
        ]
        coms = [
            [
                i.get("statistics", {}).get("commentCount", None),
                i.get("snippet", {}).get("publishedAt", None),
            ]
            for i in videos
        ]
        coms = [
            [i[0], self.extract_month(i[1]), self.extract_year(i[1])]
            for i in coms
            if i[0] is not None and i[1] is not None
        ]
        dislikes = [
            [
                i.get("statistics", {}).get("dislikeCount", None),
                i.get("snippet", {}).get("publishedAt", None),
            ]
            for i in videos
        ]
        dislikes = [
            [i[0], self.extract_month(i[1]), self.extract_year(i[1])]
            for i in dislikes
            if i[0] is not None and i[1] is not None
        ]
        return views, coms, likes, dislikes

    def get_and_plot_stats(self, videos):
        """
        Stats analysis by year and month.
        """
        views, coms, likes, dislikes = self.get_all_stats(videos)

        # agg stats
        self.sum_views, monthly_views, yearly_views = self.agg_stats(views)
        self.sum_likes, monthly_likes, yearly_likes = self.agg_stats(likes)
        self.sum_dislikes, monthly_dislikes, yearly_dislikes = self.agg_stats(dislikes)
        self.sum_comments, monthly_comments, yearly_comments = self.agg_stats(coms)

        if "yearly" in self.analysis_type:
            # save yearly stats
            fig, axs = plt.subplots(2, 2)
            x, y = self.plot_yearly_stats(yearly_views)
            axs[0, 0].bar(x, y)
            axs[0, 0].set_title("Views")
            x, y = self.plot_yearly_stats(yearly_comments)
            axs[0, 1].bar(x, y)
            axs[0, 1].set_title("Comments")
            x, y = self.plot_yearly_stats(yearly_likes)
            axs[1, 0].bar(x, y)
            axs[1, 0].set_title("Likes")
            x, y = self.plot_yearly_stats(yearly_dislikes)
            axs[1, 1].bar(x, y)
            axs[1, 1].set_title("Dislikes")
            fig.tight_layout()
            fig.savefig(self.path + "/yearly_stats.png")

        if "monthly" in self.analysis_type:
            # save monthly stats
            self.plot_monthly_stats(
                monthly_views, stat_name="views", file_name="monthly_views.png"
            )
            self.plot_monthly_stats(
                monthly_likes, stat_name="likes", file_name="monthly_likes.png"
            )
            self.plot_monthly_stats(
                monthly_dislikes, stat_name="dislikes", file_name="monthly_dislikes.png"
            )
            self.plot_monthly_stats(
                monthly_comments, stat_name="comments", file_name="monthly_comments.png"
            )

    def plot_trending_tags(self, videos):
        """
        Tags analysis.
        """
        tags = [
            [
                i.get("snippet", {}).get("tags", None),
                i.get("snippet", {}).get("publishedAt", None),
            ]
            for i in videos
        ]
        tags = [
            [
                list(set([j.lower() for j in i[0]])),
                self.extract_month(i[1]),
                self.extract_year(i[1]),
            ]
            for i in tags
            if i[0] is not None and i[1] is not None
        ]
        overall_tags = Counter([j for sublist in [i[0] for i in tags] for j in sublist])
        self.get_wordcloud(overall_tags, file_name="videos.png")

    def plot_comment_locations(self, comments):
        """
        Locations in comments analysis.
        """
        comments_list = extract_locations.get_comments_list(comments)
        locations = extract_locations.extract_locations(comments_list)
        self.get_wordcloud(Counter(locations), file_name="comment_locations.png")

    def export_to_pdf(self):
        """
        Exporting report to pdf.
        """
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", "B", size=20)
        pdf.cell(
            200, 10, txt="Analysis for {} on YouTube".format(self.keyword), ln=1, align="C"
        )
        pdf.set_font("Arial", size=14)
        pdf.cell(
            200,
            10,
            txt="Between {} and {}".format(self.start_date[0:10], self.end_date[0:10]),
            ln=2,
            align="C",
        )
        pdf.cell(200, 10, txt="", ln=3, align="C")
        pdf.set_font("Arial", "B", size=14)
        pdf.cell(200, 10, txt="Overall statistics", ln=4, align="L")
        pdf.set_font("Arial", size=12)
        pdf.cell(
            200, 10, txt="No. of views: {}".format(self.sum_views), ln=5, align="L"
        )
        pdf.cell(
            200,
            10,
            txt="No. of comments: {}".format(self.sum_comments),
            ln=6,
            align="L",
        )
        pdf.cell(
            200, 10, txt="No. of likes: {}".format(self.sum_likes), ln=7, align="L"
        )
        pdf.cell(
            200,
            10,
            txt="No. of dislikes: {}".format(self.sum_dislikes),
            ln=8,
            align="L",
        )
        pdf.cell(200, 10, txt="", ln=9, align="L")

        pdf.set_font("Arial", "B", size=14)
        new_inx = 10
        if "yearly" in self.analysis_type:

            pdf.cell(200, 10, txt="Yearly breakdown of statistics", ln=10, align="L")
            pdf.image(self.path + "/yearly_stats.png", w=150, h=150)
            new_inx = new_inx + 1

        if "monthly" in self.analysis_type:

            pdf.cell(200, 10, txt="Monthly breakdown of statistics", ln=11, align="L")
            pdf.image(self.path + "/monthly_views.png", w=150, h=90)
            pdf.image(self.path + "/monthly_comments.png", w=150, h=90)
            pdf.image(self.path + "/monthly_likes.png", w=150, h=90)
            pdf.image(self.path + "/monthly_dislikes.png", w=150, h=90)
            new_inx = new_inx + 1

        pdf.cell(
            200,
            10,
            txt="The content spoken about in the published videos",
            ln=new_inx,
            align="L",
        )
        pdf.image(self.path + "/videos.png", w=75, h=75)

        pdf.cell(
            200,
            10,
            txt="The locations mentioned in comments",
            ln=new_inx + 1,
            align="L",
        )
        pdf.image(self.path + "/comment_locations.png", w=75, h=75)

        output_path = self.path + "/{}_report.pdf".format(self.keyword.replace(" ", "_"))
        pdf.output(output_path)

        return output_path


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate analysis report")
    parser.add_argument(
        "-path",
        "--path",
        type=str,
        required=True,
        help="Path to the directory you want to save the data in",
    )
    parser.add_argument(
        "-k", "--keyword", type=str, default=None, help="Keyword to search data for"
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
        "-analysis",
        "--analysis",
        type=str,
        required=False,
        default="yearly,monthly",
        choices=["yearly", "monthly", "yearly,monthly", "monthly,yearly"],
        help="Analysis to be run yearly, monthly, or both.",
    )

    args = parser.parse_args()
    KEYWORD = args.keyword
    START_DATE = args.start_date
    END_DATE = args.end_date
    ANALYSIS_TYPE = args.analysis.split(",")  # choices - yearly, monthly
    API_TOKEN = args.token
    PATH = args.path
    rgen = ReportGenerator(PATH, KEYWORD, START_DATE, END_DATE, ANALYSIS_TYPE)

    api = crawler.YouTubeCrawler(key=API_TOKEN)
    # Fetch data from the api
    [videos, comments] = run_crawl.get_videos_and_comments(
        api, keyword=KEYWORD, start_date=START_DATE, end_date=END_DATE, comment_limit=10
    )
    print("\nFetched data\n")
    rgen.get_and_plot_stats(videos)
    rgen.plot_trending_tags(videos)
    rgen.plot_comment_locations(comments)
    print("\nFetched plots\n")
    output_path = rgen.export_to_pdf()
    print("\nGenerated pdf here {}\n".format(output_path))

    # trending tags analysis - overall (TODO: by year and month)
    # TODO: keyphrase extraction from video titles
    # TODO: Breakdown analysis by year and month

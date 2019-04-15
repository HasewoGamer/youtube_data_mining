#!/usr/bin/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import csv

DEVELOPER_KEY = "your API key"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY
                    )

def get_channel_items(youtube, options):
    search_response = youtube.search().list(
        channelId=options.id,
        part="id,snippet",
        maxResults=options.max_results,
        order=options.order,
    ).execute()

    items = search_response.get("items", [])

    content_id_list = [item["id"]["videoId"] for item in items if item["id"]["kind"]=="youtube#video"]

    return content_id_list

def get_playlist_items(youtube, options):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    search_response = youtube.playlistItems().list(
        part="id,snippet",
        playlistId=options.id,
        maxResults=50
    ).execute()

    items = search_response.get("items", [])
    content_id_list = [item["snippet"]["resourceId"]["videoId"] for item in items if item["snippet"]["resourceId"]["kind"]=="youtube#video"]

    return content_id_list


argparser.add_argument("--id", help="PlaylistsIDs", default="PLpMxP1ekqJYhnEgeEI2lASE9b5lX07orz")
args = argparser.parse_args()

play_list = get_playlist_items(youtube, args)
title = "yumesaki_pokemonUSUM"

with open("%s.txt" % (title), "wt") as f:
    f.write(' '.join(play_list))
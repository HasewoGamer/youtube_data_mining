#!/usr/bin/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import csv

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "your API key"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_saerch_video(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  data = []

  for video_id in options.id:
    videos_response = youtube.videos().list(
      part="id,snippet,statistics",
      id=video_id
    ).execute()

    data.append(videos_response.get("items", [])[0])

  return data

if __name__ == "__main__":
  argparser.add_argument("--id", help="VideoIDs", default="Sq5QW3YqipM", nargs='*')
  args = argparser.parse_args()

  try:
    raw_data = youtube_saerch_video(args)
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

  list_name = '道明寺晴翔マリオカート実況'

  with open('%s.csv' % (list_name), 'w') as csvfile:
    writer = csv.writer(csvfile, lineterminator='\n')
    writer.writerow(['id', 'title', 'publishedDatetime', 'viewCount', 'likeCount', 'dislikeCount', 'commentCount', 'list_name'])
    for dat in raw_data:
      writer.writerow([dat['id'], dat['snippet']['title'], dat['snippet']['publishedAt'], dat['statistics']['viewCount'], dat['statistics']['likeCount'], dat['statistics']['dislikeCount'], dat['statistics']['commentCount'], list_name])




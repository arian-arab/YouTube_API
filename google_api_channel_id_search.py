from apiclient.discovery import build
import numpy as np
import pandas as pd
import os

channel_id = 'UCN0VXYoN2ZdC7s8OFC_zHCg'


DEVELOPER_KEY = ''
youtube = build("youtube", "v3",developerKey=DEVELOPER_KEY)

token = None

channel_response = youtube.channels().list(part = 'contentDetails,id,snippet,statistics',id = channel_id,maxResults=50).execute()

number_of_videos = float(channel_response['items'][0]['statistics']['videoCount'])
channel_title = channel_response['items'][0]['snippet']['title']


number_of_requests = int(np.ceil(number_of_videos/50))

def extract_info_items(items):    
    channel_id = []
    video_id = []
    channel_title = []
    video_title = []
    description = []
    published_time = [] 
    no_of_views = []
    no_of_likes = []
    no_of_dislike = []
    no_of_comments = []
    url = []
    video_length = []
    for i in items:
        channel_id.append(i['snippet']['channelId'])
        video_id.append(i['id']['videoId'])
        channel_title.append(i['snippet']['channelTitle'])
        video_title.append(i['snippet']['title'])
        description.append(i['snippet']['description'])
        published_time.append(i['snippet']['publishedAt'])        
    for i in video_id:
        url.append("https://www.youtube.com/watch?v=" + i)        
        request = youtube.videos().list(part = 'liveStreamingDetails,contentDetails,statistics',id = i).execute()
        items = request['items']
        statistics = items[0]['statistics']
        content_details = items[0]['contentDetails']
        video_length.append(content_details['duration'])
        if 'viewCount' in statistics:
            no_of_views.append(statistics['viewCount'])
        else:
            no_of_views.append(0)
        if 'likeCount' in statistics:
            no_of_likes.append(statistics['likeCount'])
        else:
            no_of_likes.append(0)
        if 'dislikeCount' in statistics:
            no_of_dislike.append(statistics['dislikeCount'])
        else:
            no_of_dislike.append(0)
        if 'commentCount' in statistics:
            no_of_comments.append(statistics['commentCount'])
        else: 
            no_of_comments.append(0)        
    info = {'url':url,
            'channel_id':channel_id,
            'video_id':video_id,
            'channel_title':channel_title,
            'video_title':video_title,
            'description': description,
            'published_time': published_time,
            'no_of_views':no_of_views,
            'no_of_likes':no_of_likes,
            'no_of_dislikes':no_of_dislike,
            'no_of_comments':no_of_comments,
            'video_length':video_length}
    info_df = pd.DataFrame(data=info)    
    return info_df

token = None
data = []
for i in range(number_of_requests):
    search_response = youtube.search().list(type="video",pageToken=token,part="id,snippet", maxResults=50, channelId = channel_id).execute()
    items = search_response['items']
    if 'nextPageToken' in search_response:
        token = search_response['nextPageToken']
    data.append(extract_info_items(items))
data = pd.concat(data)

cwd = os.getcwd()
data.to_csv (cwd+'\channel_'+channel_title+'.csv', index = False, header=True)

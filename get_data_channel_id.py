from apiclient.discovery import build
import numpy as np
import pandas as pd

channel_id = 'UCK8XIGR5kRidIw2fWqwyHRA' #Reducible
DEVELOPER_KEY = ''

youtube = build("youtube", "v3",developerKey=DEVELOPER_KEY)

channel_response = youtube.channels().list(part = 'contentDetails,id,snippet,statistics',id = channel_id,maxResults=50).execute()
channel_number_of_videos = float(channel_response['items'][0]['statistics']['videoCount'])
channel_title = channel_response['items'][0]['snippet']['title']
channel_description = channel_response['items'][0]['snippet']['description']
channel_subscriber_count = float(channel_response['items'][0]['statistics']['subscriberCount'])
channel_video_count = channel_response['items'][0]['statistics']['videoCount']
channel_view_count = channel_response['items'][0]['statistics']['viewCount']

token = None
items = []
number_of_requests = int(np.ceil(channel_number_of_videos/50))
for i in range(number_of_requests):
    print(i)
    search_response = youtube.search().list(type="video",pageToken=token,part="id,snippet", maxResults=50, channelId = channel_id).execute()
    items.append(search_response['items'])  
    if 'nextPageToken' in search_response:
        token = search_response['nextPageToken']

videos_id = []
videos_title = []
videos_published_time = []
videos_description = []
for j in items:
    videos_id.append([i['id']['videoId'] for i in j])
    videos_title += [i['snippet']['title'] for i in j]
    videos_published_time += [i['snippet']['publishedAt'] for i in j]
    videos_description += [i['snippet']['description'] for i in j]

request = []
for i in videos_id:
    ids = []
    ids = [j+',' for j in i]
    ids = ''.join(ids)
    ids = ids[:-1]
    request.append(youtube.videos().list(part = 'liveStreamingDetails,contentDetails,statistics',id = ids).execute())
ids = []
for i in videos_id:
    ids += i
videos_id = ids
del ids

content_details = []
statistics = []
for j in request:
    items = j['items']
    content_details += ([i['contentDetails'] for i in items])
    statistics += ([i['statistics'] for i in items])

videos_duration = []
videos_caption = []
videos_definition = []
videos_definition = []
videos_dimension = []
videos_licensed_content = []
videos_projection = []
for i in content_details:
    videos_duration.append(i['duration'])
    videos_caption.append(i['caption'])
    videos_definition.append(i['definition'])
    videos_dimension.append(i['dimension'])
    videos_licensed_content.append(i['licensedContent'])
    videos_projection.append(i['projection'])

videos_no_of_views = []
videos_no_of_likes = []
videos_no_of_dislike = []
videos_no_of_comments = []
for i in statistics:
    if 'viewCount' in i:
        videos_no_of_views.append(i['viewCount'])
    else:
        videos_no_of_views.append(0)
    if 'likeCount' in i:
        videos_no_of_likes.append(i['likeCount'])
    else:
        videos_no_of_likes.append(0)
    if 'dislikeCount' in i:
        videos_no_of_dislike.append(i['dislikeCount'])
    else:
        videos_no_of_dislike.append(0)
    if 'commentCount' in i:
        videos_no_of_comments.append(i['commentCount'])
    else: 
        videos_no_of_comments.append(0) 
    
videos_url = [] 
for i in videos_id:
     videos_url.append("https://www.youtube.com/watch?v=" + i)  
 
info = {'url':videos_url,
            'channel_id':channel_id,
            'channel_title':channel_title,
            'channel_number_of_videos': channel_number_of_videos,
            'channel_description':channel_description,
            'channel_subscriber_count':channel_subscriber_count,
            'channel_video_count':channel_video_count,
            'channel_view_count':channel_view_count,    
            'videos_id':videos_id,            
            'videos_title':videos_title,
            'videos_description': videos_description,
            'videos_published_time': videos_published_time,
            'videos_no_of_views':videos_no_of_views,
            'videos_no_of_likes':videos_no_of_likes,
            'videos_no_of_dislikes':videos_no_of_dislike,
            'videos_no_of_comments':videos_no_of_comments,
            'videos_video_length':videos_duration}
data = pd.DataFrame(data=info)         
data.to_csv('data.csv', index = False, header=True)
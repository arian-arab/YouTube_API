from apiclient.discovery import build
import pandas as pd
import os

#https://developers.google.com/youtube/v3/docs/search/list?apix_params=%7B%22part%22%3A%5B%22id%22%5D%2C%22q%22%3A%22physics%22%7D
#https://developers.google.com/youtube/v3/docs/videos/list?apix_params=%7B%22part%22%3A%5B%22snippet%2CcontentDetails%2Cstatistics%22%5D%2C%22id%22%3A%5B%22Ks-_Mh1QhMc%22%5D%7D
query = 'bbc hard talk'
no_of_pages = 1 #each page gives 50 search results

DEVELOPER_KEY = ''
youtube = build("youtube", "v3",developerKey=DEVELOPER_KEY)

def extract_info(query, number_of_pages):    
    token = None
    data  = []
    for  i in range(number_of_pages):
        search_response = youtube.search().list(q=query,type="video",pageToken=token, order = 'relevance', part="id,snippet", maxResults=50, location=None, locationRadius=None).execute()
        items = search_response['items']
        token = search_response['nextPageToken']
        data.append(extract_info_items(items))
    data = pd.concat(data)
    return data

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

data = extract_info(query, no_of_pages)

cwd = os.getcwd()
data.to_csv (cwd+'\query_'+query+'.csv', index = False, header=True)
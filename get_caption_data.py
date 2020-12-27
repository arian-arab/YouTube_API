from pytube import YouTube
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_name = 'data'
data = pd.read_csv(file_name+'.csv')

text_data = []
for i in range(data.shape[0]):
    url = data['url'][i]
    my_video = YouTube(url)
    
    language_code = my_video.captions.lang_code_index
    if language_code:        
        if 'en' in language_code:
            caption = my_video.captions.get_by_language_code('en')
        elif 'a.en' in language_code:
            caption = my_video.captions.get_by_language_code('a.en')
        elif 'en-GB' in language_code:
            caption = my_video.captions.get_by_language_code('en-GB')     
        else:
            caption = []
            
        if caption:
            caption_text = caption.generate_srt_captions()
            text_data.append(caption_text)
            
words = []            
for i in text_data :
    i = np.array(i.split("\n"))
    lin_space = np.arange(2,len(i),4)        
    i = i[lin_space]
    i = [i.split(' ') for i in i]
    i = np.concatenate(i)        
    words.append(i)

get_shape = lambda x: x.shape[0]
total_number_of_words = sum(list(map(get_shape,words)))

all_words = np.concatenate(words)
unique_words, unique_counts = np.unique(all_words,return_counts = True)

I = [True if not i.isdigit() else False for i in unique_words]    
unique_words = unique_words[I]
unique_counts = unique_counts[I]

I = [True if i.isalpha() else False for i in unique_words] 
unique_words = unique_words[I]
unique_counts = unique_counts[I]

I = np.flip(np.argsort(unique_counts))

unique_words = unique_words[I]
unique_counts = unique_counts[I]
plt.plot(unique_counts[:20])
plt.xticks(np.arange(1, 20, step=1), unique_words[:20], rotation = 45)
plt.ylabel('Word Counts')
plt.title('Channel Name = '+data['channel_title'][0]+'\nTotal number of words ='+str(total_number_of_words))
import pandas as pd
from pytube import YouTube
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('channel_BBC HARDtalk.csv')

text_data = []
for i in range(data.shape[0]):
    url = data['url'][i]
    my_video = YouTube(url)
    
    language_code = my_video.captions.lang_code_index
    if language_code:
        language_code = list(language_code.keys())[0]
        caption = my_video.captions.get_by_language_code(language_code)
        caption_text = caption.generate_srt_captions()        
        caption_text = np.array(caption_text.split("\n"))        
        
        lin_space = np.arange(2,len(caption_text),4)        
        caption_text = caption_text[lin_space]        
        caption_text = [i.split(' ') for i in caption_text]        
        caption_text = np.concatenate(caption_text)        
        text_data.append(caption_text)

get_shape = lambda x: x.shape[0]
total_number_of_words = sum(list(map(get_shape,text_data)))

text_data_all = np.concatenate(text_data)
unique_words, unique_counts = np.unique(text_data_all,return_counts = True)

I = [True if not i.isdigit() else False for i in unique_words]    
unique_words = unique_words[I]
unique_counts = unique_counts[I]

I = [True if i.isalpha() else False for i in unique_words] 
unique_words = unique_words[I]
unique_counts = unique_counts[I]

I = np.flip(np.argsort(unique_counts))

unique_words = unique_words[I]
unique_counts = unique_counts[I]

plt.plot(np.unique(unique_counts))
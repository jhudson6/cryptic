# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:22:04 2017

@author: jhudson
"""

import feedparser
import pandas as pd
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

d = feedparser.parse('https://news.google.com/news/rss/headlines/section/q/cryptocurrency/cryptocurrency?ned=us&hl=en&gl=US')

##print title
print(d['feed']['title'])

##resolve relative links
print(d['feed']['link'])

##parse escaped HTML
print(d.feed.subtitle)

##see # of entries
print(len(d['entries']))

##each entry in feed is a dictionary. use [0] to print first
print(d['entries'][0]['title'])

##print first entry and its link
print(d.entries[0]['link'])

##for loop to print all posts and links
for post in d.entries:
    print(post.title+":\n"+post.link+"\n")
    
##feed type and version
print(d.headers)

##content-type from header
print(d.headers.get('content-type'))

titles = pd.DataFrame(columns = ['Title'], dtype = str)
for i in range(0,len(d['entries'])):
    titles = titles.append(pd.Series(d['entries'][i]['title'],index=['Title']), ignore_index = True)


test = titles.Title[1]
tokens = nltk.word_tokenize(test)
tagged = nltk.pos_tag(tokens)
entities = nltk.chunk.ne_chunk(tagged)
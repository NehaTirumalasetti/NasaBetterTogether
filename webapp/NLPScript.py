'''
Keyword Extraction for Step 2
- to obtain keywords from user's query
- these keywords are passed to the web scraper to validate authenticity
'''

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import requests
from bs4 import BeautifulSoup

import requests
import tweepy
import numpy as np
import base64
import json
import csv
import preprocessor as p

def pre_process(text):    
    # lowercase
    text = text.lower()

    #remove tags
    text = re.sub("","",text)

    # remove special characters and digits
    text = re.sub("(\\d|\\W)+"," ",text)

    return text

def get_stop_words(stop_file_path):
    """load stop words """
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)


#----------------------------------RSS FEEDS---------------------------------------------------
def script(text):    
    from nltk.corpus import stopwords 
    from nltk.tokenize import word_tokenize 
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    links_to_add = [] # Use for adding all links to CSV
    
    text = pre_process(text)
    #print(text)

    #load a set of stop words
    stopwords = get_stop_words("resources/stopwords.txt")

    #get the text column 
    docs = list(text.split(" ")) 

    #create a vocabulary of words, 
    #ignore words that appear in 85% of documents, 
    #eliminate stop words
    cv = CountVectorizer(max_df = 0.85, stop_words = stopwords, max_features = 10000)
    word_count_vector = cv.fit_transform(docs)
    warn_words = []
    warn_words = list(cv.vocabulary_.keys())[:10]
    #warn_words.append('covid')
    
    '''
    Check with RSS feeds
    - similarity score obtained with each website
    - added to total
    '''
    from nltk.corpus import stopwords 
    urls = []
    url1 = "https://blog.amnestyusa.org/feed/" #DESCRIPTION 
    url2 = "https://news.un.org/feed/subscribe/en/news/topic/human-rights/feed/rss.xml" #DESCRIPTION
    url3 = "https://bhr.stern.nyu.edu/blogs?format=RSS" #DESCRIPTION
    urls1 = [url1, url2, url3]
    total = 0
    links = []
    for everyUrl in urls1:
        resp = requests.get(everyUrl)
        soup = BeautifulSoup(resp.content, features="xml")
        items = soup.findAll('item')
        # Program to measure the similarity between  
        # two sentences using cosine similarity. first sentence
        # is from query (text) and second is description
        for item in items:
            Y = item.description.text
            linkForItem = item.link.text

            # tokenization 
            X_list = word_tokenize(text)  
            Y_list = word_tokenize(Y) 

            # sw contains the list of stopwords 
            sw = set(stopwords.words('english')) 
            l1 = []; l2 = [] 

            # remove stop words from the string 
            X_set = {w for w in X_list if not w in sw}  
            Y_set = {w for w in Y_list if not w in sw} 

            # form a set containing keywords of both strings  
            rvector = X_set.union(Y_set)  
            for w in rvector: 
                if w in X_set: l1.append(1) # create a vector 
                else: l1.append(0) 
                if w in Y_set: l2.append(1) 
                else: l2.append(0) 
            c = 0
  
            # cosine formula  
            for i in range(len(rvector)): 
                c += l1[i] * l2[i] 
            if (((sum(l1) * sum(l2)) ** 0.5) != 0):        
                cosine = c / float((sum(l1) * sum(l2)) ** 0.5) 
            if (cosine > 0):
                total += 1;
                print("Yes! Found similar sentence ", cosine) 
                links.append(linkForItem)
    print("All Links: ", links)
    '''
    Check with RSS feeds for 2 more urls
    - similarity score obtained with each website
    - added to total
    '''
    from nltk.corpus import stopwords 
    url4 = "https://www.nchrd.org/category/news/feed/" #Description has img src etc. unneeded stuff
    url5 = "https://www.theguardian.com/law/human-rights/rss" #Description has img src etc. unneeded stuff
    url6 = "https://www.reddit.com/r/humanrights/.rss?format=xml"
    urls2 = [url4]

    for everyUrl in urls2:
        resp = requests.get(everyUrl)
        soup = BeautifulSoup(resp.content, features="xml")
        wholeItems = soup.findAll('item')
        for everyItem in wholeItems:
            linkForItem = everyItem.link.text
            p_tags = everyItem.description.text
            Y = p_tags.replace(']]>', '')
     
            # Program to measure the similarity between  
            # two sentences using cosine similarity. first sentence
            # is from query (text) and second is description

            # tokenization 
            X_list = word_tokenize(text)  
            Y_list = word_tokenize(Y) 

            # sw contains the list of stopwords 
            sw = set(stopwords.words('english'))  
            l1 = []; l2 = [] 
  
            # remove stop words from the string 
            X_set = {w for w in X_list if not w in sw}  
            Y_set = {w for w in Y_list if not w in sw} 

            # form a set containing keywords of both strings  
            rvector = X_set.union(Y_set)  
            for w in rvector: 
                if w in X_set: l1.append(1) # create a vector 
                else: l1.append(0) 
                if w in Y_set: l2.append(1) 
                else: l2.append(0) 
            c = 0

            # cosine formula  
            for i in range(len(rvector)): 
                c += l1[i] * l2[i] 
            if (((sum(l1) * sum(l2)) ** 0.5) != 0):        
                cosine = c / float((sum(l1) * sum(l2)) ** 0.5) 
            if (cosine > 0):
                total += 1;
                print("Yes! Found similar sentence ", cosine)
                links.append(linkForItem)
    print("All Links: ", links)
    '''
    Check with news sites
    - for news articles with similar keywords, check text similarity and add to the similarity score
    '''

#------------------------------------------ WEB SCRAPING -------------------------------------------------

    from nltk.corpus import stopwords 
    import bs4
    from bs4 import BeautifulSoup as soup
    from urllib.request import urlopen
    import pandas as pd
    from htmldate import find_date
    import csv 
    from csv import writer

    filename = "NEWS.csv"
    f = open(filename,"a", encoding = 'utf-8')
    headers = ["Statement","Link","Date"]

    upperframe = []    
    news_url = "https://news.google.com/news/rss"
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()
    soup_page = soup(xml_page,"xml")
    news_list = soup_page.findAll("item")

    frame = []
    Links = "Links.csv"
    f1 = open(Links, "a", encoding = 'utf-8')
    linkhead = ['Link']
    for news in news_list:
        texts = news.title.text
        lsts = warn_words
        for l in lsts:
            if l in texts:
                print(news.title.text)
                print(news.link.text)
                print("\n")

                date = find_date(news.link.text)
                upperframe = [news.title.text, news.link.text, date]
                frame.append(upperframe)
                links.append(news.link.text)
                break
    print(links)
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile)  
        csvwriter.writerow(headers) 
        csvwriter.writerows(frame)  

    with open(Links, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(linkhead)
        csvwriter.writerows(links)
    
    for titleNews in frame:
        title = titleNews[0]
        # tokenization 
        X_list = word_tokenize(text)  
        Y_list = word_tokenize(Y) 

        # sw contains the list of stopwords 
        sw = stopwords.words('english')  
        l1 = []; l2 = [] 
        # remove stop words from the string 
        X_set = {w for w in X_list if not w in sw}  
        Y_set = {w for w in Y_list if not w in sw} 
        # form a set containing keywords of both strings  
        rvector = X_set.union(Y_set)  
        for w in rvector: 
            if w in X_set: l1.append(1) # create a vector 
            else: l1.append(0) 
            if w in Y_set: l2.append(1) 
            else: l2.append(0) 
        c = 0
        # cosine formula  
        for i in range(len(rvector)): 
            c += l1[i] * l2[i] 
        if (((sum(l1) * sum(l2)) ** 0.5) != 0):        
            cosine = c / float((sum(l1) * sum(l2)) ** 0.5) 
        if (cosine > 0):
            total += 1;
            #print("Yes! Found similar sentence ", cosine)
    
    #--------------TWITTER---------------------------------------------------------------------------


    from nltk.corpus import stopwords 
    #twitter credentials
    consumer_key = 'XXXXXXXXXXXXXXXXXXXXXX'
    consumer_secret_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    #Reformat the keys and encode them
    key_secret = '{}:{}'.format(consumer_key, consumer_secret_key).encode('ascii')
    #Transform from bytes to bytes that can be printed
    b64_encoded_key = base64.b64encode(key_secret)
    #Transform from bytes back into Unicode
    b64_encoded_key = b64_encoded_key.decode('ascii')

    #authentication
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    print(auth_resp.status_code) #200 indicates successful authentication
    access_token = auth_resp.json()['access_token'] #auth response stored
    #print(warn_words)

    #warn_words = ['killed', 'police', 'brutality', 'systemic', 'racism', 'Covid']
    rows = []
    twt_total = 0
    for ip in warn_words:
        search_headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

        search_params = {
            'q': ip,
            'lang': 'eu',
            'result_type': 'mixed'
        }

        search_url = 'https://api.twitter.com/1.1/search/tweets.json'
        search_resp = requests.get(search_url, headers=search_headers, params=search_params)
        # print(ip+" "+str(search_resp.status_code))
        search_data = search_resp.json()  # result of search in json format
        # print(search_data)
        with open('raw_tweets.json', 'a+', encoding='utf-8') as f:  # Will be needed later
            # data = json.load(f.decode('utf8'))
            # temp=data['statuses']
            # temp.append(data)
            json.dump(search_data, f, ensure_ascii=False, indent=4)  # file that has all tweets collected for each keyword
        with open('raw_tweets_temp.json', 'w', encoding='utf-8') as f:
            json.dump(search_data, f, ensure_ascii=False, indent=4)  # temp file that is overwritten for every keyword

        # print(ip+" "+str(len(search_data['statuses'])))
        for i in range(0, len(search_data['statuses'])):
            # print('tweet number',i+1,'=',search_data['statuses'][i])
            row = []
            row.append(search_data['statuses'][i]['id'])
            row.append(search_data['statuses'][i]['id_str'])
            row.append(ip)
            row.append(search_data['statuses'][i]['created_at'])
            row.append(search_data['statuses'][i]['text'])
            row.append(search_data['statuses'][i]['favorite_count'])
            row.append(search_data['statuses'][i]['retweet_count'])
            # print(row)
            rows.append(row)
    # print(rows)

    # fields = ["id","id_str","keyword","created_at","text","likes","retweeted","hashtags"]
    # with open('tweets.csv', 'w', encoding='utf-8') as f: #to collect tweets over time change permission to a+ and remove writerow fields
    #     csvwriter = csv.writer(f)
    #     csvwriter.writerow(fields)
    #     csvwriter.writerows(rows)


    cleaned_tweets = []
    for row in rows:
        # print(row[4])#is the text of tweet
        # extracting hashtags
        h = [s for s in row[4].split() if s.startswith('#')]
        # print(h)
        row.append(h)
        # add hashtag segmentation here later
        # forming a separate feature for cleaned tweets
        # cleaned tweets: don't have stop words, don't have hashtags URLS, Emojis, mentions
        s = p.clean(row[4]).lower()
        row.append(s)
        cleaned_tweets.append(s)
        s = word_tokenize(s)
        s = [i for i in s if i not in stopwords.words('english')]
        row.append(s)

    fields = ["id", "id_str", "keyword", "created_at", "tweet_text", "likes", "retweeted", "hashtags", "clean_text_str",
              "clean_text"]
    with open('tweets.csv', 'w',
              encoding='utf-8') as f:  # to collect tweets over time change permission to a+ and remove writerow fields
        csvwriter = csv.writer(f)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

    print(cleaned_tweets)

    for i in cleaned_tweets:
        # Program to measure the similarity between  
        # two sentences using cosine similarity. first sentence
        # is from query (text) and second is description

        # tokenization 
        X_list = word_tokenize(text)  
        Y_list = word_tokenize(i) 

        # sw contains the list of stopwords 
        sw = set(stopwords.words('english'))  
        l1 = []; l2 = [] 

        # remove stop words from the string 
        X_set = {w for w in X_list if not w in sw}  
        Y_set = {w for w in Y_list if not w in sw} 

        # form a set containing keywords of both strings  
        rvector = X_set.union(Y_set)  
        for w in rvector: 
            if w in X_set: l1.append(1) # create a vector 
            else: l1.append(0) 
            if w in Y_set: l2.append(1) 
            else: l2.append(0) 
        c = 0

        # cosine formula  
        for i in range(len(rvector)): 
            c += l1[i] * l2[i] 
        if (((sum(l1) * sum(l2)) ** 0.5) != 0):        
            cosine = c / float((sum(l1) * sum(l2)) ** 0.5) 
        if (cosine > 0):
            twt_total += 1;
            print("Yes! Found similar sentence ", cosine)
            #links.append([linkForItem])
    print("Twitter Total ",twt_total)

    return links, twt_total

#run the script
#list_of_links = script("Chinese Uyghurs community is being brutally outcast")
#print("List of Links ", list_of_links)

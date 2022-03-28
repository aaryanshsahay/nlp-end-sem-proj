import re
import nltk
import numpy as np
import psycopg2
import os

def casefolding(sentence):
    return sentence.lower()

def cleaning(sentence):
    return re.sub(r'[^a-z]', ' ', re.sub("’", '', sentence))

def tokenization(sentence):
    return sentence.split()

def sentence_split(paragraph):
    return nltk.sent_tokenize(paragraph)

def word_freq(data):
    w = []
    for sentence in data:
        for words in sentence:
            w.append(words)
    bag = list(set(w))
    res = {}
    for word in bag:
        res[word] = w.count(word)
    return res

def sentence_weight(data):
    weights = []
    for words in data:
        temp = 0
        for word in words:
            temp += wordfreq[word]
        weights.append(temp)
    return weights

def summarizer(article,n):
    global wordfreq
    sentence_list = sentence_split(article)
    data = []
    for sentence in sentence_list:
        data.append(tokenization(cleaning(casefolding(sentence))))
    data = (list(filter(None, data)))
    wordfreq = word_freq(data)
    rank = sentence_weight(data)
    result = ''
    sort_list = np.argsort(rank)[::-1][:n]
    print(sort_list)
    print(n)
    for i in range(n):
        result += '{} '.format(sentence_list[sort_list[i]])
    return result





def connect_db():
    global conn
    db_name=os.environ.get('database_name')
    db_user=os.environ.get('database_user')
    db_pass=os.environ.get('database_password')
    conn=psycopg2.connect("dbname=postgres user=postgres password=password")
    



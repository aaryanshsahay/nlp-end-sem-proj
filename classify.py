import pandas as pd
import numpy as np

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


from sklearn.feature_extraction.text import CountVectorizer

from sklearn.linear_model import LogisticRegression

import pickle



def load_weights():
	try:
		global cv,model
		with open('models/cv.pk', 'rb') as f:
			cv = pickle.load(f)

		model=pickle.load(open('models/model','rb'))

		print('cv weights and model weights loaded successfully.')

	except:
		print('some error occured in loading weights.')

def remove_tags(title):
    remove = re.compile(r'<.*?>')
    return re.sub(remove, '', title)

def special_chars(title):
    reviews = ''
    for x in title:
        reviews = reviews + x
    else:
        reviews = reviews + ' '
    return reviews

def convert_lower(title):
    return title.lower()

def remove_stopwords(title):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(title)
    return [x for x in words if x not in stop_words]


def lemmatize_word(title):
    wordnet = WordNetLemmatizer()
    return " ".join([wordnet.lemmatize(word) for word in title])


def preprocess_text(title):
    r_inp = remove_tags(title)
    s_inp = special_chars(r_inp)
    l_imp = convert_lower(s_inp)
    stopinp = remove_stopwords(l_imp)
    leminp = lemmatize_word(stopinp)
    t_inp = cv.transform([leminp]).toarray()
    
    return t_inp

def generate_result(title):
	load_weights()
	x=preprocess_text(title)
	result=model.predict(x)

	ref={
		0:'Entertainment',
		1:'Other',
		2:'Politics',
		3:'Sports',
		4:'Technology'
	}

	result=ref[result[0]]

	return result


def summarize_and_classify(title,content,timestamp):
	try:
		summary=summarizer(content,3)
		news_label=generate_result(title)
	except:
		summary=summarizer(content,2)
		news_label=generate_result(title)

	return summary,news_label,timestamp
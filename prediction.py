import psycopg2
import os

from summarizer import *
from classify import *

import streamlit as st

from datetime import datetime

import time

import keyboard


st.title('Quick News')

enter_news_title=[]
pol_news_title=[]
tech_news_title=[]
spo_news_title=[]
oth_news_title=[]


def connect_db():
	global conn
	db_name=os.environ.get('database_name')
	db_user=os.environ.get('database_user')
	db_pass=os.environ.get('database_password')
	conn=psycopg2.connect("dbname=postgres user=postgres password=password")
	
def disconnect_db():
	conn.close()

def get_data_from_db():
	# make connection to db
	connect_db()

	# get data from db
	command='''SELECT * FROM TABLE1_RAW_DATA '''
	
	#command="SELECT * FROM TABLE1_RAW_DATA ORDER BY news_title  DESC "
	curr=conn.cursor()
	curr.execute(command)
	data=curr.fetchall()
	

	# disconnect db
	disconnect_db()
	return data[-10:]

def summarize_and_classify(title,content):
	summary=summarizer(content,2)
	news_label=generate_result(title)

	return summary,news_label



def fill_data():
	#while True:
		# get most recent news article
		data=get_data_from_db()
		for value in data:
			if value[0] in tech_news_title or value[0] in oth_news_title or value[0] in enter_news_title or value[0] in spo_news_title or value[0] in pol_news_title:
				# if title already exists in list
				# duplicate values
				print('duplicate news article obtained, skipping.')
				pass
			
			else:
				# unique news articles


				summary,news_label=summarize_and_classify(str(value[0]),str(value[1]))
				


				if news_label=='Technology':
					print('news was classified as technology')
					tech_news_title.append(value[0])
					with st.expander("TECHNOLOGY"):
						st.header(value[0])
						st.write(summary+'\n\nLink to original article - {}\n\n{}'.format(value[-2], datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

					time.sleep(30)
					
				
				elif news_label=='Other':
					print('news was classified as other')
					oth_news_title.append(value[0])
					with st.expander("OTHER"):
						st.header(value[0])
						st.write(summary+'\n\nLink to original article - {}\n\n{}'.format(value[-2],datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

					time.sleep(30)
					
				elif news_label=='Entertainment':
					print('news was classified as entertainment')
					enter_news_title.append(value[0])
					with st.expander("OTHER"):
						st.header(value[0])
						st.write(summary+'\n\nLink to original article - {}\n\n{}'.format(value[-2],datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
					
					time.sleep(30)

				elif news_label=='Sports':
					print('news was classified as sports')
					spo_news_title.append(value[0])
					with st.expander("SPORTS"):
						st.header(value[0])
						st.write(summary+'\n\nLink to original article - {}\n\n{}'.format(value[-2],datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
					
					time.sleep(30)

				elif news_label=='Politics':
					print('news was classified as politics')
					pol_news_title.append(value[0])
					with st.expander("POLITICS"):
						st.header(value[0])
						st.write(summary+'\n\nLink to original article - {}\n\n{}'.format(value[-2],datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

					time.sleep(30)

def display():
	with st.expander("TECHNOLOGY"):
	        col1,col2=st.columns(2)
	        with col1:
	            st.header(tech_news_title[0])
	            st.write(tech_news[0])
	        with col2:
	            st.header(tech_news_title[1])
	            st.write(tech_news[1])
	        


	with st.expander("ENTERTAINMENT"):
	        col1,col2=st.columns(2)
	        with col1:
	            st.header(enter_news_title[0])
	            st.write(enter_news[0])
	        with col2:
	            st.header(enter_news_title[1])
	            st.write(enter_news[1])
	        
	with st.expander("SPORTS"):
	        col1,col2=st.columns(2)
	        with col1:
	            st.header(spo_news_title[0])
	            st.write(spo_news[0])
	        with col2:
	            st.header(spo_news_title[1])
	            st.write(spo_news[1])
	        
	with st.expander("POLITICS"):
	        col1,col2=st.columns(2)
	        with col1:
	            st.header(pol_news_title[0])
	            st.write(pol_news[0])
	        with col2:
	            st.header(pol_news_title[1])
	            st.write(pol_news[1])
	        
	with st.expander("OTHER"):
	        col1,col2=st.columns(2)
	        with col1:
	            st.header(oth_news_title[0])
	            st.write(oth_news[0])
	        with col2:
	            st.header(oth_news_title[1])
	            st.write(oth_news[1])


if __name__=='__main__':
	while True:
		fill_data()
		time.sleep(30)
		#keyboard.press_and_release('f5')



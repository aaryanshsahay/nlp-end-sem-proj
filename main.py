from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import requests
import lxml
import psycopg2
from selenium import webdriver
import time


def connect_db():
	global conn
	db_name=os.environ.get('database_name')
	db_user=os.environ.get('database_user')
	db_pass=os.environ.get('database_password')
	conn=psycopg2.connect("dbname={} user={} password={}".format(db_name,db_user,db_pass))
	

def disconnect_db():
	conn.close()

def insert_into_db(table_name,news_title,news_content,news_link,news_timestamp):
	curr=conn.cursor()
	query="SELECT news_title FROM {} WHERE news_link='{}'".format(table_name,news_link)
	curr.execute(query)
	res=curr.fetchone()
	if res==None:
		# means entry doesnt exist in database
		query="INSERT INTO {} VALUES ('{}','{}','{}','{}');".format(table_name,news_title,news_content,news_link,news_timestamp)
	
		curr.execute(query)
		conn.commit()
		print('DATA ADDED !!!!')
	else:
		# means entry is already present in database.
		# skip those articles.
		pass
		

	curr.close()

def get_data_from_db(label):
	# make connection to db
	connect_db()

	# get data from db
	curr=conn.cursor()
	command="SELECT * FROM demo_1 where class_label='{}'".format(label)
	curr.execute(command)
	data=curr.fetchone()
	
	# disconnect db
	disconnect_db()
	
	print(data)

def initialize_selenium():
	global driver
	chrome_driver=os.environ.get('chrome_driver_path')
	options=webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--incognito')
	options.add_argument('--headless')
	driver=webdriver.Chrome(chrome_driver,chrome_options=options)

def get_recent_data():
	url='https://www.dnaindia.com/headlines'

	driver.get(url)

	page_source=driver.page_source

	soup=BeautifulSoup(page_source,'lxml')
	card_div=soup.find_all('div',class_='list-news')

	url_links=[]
	for divs in card_div:
		link=divs.find('a')['href']
		url_links.append(link)

	
	return url_links

def get_appropriate_data(link):
	try:
		link_new='https://dnaindia.com'+str(link)

		driver.get(link_new)

		page_source=driver.page_source
		soup=BeautifulSoup(page_source,'lxml')
		
		news=soup.find('div',class_='article-box-details')
		news_title=news.find('h1').text
		news_date=news.find('div',class_='article-author-txt').text.split('|')[-1].split('Updated: ')[1]
		news_data=soup.find('div',class_='article-description')
		
		news_content=news_data.find_all('p')
		for i in range(len(news_content)):
			news_content[i]=news_content[i].text
		content=' '
		content=content.join(news_content)

		# removing quotes as it will cause error in performing db actions
		news_title=news_title.replace('"','')
		news_title=news_title.replace("'","")
		content=content.replace('"','')
		content=content.replace("'","")

		res={
			'title':news_title,
			'content':content,
			'link':link_new,
			'timestamp':news_date
		}
		return res 
	except:
		print('error occured in collecting data, skipping to next one.')
		pass

if __name__=='__main__':
	load_dotenv()
	connect_db()
	initialize_selenium()
	table_name='TABLE1_RAW_DATA'
	while True:
		url_links=get_recent_data()
		print('='*100)
		print('TOTAL NUMBER OF URLS : ',len(url_links))
	
		for i in range(len(url_links)):
			try:
				data=get_appropriate_data(url_links[i])
				title,content,link,timestamp=data['title'],data['content'],data['link'],data['timestamp']
				insert_into_db(table_name,title,content,link,timestamp)
				#print('='*50,'data addded sleeping for 30 secs','='*50)
				time.sleep(2*30)
			except:
				pass
		time.sleep(15*60)
		print('sleeping for 15 mins')
	
	disconnect_db()
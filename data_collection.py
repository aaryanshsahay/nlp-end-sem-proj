import pandas as pd
from bs4 import BeautifulSoup
import requests
import lxml
import os

from selenium import webdriver

from dotenv import load_dotenv



def initialize_selenium():
	global driver
	chrome_driver=os.environ.get('chrome_driver_path')
	options=webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--incognito')
	options.add_argument('--headless')
	#options.add_argument('--disable-blink-features=AutomationControlled')
	driver=webdriver.Chrome(chrome_driver,chrome_options=options)


def get_recent_data(query,page):
	url='https://www.dnaindia.com/{}&page={}'.format(query,page)

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
		print(link)
		print(type(link))
	
		link_new='https://dnaindia.com'+str(link.strip())
		print(link_new)
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
		#news_label=link.split('/')[1]

		res={
			'title':news_title,
			'content':content,
			'link':link_new,
			'timestamp':news_date,
		}

		return res 

	except:
		print('error occured in obtaining data, skipping to next one.')
		pass
		
# tech
# politics
# entertainment
# sports
# other

def app(queries,pages,labels):
	'''
	input -> 

	output ->

	abstract ->
	'''
	page_no=[int(i) for i in range(pages)]
	title,content,timestamp,news_label,links=[],[],[],[],[]


	try:
		
		# iterating through all queries
		for query,page,tag in zip(queries,page_no,labels):
			url_links=get_recent_data(query,page)
			print('total news articles : ',len(url_links))
		# iterating through all links in a query search
			for link in url_links:
				res=get_appropriate_data(link)
				title.append(res['title'])
				content.append(res['content'])
				links.append(res['link'])
				timestamp.append(res['timestamp'])
				news_label.append(str(tag))

	except:
		pass

	data={
			'title':title,
			'content':content,
			'news_label':news_label,
			'link':links
		}

	df=pd.DataFrame(data)
	print(df.shape)
	print(df.head())

	df.to_csv('final_data.csv',index=False)

	print('data saved to local directory')
	
	#except:
 	#	print('error occured while getting data, skipping and collecting the next one.')
 	#	pass




if __name__=='__main__':
	load_dotenv()

	initialize_selenium()
	print('='*50,'selenium initialized','='*50)

	query=input('Enter Query :')
	news_label=input('Enter News Label')
	pages=int(input('Enter total number of pages to search for :'))

	title,content,timestamp,links,news_labels=[],[],[],[],[]



	for page in range(pages):
		url_links=get_recent_data(query,page)
		try:

			for link in url_links:
				output=get_appropriate_data(link)
				title.append(output['title'])
				content.append(output['content'])
				timestamp.append(output['timestamp'])
				links.append(output['link'])
				news_labels.append(str(news_label))
				print('got data for one article')
		except:
			print('skipping one article')
			pass
		print('collection succesfull for  page : {}/{}'.format(page,pages))
		
	print('collection successful for all pages.')

	data={
		'title':title,
		'content':content,
		'timestamp':timestamp,
		'link':links,
		'label':news_labels
	}

	df=pd.DataFrame(data)

	print(df.shape)

	df.to_csv('{}.csv'.format(query),index=False)
	print('data collected for query : {} succesfully'.format(query))






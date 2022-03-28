import re
import nltk
import numpy as np

import psycopg2

# database functions
from main import connect_db,disconnect_db

# summarization funcitons
from summarizer import *
# classificatoin functions
from classify import *
# database connections





def get_data_from_db():
	query='''SELECT * FROM scraped_data limit 10'''
	curr=conn.Cursor()
	curr.execute(query)
	data=curr.fetchone()

def prepare_data():
	pass

def display_data():
	pass


if __name__=='__main__':
	while True:
		connect_db()

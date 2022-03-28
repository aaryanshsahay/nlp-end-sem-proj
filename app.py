import streamlit as st
from dotenv import load_dotenv
# database functions
from main import connect_db,disconnect_db
# summarization functions
from summarizer import *
# classification functions
from classify import *


import os
import psycopg2

import re







while True:

    with st.expander("TECHNOLOGY"):
        col1,col2,col3=st.columns(3)
        with col1:
            st.header("news 1")
            st.write("content")
        with col2:
            st.header("news 2")
            st.write("content")
        with col3:
            st.header("news 3")
            st.write("content")

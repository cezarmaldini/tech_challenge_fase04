from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import os

load_dotenv()

# Cache para evitar reconexões em cada reload
@st.cache_resource
def get_engine():
    db_url = os.getenv('URL_DB')
    engine = create_engine(db_url)
    return engine
import streamlit as st
from streamlit_option_menu import option_menu  # for horizontal menu bar
from streamlit_card import card  # for car element from extras
from streamlit_extras.switch_page_button import switch_page  # for switching pages
from streamlit_lottie import st_lottie
import requests
from st_functions import st_button, load_css

import pandas as pd
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
# with st.form(key='my_form'):
#     username = st.text_input('Username')
#     password = st.text_input('Password')
#     st.form_submit_button('Login')
# getting the data set



books = pd.read_csv("D:\internship\data\dataset\Books.csv")

ratings = pd.read_csv("D:\internship\data\dataset\Ratings.csv")

users = pd.read_csv("D:\\internship\\data\\dataset\\Users.csv")

name_ratings = pd.merge(books, ratings, on='ISBN')

# popular-based

name_ratings.sort_values('Book-Rating', ascending=False, inplace=True)

num_ratings = name_ratings.groupby(['Book-Title', 'Image-URL-M']).count(
)['Book-Rating'].reset_index().rename(columns={'Book-Rating': 'Count'})

mean_ratings = name_ratings.groupby(
    ['Book-Title']).mean()['Book-Rating'].reset_index().rename(columns={'Book-Rating': 'Mean'})

mean_ratings.sort_values('Mean', inplace=True)

popular_df = pd.merge(num_ratings, mean_ratings, on='Book-Title')

popular_10 = popular_df[popular_df['Count'] >= 250].sort_values(
    'Mean', ascending=False).head(10).groupby(['Book-Title']).size().reset_index()
pop_10 = pd.DataFrame(popular_10)

# colaborative-filtering-based

x = name_ratings.groupby('User-ID').count()['Book-Rating'] > 200
literate_users = x[x].index

filter1 = name_ratings['User-ID'].isin(literate_users)
filtered_rating = name_ratings[filter1]

y = name_ratings.groupby('Book-Title').count()['Book-Rating'] >= 50
popular_books = y[y].index

filter2 = filtered_rating['Book-Title'].isin(popular_books)
final_df = filtered_rating[filter2]

pt = final_df.pivot_table(
    index='Book-Title', columns='User-ID', values='Book-Rating')
pt.replace(np.nan, 0, inplace=True)

similarity = cosine_similarity(pt)


def recommender(books):
    index = np.where(pt.index == books)[0][0]
    similar_items = sorted(
        list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:11]

    for i in similar_items:
        st.write(pt.index[i[0]])

# animation
def load_lottieurl(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
lottie_coding = load_lottieurl("https://assets1.lottiefiles.com/private_files/lf30_j57dwawi.json")


# streamlit

def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
st.set_page_config(page_title='Book-Recommendation-system',page_icon='📘',layout='wide')
# st.set_page_config(layout='wide')
st.title('📘 Book Recommender System')
st.write("###")
st.write("###")
selected = option_menu(
    menu_title=None,
    options=['Home', 'About Me', 'Contact'],
    icons=['house', 'person', 'envelope'],
    default_index=0,
    orientation='horizontal',
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "#0d47a1", "font-size": "25px"},
        "nav-link": {"font-size": "25px", "text-align": "center", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#bbdefb"},
    }
)

if selected == 'Home':
     col1, col2 = st.columns(2)
     with col1:
        st.title('Top 10 *Books*')
        st.dataframe(pop_10)
     with col2:
        st.write("###")
        st_lottie(lottie_coding,height=400,key="coding")
        st.write("###")
     st.code('# Tip: If you are confuse how to use this, then just Double-click the Selected one from the Top 10 df')
     with st.form(key='my_form'):
        st.title('Recommender')
        search = st.text_input('Search')
        if st.form_submit_button('Sumbit'):
            st.title("Recommended")
            recommender(search)
        
if selected == 'About Me':
    st.subheader("About Me")
    st.write("""
        What I have done
        1. Intern at ineuron.ai 
        2. Persuing b.tech in Artificial Intellengence and machine learning 
        3. Having the specialisation in machine learning (by DeepLearning.AI)
        """)
    st.write("###")
    st.write("---")
    st.write("###")
    icon_size = 35
    st.subheader('Profile')
    st_button('linkedin','https://www.linkedin.com/in/%F0%9F%8E%8A-shuvam-mandal-%F0%9F%8E%8A-02a18a212/',icon_size)
    st_button('twitter','https://twitter.com/00_shuv_00?t=SAkG2hst8S9qtn5r8GKCCQ&s=09',icon_size)
if selected == 'Contact':
    with st.form(key='my_form1'):
        st.title('Contact')
        name = st.text_input('Name')
        email= st.text_input('Email')
        comments = st.text_area('Comment') 
        if st.form_submit_button('Sumbit'):
            with open('detail.txt', 'a') as f:
                f.writelines(f'{name}  |  {email} | {comments}\n')

hide_default_format = """
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""

st.markdown(hide_default_format, unsafe_allow_html=True)


# background img for webapp

pg_bg_custom = """
    <style>
    [data-testid = " stAppViewContainer"]{
    background-image = "https://images.unsplash.com/photo-1454117096348-e4abbeba002c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80";
    background-size= cover;
    }
    [data-testid = " stToolbar"]{
    right: 2rem
    }
    </style>
"""
st.markdown(pg_bg_custom, unsafe_allow_html=True)

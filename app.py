# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 17:55:26 2023

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:36:00 2023

@author: user
"""

import streamlit as st
import pickle
import pandas as pd
from scipy.stats import pearsonr


users_df=pickle.load(open("user_model.pkl",'rb'))
popular = pickle.load(open('popular.pkl','rb'))

def recommend(target_user):
    user_books=users_df[users_df['user_id']==target_user]
    new_user=user_books[['user_id', 'Book-Title', 'rating']]
    other_users = users_df[users_df['Book-Title'].isin(new_user['Book-Title'].values)]
    other_users=other_users[other_users['user_id'] != target_user]
    users_mutual_books = other_users.groupby(['user_id'])
    top_users = sorted(users_mutual_books, key=lambda x: len(x[1]), reverse=True)[:50]
    
    pearson_corr = {}
    for user_id, book_s in top_users:
        # Books should be sorted
        books_new = book_s.sort_values(by='user_id')
        book_list = books_new['Book-Title'].values

        new_user_ratings = new_user[new_user['Book-Title'].isin(book_list)]['rating'].values 
        user_ratings = books_new[books_new['Book-Title'].isin(book_list)]['rating'].values

        corr = pearsonr(new_user_ratings, user_ratings)
        pearson_corr[user_id] = corr[0]
    #pearson_corr=recommend(select_userid)
    pearson_df = pd.DataFrame(columns=['user_id', 'similarity_index'], data=pearson_corr.items())
    pearson_df = pearson_df.sort_values(by='similarity_index', ascending=False)[:5]
    users_rating = pearson_df.merge(users_df, on='user_id', how='inner')
    users_rating['weighted_rating'] = users_rating['rating'] * users_rating['similarity_index']
    
    #removing books that already read by target
    users_ratings = users_rating.merge(new_user, how="left", on=["Book-Title"], indicator=True)
    users_ratings=users_ratings[users_ratings['_merge']=='left_only'].drop(['user_id_y', 'rating_y','_merge'],
                            axis=1).rename(columns={"user_id_x":"user_id",'rating_x':"rating"})
    grouped_ratings = users_ratings.groupby('Book-Title').sum()[['similarity_index', 'weighted_rating']]
    recommend_books = pd.DataFrame()
    
    # Add average recommendation score
    recommend_books['avg_reccomend_score'] = grouped_ratings['weighted_rating']/grouped_ratings['similarity_index']
    recommend_books['Book-Title'] = grouped_ratings.index
    recommend_books = recommend_books.reset_index(drop=True).drop_duplicates('Book-Title')
    recommend_books = recommend_books.merge(users_df,on='Book-Title',how='inner').drop(['ISBN', 'Year-Of-Publication', 'Publisher'], axis=1)
    
    # Left books with the highest 10 score
    recommend_books = recommend_books[(recommend_books['avg_reccomend_score'] >= 1)].drop_duplicates('Book-Title').sort_values(by='avg_reccomend_score', 
                                                                                                 ascending=False).head(10)
    recommend_books=recommend_books['Book-Title'].reset_index(drop=True)
    return recommend_books 

image_url = popular['Image-URL-M'].tolist()
book_title = popular['Book-Title'].tolist() 
book_author = popular['Book-Author'].tolist()
total_ratings = popular['num_rating'].tolist()
avg_ratings = popular['avg_rating'].tolist()

st.sidebar.title(":blue[_Top 50 Books_]")
if st.sidebar.button("SHOW"):
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.image(image_url[0])
        st.text(book_author[0])
        st.text("Ratings:" + str(total_ratings[0]))
        st.text("Avg.Rating:" + str(round(avg_ratings[0],2)))
    with col2:
        st.image(image_url[1])
        st.text(book_author[1])
        st.text("Ratings:" + str(total_ratings[1]))
        st.text("Avg.Rating:" + str(round(avg_ratings[1],2)))
    with col3:
        st.image(image_url[2])
        st.text(book_author[2])
        st.text("Ratings:" + str(total_ratings[2]))
        st.text("Avg.Rating:" + str(round(avg_ratings[2],2)))
    with col4:
        st.image(image_url[3])
        st.text(book_author[3])
        st.text("Ratings:" + str(total_ratings[3]))
        st.text("Avg.Rating:" + str(round(avg_ratings[3],2)))
    with col5:
        st.image(image_url[4])
        st.text(book_author[4])
        st.text("Ratings:" + str(total_ratings[4]))
        st.text("Avg.Rating:" + str(round(avg_ratings[4],2)))
        
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.image(image_url[5])
        st.text(book_author[5])
        st.text("Ratings:" + str(total_ratings[5]))
        st.text("Avg.Rating:" + str(round(avg_ratings[5],2)))
    with col2:
        st.image(image_url[6])
        st.text(book_author[6])
        st.text("Ratings:" + str(total_ratings[6]))
        st.text("Avg.Rating:" + str(round(avg_ratings[6],2)))
    with col3:
        st.image(image_url[7])
        st.text(book_author[7])
        st.text("Ratings:" + str(total_ratings[7]))
        st.text("Avg.Rating:" + str(round(avg_ratings[7],2)))
    with col4:
        st.image(image_url[8])
        st.text(book_author[8])
        st.text("Ratings:" + str(total_ratings[8]))
        st.text("Avg.Rating:" + str(round(avg_ratings[8],2)))
    with col5:
        st.image(image_url[9])
        st.text(book_author[9])
        st.text("Ratings:" + str(total_ratings[9]))
        st.text("Avg.Rating:" + str(round(avg_ratings[9],2)))

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.image(image_url[10])
        st.text(book_author[10])
        st.text("Ratings:" + str(total_ratings[10]))
        st.text("Avg.Rating:" + str(round(avg_ratings[10],2)))
    with col2:
        st.image(image_url[11])
        st.text(book_author[11])
        st.text("Ratings:" + str(total_ratings[11]))
        st.text("Avg.Rating:" + str(round(avg_ratings[11],2)))
    with col3:
        st.image(image_url[12])
        st.text(book_author[12])
        st.text("Ratings:" + str(total_ratings[12]))
        st.text("Avg.Rating:" + str(round(avg_ratings[12],2)))
    with col4:
        st.image(image_url[13])
        st.text(book_author[13])
        st.text("Ratings:" + str(total_ratings[13]))
        st.text("Avg.Rating:" + str(round(avg_ratings[13],2)))
    with col5:
        st.image(image_url[14])
        st.text(book_author[14])
        st.text("Ratings:" + str(total_ratings[14]))
        st.text("Avg.Rating:" + str(round(avg_ratings[14],2)))  
    
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.image(image_url[15])
        st.text(book_author[15])
        st.text("Ratings:" + str(total_ratings[15]))
        st.text("Avg.Rating:" + str(round(avg_ratings[15],2)))
    with col2:
        st.image(image_url[16])
        st.text(book_author[16])
        st.text("Ratings:" + str(total_ratings[16]))
        st.text("Avg.Rating:" + str(round(avg_ratings[16],2)))
    with col3:
        st.image(image_url[17])
        st.text(book_author[17])
        st.text("Ratings:" + str(total_ratings[17]))
        st.text("Avg.Rating:" + str(round(avg_ratings[17],2)))
    with col4:
        st.image(image_url[18])
        st.text(book_author[18])
        st.text("Ratings:" + str(total_ratings[18]))
        st.text("Avg.Rating:" + str(round(avg_ratings[18],2)))
    with col5:
        st.image(image_url[19])
        st.text(book_author[19])
        st.text("Ratings:" + str(total_ratings[19]))
        st.text("Avg.Rating:" + str(round(avg_ratings[19],2))) 

st.title("Recommend Books")

users_list=users_df['user_id'].drop_duplicates().values
select_userid=st.selectbox('Enter target userid', users_list)
if st.button('recommend'):
    recommendation=recommend(select_userid)
    for i in recommendation:
        st.write(i)
    
        


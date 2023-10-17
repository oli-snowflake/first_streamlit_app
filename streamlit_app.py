import streamlit as st
import snowflake.connector
from urllib.error import URLError


def insert_row_snowflake(new_fruit) : 
    with my_cur = my_cnx.cursor() :
        my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")


my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("Hello from Snowflake:")
st.dataframe(my_data_rows)

st.title("This is my first streamlit cloud app !! ")

st.header("Breakfast menu")

st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')

st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas as pd
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]



# Display the table on the page.
st.dataframe(fruits_to_show)

st.header("Fruityvice Fruit Advice!")

import requests
try :
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice :
        st.error("Please  choose a fruit !")
    else :
        st.write('The user entered ', fruit_choice)
        insert_row_snowflake(fruit_choice)
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
        # write your own comment -what does the next line do? 
        fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
        # write your own comment - what does this do?
        st.dataframe(fruityvice_normalized)
except URLError as e :
    st.error()
##st.text(fruityvice_response.json())
st.stop()




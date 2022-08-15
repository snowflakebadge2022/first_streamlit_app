import streamlit
import pandas 
import snowflake.connector
from urllib.error import URLError
import requests

streamlit.title("My parents new healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(my_fruit_list) 

streamlit.header("Fruityvice Fruit Advice!")
try: 
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice: 
    streamlit.error("please select a fruit to get information")
    streamlit.write('The user entered ', fruit_choice)
  else: 
    back_from_function = get_fruitvice_data(fruit_choice) 
    streamlit.dataframe(fruityvice_normalized)
    
except URLError as e: 
    streamlit.error()
  


streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
  with  my_cnx.cursor() as my_cur: 
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall(); 
if streamlit.button('get fruit load list'): 
     my_data_rows = get_fruit_load_list()
     my_cnx.close()
     streamlit.dataframe(my_data_rows)
def insert_row_snowflake(new_fruit):
  with  my_cnx.cursor() as my_cur: 
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return "thanks for adding" + new_fruit 
    

add_my_fruit = streamlit.text_input('what fruit would you like to add?')
if streamlit.button('add fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)


def get_fruitvice_data(fruit_choice): 
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

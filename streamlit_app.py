import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(this_fruit_choice);
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #streamlit.text(fruityvice_response)
    streamlit.text(fruityvice_response.json())

    # flatten the json
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
 
streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))   # works
#fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avacado', 'Strawberries'])  # doesn't work
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
    back_from_functin = get_fruityvice_data(fruit_choice)
   # put the flattened json into a pandas dataframe
    streamlit.dataframe(back_from_function)

except URLERROR as e:
    streamlit.error()
    
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# challenge lab
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', add_my_fruit)

# This has flow control problems
my_cur.execute("insert into fruit_load_list values ('from streamlit')")

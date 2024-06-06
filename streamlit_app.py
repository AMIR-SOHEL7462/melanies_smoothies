# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothies! :cup_with_straw:")
st.write(
    """Choose the Fruit you want on your Smoothies!"""
)

cnx = st.connection("snowflake")
session = cnx.session()

title = st.text_input("Name On Smoothie")
st.write("The name on your smoothie will be: ", title)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()


ingredients_list = st.multiselect(
    'Choose upto 5 ingredients: ', my_dataframe , max_selections = 5
)


if ingredients_list: 
    ingredients_string = ''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
        st.subheader(each_fruit + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + each_fruit)
        fv_df = st.dataframe(data = fruityvice_response.json(),use_container_width=True)
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """' , '""" + title + """')"""
    time_to_submit = st.button('Submit Order')
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ title + '!',  icon="✅")




    

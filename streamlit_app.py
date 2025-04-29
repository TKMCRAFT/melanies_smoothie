# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you wat in your custom Smoothie!")

Name_on_order = st.text_input("Name on smothie: ")
st.write("The name on your smoothie will be: ", Name_on_order)

cnx = st.connection("snowflake")
session = get_active_session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingrediants:'
    ,my_dataframe
    ,max_selections = 5
)
if ingredients_list:

    ingredients_string = ''
    for  fruit_chosen in ingredients_list:
        ingredients_string +=  fruit_chosen+' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df= st.text(smoothiefroot_response.json(),use_container_width = True)
        
   # search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
   # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    #st.write(ingredients_list) 

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','"""+ Name_on_order +""""')"""
    
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        


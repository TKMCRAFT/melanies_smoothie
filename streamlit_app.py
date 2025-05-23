# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on smoothie: ")
st.write("The name on your smoothie will be:", name_on_order)

# Initialize Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

try:
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
    pd_df = my_dataframe.to_pandas()

    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        my_dataframe,
        max_selections=5
    )

    if ingredients_list:
        ingredients_string = ''
        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '
            
            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
           # st.write('The search value for', fruit_chosen, 'is', search_on, '.')
            
            st.subheader(fruit_chosen + ' Nutrition Information')
            # Fixed the API URL by removing "watermelon" from the string
            fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on.lower()}")
            fv_df = st.dataframe(fruityvice_response.json(), use_container_width= True)
        
        my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                    VALUES ('""" + ingredients_string + """','""" + name_on_order + """')"""
        
        time_to_insert = st.button('Submit Order')
        
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")

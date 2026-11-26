# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on the Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
                 'Choose Up To 5 ingredients :',
                  my_dataframe,
                  max_selections = 5
)


if ingredients_list : 
    ingredients_string = ''
    for fruit_Chosen in ingredients_list:
        ingredients_string += fruit_Chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefruit_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen") 
        sf_df = st.dataframe(data = smoothiefruit_response.json(), use_container_width = True )

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Sumbit Order')
    if time_to_insert :
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")

# New section to display smoothiefruit nutrition information



# smoothiefruit_response = requests.get( "https://my.smoothiefroot.com/api/fruit/watermelon")

# st.text(smoothiefruit_response.json())


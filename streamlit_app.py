# Import python packages
import streamlit as st


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

import streamlit as st
Name_on_Smoothi = st.text_input('Name on Smoothie')
st.write("The Name on Smoothie will be:", Name_on_Smoothi)
cnx =st.connection("snowflake")
session = cnx.session()

from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections  = 5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_list)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" +ingredients_string+ """','""" +Name_on_Smoothi+ """')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    st.stop()

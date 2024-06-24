# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothies will be:',name_on_order)
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list= st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string= ' '.join(fruit for fruit in ingredients_list)
    insert_stmt="""insert into smoothies.public.orders(ingredients,name_on_order) values
    ('"""+ingredients_string+"""','"""+name_on_order+"""')"""
    insert_time=st.button('Submit Order')
    if insert_time:
        session.sql(insert_stmt).collect()
        st.success('Your Smoothie is ordered! {}!'.format(name_on_order),icon="\u2705")  

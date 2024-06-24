# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothies will be:',name_on_order)
session =st.connection("snowflake").session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

# Convert snowpark dataframe to pandas so we can use the LOC function
pd_df=my_dataframe.to_pandas()

ingredients_list= st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredient_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(f'{fruit_chosen} Nutritional Information')
        # New section to display fruityvice nutrition information
        search_on =pd_df.loc[pd_df['FRUIT_NAME']==fruit_chosen, 'SEARCH_ON'].iloc[0]
        fv_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df = st.dataframe(data=fv_response.json(),use_container_width=True)
    insert_stmt="""insert into smoothies.public.orders(ingredients,name_on_order) values
    ('"""+ingredients_string+"""','"""+name_on_order+"""')"""
    insert_time=st.button('Submit Order')
    if insert_time:
        session.sql(insert_stmt).collect()
        st.success('Your Smoothie is ordered! {}!'.format(name_on_order),icon="\u2705")  

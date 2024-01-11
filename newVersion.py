#cd 'C:\Users\lghoualm\OneDrive - University of Tennessee\Desktop\Automated-categorical-data-cleaning-using-AI'
#

import openai
import numpy as np
import streamlit as st
import pandas as pd
from fuzzywuzzy import process



# Load OpenAI API key from secrets file
openai.api_key = st.secrets["pass"]


#_________________________________________________________________________________________
# Function to clean data using AI
def ai_clean(message):
    messages = [
    {
        "role": "system",
        "content": "Correct spelling errors. Standardize the words. Remove punctuation points. Convert everything to lowercase. "
    }
]

    #while True: 
    if message: 
        messages.append( 
            {"role": "user", "content": message}, 
        ) 
        chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=messages,  temperature=0.7, max_tokens=64,top_p=1
        ) 
    reply = chat.choices[0].message.content 
    return reply
#____________________________________________________________________________________________________

def find_closest_match(word, choices):
    return process.extractOne(word, choices)[0]
#____________________________________________________________________________________________________


#______________________________________Streamlit app_________________________________________________
st.sidebar.image("UT-logo.PNG")
st.sidebar.header('Automated categorical data cleaning using AI.')
st.sidebar.write("""
         ######  This app is made with python using Streamlit and OpenAI APIs to Automated the categorical data cleaning using AI. 
         """)


# Display the header
st.markdown("""<hr style="height:2px; border:none; color:#66CD00; background-color:orange;" /> """, unsafe_allow_html=True)
st.title('Automated Categorical Data Cleaning using AI.')
st.text('Inaugural UT IT Symposium: Engage, Enlighten, Enjoy.')
st.markdown("""<hr style="height:2px; border:none; color:#66CD00; background-color:orange;" /> """, unsafe_allow_html=True)


#___________________________________________PRESENT THE DATASET___________________________________________________________________________________________________

option = st.selectbox('Choose a dataset:', (' ', 'Load a dataset'))

if option == 'Load a dataset':
    uploaded_file = st.file_uploader("Upload a dataset (CSV file)", type=['csv'], accept_multiple_files=False, key=None, help=None,
                                             on_change=None, args=None, kwargs=None, disabled=False)
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        st.markdown("""<hr style="height:2px; border:none; color:#66CD00; background-color:orange;" /> """, unsafe_allow_html=True)
        st.write("""
         ####  Analyze a categorical field. 
         """)
        FieldName = st.text_input('Enter a categorical field name to analyze:', '')
        if st.button('Analyse field'):
            if FieldName in df.columns:
             unique_values = df[FieldName].unique()
             num_unique_values = df[FieldName].nunique()
             st.write('Variable name:', FieldName)
             st.write('Unique values', unique_values)
             st.write('Number of unique values', num_unique_values)
            else:
                st.warning("Enter a valid field name from the DataFrame.")

    
        st.markdown("""<hr style="height:2px; border:none; color:#66CD00; background-color:orange;" /> """, unsafe_allow_html=True)
        st.write("""
         ####  Clean and analyze a categorical field using AI. 
         """)
        FieldName1 = st.text_input('Enter a categorical field name to clean using AI', key='unique_key')


        #________________________________  Ai _________________________________
        if st.button('Clean the categorical field using AI'):
            if FieldName1 in df.columns:
        
              message= df[FieldName1].tolist()
              # Convert the list to a string without square brackets
              message = str(message)[1:-1]
              Respo = ai_clean(message)

             # Converting the string to a list
              result_list = '[' + Respo + ']'
              result_list =result_list.strip('[]')
              result_list = result_list.replace(',', '')
              #st.write('CHATGPT result:', result_list)

              # Extracting words from the string
              words = result_list.split()

              # Creating a DataFrame with a single column
              dataf = pd.DataFrame({'Words': words})
              #st.write('_______________CHATGPT result:',  dataf)

              dataf2 = pd.DataFrame({'Unique': dataf['Words'].drop_duplicates()})
              st.write('CHATGPT result (Distinct unqiue result):',  dataf2)

         #    # Apply the function to update the 'Fruit' column
              df[FieldName1] = df[FieldName1].apply(lambda x: find_closest_match(x, dataf2['Unique']))
              st.write('Cleanned data using Ai')
              st.write(df)
              unique_values1 = df[FieldName1].unique()
              num_unique_values1 = df[FieldName1].nunique()
              st.write('Variable name:', FieldName1)
              st.write('Unique values', unique_values1)
              st.write('Number of unique values', num_unique_values1)
            else:
                st.warning("Enter a valid categorical field name from the DataFrame.")
        

    



st.sidebar.write("""
         ######  Made by Lamis Ghoualmi  
         """)




#____________________________________________________________________________________________________________________________________
#____________________________________________________________________________________________________________________________________




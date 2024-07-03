import streamlit as st
import random
import pandas as pd


@st.cache_data
def read_oxford_file(file_path):
    # function to parse the HSK text files
    columns = ['word']
    # Read the file into a pandas DataFrame
    df = pd.read_csv(file_path, sep='\t', header=None, names=columns)
    return df

def reset_index():
    st.session_state.index = 0

def previous():
    st.session_state.index = max(st.session_state.index-1,0)

def nextone():
    st.session_state.index = min(st.session_state.index+1,49)

# Center the title in the middle of the page
st.markdown("<h1 style='text-align: center;'>Learn English Flashcard</h1>", unsafe_allow_html=True)

# Initialize session state for tracking progress
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'unknown_words_index' not in st.session_state:
    st.session_state.unknown_words_index = []

data_file = st.selectbox('Please choose level to start',['Oxford-3k','Oxford-5k'])
if not data_file:
    st.warning("Please select at least one data file to start!")
    st.stop()

df = read_oxford_file(f'data/Oxford/{data_file}.txt')
n_word = df.shape[0]
num_groups = (n_word // 50) + 1

# Create a list of group labels
group_labels = [f"{i*50+1}-{(i+1)*50}" for i in range(num_groups)]

# Select slider to choose the group
selected_group = st.select_slider("Select a group of rows to display:", options=group_labels,on_change=reset_index)

# Determine the start and end indices of the selected group
start_index = int(selected_group.split('-')[0]) - 1
end_index = int(selected_group.split('-')[1])

# Display the current word in larger font size
word = df.word.loc[st.session_state.index+start_index]
st.markdown(f"<h1 style='text-align: center; font-size: 6em;'>{word}</h1>", unsafe_allow_html=True)


# Navigation buttons and "I do not know this" button
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.button("⬅️ Previous",on_click=previous)

with col2:
    if st.button("I do not know this", key="unknown"):
        st.session_state.unknown_words_index.append(st.session_state.index+start_index)
with col3:
    st.button("Next ➡️",on_click=nextone)


# Display current word index
st.write(f"Flashcard {st.session_state.index + 1+start_index} of {n_word}")

# Check my status checkbox to display unknown words
if st.checkbox("Show the records of unknown words"):
    st.write(', '.join(df.word.loc[st.session_state.unknown_words_index].unique()))


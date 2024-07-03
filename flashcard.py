import streamlit as st
import random
import pandas as pd


@st.cache_data
def read_hsk_file(file_path):
    # function to parse the HSK text files
    columns = ['simplified', 'traditional', 'pingyin_a', 'pingyin', 'meaning']
    # Read the file into a pandas DataFrame
    df = pd.read_csv(file_path, sep='\t', header=None, names=columns)
    return df

# Center the title in the middle of the page
st.markdown("<h1 style='text-align: center;'>Learn Chinese Flashcard</h1>", unsafe_allow_html=True)

# Initialize session state for tracking progress
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'known_words_index' not in st.session_state:
    st.session_state.known_words_index = []
if 'unknown_words_index' not in st.session_state:
    st.session_state.unknown_words_index = []

data_file = st.selectbox('Please choose word set',['hsk_l1','hsk_l2','hsk_l3','hsk_l4','hsk_l5','hsk_l6'])
if not data_file:
    st.warning("Please select at least one data file to start!")
    st.stop()

df = read_hsk_file(f'data/HSK/{data_file}.txt')
n_word = df.shape[0]

col1, col2, col3, col4= st.columns(4)
with col2:
    show_pingyin = st.checkbox("Show Pingyin", value=False)
with col3:
    show_english = st.checkbox("Show English", value=False)

    
# Display the current flashcard

word = df.simplified.iloc[st.session_state.index]
if show_pingyin:
    pingyin = df.pingyin.iloc[st.session_state.index]
    st.markdown(f"<p style='text-align: center; font-size: 3em;'>{pingyin}</p>", unsafe_allow_html=True)

# Display word in larger font size
st.markdown(f"<h1 style='text-align: center; font-size: 6em;'>{word}</h1>", unsafe_allow_html=True)

if show_english:
    meaning = df.meaning.iloc[st.session_state.index]
    st.markdown(f"<p style='text-align: center; font-size: 3em;'>{meaning}</p>", unsafe_allow_html=True)

# Navigation buttons and "I do not know this" button
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("⬅️ Previous"):
        st.session_state.index = max(st.session_state.index-1,0)
        st.rerun()
with col2:
    if st.button("I do not know this", key="unknown"):
        st.session_state.unknown_words_index.append(st.session_state.index)
        st.rerun()
with col3:
    if st.button("Next ➡️"):
        st.session_state.index = min(st.session_state.index+1,n_word-1)
        st.rerun()

# Display current word index
st.write(f"Flashcard {st.session_state.index + 1} of {n_word}")

# Check my status checkbox
st.session_state.show_status = st.checkbox("Show the records of unknown words")

# Display learning status
if st.session_state.show_status:
    st.write(df.simplified.loc[st.session_state.unknown_words_index].unique())
#    st.write("### Words you know:")
#    st.write(", ".join(st.session_state.known_words))

#    st.write("### Words you do not know:")
#    st.write(", ".join(st.session_state.unknown_words))

# Automatically add words to known list if not marked unknown
#record_known()

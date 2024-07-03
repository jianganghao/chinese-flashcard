import streamlit as st
import random
import pandas as pd

# Function to read words from a file
def read_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file.readlines()]
    return words

@st.cache_data
def read_hsk_file(file_path):
    # function to parse the HSK text files
    columns = ['simplified', 'traditional', 'pinyin_a', 'pinyin_b', 'meaning']
    # Read the file into a pandas DataFrame
    df = pd.read_csv(file_path, sep='\t', header=None, names=columns)
    return df

# Center the title in the middle of the page
st.markdown("<h1 style='text-align: center;'>Flashcards</h1>", unsafe_allow_html=True)

# Load English words and Chinese characters
english_words = read_words('data/english_words.txt')
chinese_characters = read_words('data/chinese_characters.txt')

df = read_hsk_file('data/HSK/hsk_l1.txt')
#st.dataframe(df)
# Initialize session state for tracking progress
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'known_words' not in st.session_state:
    st.session_state.known_words = []
if 'unknown_words' not in st.session_state:
    st.session_state.unknown_words = []
if 'learning' not in st.session_state:
    st.session_state.learning = True
if 'language_preference' not in st.session_state:
    st.session_state.language_preference = 'English'
if 'show_status' not in st.session_state:
    st.session_state.show_status = False

def navigate(offset):
    st.session_state.index += offset
    st.session_state.index = max(0, min(st.session_state.index, len(current_words) - 1))

# Checkboxes to choose language preference
col1, col2, col3, col4= st.columns(4)
with col2:
    english_checkbox = st.checkbox("English", value=False)
with col3:
    chinese_checkbox = st.checkbox("Chinese", value=True)

if english_checkbox and chinese_checkbox:
    st.session_state.language_preference = random.choice(['English', 'Chinese'])
elif english_checkbox:
    st.session_state.language_preference = 'English'
elif chinese_checkbox:
    st.session_state.language_preference = 'Chinese'
else:
    st.warning("Please select at least one language.")
    st.stop()

# Set current words based on language preference
if st.session_state.language_preference == 'English':
    current_words = english_words
else:
    current_words = chinese_characters

# Function to record the unknown words
def record_unknown():
    word = current_words[st.session_state.index]
    if word not in st.session_state.unknown_words:
        st.session_state.unknown_words.append(word)
    if word in st.session_state.known_words:
        st.session_state.known_words.remove(word)

# Function to record the known words
def record_known():
    word = current_words[st.session_state.index]
    if word not in st.session_state.unknown_words and word not in st.session_state.known_words:
        st.session_state.known_words.append(word)

# Display the current flashcard
if st.session_state.learning:
    word = current_words[st.session_state.index]

    # Display word in larger font size
    st.markdown(f"<h1 style='text-align: center; font-size: 6em;'>{word}</h1>", unsafe_allow_html=True)

    # Navigation buttons and "I do not know this" button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Previous"):
            navigate(-1)
    with col2:
        if st.button("I do not know this", key="unknown"):
            record_unknown()
    with col3:
        if st.button("Next ➡️"):
            navigate(1)

    # Display current word index
    st.write(f"Flashcard {st.session_state.index + 1} of {len(current_words)}")

# Check my status checkbox
st.session_state.show_status = st.checkbox("Show My Learning Status")

# Display learning status
if st.session_state.show_status:
    st.write("### Words you know:")
    st.write(", ".join(st.session_state.known_words))

    st.write("### Words you do not know:")
    st.write(", ".join(st.session_state.unknown_words))

# Automatically add words to known list if not marked unknown
record_known()

import streamlit as st
import random

# Function to read words from a file
def read_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file.readlines()]
    return words

# Load English words and Chinese characters
english_words = read_words('data/english_words.txt')
chinese_characters = read_words('data/chinese_characters.txt')

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
if 'knowledge_status' not in st.session_state:
    st.session_state.knowledge_status = {}

def navigate(offset):
    st.session_state.index += offset
    st.session_state.index = max(0, min(st.session_state.index, len(current_words) - 1))

# Checkboxes to choose language preference
st.title("FlashCard")
col1, col2 = st.columns(2)
with col1:
    english_checkbox = st.checkbox("English", value=True)
with col2:
    chinese_checkbox = st.checkbox("Chinese")

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
    language = 'English'
else:
    current_words = chinese_characters
    language = 'Chinese'

# Function to record the knowledge status
def record_knowledge():
    word = current_words[st.session_state.index]
    knowledge = st.session_state[f'knowledge_{st.session_state.index}']
    if knowledge == "Known":
        if word not in st.session_state.known_words:
            st.session_state.known_words.append((word, language))
        if (word, language) in st.session_state.unknown_words:
            st.session_state.unknown_words.remove((word, language))
    else:
        if word not in st.session_state.unknown_words:
            st.session_state.unknown_words.append((word, language))
        if (word, language) in st.session_state.known_words:
            st.session_state.known_words.remove((word, language))

# Display the current flashcard
if st.session_state.learning:
    word = current_words[st.session_state.index]

    # Display word in large font size
    st.markdown(f"<h1 style='text-align: center; font-size: 4em;'>{word}</h1>", unsafe_allow_html=True)
    st.write(f"**{language} Word**")

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous"):
            navigate(-1)
    with col2:
        st.write(f"Flashcard {st.session_state.index + 1} of {len(current_words)}")
    with col3:
        if st.button("Next ➡️"):
            navigate(1)

    # Radio buttons to indicate if the user knows the word
    st.radio(
        "Do you know this word?",
        ("Unknown", "Known"),
        key=f'knowledge_{st.session_state.index}',
        on_change=record_knowledge
    )

    # Stop learning button
    if st.button("Stop Learning"):
        st.session_state.learning = False
        st.experimental_rerun()

else:
    st.title("Learning Results")
    st.write("### Words you know:")
    for word, language in st.session_state.known_words:
        st.write(f"{word} ({language})")

    st.write("### Words you do not know:")
    for word, language in st.session_state.unknown_words:
        st.write(f"{word} ({language})")


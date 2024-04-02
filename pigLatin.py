import streamlit as st
from gtts import gTTS
import os

def speak_text(text):
    """Converts the given text to speech."""
    tts = gTTS(text=text, lang='en')  # Create a gTTS object for English
    filename = 'temp_audio.mp3'  # Temporary file to save audio
    tts.save(filename)  # Save the spoken text to a file
    return filename

def pig_latin_text(phrase):
    vowels = "aeiouAEIOU"
    pig_latin_words = []

    # Splitting the phrase into words while keeping punctuation marks
    words = phrase.split()

    for word in words:
        # Handling punctuation and uppercase
        prefix_non_letters = ''
        while len(word) > 0 and not word[0].isalpha():
            prefix_non_letters += word[0]
            word = word[1:]

        suffix_non_letters = ''
        while len(word) > 0 and not word[-1].isalpha():
            suffix_non_letters = word[-1] + suffix_non_letters
            word = word[:-1]

        # Convert the word to Pig Latin
        was_upper = word.isupper()
        was_title = word.istitle()
        
        word = word.lower()  # Converting word to lowercase for uniform processing
        first_vowel_pos = min([word.find(v) for v in vowels if word.find(v) != -1] or [len(word)])
        
        if first_vowel_pos == 0:
            pig_latin_word = word + "way"
        else:
            pig_latin_word = word[first_vowel_pos:] + word[:first_vowel_pos] + "ay"
        
        # Restoring case
        if was_upper:
            pig_latin_word = pig_latin_word.upper()
        elif was_title:
            pig_latin_word = pig_latin_word.capitalize()
        
        # Adding non-letter characters back
        pig_latin_word = prefix_non_letters + pig_latin_word + suffix_non_letters
        pig_latin_words.append(pig_latin_word)
    
    return " ".join(pig_latin_words)

def pig_latin(phrase):
    vowels = "aeiou"
    pig_latin_words = []

    # Splitting the phrase into words
    words = phrase.split()

    for word in words:
        # If word starts with a vowel, just add "way" to the end
        if word[0].lower() in vowels:
            pig_latin_word = word + "way"
        else:
            # Move the consonants before the first vowel to the end and add "ay"
            first_vowel_pos = min([word.find(v) for v in vowels if word.find(v) != -1] or [len(word)])
            if len(word[first_vowel_pos:]) == 2:  # If the length of the part after the first vowel is 2
                pig_latin_word =  word[1]+word[first_vowel_pos:] + word[first_vowel_pos + 1] + word[:first_vowel_pos] + "ay"
            else:
                pig_latin_word = word[first_vowel_pos:] + " " + word[:first_vowel_pos] + "ay"

        pig_latin_words.append(pig_latin_word)

    return " ".join(pig_latin_words)

# Streamlit UI
st.set_page_config(
    page_title="Pig Latin",
    page_icon="🔊"
)

st.title('Pig Latin Converter')
user_input = st.text_area("Enter English test you want to convert to normal speech:", "Hello world")

if st.button('Speak'):
    st.write("Pig Latin...")
    pigLatin = pig_latin(user_input)
    audio_file = speak_text(pigLatin)
    audio_file_opened = open(audio_file, 'rb')
    audio_bytes = audio_file_opened.read()
    st.audio(audio_bytes, format='audio/mp3', start_time=0)#, autoplay=True, controls=False)
    
    pig_latin_text = pig_latin_text(user_input)
    st.write("Pig Latin Phrase:", pig_latin_text)
    
    os.remove(audio_file)  # Clean up the temporary file after use

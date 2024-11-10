import streamlit as st
from transformers import MBartForConditionalGeneration, MBart50Tokenizer

# Load mBART model and tokenizer
model_name = "facebook/mbart-large-50-many-to-one-mmt"
tokenizer = MBart50Tokenizer.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer.src_lang = "te_IN"

# Define translation function
def translate(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])
    translation = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translation

# Streamlit UI components
st.title("Telugu to English Translator")
text_input = st.text_area("Enter Telugu text:", height=200)

if st.button("Translate"):
    if text_input:
        translation = translate(text_input)
        st.text_area("English Translation:", translation, height=200)
    else:
        st.warning("Please enter text to translate.")

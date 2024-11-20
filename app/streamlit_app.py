import streamlit as st
from transformers import MBartForConditionalGeneration, MBart50Tokenizer, BartForConditionalGeneration, BartTokenizer

# Load mBART model and tokenizer for translation
model_name = "facebook/mbart-large-50-many-to-one-mmt"
tokenizer = MBart50Tokenizer.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer.src_lang = "te_IN"

# Load BART model and tokenizer for summarization
summarizer_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
summarizer_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

# Define translation function
def translate(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])
    translation = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translation

# Define summarization function
def summarize(text):
    inputs = summarizer_tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_tokens = summarizer_model.generate(**inputs)
    summary = summarizer_tokenizer.decode(summary_tokens[0], skip_special_tokens=True)
    return summary

# Streamlit UI components
st.title("Telugu to English Translator with Summarization")
text_input = st.text_area("Enter Telugu text:", height=200) 

if st.button("Translate & Summarize"):
    if text_input:
        translation = translate(text_input)
        summary = summarize(translation)  # Summarizing the generated translation
        st.text_area("English Translation:", translation, height=200)
        st.text_area("Summarized Translation:", summary, height=200)
    else:
        st.warning("Please enter text to translate.")

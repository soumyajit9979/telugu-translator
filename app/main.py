from fastapi import FastAPI
from pydantic import BaseModel
from transformers import MBartForConditionalGeneration, MBart50Tokenizer

# Initialize FastAPI app
app = FastAPI()

# Load mBART model and tokenizer
model_name = "facebook/mbart-large-50-many-to-one-mmt"
tokenizer = MBart50Tokenizer.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

# Set the source language to Telugu and target language to English
tokenizer.src_lang = "te_IN"

# Define the request body structure
class TranslationRequest(BaseModel):
    text: str

# Define the translation endpoint
@app.post("/translate")
def translate_text(request: TranslationRequest):
    text = request.text
    lines = text.split('\n')  # Split text into lines
    translations = []

    # Translate each line
    for line in lines:
        # Tokenize the input text
        inputs = tokenizer(line, return_tensors="pt", padding=True)
        
        # Generate the translation
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"]
        )
        
        # Decode the translated tokens
        translation = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        translations.append(translation)

    # Join the translated lines with newline characters
    return {"translation": "\n".join(translations)}


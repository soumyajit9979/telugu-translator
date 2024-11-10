from flask import Flask, render_template, request
from transformers import MBartForConditionalGeneration, MBart50Tokenizer

app = Flask(__name__)

# Load mBART model and tokenizer
model_name = "facebook/mbart-large-50-many-to-one-mmt"
tokenizer = MBart50Tokenizer.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer.src_lang = "te_IN"

def translate(text):
    # Split text into lines
    lines = text.split('\n')
    translations = []

    # Translate each line
    for line in lines:
        inputs = tokenizer(line, return_tensors="pt", padding=True)
        translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])
        translation = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        translations.append(translation)

    # Join the translated lines with newline characters
    return '\n'.join(translations)

@app.route("/", methods=["GET", "POST"])
def index():
    translation = ""
    if request.method == "POST":
        text = request.form["text"]
        translation = translate(text)
    return render_template("index.html", translation=translation)

if __name__ == "__main__":
    app.run(debug=True)

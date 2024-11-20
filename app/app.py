from flask import Flask, render_template, request
from transformers import MBartForConditionalGeneration, MBart50Tokenizer, BartForConditionalGeneration, BartTokenizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

app = Flask(__name__)

# Load mBART model and tokenizer for translation
model_name = "facebook/mbart-large-50-many-to-one-mmt"
model_checkpoint = "aryaumesh/english-to-telugu"
tokenizer = MBart50Tokenizer.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer.src_lang = "te_IN"

# Load tokenizer and model
sum_tokenizer = AutoTokenizer.from_pretrained("agentlans/text-summarization")
sum_model = AutoModelForSeq2SeqLM.from_pretrained("agentlans/text-summarization")

# Load BART model and tokenizer for summarization
summarizer_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
summarizer_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

tokenizer_english_telugu = MBart50TokenizerFast.from_pretrained(model_checkpoint)
model_english_telugu = MBartForConditionalGeneration.from_pretrained(model_checkpoint)


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

# def summarize(text):
#     inputs = summarizer_tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
#     summary_tokens = summarizer_model.generate(**inputs)
#     summary = summarizer_tokenizer.decode(summary_tokens[0], skip_special_tokens=True)
#     return summary


def summarize(paragraph):
    inputs = sum_tokenizer.encode(paragraph, return_tensors="pt", max_length=1024, truncation=True)
    # Generate the summary
    summary_ids = sum_model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = sum_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def english_telugu(text):
    inputs = tokenizer_english_telugu(text, return_tensors="pt")
    outputs = model_english_telugu.generate(**inputs)
    res=tokenizer_english_telugu.decode(outputs[0], skip_special_tokens=True)
    return res


@app.route("/", methods=["GET", "POST"])
def index():
    translation = ""
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        translation = translate(text)
        # print("Translation:", translation)  # Print translation to console
        summary = summarize(translation)  # Summarizing the generated translation
        print(summary)
        final_res=english_telugu(summary)
        print("Final_text: ",final_res)
    return render_template("index.html", translation=translation, summary=summary)

if __name__ == "__main__":
    app.run(debug=True)

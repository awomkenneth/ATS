from flask import Flask, render_template, request
from newspaper import Article
from newspaper import Config
import nltk
from gtts import gTTS
import os
import uuid
import requests
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_url = request.form['article_url']
        audio_file_path = generate_audio(input_url)
        return render_template('index.html', audio_file_path=audio_file_path)

    return render_template('index.html', audio_file_path=None)

def generate_audio(url):
    if url.endswith('.pdf'):
        # If the URL is a PDF link, process the PDF content
        text_content = extract_text_from_pdf(url)
    else:
        # Otherwise, treat it as a regular article link
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
        config = Config()
        config.browser_user_agent = user_agent


        article = Article(url, config=config)
        article.download()
        article.parse()

        nltk.download('punkt')
        article.nlp()

        text_content = article.text

    language = "en"

    # Generate a unique filename using uuid
    unique_filename = str(uuid.uuid4()) + ".mp3"
    audio_file_path = os.path.join("static", unique_filename)

    myobj = gTTS(text=text_content, lang=language, slow=False)
    myobj.save(audio_file_path)
    return audio_file_path

def extract_text_from_pdf(pdf_url):
    # Download the PDF content
    response = requests.get(pdf_url)
    pdf_content = response.content

    # Extract text from PDF using PyPDF2
    pdf_reader = PdfReader(pdf_content)
    text_content = ""
    for page in pdf_reader.pages:
        text_content += page.extract_text()

    return text_content

if __name__ == '__main__':
    app.run(debug=True)
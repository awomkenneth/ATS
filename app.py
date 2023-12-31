from flask import Flask, render_template, request
from newspaper import Article
import nltk
from gtts import gTTS
import os
import uuid


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        article_url = request.form['article_url']
        audio_file_path = generate_audio(article_url)
        return render_template('index.html', audio_file_path=audio_file_path)

    return render_template('index.html', audio_file_path=None)

def generate_audio(url):
    article = Article(url)
    article.download()
    article.parse()

    nltk.download('punkt')
    article.nlp()

    mytext = article.text
    language = "en"

    # myobj = gTTS(text=mytext, lang=language, slow=False)
    # audio_file_path = "static/newread_article.mp3"
    # myobj.save(audio_file_path)
    # return audio_file_path
    
    # Generate a unique filename using uuid
    unique_filename = str(uuid.uuid4()) + ".mp3"
    
    audio_file_path = os.path.join("static", unique_filename)
    
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save(audio_file_path)
    return audio_file_path

if __name__ == '__main__':
    app.run(debug=True)
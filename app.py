from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import os
import requests

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from flask import Flask, render_template, request

app = Flask(__name__)

LANGUAGE = "english"

@app.route('/', methods=['POST'])
def boring():
    boringStuff = request.form['boringstuff'];
    parser = PlaintextParser.from_string(request.form['boringstuff'], Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sentencesCount = request.form['sentences'] if request.form['sentences'] else 3;
    
    sentences = summarizer(parser.document, sentencesCount)
    return render_template('index.html', sentences=sentences, sentencesCount=sentencesCount, boringStuff=boringStuff)

@app.route("/")
def home():
    boringStuff = 'Blah blah blah...'
    return render_template('index.html', sentencesCount=3, boringStuff=boringStuff)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
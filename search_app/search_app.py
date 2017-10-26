import os
import re
import pymorphy2
import json
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from flask import Flask
from flask import url_for, render_template, request
from math import log

app = Flask(__name__)

morph = pymorphy2.MorphAnalyzer()

k1 = 2.0
b = 0.75

def score_BM25(n, qf, N, dl, avdl):
    K = compute_K(dl, avdl)
    IDF = log((N - n + 0.5) / (n + 0.5))
    frac = ((k1 + 1) * qf) / (K + qf)
    return IDF * frac

def compute_K(dl, avdl):
    return k1 * ((1-b) + b * (float(dl)/float(avdl)))

def get_data():
    with open("data/inv_index.json", "r", encoding = "utf-8") as f:
        index = json.loads(f.read())
    with open("data/articles_info.json", "r", encoding = "utf-8") as f:
        articles_info = json.loads(f.read())   
    with open("data/avg_article_len.txt", "r", encoding = "utf-8") as f:
        avg_len = float(f.read())
    return index, articles_info, avg_len

def search(query):
    articles_relevance = defaultdict(float)
    result = []
    words = word_tokenize(query)
    lemmas = []
    for word in words:
        r = re.search("[^А-ЯЁа-я-ё]", word)
        if not r:
            lemma = morph.parse(word)[0].normal_form
            if lemma not in stopwords.words('russian'):
                lemmas.append(lemma)
    if len(lemmas) > 0:
        index, articles_info, avg_len = get_data()
        N = len(articles_info)
        for lemma in lemmas:
            if lemma in index:
                n = len(index[lemma])
                for document in index[lemma]:
                    qf = document[1]
                    dl = articles_info[document[0]]["length"]
                    title = articles_info[document[0]]["title"]
                    url = articles_info[document[0]]["url"]
                    articles_relevance[(url, title)] += score_BM25(n, qf, N, dl, avg_len)
        result = [item[0] for item in sorted(articles_relevance.items(), key=lambda x: x[1], reverse=True)]
        if len(result) > 10:
            result = result[:10]
    return result
 
@app.route('/')
def index():
    if request.args:
        query = request.args['query']
        links = search(query)
        return render_template('index.html',links=links)
    return render_template('index.html',links=[])

if __name__ == '__main__':
    app.run(debug=True)
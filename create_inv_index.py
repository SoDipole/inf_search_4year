import os
import re
import pymorphy2
from collections import defaultdict, Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

morph = pymorphy2.MorphAnalyzer()

index = defaultdict(list)
articles_info = {}
avg_len = 0

collection = os.listdir("./yaskluch_acricles")

for document in collection:
    with open("yaskluch_acricles/"+document, encoding = "utf-8") as f:
        text = f.read()
    r = re.search("@url.+?\n(.+)", text)
    if r:
        article_text = r.group(1) 
        r = re.search("@ti (.+?)\n", text)
        if r:
            title = r.group(1)
        r = re.search("@url (.+?)\n", text)
        if r:
            url = r.group(1)
            
        words = word_tokenize(article_text)
        lemmas = []
        for word in words:
            r = re.search("[^А-ЯЁа-я-ё]", word)
            if not r:
                lemma = morph.parse(word)[0].normal_form
                if lemma not in stopwords.words('russian'):
                    lemmas.append(lemma)
        c = Counter(lemmas)
        
        for lemma in set(lemmas):
            index[lemma].append([document, c[lemma]])
            
        articles_info[document] = {"title": title, "url": url, "length": len(lemmas)}
        avg_len = (avg_len + len(lemmas)) / 2
        
        print(document)

with open("data/inv_index.json", encoding = "utf-8") as f:
    f.write(index)
with open("data/articles_info.json", encoding = "utf-8") as f:
    f.write(articles_info)
with open("data/avg_article_len.txt", encoding = "utf-8") as f:
    f.write(avg_len)
import json
import urllib
from glob import glob
import os
from rus_rap.preprocessing import text_stemming
from gensim import corpora, models, similarities
import numpy as np

texts = list()
DIR_PATH_TEXTS = ".\\songs"

countTexts = 0

for path in glob(os.path.join(os.path.expanduser(DIR_PATH_TEXTS), '*.json')):
    file = open(path, mode="r", encoding="maccyrillic")
    data = json.load(file)
    text = text_stemming(
        urllib.parse.unquote(' '.join(data['text'])).encode('maccyrillic').decode('utf-8', errors="ignore"))
    # print(text)
    texts.append(text.split())
    countTexts += 1
    if countTexts % 1 == 0:
        print("Complete: " + str(countTexts))

with open('for_lda.json', 'w', encoding='utf-8') as filehandle:
    json.dump(texts, filehandle, ensure_ascii=False)


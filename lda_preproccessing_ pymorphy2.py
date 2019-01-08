import string
import json
import urllib
from glob import glob
import os
from nltk.corpus import stopwords

import pymorphy2
morph = pymorphy2.MorphAnalyzer()

texts = list()
DIR_PATH_TEXTS = ".\\songs"

countTexts = 0

def text_lemmat(raw_text):

  clean_text = []

  raw_text=raw_text.replace('\t', ' ').replace('\n', ' ').replace('\r', '').replace('–', '')
  for punctuation in string.punctuation:
    raw_text = raw_text.replace(punctuation, ' ')
  raw_text = raw_text.split()

  for word in raw_text:
    word_low = word.lower()
    if word_low not in stopwords.words('russian') and not word.isdigit():
        clean_text.append(morph.parse(word_low)[0].normal_form)

  clean_text = ' '.join(clean_text)
  return clean_text

for path in glob(os.path.join(os.path.expanduser(DIR_PATH_TEXTS), '*.json')):
    file = open(path, mode="r", encoding="maccyrillic")
    data = json.load(file)
    text = text_lemmat(
        urllib.parse.unquote(' '.join(data['text'])).encode('maccyrillic').decode('utf-8', errors="ignore"))
    texts.append(text.split())
    countTexts += 1
    if countTexts % 100 == 0:
        print("Complete: " + str(countTexts))

with open('for_lda_pymorphy2.json', 'w', encoding='utf-8') as filehandle:
    json.dump(texts, filehandle, ensure_ascii=False)


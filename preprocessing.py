import string
import json
from glob import glob
import os
from nltk import SnowballStemmer
from nltk.corpus import stopwords
import urllib.parse
import rus_rap.uniqueNames as un

DIR_PATH = ".\\songs"

docCollection = dict()

def text_stemming(raw_text, wordDict = None):

  clean_text = []

  raw_text=raw_text.replace('\t', ' ').replace('\n', ' ').replace('\r', '').replace('–', '')
  for punctuation in string.punctuation:
    raw_text = raw_text.replace(punctuation, ' ')
  raw_text = raw_text.split()

  stemmer = SnowballStemmer("russian")
  for word in raw_text:
    word_low = word.lower()
    if word_low not in stopwords.words('russian') and not word.isdigit():
        if wordDict is not None:
            if word_low in wordDict:
                clean_text.append(stemmer.stem(word_low))
        else:
            clean_text.append(stemmer.stem(word_low))

  clean_text = ' '.join(clean_text)
  return clean_text

def findArtistsKey(str):
    for item in docCollection.keys():
        if un.levenshtein(un.normilizeArtist(str), un.normilizeArtist(item)) < 3:
            return item
    return None

def main_func():
    for item in un.findUniqueName(DIR_PATH):
        docCollection[item] = list()

    print(docCollection)

    # file = open(".\\songs\\$APER__Welcome_2_Moscow.json", mode="r", encoding="maccyrillic")
    # data = json.load(file)
    # text = urllib.parse.unquote(' '.join(data['text'])).encode('maccyrillic').decode('utf-8')

    for path in glob(os.path.join(os.path.expanduser(DIR_PATH), '*.json')):
        file = open(path, mode="r", encoding="maccyrillic")
        data = json.load(file)
        artist = un.normilizeArtist(urllib.parse.unquote(data["artist"]).encode('maccyrillic').decode('utf-8'))

        keyArtist = findArtistsKey(artist)
        if keyArtist is not None:
            text = text_stemming(urllib.parse.unquote(' '.join(data['text'])).encode('maccyrillic').decode('utf-8', errors="ignore"))
            docCollection[keyArtist].append(text)

    for key in docCollection.keys():
        with open('.\\textsByArtist\\' + key.replace(' ', '_') + '.json', 'w', encoding='utf-8') as outfile:
            json.dump({"artist": key, "texts": docCollection[key]}, outfile, ensure_ascii=False)

# main_func()

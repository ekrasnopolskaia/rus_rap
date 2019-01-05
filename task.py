import json
import os
from glob import glob
import re
from pprint import pprint
import urllib.parse

FLAG_ABOUT_REPEAT = 'hvjkbvjkjkbjkerk'

patternFeat = re.compile(".* ?feat ?.*")
patternFeat2 = re.compile(".+[,&] ?.+")
artists = set()


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def normilizeArtist(str):
    return re.sub('\(.*\)', '', str).lower().replace(' ', '')


dirpath = os.path.expanduser("C:\\Users\\KAS\\Documents\\dev\\lena\\songs_from_rap")
for path in glob(os.path.join(dirpath, '*.json')):
    file = open(path, mode="r", encoding="maccyrillic")
    data = json.load(file)
    artist = urllib.parse.unquote(data["artist"]).encode('maccyrillic').decode('utf-8')
    if not (bool(patternFeat.match(artist)) or bool(patternFeat2.match(artist))):
        artists.add(normilizeArtist(artist))

artList = list(sorted(artists))

for art in artList:
    print(art)

print("----------------------------------")

for i in range(0, len(artList) - 1):
    for j in range(i + 1, len(artList)):
        if levenshtein(artList[i], artList[j]) < 3:
            artList[j] = FLAG_ABOUT_REPEAT

artList = list(set(artList) - set([FLAG_ABOUT_REPEAT]))

for art in sorted(artList):
    print(art)
if not exist ".\sortWordFreq" mkdir .\sortWordFreq
for %%f in (.\textsByArtist\*) do python freq_words.py %%f .\sortWordFreq\%%~nf
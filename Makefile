install-wordnet:
	curl https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet31.zip -o nltk_data/wordnet31.zip
	cd nltk_data/
	mkdir -p -v corpora/
	unzip wordnet31.zip -d corpora/ 
	mv -v corpora/wordnet31 corpora/wordnet

# PoliTrend
A Sentiment Trend Analyser for Political Entities in Wikipedia



## Dependencies
Run the following command to set up the dependencies required for this app:
```
pip install -r requirements.txt
```

## Method
### Web-app
Running the app:
```
1. cd app/
2. python app.py
3. open the URL: "http://localhost:5000/" in your browser.
```


### Data Collection
[MediaWiki](https://www.mediawiki.org/wiki/API:Parsing_wikitext) API is used to collect all the revision history of wikipedia pages. 

Download relevant wikipedia pages: 
```
1. cd dataCollect/
2. set the names of the pages to be downloaded in "./input/political_parties.csv"
3. python wikipedia_fetcher.py
```
Train classifier:
```
1. cd train/
2. python trainCLassifier.py
```






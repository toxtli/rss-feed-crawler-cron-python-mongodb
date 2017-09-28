import json, feedparser, pymongo, crython

mongo_db, mongo_col = "test", "articles"
sources = ["https://futurism.com/feed/", "http://feeds.feedburner.com/crunchgear", "https://www.wired.com/feed/category/gear/latest/rss", "http://www.techradar.com/rss/news/software", "http://feed.cnet.com/feed/podcast/all/hd.xml", "https://spectrum.ieee.org/rss/videos", "http://rss.slashdot.org/Slashdot/slashdotDevelopers"]
conn = pymongo.MongoClient()[mongo_db]

@crython.job(expr='@minutely')
def extract():
	for source in sources:
		feed = feedparser.parse(source)
		for entry in feed["entries"]:
			article = json.loads(json.dumps(entry, default=str))
			print(article["title"])
			article["_id"] = article["link"]
			conn[mongo_col].save(article)

if __name__ == '__main__':
	crython.start()
	extract()
	input("")
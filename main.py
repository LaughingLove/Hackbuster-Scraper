import emailer
from hackbuster_scraper import HackbusterScraper

import json
import time

with open('personal_config.json') as f:
    data = json.load(f)

email = emailer.HackbusterEmail(data['email'], data['password'])

while True:

    with open('recent_article.json') as f:
        article_info = json.load(f)

    is_new_results = HackbusterScraper().is_new(True) # Basically I did this so we don't have to call is_new() again and make it complicated
    status, index = is_new_results['status'], is_new_results['index']

    if status:
        articles = HackbusterScraper().get_recent_articles(index)
        email.send_message(articles)
    else:
        print("No new articles! Sleeping for an hour!")
    time.sleep(3600)
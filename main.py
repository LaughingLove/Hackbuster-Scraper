import emailer
import hackbuster_scraper

import scheduler

import json

with open('personal_config.json') as f:
    data = json.load(f)


while True:

    scheduler.hackbuster_scheduler().start_timer()

    email = emailer.HackbusterEmail(data['email'], data['password'])

    with open('recent_article.json') as f:
        article_info = json.load(f)
    if not article_info.get("title"):
        article = hackbuster_scraper.HackbusterScraper().get_full_article()
    email.send_message(article['title'], article['author'], article['img_url'], article['content'], article['url'])
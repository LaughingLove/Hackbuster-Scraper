import emailer
import hackbuster_scraper

import scheduler

import json

with open('personal_config.json') as f:
    data = json.load(f)

scheduler.hackbuster_scheduler().start_timer()

email = emailer.HackbusterEmail(data['email'], data['password'])
article = hackbuster_scraper.HackbusterScraper().get_full_article()
email.send_message(article['title'], article['author'], article['img_url'], article['content'], article['url'])
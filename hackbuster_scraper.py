from selenium import webdriver, common
import time
import json
class HackbusterScraper:
    def __init__(self):
        

        with open('personal_config.json') as f:
            data = json.load(f)
        print(data['driver_browser'].lower())
        if data['driver_browser'].lower() == "firefox":
            self.browser = webdriver.Firefox()
        elif data['driver_browser'].lower() == "chrome":
            self.browser = webdriver.Chrome()
        elif data['driver_browser'].lower() == "edge":
            self.browser = webdriver.Edge()
        else:
            self.browser = webdriver.Chrome()
        try:
            self.browser.get("https://hackbusters.com/recent")
            time.sleep(3)
            self.browser.set_window_size(800,600)
        except Exception as e:
            print("Getting error: {}".format(str(e)))
            print("Retrying to connect to website in 10 seconds!")
            time.sleep(10)
            try:
                self.browser.get("https://hackbusters.com/recent")
                time.sleep(3)
                self.browser.set_window_size(800,600)
            except Exception as e:
                print("Getting error: {}".format(str(e)))
                print("Tried twice! Can't connect to website! Aborting....")
                raise e


    def is_new(self, from_main=False):
        with open('recent_article.json') as f:
            article_info = json.load(f)

        articles = self.browser.find_elements_by_class_name("ArticleRegular_articleWrap_2EPwi")
        if article_info['title'] == "":
            if from_main:
                # So that we don't have 2 browsers open
                self.close_browser()
            return {"status": True, "index": 0}
        else:
            for i in range(0, len(articles) - 1):

                title = articles[i].find_element_by_class_name("ArticleTitle_regular_1vl1D").text
                if (title == article_info['title']) and i == 0:
                    if from_main:
                        self.close_browser()
                    return {"status": False, "index": None}
                elif (title == article_info['title']) and i != 0:
                    index = i
                    if from_main:
                        self.close_browser()
                    return {"status": True, "index": index}
    
    def get_recent_articles(self, index):
        with open('recent_article.json') as f:
            recent_article = json.load(f)
        articles = self.browser.find_elements_by_class_name("ArticleRegular_articleWrap_2EPwi")
        article_information = []
        for i, a in enumerate(articles[:index if index > 0 else 1]):
            article_information.append(self.get_full_article(i))
            if i is 0:
                title = article_information[0]['title']
                recent_article['title'] = title
                with open('recent_article.json', 'w') as d:
                    json.dump(recent_article, d)
        print(len(article_information))
        self.close_browser()
        return article_information

    def close_browser(self):
        time.sleep(2)
        self.browser.quit()

    def get_article_page(self, index):
        # Gets the most recent article and clicks on it, redirecting selenium to the article page
        element = self.browser.find_elements_by_class_name("ArticleRegular_articleWrap_2EPwi")[index] # <--- First element
        header = element.find_element_by_tag_name("h4")
        
        time.sleep(1)
        header.click()

    def get_article_text_brief(self):
        articles = self.browser.find_elements_by_class_name("ArticleRegular_articleWrap_2EPwi")
        headers = []
        for article in articles:
            headers.append(article.find_element_by_class_name("ArticleTitle_regular_1vl1D").text)
        self.close_browser()
        return headers
    
    def get_article_link(self):
        try:
            self.browser.find_element_by_class_name("ArticleDetail_viewArticleBtn_VmdO0")
        except common.exceptions.NoSuchElementException:
            self.get_article_page(0)
        button_div = self.browser.find_element_by_class_name("ArticleDetail_viewArticleBtn_VmdO0")
        nested_link = button_div.find_element_by_tag_name("a").get_attribute("href")
        return nested_link
    
    def get_full_article(self, index):
        time.sleep(1)
        self.get_article_page(index)
        image = self.browser.find_element_by_class_name("ArticleImage_xlarge_3coPE")
        # Getting image URL from this string: "url({url})"
        img_url = image.value_of_css_property("background-image")[5:][:-2]

        title = self.browser.find_element_by_class_name("ArticleTitle_xlarge_3G107")

        meta_info = self.browser.find_element_by_class_name("ArticleDetail_meta_3yeSQ")
        # Getting embedded span
        author = meta_info.find_element_by_tag_name("span")

        content = self.browser.find_element_by_class_name("ArticleDetail_content_m0vfp")

        paragraphs = content.find_elements_by_tag_name("p")
        
        final_text = ""
        for p in paragraphs:
           #If it's not the last paragraph you can have 2 new lines
            if not paragraphs.index(p) == len(paragraphs) - 1:
                final_text += "{}\n\n".format(p.text)
            else:
                # If it is the end no new lines
                final_text += "{}".format(p.text)

        # Packaging everything nice and neat into a dict
        everything_together = {
            "title": title.text,
            "author": author.text,
            "img_url": img_url,
            "content": final_text,
            "url": self.get_article_link()
        }

        self.browser.back()
        # Sending it out
        return everything_together
from selenium import webdriver, common
import time
import json
class HackbusterScraper:
    def __init__(self):
        

        with open('personal_config.json') as f:
            data = json.load(f)
        if data['driver_browser'].lower() is "firefox":
            self.browser = webdriver.Firefox()
        elif data['driver_browser'].lower() is "chrome":
            self.browser = webdriver.Chrome()
        elif data['driver_browser'].lower() is "edge":
            self.browser = webdriver.Edge()
        else:
            self.browser = webdriver.Chrome()
        self.browser.get("https://hackbusters.com/recent")
        self.browser.set_window_size(800,600)

    def is_new(self):
        with open('recent_article.json') as f:
            article_info = json.load(f)

        articles = self.browser.find_elements_by_class_name("ArticleRegular_articleWrap_2EPwi")
        for i in range(0, len(articles) - 1):

            title = articles[i].find_element_by_class_name("ArticleTitle_regular_1vl1D").text
            if (title == article_info.get("title")) and i is 0:
                return {"status": False}
            elif title == article_info.get("title") and i is not 0:
                index = i
                return {"status": True, "index": index}
    
    def get_recent_articles(self):
        with open('recent_article.json') as f:
            recent_article = json.load(f)
        articles = self.browser.find_elements_by_class_name("ArticleRegular_articleWrap_2EPwi")
        index = self.is_new()['index']
        article_information = []
        for i in range(0, len(articles[:index]) - 1):
            article_information.append(self.get_full_article(i))
            # TODO: Will add this later
            # if i is 0:
            #     title = article_information[0]['title']
            #     recent_article['title'] = title
            #     with open('recent_article.json', 'w') as d:
            #         json.dump(recent_article, d)
        print(len(article_information))
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
        # element = self.browser.find_element_by_class_name("ArticleLarge_featureWrap_1TJdN")
        articles = self.browser.find_elements_by_class_name("ArticleRegular_articleWrap_2EPwi")
        #header = articles.find_elements_by_class_name("ArticleTitle_regular_1vl1D")
        headers = []
        for article in articles:
            headers.append(article.find_element_by_class_name("ArticleTitle_regular_1vl1D").text)
        # text = element.text
        self.close_browser()
        return headers
    
    def get_article_link(self):
        try:
            self.browser.find_element_by_class_name("ArticleDetail_viewArticleBtn_VmdO0")
        except common.exceptions.NoSuchElementException:
            self.get_article_page()
        button_div = self.browser.find_element_by_class_name("ArticleDetail_viewArticleBtn_VmdO0")
        nested_link = button_div.find_element_by_tag_name("a").get_attribute("href")
        self.close_browser()
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
        #p_list = []
        for p in paragraphs:
           #If it's not the last paragraph you can have 2 new lines
            if not paragraphs.index(p) == len(paragraphs) - 1:
                final_text += "{}\n\n".format(p.text)
            else:
                # If it is the end no new lines
                final_text += "{}".format(p.text)
            #p_list.append(p.text)

        # Packaging everything nice and neat into a dict
        everything_together = {
            "title": title.text,
            "author": author.text,
            "img_url": img_url,
            "content": final_text,
            "url": self.get_article_link()
        }

        self.close_browser()
        # Sending it out
        return everything_together


new_scrape = HackbusterScraper()
print(new_scrape.get_recent_articles())
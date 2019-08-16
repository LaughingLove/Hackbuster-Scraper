from selenium import webdriver, common
import time

class HackbusterScraper:
    def __init__(self):
        import json

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
        self.browser.get("https://hackbusters.com/recent")

    def close_browser(self):
        time.sleep(2)
        self.browser.quit()

    def get_article_page(self):
        element = self.browser.find_element_by_class_name("ArticleLarge_featureWrap_1TJdN")
        header = element.find_element_by_tag_name("h4")
        
        time.sleep(1)
        header.click()

    def get_article_text_brief(self):
        element = self.browser.find_element_by_class_name("ArticleLarge_featureWrap_1TJdN")
        text = element.text
        self.close_browser()
        return text
    
    def get_article_link(self):
        try:
            self.browser.find_element_by_class_name("ArticleDetail_viewArticleBtn_VmdO0")
        except common.exceptions.NoSuchElementException:
            self.get_article_page()
        button_div = self.browser.find_element_by_class_name("ArticleDetail_viewArticleBtn_VmdO0")
        nested_link = button_div.find_element_by_tag_name("a").get_attribute("href")
        self.close_browser()
        return nested_link
    
    def get_full_article(self):
        time.sleep(1)
        self.get_article_page()
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
    
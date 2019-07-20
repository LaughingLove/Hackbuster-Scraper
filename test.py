from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get("https://hackbusters.com/recent")

element = browser.find_element_by_class_name("ArticleLarge_featureWrap_1TJdN")
print(element.text)

header = element.find_element_by_tag_name("h4")
header.click()

button_div = browser.find_element_by_class_name("ArticleDetail_viewArticleBtn_VmdO0")

nested_link = button_div.find_element_by_tag_name("a")

print(nested_link.get_attribute("href"))


browser.close()
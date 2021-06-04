from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def getNaverBlogLink(link, max):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    urls = []
    url = link
    count = 1
    while (count <= max):
      browser = webdriver.Chrome(
          ChromeDriverManager().install(), chrome_options=options)
      browser.get(url + str(count))
      time.sleep(5)
      html = browser.page_source
      soup = BeautifulSoup(html, 'lxml')
      l = soup.find_all("a", {"class": "desc_inner"})
      for i in l:
        urls.append(i["href"])
      count += 1
      print("sel : {0}/{1}".format(max, count))
      browser.quit()
    urls = list(set(urls))
    return urls


def saveData(link):
    titleClass = ["se_textarea", "se_title", "se-title-text"]
    contentClass = "p.se-text-paragraph.se-text-paragraph-align-,p.se_textarea,p.se-text-paragraph.se-text-paragraph-align-center"
    for i in range(len(link)):
        text = ""
        page = requests.get(link[i])
        soup = BeautifulSoup(page.text, 'html.parser')
        # iframe 정보 가져오기
        iframe = soup.find("iframe")
        page = requests.get("https://blog.naver.com/" + iframe.attrs['src'])
        soup = BeautifulSoup(page.text, 'html.parser')
        ## title, content
        contents = soup.select(contentClass)
        for c in contents:
            text += c.getText().strip()
        saveJson(text, i)
        print("file download... {0}/{1}".format(len(link), i))


def saveJson(text, i):
    data = {"content": text}
    # folder variable set
    folder = "{0}.json".format(i+90)
    with open(folder, 'w') as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    n = getNaverBlogLink(
        "https://section.blog.naver.com/ThemePost.naver?directoryNo=7&activeDirectorySeq=1&currentPage=", 9)
    saveData(n)

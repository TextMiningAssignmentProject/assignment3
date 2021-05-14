from bs4 import BeautifulSoup
import requests
import json


## search url list
def getUrlLink():
    urls_list = []
    count = 1
    while (True):
        url = "https://blog.naver.com/PostList.nhn?from=postList&blogId=asdf2017&categoryNo=0&currentPage=" + str(
            count)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        text = soup.find("strong", {"class": "pcol1"})
        l = soup.find_all("a", {"class": "_se3copybtn"})
        if (not (text)):
            for i in l:
                urls_list.append(i.get("title"))
            print("URL search Counting ... : {0}".format(count))
            count += 1
        else:
            break
    urls_list = list(set(urls_list))
    return urls_list


## url 정보들 가지고 와서 json 형태로 저장
def jsonSave(location):
    d = getUrlLink()
    titleClass = ["se_textarea", "se_title", "se-title-text"]
    contentClass = "p.se-text-paragraph.se-text-paragraph-align-,p.se_textarea,p.se-text-paragraph.se-text-paragraph-align-center"
    ## 텍스트 찾기
    # title, content 형태로 찾을 수 있게 해야함!
    for i in range(len(d)):
        text = ""
        page = requests.get(d[i])
        soup = BeautifulSoup(page.text, 'html.parser')
        # iframe 정보 가져오기
        iframe = soup.find("iframe")
        page = requests.get("https://blog.naver.com/" + iframe.attrs['src'])
        soup = BeautifulSoup(page.text, 'html.parser')
        ## title, content, cat
        cat = soup.find(["a"], {"class": "pcol2"})
        contents = soup.select(contentClass)
        title = soup.find(["div", "h3"], {"class": titleClass})
        for c in contents:
            text += c.getText().strip()
        # 정보 저장
        saveFile(i, title.getText().strip(), text, cat, location)
        print("file download... {0}/{1}".format(len(d), i))


## f - save type json
def saveFile(index, title, content, cat, location):
    data = {"category": cat, "title": title, "content": content}
    # folder variable set
    folder = "{0}/{1}.json".format(location, index)
    with open(folder, 'w') as outfile:
        json.dump(data, outfile)


def readFile(index):
    # json ascii igonre refer ::
    with open('./json/{0}.json'.format(index)) as json_file:
        data = json.load(json_file)
        return data


def saveToCorpus(loop):
    ## text 로 모으기
    file_text = open("text.txt", "a+", -1, 'utf-8')
    for i in range(loop):
        f = readFile(i)
        fcontent = "{0} {1}".format(f["title"], f["content"])
        file_text.write(fcontent)
    file_text.close()
    print("successfully save")


def getText():
    file_text = open("text.txt", "r", -1, "utf-8")
    return file_text.read()


def importTest():
    print("successfully importing")


if __name__ == '__main__':
    print("make by yonghoon")
    print("reference link", "*"*20)
    print("해당 스크립트는 https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/ 부분을 참조하였습니다.")
    print("https://stackoverflow.com/questions/59982041/how-do-i-keep-only-ascii-and-discard-non-ascii-nbsp-etc-while-doing-json-dumps")

from bs4 import BeautifulSoup
import requests
import json


# search url list
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


# url 정보들 가지고 와서 json 형태로 저장
def jsonSave(location):
    d = getUrlLink()
    titleClass = ["se_textarea", "se_title", "se-title-text"]
    contentClass = "p.se-text-paragraph.se-text-paragraph-align-,p.se_textarea,p.se-text-paragraph.se-text-paragraph-align-center"
    # 텍스트 찾기
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
        cat = soup.find(["a"], {"class": "pcol2"}).text
        print(cat)
        contents = soup.select(contentClass)
        title = soup.find(["div", "h3"], {"class": titleClass})
        for c in contents:
            text += c.getText().strip()
        # 정보 저장
        saveFile(i, title.getText().strip(), text, cat, location)
        print("file download... {0}/{1}".format(len(d), i))


# 카테고리를 4개로 나눈다
# 1. 자기계발
selfDev = ["웁운투", "리눅스 명령어", "bash_shell", "서버 및 시스템", "기타", "보안", "관심", "AWS", "github", "파이크래프트",
           "OS 업데이트 내용", "프로젝트", "제로(W, H)", "설정", "오류 해결", "기타", "Cisco Aspire", "소프트웨어 교육", "아두이노"]
# 2. 봉사활동
volunteer = ["코드클럽(TIP)", "코드클럽(17-1)", "코드클럽(17-2)",
             "코드클럽(18-1)", "코드클럽(RPi)", "사회봉사"]
# 3. 프로그래밍
programming = ["C++", "php", "python", "java", "안드로이드",
               "JSP", "기타", "이론", "HTML", "CSS", "Javascript", "sql 실습"]
# 4. 책
books = ["책*"]


def changeCategory(cat):
    if cat in selfDev:
        cat = "자기계발"
    elif cat in volunteer:
        cat = "봉사활동"
    elif cat in programming:
        cat = "프로그래밍"
    elif cat in books:
        cat = "책"
    return cat


# f - save type json
def saveFile(index, title, content, cat, location):
    cat = changeCategory(cat)
    data = {"category": cat, "title": title, "content": content}
    # folder variable set
    folder = "{0}/{1}.json".format(location, index)
    with open(folder, 'w') as outfile:
        json.dump(data, outfile)


def readFile(index, location):
    # json ascii igonre refer ::
    with open('{0}/{1}.json'.format(location,  index)) as json_file:
        data = json.load(json_file)
        return data


def divCatAnoun(loop, gLoc, sLoc):
    selfDev = open("{0}/selfdev.txt".format(sLoc), "a+", -1, 'utf-8')
    volunteer = open("{0}/volunteer.txt".format(sLoc), "a+", -1, 'utf-8')
    programming = open("{0}/programming.txt".format(sLoc), "a+", -1, 'utf-8')
    books = open("{0}/books.txt".format(sLoc), "a+", -1, 'utf-8')

    for i in range(loop):
        f = readFile(i, gLoc)
        fcontent = "{0} {1}|".format(f["title"], f["content"])
        if (f["category"] == "자기계발"):
            selfDev.write(fcontent)
        elif (f["category"] == "봉사활동"):
            volunteer.write(fcontent)
        elif (f["category"] == "프로그래밍"):
            programming.write(fcontent)
        elif (f["category"] == "책"):
            books.write(fcontent)

    contents = [selfDev, volunteer, programming, books]
    for f in contents:
        f.close()
    print("succesfully make cat files")


def saveToCorpus(loop, gLoc, sLoc):
    # text 로 모으기
    file_text = open("{0}/text.txt".format(sLoc), "a+", -1, 'utf-8')
    for i in range(loop):
        f = readFile(i, gLoc)
        fcontent = "{0} {1}".format(f["title"], f["content"])
        file_text.write(fcontent)
    file_text.close()
    print("successfully save")

def getCatText(location, file):
    file_text = open("{0}/{1}".format(location, file), "r", -1, "utf-8")
    return file_text.read()

def getText(location):
    file_text = open("{0}/text.txt".format(location), "r", -1, "utf-8")
    return file_text.read()


if __name__ == '__main__':
    print("make by yonghoon")
    print("reference link", "*"*20)
    print("해당 스크립트는 https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/ 부분을 참조하였습니다.")
    print("https://stackoverflow.com/questions/59982041/how-do-i-keep-only-ascii-and-discard-non-ascii-nbsp-etc-while-doing-json-dumps")

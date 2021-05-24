# %%
from sklearn.feature_extraction.text import CountVectorizer
from math import log
import lib.getURL as url
from konlpy.tag import Okt  # 명사 추출기
okt = Okt()

getLocation = "./data/json"
saveLocation = "./data"
# %%
# text save
# url.saveToCorpus(362, getLocation, saveLocation)

# %%
# 명사 추출하기
print("명사 추출중...")
corpus = url.getText(saveLocation)
corpus_anoun = okt.nouns(corpus)
# 명사 중복 제거
corpus_anoun = list(set(corpus_anoun))
print(len(corpus_anoun))

# %%
# 2개 이상 명사만 추출
corpus_result = []
for c in corpus_anoun:
    if (len(c) <= 1):
        continue
    corpus_result.append(c)
print(len(corpus_result))

# %%
# 총 카테고리(4) : 자기계발, 프로그래밍, 봉사활동, 책
# 카테고리별 파일 생성하기
# url.divCatAnoun(362, getLocation, saveLocation)
# %%
# sort
corpus_anoun.sort()
# cmax 값 구하기
# 카테고리별 텍스트 값 가져오기
booksText = url.getCatText(saveLocation, "books.txt")
selfDev = url.getCatText(saveLocation, "selfdev.txt")
program = url.getCatText(saveLocation, "programming.txt")
volunteer = url.getCatText(saveLocation, "volunteer.txt")

# %%
# Cmax 값 구하기
# 모든 카테고리에서 빈도수(TF)가 가장 큰 카테고리 == Cmax
booksCorpus = booksText.split("|")
selfCorpus = selfDev.split("|")
programCorpus = program.split("|")
volunCorpus = volunteer.split("|")
# corpus_result 사용
c = {  # 카테고리 정의하기
    "자기계발": {},
    "프로그래밍": {},
    "책": {},
    "봉사활동": {}
}
# %%
for word in corpus_result:
    if (booksText.count(word) != 0):
        c["책"][word] = booksText.count(word)
    if (selfDev.count(word) != 0):
        c["자기계발"][word] = selfDev.count(word)
    if (program.count(word) != 0):
        c["프로그래밍"][word] = program.count(word)
    if (volunteer.count(word) != 0):
        c["봉사활동"][word] = volunteer.count(word)
print(c)
# %%
# sorted를 활용한 딕셔너리 정렬
booksMax = ["책", sorted(c["책"].items(), key=lambda item: item[1])[-1][1]]
selfDevMax = [ "자기계발", sorted(c["자기계발"].items(), key=lambda item: item[1])[-1][1] ]
programMax = [ "프로그래밍", sorted(c["프로그래밍"].items(), key=lambda item: item[1])[-1][1] ]
volunMax = ["봉사활동", sorted(c["봉사활동"].items(), key=lambda item: item[1])[-1][1]]
print(booksMax)
print(selfDevMax)
print(programMax)
print(volunMax)

# %%

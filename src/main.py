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
print(corpus_result)

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

vector = CountVectorizer()
print(vector.fit_transform(booksCorpus).toarray())

# %%

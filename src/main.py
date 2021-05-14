#%%
from math import log
import lib.getURL as url
from konlpy.tag import Okt  # 명사 추출기
okt = Okt()

getLocation = "./data/json"
saveLocation = "./data"
#%%
## text save
# url.saveToCorpus(362, getLocation, saveLocation)

#%%
## 명사 추출하기
print("명사 추출중...")
corpus = url.getText(saveLocation)
corpus_anoun = okt.nouns(corpus)
## 명사 중복 제거
corpus_anoun = list(set(corpus_anoun))
print(len(corpus_anoun))

# %%
# 총 카테고리(4) : 자기계발, 프로그래밍, 봉사활동, 책
# 카테고리별 파일 생성하기
# url.divCatAnoun(362, getLocation, saveLocation)
# %%
# cmax 값 구하기
c = {  # 카테고리 정의하기
    "자기계발": {},
    "프로그래밍": {},
    "책": {},
    "봉사활동": {}
}
booksText = url.getCatText(saveLocation, "books.txt")
# %%
## 자기계발 Cmax 값 구하기
print("진행 중...")
i = 0
cmax_anoun = ""
cmax_count = -1
for anoun in corpus_anoun:
  count = booksText.count(anoun)
  c["자기계발"][anoun] = count
  if (cmax_count < count and len(anoun) > 1):
    cmax_anoun = anoun
    cmax_count = count
  i += 1
c["자기계발"]["$CmaxValue"] = {cmax_anoun: cmax_count}
print(c["자기계발"])
print(c["자기계발"]["$CmaxValue"])

# %%
# IECDF 구하기
# 총 문서 수가 362개 존재함
# A : C others : 362 - 자기계발 문서수
# B : C others 에서 Wi(생각) 이/가 존재하는 문서수
# log(A/B) == IECDF

# 일단 먼저 자기계발의 문서 수를 구하면 됨
A = 362 - len(booksText.split("|"))
programmingText = url.getCatText(saveLocation, "programming.txt")
selfDevText = url.getCatText(saveLocation, "selfdev.txt")
volunteerText = url.getCatText(saveLocation, "volunteer.txt")
B = programmingText.count(list(c["자기계발"]["$CmaxValue"].keys())[0]) + selfDevText.count(list(
    c["자기계발"]["$CmaxValue"].keys())[0]) + volunteerText.count(list(c["자기계발"]["$CmaxValue"].keys())[0])
print(A, B)
print("IECDF : ", log(A/B))

# %%
## CTF-IDCDF
# log(CTF * IECDF)
IECDF = log(A/B)
CTF = c["자기계발"]["$CmaxValue"]["생각"]
print(log(CTF * IECDF))
# %%

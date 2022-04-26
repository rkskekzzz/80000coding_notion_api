#!/usr/bin/env python
# coding: utf-8
import requests
import json
import os
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

# notion api key 가져오기
load_dotenv()
my_bearer = os.getenv("BEARER")

# notion api libraryDbUrl
libraryDbUrl = "https://api.notion.com/v1/databases/94e689f5b19947b1ab0f9b5f2d52962b/query"
contributorDbUrl = "https://api.notion.com/v1/databases/10909fc406ab42c29fa7f82d6a08d741/query"

headers = {
    "Authorization": "Bearer {}".format(my_bearer),
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json"
}

libraryBody = {
    "filter": {
        "and": [
            {
                "property": "create_date",
                "created_time": {
                    "on_or_after": "{}".format(args.start_date),
                }
            },
            {
                "property": "visible",
                "select": {
                    "does_not_equal": "no"
                }
            }
        ]
    },
    "page_size": 100
}

contributorBody = {
    "filter": {
        "property": "구분",
        "multi_select" : {
            "contains": "2기"
        }
    }
}

# 조건에 맞는 데이터를 가져옴
# notion api가 100개씩 paging 되어있기 떄문에, next_cursor을 비교해서 존재한다면 해당 커서를 body로 넘겨줌
# next_corsor가 없을때까지 반복
libraryObjectList = []
while True:
    libraryResponse = requests.request("POST", libraryDbUrl, headers=headers, data=json.dumps(libraryBody))
    libraryObject = json.loads(libraryResponse.text)
    libraryObjectList.extend(libraryObject["results"])
    if not libraryObject["next_cursor"]:
        break
    libraryBody["start_cursor"] = libraryObject["next_cursor"]

print("총 게시글 수 : ", len(libraryObjectList))

contributorResponse = requests.request("POST", contributorDbUrl, headers=headers, data=json.dumps(contributorBody))
contributorObject = json.loads(contributorResponse.text)

contributorList = []
for contributor in contributorObject["results"]:
    contributorList.append(contributor["properties"]["이름"]['title'][0]["plain_text"])

def filterByContributors(x, cadet):
    return cadet == x["properties"]["rich_text"]["formula"]["string"]


# 파일에 결과 출력
resultList = []
with open("result.txt", 'w') as resultFile:
    for contributor in tqdm(contributorList):
        result = [x for x in libraryObjectList if filterByContributors(x, contributor)]
        resultList.append([contributor, str(len(result))])

print("{}기 카뎃 수 : ".format(args.th), len(contributorList))

# 데이터 프레임으로 변환 및 시각화
df = pd.DataFrame(resultList)
# 컬럼 명 지정
df.columns = ['contributor', 'yes']
# yes 컬럼을 int 타입으로 변환
df['yes'] = df['yes'].astype(int)
# filtering을 위한 mask 지정
mask = (df.yes >= 2)
# 2개 이상의 yes 게시글을 작성한 카뎃만 필터링
df_done = df.loc[mask,:]
# yes 개수로 내림차순 정렬
df_done = df_done.sort_values(by='yes',axis=0, ascending=False)
# 출력
print(df_done)









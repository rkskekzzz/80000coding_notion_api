#!/usr/bin/env python
# coding: utf-8
import requests
import json
import os
import argparse
import pandas as pd
from dotenv import load_dotenv

parser = argparse.ArgumentParser(description='팔만코딩경 컨트리뷰터 활동 체크 스크립트')
parser.add_argument('--start-date', '-s', required=True, help='측정을 시작할 날짜')
# parser.add_argument('--end-date', '-e', required=True, help='측정이 끝나야할 날짜')

args = parser.parse_args()

# 카뎃 목록 지정
# cadets = "suhshin dha"
# start_date = "2022-04-01"

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


libraryObjectList = []
while True:
    libraryResponse = requests.request("POST", libraryDbUrl, headers=headers, data=json.dumps(libraryBody))
    libraryObject = json.loads(libraryResponse.text)
    libraryObjectList.extend(libraryObject["results"])
    if not libraryObject["next_cursor"]:
        break
    libraryBody["start_cursor"] = libraryObject["next_cursor"]

print(len(libraryObjectList))
contributorResponse = requests.request("POST", contributorDbUrl, headers=headers, data=json.dumps(contributorBody))
contributorObject = json.loads(contributorResponse.text)

contributorList = []
for contributor in contributorObject["results"]:
    contributorList.append(contributor["properties"]["이름"]['title'][0]["plain_text"])

def filterByContributors(x, cadet):
    return cadet == x["properties"]["rich_text"]["formula"]["string"]


resultList = []
with open("result.txt", 'w') as resultFile:
    for contributor in contributorList:
        result = [x for x in libraryObjectList if filterByContributors(x, contributor)]
        resultList.append([contributor, str(len(result))])












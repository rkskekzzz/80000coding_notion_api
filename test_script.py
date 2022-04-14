#!/usr/bin/env python
# coding: utf-8
import requests
import json
import os
import argparse
from dotenv import load_dotenv

parser = argparse.ArgumentParser(description='팔만코딩경 컨트리뷰터 활동 체크 스크립트')
parser.add_argument('--date', required=True, help='측정을 시작할 날짜')
parser.add_argument('--contributors', required=True, help='컨트리뷰터 리스트')

args = parser.parse_args()

# 카뎃 목록 지정
# cadets = "suhshin dha"
# start_date = "2022-04-01"

# notion api key 가져오기
load_dotenv()
my_bearer = os.getenv("BEARER")

# notion api url
url = "https://api.notion.com/v1/databases/94e689f5b19947b1ab0f9b5f2d52962b/query"
headers = {
    "Authorization": "Bearer {}".format(my_bearer),
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json"
}

body = {
    "filter": {
        "and": [
            {
                "property": "create_date",
                "created_time": {
                    "on_or_after": "{}".format(args.date),
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

response = requests.request("POST", url, headers=headers, data=json.dumps(body))
jsonObject = json.loads(response.text)

def filterByContributors(x, cadet):
    return cadet == x["properties"]["cadet_intraID"]["rich_text"][0]["plain_text"]


for contributor in args.contributors.split():
    result = [x for x in jsonObject["results"] if filterByContributors(x, contributor)]
    print("{} : {}개".format(contributor, len(result)))








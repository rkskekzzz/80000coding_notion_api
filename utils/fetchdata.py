
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

def fetchLibraryObjectList(args):
	libraryObjectList = []
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

	while True:
		libraryResponse = requests.request("POST", libraryDbUrl, headers=headers, data=json.dumps(libraryBody))
		libraryObject = json.loads(libraryResponse.text)
		libraryObjectList.extend(libraryObject["results"])
		if not libraryObject["next_cursor"]:
			break
		libraryBody["start_cursor"] = libraryObject["next_cursor"]

	return libraryObjectList


def fetchContributorObjectList(args):
	contributorList = []
	contributorBody = {
		"filter": {
			"property": "구분",
			"multi_select" : {
				"contains": args.th
			}
		}
	}

	contributorResponse = requests.request("POST", contributorDbUrl, headers=headers, data=json.dumps(contributorBody))
	contributorObject = json.loads(contributorResponse.text)

	for contributor in contributorObject["results"]:
		contributorList.append(contributor["properties"]["이름"]['title'][0]["plain_text"])

	return contributorList



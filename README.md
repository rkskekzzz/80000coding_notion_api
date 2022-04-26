# 80000coding_notion_api

팔만코딩경 컨트리뷰터 관리용 프로젝트입니다. 해당 프로젝트는 contributor db를 통합하면서, 코드의 재사용성과 자동화 기능을 더욱 강력하게 만들었습니다. 코드관련 문의와 이슈는 자유롭게 등록해주세요.

</br>

# Install

requirements.txt를 활용해 필요한 모듈을 설치할 수 있습니다.

```
pip install -r requirements.txt
```

아래 명령을 활용해서 필요한 모듈을 하나씩 설치할 수 있습니다.

- `pip install pandas` for use data management
- `pip install requests` for use api request
- `pip install python-dotenv` for use .env

| 해당 스크립트를 사용할 운영진은, 저에게 사전에 .env 파일에 필요한 key를 발급 받으세요.

</br>

# Usage

```bash
python3 main.py -s {시작 날짜 입력} \
				 -e {종료 날짜 입력} \
				 -t {원하는 컨트리뷰터 종류 ex 2기}
```

</br>

# Example

2022년 4월 1일부터 2022년 4월 31일까지 2기 컨트리뷰터를 터미널에 출력하고 싶은 경우

```bash
python3 main.py -s 2022-04-01 \
				 -e 2022-04-31 \
				 -t 2기
```

또한 출력 위치와 데이터 형태를 지정할 수 있습니다.

동일한 기간동안 운영진의 게시글을 개수로 내림차순 정렬해 csv파일로 저장하려면 아래와 같이 사용합니다. 필수 옵션을 제외한 옵션들은 원하는 값의 앞글자만 사용해도 됩니다.

```
python3 main.py -s 2022-04-01 \
				 -e 2022-04-31 \
				 -t 운영진 \
				 -p csv \
				 -a amount \
				 -d descending \

```

</br>

# Options

| option                 | required  | default       | description                 |
| ---------------------- | --------- | ------------- | --------------------------- |
| `-s`, `--start-date`   | **True**  |               | 측정을 시작할 날짜          |
| `-e`, `--end-date`     | **True**  |               | 측정이 끝나야할 날짜        |
| `-t`, `--th`           | **True**  |               | 측정을 할 기수(숫자만 입력) |
| `-r` `--result-option` | **False** | "all"         | 결과 옵션 지정              |
| `-p` `--print-type`    | **False** | "terminal"    | 출력 위치 지정              |
| `-o` `--print-option`  | **False** | "pandas"      | 데이터 형태 지정            |
| `-a` `--align-item`    | **False** | "contributor" | 정렬 아이템 지정            |
| `-d` `--align-dir`     | **False** | "ascending"   | 정렬 방향 지정              |

- 결과 옵션 지정

  - a, all : 모든 결과 출력 (default)
  - s, success : 목표 달성 성공한 사람 출력
  - f, fail : 목표 달성 실패한 사람 출력

- 출력 형태 지정

  - t, terminal : 터미널 출력 (default)
  - f, file : txt 파일 출력
  - c, csv : csv 파일 출력

- 데이터 출력 방식 지정

  - p, pandas : dataframe보기 출력 (default)
  - s, string : 문자열로 출력

- 정렬 아이템 지정

  - c, contributor : 이름으로 정렬 (default)
  - a, amount : 게시글 개수로 정렬

- 정렬 방향 지정
  - a, ascending : 오름차순 정렬 (default)
  - d, descending : 내림차순 정렬

#

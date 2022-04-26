from utils.result import Result
from utils.loader import Loader
from utils.fetchdata import fetchContributorObjectList, fetchLibraryObjectList
from time import sleep
import argparse
import sys

def args_check(_args):
	if _args.th == None:
		return False
	if _args.result_option and not _args.result_option in ["all", "a", "success", "s", "fail", "f"]:
		return False
	if _args.print_type and not _args.print_type in ["terminal", "t", "file", "f", "csv", "c" ]:
		return False
	if _args.print_option and not _args.print_option in ["pandas", "p", "string", "s"]:
		return False
	return True

def args():
	# Requried
	parser = argparse.ArgumentParser(description='팔만코딩경 컨트리뷰터 활동 체크 스크립트')
	parser.add_argument('--start-date', '-s', required=True, help='측정을 시작할 날짜')
	# parser.add_argument('--end-date', '-e', required=True, help='측정이 끝나야할 날짜')
	parser.add_argument('--th', '-t', required=True, help='측정을 할 기수(숫자만 입력)')
	# Optional
	parser.add_argument('--result-option', '-r', required=False, help='결과 옵션 지정')
	parser.add_argument('--print-type', '-p', required=False, help='출력 형태 지정')
	parser.add_argument('--print-option', '-o', required=False, help='데이터 출력 방식 지정')
	parser.add_argument('--align-item', '-a', required=False, help='정렬 아이템 지정')
	parser.add_argument('--align-dir', '-d', required=False, help='정렬 방향 지정')

	_args = parser.parse_args()

	if not args_check(_args):
		parser.print_help()
		sys.exit()

	return _args


if __name__ == "__main__":
	# loader test
	with Loader("...args checking", "args ready ✅"):
		args = args()

	with Loader("...fetching library", "library ready ✅"):
		libraryList = fetchLibraryObjectList(args)

	with Loader("...fetching contributor", "contributor ready ✅"):
		contributorList = fetchContributorObjectList(args)

	with Loader("...make result", "Done 😀"):
		result = Result(contributorList, libraryList, args)
		result.filterResult()
		result.printResult()

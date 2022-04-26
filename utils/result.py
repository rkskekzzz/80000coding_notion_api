import pandas as pd

class Result:
	def __init__(self, contributorList, libraryList, args):
		"""
		Result 파라미터 옵션 설명

		[--result-option, -r] 결과 옵션 지정
			a, all : 모든 결과 출력 (default)
			s, success : 목표 달성 성공한 사람 출력
			f, fail : 목표 달성 실패한 사람 출력

		[--print-type, -p] 출력 형태 지정
			t, terminal : 터미널 출력 (default)
			f, file : txt 파일 출력
			c, csv : csv 파일 출력

		[--print-option, -o] 데이터 출력 방식 지정
			p, pandas : dataframe보기 출력 (default)
			s, string : 문자열로 출력

		[--align-item, -a] 정렬 아이템 지정
			c, contributor : 이름으로 정렬 (default)
			a, amount : 게시글 개수로 정렬

		[--align-dir, -d] 정렬 방향 지정
			a, ascending : 오름차순 정렬 (default)
			d, descending : 내림차순 정렬

		"""
		self.result_option = "all" if args.result_option == None else args.result_option
		self.print_type = "terminal" if args.print_type == None else args.print_type
		self.print_option = "pandas" if args.print_option == None else args.print_option
		self.align_item = "contributor" if args.align_item == None else args.align_item
		self.align_dir = True if args.align_dir == None or args.align_dir == "ascending" else False

		self.contributorList = contributorList
		self.libraryList = libraryList

		self.resultList = []

	def filterResult(self):
		def filterByContributors(x, cadet):
			return cadet == x["properties"]["rich_text"]["formula"]["string"]


		for contributor in self.contributorList:
			result = [x for x in self.libraryList if filterByContributors(x, contributor)]
			self.resultList.append([contributor, str(len(result))])


	def printResult(self):
		# 데이터 프레임으로 변환 및 시각화
		df = pd.DataFrame(self.resultList)
		# 컬럼 명 지정
		df.columns = ['contributor', 'amount']
		# amount 컬럼을 int 타입으로 변환
		df['amount'] = df['amount'].astype(int)
		# row 생략없이
		df_align = df.sort_values(by=self.align_item, axis=0, ascending=self.align_dir)
		pd.set_option('display.max_rows', None)

		if self.print_type in ["t", "terminal"]: # default
			print(df_align)
		elif self.print_type in ["f", "file"]:
			resultFile = open("result.txt", "w")
			resultFile.write(df_align)
			resultFile.close()
		elif self.print_type in ["c", "csv"]:
			df_align.to_csv('./result.csv', sep=',', na_rep='NaN')
		else:
			print('invalid print option!')




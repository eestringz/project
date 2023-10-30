0. 모듈, 패키지
- requests
- pprint (pretty print) : 결과를 깔끔하게 보여주는 함수. 


1. 데이터 추출 
- API 요청 -> 응답 -> json 형태로 변환

- dict의 key만 출력 -> dict.keys()

- response['result']['baseList'] 
: 응답의 'result'의 데이터 중 'baseList'의 데이터만 추출


2. 데이터 가공
- dict의 key 변경  
: dict_swap = {v:k for k,v in dict_ex.items()}

- dict key 삭제
del dict['key']

- list와 dict의 혼용에서 반복문 쓰기



3. 느낀점
: API를 활용하여 데이터를 사용해본 적이 있지만, 상대적으로 리스트와 딕셔너리의 혼용에 어려움을
느낌. 또한 반복문과 제어문을 적절히 사용해가며, 함수를 생성하는 것에 많은 고민을 거쳐감. 끝내 오류를 반복하며 얻은 결과는 뿌듯한 감정을 가져다 줌.








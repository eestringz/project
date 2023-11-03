from django.http import JsonResponse
from rest_framework.decorators import api_view
from performence_test.settings import BASE_DIR
import random
import pandas as pd
import os

# 강의 내용 스켈레톤

# array_length = 1000
# random_range = 5000

# @api_view(['GET'])
# def bubble_sort(request):
#     li = []
#     for i in range(array_length):
#         li.append(random.choice(range(1, random_range)))
#     for i in range(len(li) - 1, 0, -1):
#         for j in range(i):
#             if li[j] < li[j + 1]:
#                 li[j], li[j + 1] = li[j + 1], li[j]
#     context = {
#       'top': li[0]
#     }
#     return JsonResponse(context)

# @api_view(['GET'])
# def normal_sort(request):
#     li = []
#     for i in range(array_length):
#         li.append(random.choice(range(1, random_range)))
#     li.sort(reverse=True)
#     context = {
#         'top': li[0]
#     }
#     return JsonResponse(context)

# from queue import PriorityQueue

# @api_view(['GET'])
# def priority_queue(request):
#     pq = PriorityQueue()
#     for i in range(array_length):
#         pq.put(-random.choice(range(1, random_range)))
#     context = {
#         'top': -pq.get()
#     }
#     return JsonResponse(context)





# A. CSV 데이터를 DataFrame 으로 변환 후 반환
# B. 결측치 처리 후 데이터 반환


# CSV 파일을 직접 열고 Pandas DataFrame으로 변환
def csv_to_dataframe(csv_path):
    try:
        df = pd.read_csv(csv_path, encoding='euc-kr')
        # 결측치를 "NULL" 문자열로 치환 
        df.fillna("NULL", inplace=True)
        return df
    except Exception as e:
        print("An error occurred while reading the CSV file:", str(e))
        return None


# Django 뷰 함수에서 데이터를 읽어와서 JSON 응답 반환
def csv_return_json(request):
    csv_path = BASE_DIR/"data/test_data.CSV"
    df = csv_to_dataframe(csv_path)

    if df is not None:
        data = df.to_dict('records')
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error': 'Failed to read CSV data into a DataFrame'}, status=500)



def csv_return_json_has_null(request):
    csv_path = BASE_DIR/"data/test_data_has_null.CSV"
    df = csv_to_dataframe(csv_path)

    if df is not None:
        data = df.to_dict('records')
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error': 'Failed to read CSV data into a DataFrame'}, status=500)




# C. 알고리즘 구현하기(평균 나이와 가장 비슷한 10명 구하기)
# D. Loucst 를 활용한 알고리즘 성능 측정

csv_path = BASE_DIR /"data/test_data_has_null.CSV"
df = csv_to_dataframe(csv_path)
df = df.dropna(subset=['나이'])

# '나이' 필드에서 NaN 값을 가지고 있지 않은 행을 선택
df['나이'] = pd.to_numeric(df['나이'], errors='coerce')

# 각 행의 나이와 평균 나이와의 차이를 계산하여 새로운 필드를 만듭니다.
df_avg = df['나이'].mean()


def find_similar(request):
    avg = df_avg
    df['diff'] = abs(df['나이'] - avg)

    # '나이_차이' 필드를 기준으로 가장 작은 10개의 행을 선택
    similar_ten = df.nsmallest(10, 'diff')

    # JSON 형태로 응답
    data = similar_ten.to_dict('records')
    return JsonResponse({'data': data})




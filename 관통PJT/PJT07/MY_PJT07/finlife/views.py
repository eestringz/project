from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
import requests
from django.http import JsonResponse


# Create your views here.

BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'

@api_view(['GET'])
def api_test(request):
    API_KEY= settings.API_KEY
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth' : API_KEY,
        'topFinGrpNo' : '020000',
        'pageNo' : 1
    }

    response = requests.get(URL, params=params).json()
    return JsonResponse({'response': response})


# A. 정기예금 상품 목록 및 옵션 목록 저장
@api_view(['GET'])
def save_deposit_products(request):
    API_KEY= settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    
    # API로부터 데이터를 가져와 JSON 형식으로 파싱
    response = requests.get(url).json()

    ## product
    for li in response.get('result').get('baseList'):
        save_data = {
            'fin_prdt_cd' : li.get('fin_prdt_cd'),
            'kor_co_nm' : li.get('kor_co_nm'),
            'fin_prdt_nm' : li.get('fin_prdt_nm'),
            'etc_note' : li.get('etc_note'),
            'join_deny' : li.get('join_deny'),
            'join_member' : li.get('join_member'),
            'join_way' : li.get('join_way'),
            'spcl_cnd' : li.get('spcl_cnd')
        }
        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid():
            serializer.save()

 
    ## option
    for li in response.get('result').get('optionList'):
        product = DepositProducts.objects.get(fin_prdt_cd=li.get('fin_prdt_cd'))
        save_data = {
            'fin_prdt_cd' : li.get('fin_prdt_cd'),
            'intr_rate_type_nm' : li.get('intr_rate_type_nm','') or '',
            'intr_rate' : li.get('intr_rate',-1) or -1,
            'intr_rate2' : li.get('intr_rate2', -1) or -1,
            'save_trm' : li.get('save_trm', -1) or -1,        
            }


        serializer = DepositOptionsSerializer(data=save_data)
        if serializer.is_valid():
            # 옵션 데이터를 상품과 연결하여 저장
            serializer.save(product = product)
    
    return Response({'message':'okay'})



# B. 전체 정기예금 상품 목록 출력
# C. 정기예금 상품 추가하기
@api_view(['GET','POST'])
def deposit_products(request):
    # GET 요청 처리: 정기예금 상품 목록 조회
    if request.method == 'GET':
        products = get_list_or_404(DepositProducts)
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)
    
    # POST 요청 처리: 새로운 정기예금 상품 생성
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



# D. 특정 상품의 옵션 리스트 출력
@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    options = get_list_or_404(DepositOptions, fin_prdt_cd = fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)



# E. 금리가 가장 높은 상품의 정보 출력
@api_view(['GET'])
def top_rate(request):
    # "최고 우대 금리" 가 가장 높은 옵션 찾기
    highest_option = DepositOptions.objects.all().order_by('-intr_rate2').first()

    # "최고 우대 금리" 가 가장 높은 상품의 정보와 옵션 리스트를 반환
    product = DepositProducts.objects.get(pk= highest_option.product.pk)
    options = DepositOptions.objects.filter(fin_prdt_cd= highest_option.fin_prdt_cd)

    option_serializer = DepositOptionsSerializer(options, many= True)
    product_serializer = DepositProductsSerializer(product)

    response_data = {
        'deposit_product': product_serializer.data,
        'options': option_serializer.data
    }

    return Response(response_data)
    


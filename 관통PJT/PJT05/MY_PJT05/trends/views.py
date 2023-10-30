from django.shortcuts import render,  redirect
from .models import Keyword, Trend
from .forms import KeywordForm

import re
from bs4 import BeautifulSoup
from selenium import webdriver

import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Create your views here.

def keyword(request):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trends:keyword') 
    else:
        form = KeywordForm()  
    
    keywords = Keyword.objects.all()

    context = {
        'form': form,
        'keywords':keywords,
    }
    return render(request, 'trends/keyword.html', context)


def keyword_detail(request, pk):

    keyword = Keyword.objects.get(pk=pk)

    if request.method == 'POST':
        keyword.delete()
        trends = Trend.objects.filter(name = keyword.name)
        for trend in trends:
            trend.delete() 

        return redirect('trends:keyword')
    

    
def get_google_num(keyword, flag):
    # flag 값에 따라 검색 URL을 생성한다. 
    # flag가 0이면 검색 기간 제한이 없는 URL을 생성, 그 외의 경우는 1년 이내 결과를 가져올 URL을 생성한다.
    if flag == 0:
        url = f"https://www.google.com/search?q={keyword}"
    else:
        url = f"https://www.google.com/search?q={keyword}&tbs=qdr:y"

    # Selenium 웹 드라이버를 초기화하고 생성한 URL로 이동
    driver = webdriver.Chrome()
    driver.get(url)
     # 현재 웹 페이지의 HTML을 가져온다.
    html = driver.page_source
    # BeautifulSoup를 사용하여 HTML을 파싱하기
    soup = BeautifulSoup(html, "html.parser")

    # 검색 결과의 숫자를 포함하는 요소를 선택하는 과정.
    # 이 요소는 Google 검색 결과 페이지에서 결과 수를 나타내는 부분임.
    result_stats = soup.select_one("div#result-stats")

    # 검색 결과가 있는지 확인하고, 숫자 부분을 추출하여 반환한다.
    if result_stats:
        numeric_part = re.sub(r'\D', '', result_stats.text) # 숫자 이외의 문자를 제거하고 숫자 부분만 남긴다.
        return int(numeric_part) if numeric_part else -1    # 숫자로 변환하고 숫자가 없으면 -1을 반환.
    else:
        return -1       #  검색 결과가 없으면 -1을 반환.


def crawling(request):

    keywords = Keyword.objects.all()

    for keyword in keywords:
        # 해당 키워드로 Google에서 검색 결과의 숫자를 가져오기
        result_stats = get_google_num(keyword.name, 0)
         # 해당 키워드와 검색 기간이 'all'로 이미 데이터베이스에 있는지 확인하고, 없으면 생성하기
        try:
            trend, created = Trend.objects.get_or_create(name=keyword.name, search_period = "all")
        except:
            trend = Trend(name=keyword.name, search_period="all", result=-1)
        
        trend.result = result_stats
        trend.save()

    trends = Trend.objects.all()

    context = {
        'trends':trends,
    }
    return render(request, 'trends/crawling.html', context)


def crawling_histogram(request):

    trends = Trend.objects.all()

    x,y = [],[]
    for trend in trends:
        x.append(trend.name)
        y.append(trend.result)

    plt.clf()
    plt.figure(figsize=(12,6))
    plt.bar(x,y, label='Trends')
    plt.title('Technology Trend Analysis')
    plt.xlabel('Keyword')
    plt.ylabel('Result')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # 그래프를 이미지로 변환하고 base64로 인코딩하여 컨텍스트에 추가.
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()

    context = {
        'chart_image':f'data:image/png;base64,{image_base64}'
    }

    return render(request, 'trends/crawling_histogram.html', context)


def crawling_advanced(request):

    keywords = Keyword.objects.all()

    for keyword in keywords:
        result_stats = get_google_num(keyword.name , 1)
        try:
            trend, created = Trend.objects.get_or_create(name=keyword.name, search_period = "all")
        except:
            trend = Trend(name=keyword.name, search_period="all", result=-1)
        trend.result = result_stats
        trend.save()

    trends = Trend.objects.all()

    x,y = [],[]
    for trend in trends:
        x.append(trend.name)
        y.append(trend.result)

    plt.clf()
    plt.figure(figsize=(12,6))
    plt.bar(x,y, label='Trends')
    plt.title('Technology Trend Analysis')
    plt.xlabel('Keyword')
    plt.ylabel('Result')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()

    context = {
        'trends': trends,
        'chart_image':f'data:image/png;base64,{image_base64}'
    }

    return render(request, 'trends/crawling_advanced.html', context)


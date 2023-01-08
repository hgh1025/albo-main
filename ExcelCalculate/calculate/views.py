from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render, redirect
from random import *
from main.models import *
from sendEmail.views import * 
from django.db import connection

from django.db.models import Count
import os


# Create your views here.
# def calculate(request):
#     file = request.FILES['fileInput']
#     # print("# 사용자가 등록한 파일의 이름: ", file)

#     #파일 저장하기
#     origin_file_name = file.name
#     user_name = request.session['user_name']
#     now_HMS = datetime.today().strftime('%H%M%S')
#     file_upload_name = now_HMS+'_'+user_name+'_'+origin_file_name
#     file.name = file_upload_name
#     document = Document(user_upload_file = file)
#     document.save()

def calculate(request):

    return render(request, 'modeling.html')

#---------데이터 보강 실행-----------#
import calculate.modeling as modeling
import pandas as pd

def update_model(request):

    # trade = Trade.objects.all() 
    # trade_count = len(trade)
    # td = Trade.objects.get(pk=1)

    modeling.main()

    #테이블에 데이터가 64개 이상일 경우에만 실행
    # if trade_count >= 64:
    #     # 기존 모델 파일 삭제
    #     os.remove(r'C:\albino\My-albo\ExcelCalculate\epoch100.h5')

        

    #     #데이터 보강 실행
    #     modeling.main()
    #     print(type(td.item_price))

    
    # else:
    #     print(trade_count)
        

    return render(request, 'modeling.html')
    # return HttpResponse('데이터 재보강중')
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


#modeling.py
    modeling.main() 

        

    return render(request, 'modeling.html')
    # return HttpResponse('데이터 재보강중')
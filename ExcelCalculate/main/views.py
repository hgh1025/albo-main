from django.shortcuts import render, redirect
from random import *
from .models import *
from sendEmail.views import * 
from django.db import connection
from django.urls import reverse
from django.db.models import Q # Q는 Django내 Model을 관리할 때 사용되는 ORM으로 SQL의 WHERE절과 같은 조건문을 추가할 때 사용한다.
from .forms import *
from datetime import datetime


from google.protobuf import descriptor as _descriptor

from PIL import Image

import os,glob
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
import numpy as np
import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go
from django.core.files.uploadedfile import InMemoryUploadedFile

import hashlib
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator #페이징 처리 
# 22/12/29 chart 함수 만들어서 다른 함수에 적용
def chart():
    items = Item.objects.all().order_by('-pk') 
    
    df_item = pd.DataFrame(list(Item.objects.all().values()))
    filt_1 = ((df_item['item_price'] >= 100000) & (df_item['item_price'] < 450000))
    filt_2 = ((df_item['item_price'] >= 450000) & (df_item['item_price'] < 800000))
    filt_3 = ((df_item['item_price'] >= 800000) & (df_item['item_price'] < 1600000))
    df_item_1 = df_item[filt_1]
    df_item_2 = df_item[filt_2]
    df_item_3 = df_item[filt_3]

    labels = ['10만원~45만원', '45만원~80만원', '80만원~160만원']
    values = [len(df_item_1['item_price']), len(df_item_2['item_price']),len(df_item_3['item_price'])]

    fig = go.Pie(labels=labels, values=values, hoverinfo='percent+label', insidetextorientation='radial', hole=.3)

    graphs2 = []
    graphs2.append(fig)

    layout_pie = {'title': '지금 이만큼이나 거래 중이에요 :0',
                    'height': 480,
                    'width': 1270,}
                    
    fig_div = plot({'data':graphs2, 'layout' : layout_pie}, output_type='div')
    

    df_trade = pd.DataFrame(list(Trade.objects.all().values()))
   
    Filt_1 = ((df_trade['item_price'] >= 100000) & (df_trade['item_price'] < 450000))
    Filt_2 = ((df_trade['item_price'] >= 450000) & (df_trade['item_price'] < 800000))
    Filt_3 = ((df_trade['item_price'] >= 800000) & (df_trade['item_price'] < 1600000))
    df_trade_1 = df_trade[Filt_1]
    df_trade_2 = df_trade[Filt_2]
    df_trade_3 = df_trade[Filt_3]
    x1 = df_trade_1['item_date']
    x2 = df_trade_2['item_date']
    x3 = df_trade_3['item_date']

    def get_counts(seq):
        counts={}
        for x in seq:
            if x in counts:
                counts[x] += 1
            else : 
                counts[x] = 1
        return counts

    count_1 = get_counts(x1)
    count_2 = get_counts(x2)
    count_3 = get_counts(x3)

    x1 = list(count_1.keys())
    x2 = list(count_2.keys())
    x3 = list(count_3.keys())
    y1 = []
    y2 = []
    y3 = []

    for i in list(count_1.keys()):
        y1.append(count_1[i])
    for i in list(count_2.keys()):
        y2.append(count_2[i])  
    for i in list(count_3.keys()):
        y3.append(count_3[i])      

    graphs1 = []
    graphs1.append(go.Bar(x=x1, y=y1, name="10만원~45만원",))
    graphs1.append(go.Bar(x=x2, y=y2, name="45만원~80만원",))
    graphs1.append(go.Bar(x=x3, y=y3, name="80만원~160만원",))
   
    

    layout_graph = {
        'title': '최근 이만큼이나 거래됐어요! :)',
        'xaxis_title': 'Date',
        'yaxis_title': '수량 (개)',
        'height': 480,
        'width': 1270,}

    plot_div = plot({'data': graphs1, 'layout': layout_graph}, 
                    output_type='div')
    context = dict() 
    context['items'] = items
    context['plot_div'] = plot_div
    context['fig_div'] = fig_div 
    
    return context

def index(request):
    # if not 'user_name' in request.session.keys():
    #     return HttpResponse('로그인을 진행해주세요')
    
    
    # ----chart start-------22/12/29               
    df = chart()              
           
    return render(request, 'main/index.html',df)
    
# 회원가입 html
def signup(request):
    return render(request, 'main/signup.html')


def join(request):
    

# 회원가입 start
    
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    gender= request.POST['gender']
    #year()로 하면 'int' object is not callable 에라가 나옴. 
    # 이유->예약어year(),sum()등등으로 변수명으로 했기때문에
    now=int(datetime.now().year)
    age= request.POST['year']
    age1= int(age)
   
    # 만 나이 구하기
    real_age = now - age1 + 1

    #생년,월,일 
    year = request.POST.get('year')
    month = request.POST.get('month', False)
    day = request.POST.get('day', False)
   
    user = User(year=year,month=month, day=day, age=real_age, gender= gender ,user_name = name, user_email = email, user_password = pw)
    user.save()
 # 회원가입 end

# ----chart start-------22/12/29
    df = chart()   
    
    return render(request, 'main/index.html',df )
    
    # code = randint(1000, 9999)
    # response = redirect('main_verifyCode')
    # response.set_cookie('code', code)
    # response.set_cookie('user_id',user.id) #set_cookie('name', value)
   
    # send_result = send(email,code)
    # if send_result:
        
    #     return response
    # else:
        
    #     return HttpResponse("이메일 발송에 실패했습니다.")
def signin(request):
    

    return render(request, 'main/signin.html')   

def login(request):
    
    loginEmail = request.POST['loginEmail'] # signin.html <input name=loginEmail> 사용을 위해
    loginPW = request.POST['loginPW']  # signin.html <input name=loginPW> 사용을 위해
    
    # 22/12/30 예외처리
    
    try:
        user = User.objects.get(user_email=loginEmail)
       

        if loginPW ==user.user_password:
            request.session['user_name'] = user.user_name
            request.session['user_email'] = user.user_email
            return redirect('main_index')
        elif user.user_password != loginPW:
            return HttpResponse('비밀번호를 틀렸습니다.')
        else:
            return redirect('main_index')
    except ObjectDoesNotExist:   
        message = '이메일이 존재하지 않습니다.'
        return HttpResponse(message)
    except:
        message = '알 수 없는 오류가 발생했습니다..'
        return HttpResponse(message)
    
    
   
def logout(request):
    del request.session['user_name']
    del request.session['user_email']
    return redirect('main_signin')

def verifyCode(request): 
    return render(request, 'main/verifyCode.html')

def verify(request):
    user_code = request.POST['verifyCode']
    cookie_code = request.COOKIES.get('code')
    if user_code == cookie_code:
        user = User.objects.get(id = request.COOKIES.get('id'))
        user.user_validate = 1
        user.save()
        response = redirect('main_index')
        response.delete_cookie('code')
        response.delete_cookie('user_id')
       
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return response
    else:
        redirect('main_verifyCode')






def result(request):
    if 'user_name' in request.session.keys():

        return render(request, 'main/result.html')
    else:
        return redirect('main_signin')

def upload(request):
    if not 'user_name' in request.session.keys():
        return HttpResponse('로그인을 진행해주세요')
    else:    
        return render(request, 'main/upload.html')
    

    page = request.GET.get('page','1')
    item_list =Item.objects.all().order_by('-pk')
    paginator = Paginator(item_list,8) #페이지당 8개씩 보여주기
    page_obj = paginator.get_page(page)
    context={'item_list': page_obj}
    return context
def posting(request):
    
    # 1208 수정 : 바로 글목록 볼 수 있게(양식다시제출 팝업 안 뜨게)
    if request.FILES.get('item_img'):

     

      users = User.objects.get(user_name=request.session['user_name']) #fk추가 로그인되어있는 회원이름 정보 가져옴

        
      item_name = request.POST.get('item_name',False)
      item_price =request.POST.get('item_price',False)
      item_content = request.POST.get('item_content',False)
      item_img= request.FILES.get('item_img')
      now_HMS = datetime.today().strftime('%Y.%H.%M.%S')
      item_upload_name  = now_HMS + '.jpeg'
      item_img.name = item_upload_name  #???


      new_name = Item(item_name=item_name, item_price=item_price, 
                        item_content=item_content, item_img = item_img, 
                        user_name= users)
      new_name.save()

      
      
      
# ----chart start-------22/12/29
   
    
     #페이지당 8개씩 보여주기   
    page = request.GET.get('page','1')
    items =Item.objects.order_by('-pk')
    paginator = Paginator(items,8)
    page_obj = paginator.get_page(page)
    context={'items': page_obj}
    # context={'item_list': items}     
        
    return render(request, 'main/posting.html',context) 

  




    

def new_post(request, pk):
    
    items = Item.objects.get(pk=pk)
    
    # trade_status = items.trade_status
    login_user = request.session['user_name'] #로그인한 유저
    post_user = str(items.user_name) #상품을 등록한 유저
     
    comments = CommentForm() #forms.py
   
    context = dict()
    context['items'] = items
    context['comments'] = comments
    context['login_user'] = login_user
    context['post_user'] =  post_user
    context['trade_status'] = items.trade_status
    
    
        
                                    
    return render(request, 'main/new_post.html', context)
    
    #전역변수 지정
UPLOAD_DIR = r'C:\practice\adminpractice\ExcelCalculate\media\images'


#가격예측버튼 누르면 실행되는 함수
def predict_price(request):
    #predict_img = request.POST['predict_img']

    if 'file1' in request.FILES:
        file = request.FILES['file1']
        file_name = file.name
        fp = open("%s%s" % (UPLOAD_DIR, file_name), 'wb')

    for chunk in file.chunks():
        fp.write(chunk)
        fp.close()

    model_weight_path = r'C:\practice\adminpractice\ExcelCalculate\epoch100.h5'
    img = Image.open("%s%s"%(UPLOAD_DIR,file_name))


    #가격예측함수
    def predict(model_path, img):
        
        model_saved = load_model(model_path)

        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)

        prediction = model_saved.predict(img)
        label = np.argmax(prediction[0])

        if label == 0:
            return '10만원 이상 45만원 미만'
        elif label == 1:
            return '45만원 이하 80만원 미만'
        else:
            return '80만원 이상 160만원 미만'

    
    
    context = dict()
    context['predict'] = predict(model_weight_path, img)

    return render(request, 'main/upload.html', context) 
def user_remove(request):
    return render(request, 'main/user_remove.html')

def user_remove2(request):
    
   
    user = User.objects.get(user_name=request.session['user_name'])
    user.delete()

    # ----chart start-------22/12/29
    df = chart()
    return render(request, 'main/index.html', df)

def remove_post(request, pk):
    post = Item.objects.get(pk=pk)
    
  
    post.delete()

    #post = request.GET['name(PK)'] <-- <input> 태그에 있는 name
    #delete_post= Item.objects.get(id=post)
    #delete_post.delete() <-- 여기선 new_post.html에서 pk로 설정할 수 있는 값이 없기에 
    # 위 와 같은 방법을 사용해야한다. user_name을 pk로 두면 회원탈퇴와 같은 기능이 되지 않을까?.

    # ----chart start-------22/12/29
    df = chart() 

        
    return render(request, 'main/index.html', df)
    
def editpage(request,pk):
    items = Item.objects.get(pk=pk)
    return render(request, 'main/editpage.html',{'items':items})

def boardEdit(request, pk):
  
    items = Item.objects.get(pk=pk)
   
     
    if request.method == "POST":
       
        items.item_name = request.POST.get('item_name')
        items.item_content = request.POST.get('item_content')
        items.item_price = request.POST.get('item_price')
        # items.item_img = request.FILES.get('item_img')
        items.trade_status =request.POST.get('trade_status')
        item_date= request.POST.get('item_date',False)

        
        items.save()

        items = Item.objects.get(pk=pk)
        print(items)
        if items.trade_status == "거래완료" :
            
            #image의 파일 형태가 PIL 형태
            image = items.item_img
            
            print(image)
            
            
            # PIL 파일 또는 경로는 save할수 없기 때문에 InMemoryUploadedFile 함수를 이용하여 request해온
            # 이미지 파일 형식과 동일하게 맞춰줘야한다.(불러올 이미지, 새로 저장할 이미지 이름, 저장할 이미지 경로)
            heat_file = InMemoryUploadedFile(image, None, 'heat.jpeg', 'trade_images/jpeg',
                                     None, None)
            
            print(heat_file)
            item_price = items.item_price
            
            status = Trade(item_date=item_date, item_img=heat_file ,item_price=item_price)

            status.save()

    # ----chart start-------22/12/29
    df = chart()  
        
   
   
    return render(request, 'main/index.html', df)
 
   

def create_comment(request, items_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.cleaned_data['comment']
        parent=None
        

    user = User.objects.get(user_name=request.session['user_name'])
    items = Item.objects.get(pk=items_id)
    

    new_comment = Comment(comment=comment, user_name=user, item_id=items, parent=parent)
    new_comment.save()

    return redirect('new_post', items_id)

def create_reply(request, items_id):
    reply_form = ReplyForm(request.POST) 
    if reply_form.is_valid():
        parent = reply_form.cleaned_data['parent']
        reply = reply_form.cleaned_data['comment']
        

    user = User.objects.get(user_name=request.session['user_name'])
    items = Item.objects.get(pk=items_id)

    print("hello")

    new_comment = Comment(comment=reply, user_name=user, item_id=items, parent=parent)
    new_comment.save()

    return redirect('new_post', items_id)


# def trade(request, item_id):
#     filled_form = Trade(request.POST) 
#     if filled_form.is_valid(): 
        
#         temp_form = filled_form.save(commit=False)
        
#         temp_form.item_id = Item.objects.get(id=item_id)
#         temp_form.user_name = User.objects.get(user_name=request.session['user_name'])
#         temp_form.item_status = "거래상태"
#         temp_form.save()
#     return redirect('posting', {'trade':trade})


def mypage(request):
    # 22/12/28 현재 로그인한 유저가 등록한 상품을 마이페이지로 확인
    users = User.objects.filter(user_name=request.session['user_name'])
    items = Item.objects.filter(user_name=request.session['user_name'])
    return render(request, 'main/mypage.html', {'items':items ,'users':users})


def uppass(request):
    if request.method == 'POST':
        u = request.user
        up = request.POST.get("uppass")
        u.set_password(up)
        u.save()
        return redirect("main_login")
    return render(request, 'main/uppass.html')
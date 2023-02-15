from django.shortcuts import render, redirect
from random import *
from .models import *
from sendEmail.views import * 
from django.db import connection
from django.urls import reverse
from django.db.models import Q # Q는 Django내 Model을 관리할 때 사용되는 ORM으로 SQL의 WHERE절과 같은 조건문을 추가할 때 사용한다.
from .forms import *
from datetime import datetime
from django.contrib import messages, auth
from django.contrib.auth import authenticate # 로그인 인증 사용하기 위해
from google.protobuf import descriptor as _descriptor
import math
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
import matplotlib.pylab as plt
from django.core.files.uploadedfile import InMemoryUploadedFile
from hashlib import sha256 as SHA #해쉬함수 무결성 검증을 위해 
import hashlib #비밀번호 보완처리
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator #페이징 처리 


# 22/12/29 chart 함수 만들어서 다른 함수에 적용
def chart():
    global get_counts
    # Item table에서 value값만 추출
    df_item = pd.DataFrame(list(Item.objects.all().values())) 

    # 가격 별로 item 추출
    df_item_1 = df_item[(df_item['item_price'] >= 100000) & (df_item['item_price'] < 450000)]
    df_item_2 = df_item[(df_item['item_price'] >= 450000) & (df_item['item_price'] < 800000)]
    df_item_3 = df_item[(df_item['item_price'] >= 800000) & (df_item['item_price'] < 1600000)]

    # 각 가격대 별 item 개수
    values = [len(df_item_1), len(df_item_2), len(df_item_3)] 

    # pie chart
    fig = go.Pie(labels=['10만원~45만원', '45만원~80만원', '80만원~160만원'], 
                 values=values, 
                 hoverinfo='percent+label', 
                 insidetextorientation='radial', 
                 hole=.3) 

    # pie chart layout
    layout_pie = {
        'title': '지금 이만큼이나 거래 중이에요 :0',
        'height': 480,
        'width': 1270,
    }
    
    # bar chart
    graphs1 = []
    for filt, name in [((100000, 450000), "10만원~45만원"),
                       ((450000, 800000), "45만원~80만원"),
                       ((800000, 1600000), "80만원~160만원")]:
        df_trade = pd.DataFrame(list(Trade.objects.filter(item_price__range=filt).values()))
        count = get_counts(df_trade['item_date'])
        graphs1.append(go.Bar(x=list(count.keys()), y=list(count.values()), name=name))

    # bar chart layout
    layout_graph = {
        'title': '최근 이만큼이나 거래됐어요! :)',
        'xaxis_title': 'Date',
        'yaxis_title': '수량 (개)',
        'height': 480,
        'width': 1270,
    }

    # pie chart div
    fig_div = plot({'data': [fig], 'layout': layout_pie}, output_type='div')

    # bar chart div
    plot_div = plot({'data': graphs1, 'layout': layout_graph}, output_type='div')
                    
    users = User.objects.all()
    context = {
        'items': Item.objects.all().order_by('-pk'),
        'plot_div': plot_div,
        'fig_div': fig_div,
        'users': users,
    }
    return context

from collections import Counter #collections.counter 동일한 요소 개수 구하기

def get_counts(seq):
    return dict(Counter(seq)) 
    
# def get_counts(seq):
#         counts={}
#         for x in seq:
#             if x in counts:
#                 counts[x] += 1
#             else : 
#                 counts[x] = 1
#         return counts    
    
# def get_counts(seq):
#     counts={}
#     for x in seq:
#         counts[x] = counts.get(x, 0) + 1
#     return counts
    
# def get_counts(seq):
#     counts = {x: seq.count(x) for x in seq}  # x:seq.count(x) --> {10:1 , 20:2 , 30:8 ....}
#     return counts    --> multiIndex error
    

    
def chart_user(request):
    df_user = pd.DataFrame(list(User.objects.all().values()))

    # Pie chart
    df_gender = df_user.groupby('gender').size()
    fig_gender = go.Pie(labels=df_gender.index, values=df_gender.values, hoverinfo='percent+label', insidetextorientation='radial', hole=.3)
    fig_gender_layout = {'title': '가입한 성별', 'height': 480, 'width': 1260}
    fig_gender_div = plot({'data': [fig_gender], 'layout': fig_gender_layout}, output_type='div')

    # Bar chart
    age = df_user['age']
    x_age = age.apply(lambda x: (x // 10) * 10).value_counts().sort_index().index.tolist() #apply는 Series와 DataFrame에서 lambda 함수를 쓸 수 있는 메쏘드라고 볼 수 있습니다.
    y_age = age.apply(lambda x: (x // 10) * 10).value_counts().sort_index().tolist()
    print(x_age)
    print(y_age)
    fig_age = go.Bar(x=x_age, y=y_age, name='age')
    fig_age_layout = {'title': '가입자 나이대별 그래프', 'xaxis_title': '나이(대)', 'yaxis_title': '가입자 수', 'height': 480, 'width': 1270}
    fig_age_div = plot({'data': [fig_age], 'layout': fig_age_layout}, output_type='div')
    
    
    context = dict()
    context['fig_gender_div'] = fig_gender_div
    context['fig_age_div'] = fig_age_div
    context['users'] = User.objects.all()
    
    return render(request, 'main/chart_user.html', context)
    
    
    
    
def index(request):
    
    
    # ----chart start-------22/12/29               
    df = chart()              
         
    return render(request, 'main/index.html',df)
    
# 회원가입 html
def signup(request):
    return render(request, 'main/signup.html')


def join(request):
    if request.method == 'POST':
        name = request.POST.get('signupName')
        email = request.POST.get('signupEmail')
        pw = request.POST.get('signupPW')
        pw_check = request.POST.get('signupPWcheck')
        gender = request.POST.get('gender')
        year = request.POST.get('year')
        month = request.POST.get('month')
        day = request.POST.get('day')
        
        if pw != pw_check:
            return HttpResponse("<script>alert('비밀번호가 다릅니다.');location.href='/signup'</script>")
        elif User.objects.filter(user_email=email).exists():
            return HttpResponse("<script>alert('이메일이 중복됩니다.');location.href='/signup'</script>")
        
        encoded_pw = hashlib.sha256(pw.encode()).hexdigest()
        now = datetime.now().year
        age = now - int(year) + 1
        
        user = User(year=year, month=month, day=day, age=age, gender=gender, user_name=name, user_email=email, user_password=encoded_pw)
        user.save()
        
        df = chart()    
        return render(request, 'main/index.html', df)
    
    # code = randint(1000, 9999)
    # response = redirect('main_verifyCode')
    # response.set_cookie('code', code)
    # response.set_cookie('user_id',user.id) #set_cookie('name', value)
   
    # send_result = send(email,code)
    # if send_result:
        
    #     return response
    # else:
        
    #     return HttpResponse("이메일 발송에 실패했습니다.")
def signin(request): #로그인페이지
   

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
            # return HttpResponse("<script>alert('로그인성공'); location.href='/'</script>")
        elif user.user_password != loginPW:
            return HttpResponse("<script>alert('비밀번호가 다릅니다..'); location.href='/signin'</script>")
            
            
        else:
            return redirect('main_signin')
    except ObjectDoesNotExist:   
        
        return HttpResponse("<script>alert('이메일이 존재하지 않습니다. 회원가입페이지로 이동합니다.'); location.href='/signup'</script>")
    except:
        
        return HttpResponse("<script>alert('알 수 없는 오류가 발생했습니다..'); location.href='/signin'</script>")


   
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
        
        return HttpResponse("<script>alert('로그인을 진행해주세요. 로그인 페이지로 이동합니다.'); location.href='/signin'</script>")
    else:    
        return render(request, 'main/upload.html')
    

  
def posting(request):
    
    # 1208 수정 : 바로 글목록 볼 수 있게(양식다시제출 팝업 안 뜨게)
    if request.FILES.get('item_img'):

     

      users = User.objects.get(user_name=request.session['user_name']) #fk추가 로그인되어있는 회원이름 정보 가져옴

        
      item_name = request.POST.get('item_name',False)  #False 값이 안나와도 에러나지 않도록
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

     #페이지당 10개씩 보여주기  최근순 
    page = request.GET.get('page','1') # /?page=1 처럼 GET 방식으로 호출된 URL에서 page값을 가져올때 ,, page값이 없는 상태로 호출되면 디폴트 1
    items =Item.objects.order_by('-pk')
    paginator = Paginator(items,10) #10개씩 보여주기
    page_obj = paginator.get_page(page) #paginator을 이용하여 요청된 페이지에 해당하는 페이징 객체(page_obj)를 생성->이를통해 데이터전체가 아닌 해당 페이지의 데이터만 조회하도록 쿼리를 변경
    context={'items': page_obj}
    # context={'item_list': items}     
        
    return render(request, 'main/posting.html',context) 

  
def desc(request):
    
     #페이지당 10개씩 보여주기  내림차순 23/01/16
      
      page = request.GET.get('page','1')
      items =Item.objects.all().order_by('item_price')
      paginator = Paginator(items,10)
      page_obj = paginator.get_page(page) # 현재 페이지에 해당하는 게시물만 얻는다.
      context={'items': page_obj}    
         
      return render(request, 'main/desc.html',context) 

def asc(request):
  
     #페이지당 10개씩 보여주기 오름차순  23/01/16
      page = request.GET.get('page','1')
      items =Item.objects.order_by('-item_price')
      paginator = Paginator(items,10)
      page_obj = paginator.get_page(page) # 현재 페이지에 해당하는 게시물만 얻는다.
      context={'items': page_obj}
      
         
      return render(request, 'main/asc.html',context)

    

def new_post(request, pk):
    
    items = Item.objects.get(pk=pk)
    
    
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
UPLOAD_DIR = r'C:\practice\adminpractice\albo-main\ExcelCalculate\media\images'  #상품등록으로 인하여 업로드된 이미지 경로

#예상 가격 구간 버튼 누르면 실행되는 함수
def predict_price(request):

    if 'file1' in request.FILES:
        file = request.FILES['file1']
        file_name = file.name
        fp = open("%s%s" % (UPLOAD_DIR, file_name), 'wb')

    for chunk in file.chunks(): #바이트 형식의 데이터를 하나씩 써주겠다== 특정 크기만큼 짤라서 사용하겠다.
        fp.write(chunk) #//파일을 업로드하면 파일이 메모리에 담기게 되는데 read(),write()를 하면 메모리에 부담이 되어 서버가 다운될수 있어서 chunk를 사용한다
        fp.close()
# github = https://github.com/hgh1025/albo_epoch100.git 에서 다운로드 필요
    model_weight_path = r'C:\practice\adminpractice\albo-main\ExcelCalculate\epoch100.h5' # 범위 예측을 위한 모델링 코드
    img = Image.open("%s%s"%(UPLOAD_DIR,file_name))


    #가격예측함수 -
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

    
    # df = predict()
    # context['df']= df
    context = dict()
    context['predict'] = predict(model_weight_path, img) # 예측모델링 소스코드 경로, 예측하고자 하는 이미지 이름(등록날짜로 저장되어있음)
    # context['df']= df
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
        items.trade_status =request.POST.get('trade_status')
        item_date= request.POST.get('item_date',False)  
        items.save() #Item 테이블에 저장
        items = Item.objects.get(pk=pk) 
        
        if items.trade_status == "거래완료" :
            
            #image의 파일 형태가 PIL 형태
            image = items.item_img # Item 테이블에 img 이미지경로를 불러옴.
            # PIL 파일 또는 이미지경로는 save할수 없기 때문에 InMemoryUploadedFile 함수를 이용하여 request해온
            # 이미지 파일 형식과 동일하게 맞춰줘야한다.(불러올 이미지, 새로 저장할 이미지 이름, 저장할 이미지 경로)
            heat_file = InMemoryUploadedFile(image, None, 'heat.jpeg', 'trade_images/jpeg', None, None) #거래 완료 이미지 해당 경로로 저장
            item_price = items.item_price      
            status = Trade(item_date=item_date, item_img=heat_file ,item_price=item_price) #Trade 테이블에 저장
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
    if not 'user_name' in request.session.keys():
        return HttpResponse("<script>alert('로그인을 진행해주세요. 로그인 페이지로 이동합니다.'); location.href='/signin'</script>")
    else:
      users = User.objects.filter(user_name=request.session['user_name'])
      items = Item.objects.filter(user_name=request.session['user_name'])
      return render(request, 'main/mypage.html', {'items':items ,'users':users})

#비밀번호수정 ~ing
def uppass(request):
    if request.method == 'POST':
        u = request.user
        up = request.POST.get("uppass")
        u.set_password(up)
        u.save()
        return redirect("main_login")
    return render(request, 'main/uppass.html')
    
    
    
SIZE = 1024*256     # 256KB 크기만큼 파일을 읽음
UPLOAD_DIR1 = r'C:\practice\adminpractice\albo-main\ExcelCalculate\main\static\hash/' 
def getFileHash(filename):
    sha = SHA()
    h = open("%s%s" % (UPLOAD_DIR1, filename), 'rb')
    content = h.read(SIZE)
    while content:
        sha.update(content)         # 256KB 만큼 정보를 읽고, 해시 값을 업데이트 함  
        content = h.read(SIZE)      # 파일에서 그 다음 256KB를 읽음
    h.close()

    hashval = sha.digest()          # 최종 해시값 계산
    return hashval 

def hashCheck(file1, file2):
    hashval_1 = getFileHash(file1)
    hashval_2 = getFileHash(file2)

    if hashval_1 == hashval_2:
        print("Two Files Are Same")
    else:
        print("Two Files Are Different")

if __name__ == '__main__':

    file1 = 'plain.txt'
    file2 = 'plain_modify.txt'

    hashCheck(file1, file2)
    

    

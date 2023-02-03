from .models import *
from django import forms
from django.contrib.auth.hashers import check_password



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment',]

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment','parent']

# class EditForm(forms.ModelForm):
#     class Meta:
#         model = Item
#         fields= ['item_name','item_price','item_content','item_img']


class LoginForm(forms.Form):                                  
    username = forms.CharField(                               
        error_messages={                                     
            'required': '아이디를 입력해주세요'
        },
        max_length=32, label="사용자이름")                   
    
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label="비밀번호")         
    
    def clean(self):                                           
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password :
            try:
                user = User.objects.get(username=username)
                if not check_password(password, user.user_password):
                    self.add_error('user_password', '비밀번호를 틀렸습니다.')    
                else:
                    self.user_email = user.user_email                             
            except Exception:
                self.add_error('user_email', '존재하지 않는 아이디 입니다.')



from django import forms
import re
from webapp.models import *
from django.contrib.auth import authenticate

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, help_text="Введите имя пользователя", min_length=5, max_length=25, widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Имя пользователя'} ))
    password = forms.CharField(required=True, help_text="Укажите пароль от аккаунта", min_length=8, widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Пароль', 'type': 'password'}))
    password_con = forms.CharField(required=True, help_text="Подтверите пароль от аккаунта", min_length=8, widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Повторите пароль', 'type': 'password'}))
    email = forms.CharField(required=True, help_text="Укажите почту аккаунта", min_length=6, widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Почта'}))
    phone_number = forms.CharField(required=True, help_text="Укажите ващ номер телефона", initial="+37529", min_length=13, max_length=13, widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Номер телефона'}))
    age = forms.IntegerField(required=True, help_text="Укажите ваш возраст", widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Возраст'}))
    f_name = forms.CharField(required=True, help_text="Укажите ваше имя", widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Имя'}))
    l_name = forms.CharField(required=True, help_text="Укажите вашу фамилию", widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Фамилия'}))

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_con')
        if password != password2:
            raise forms.ValidationError("Пароли не совпадают",code='invalid')
        return self.cleaned_data

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'\+37529[0-9]{7}', phone_number):
            raise forms.ValidationError('Неправильный номер телефона', code='invalid')
        return phone_number
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError('Несовершеннолетним нельзя создавать аккаунт', code='invalid')
        elif age > 100:
            raise forms.ValidationError('Введенный возраст слишком велик', code='invalid')
        return age
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'[a-zA-Z@_\-.]+', email):
            raise forms.ValidationError('Неправильная почта', code='invalid')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Имя пользователя уже существует")
    
        return username
    
    def clean_f_name(self):
        f_name = self.cleaned_data.get('f_name')

        if not re.match(r'^[a-zA-ZА-Яа-яЁё]+$', f_name):
            raise forms.ValidationError('Неккоректный ввод имени', code='invalid')
        return f_name
    
    def clean_l_name(self):
        l_name = self.cleaned_data.get('l_name')

        if not re.match(r'^[a-zA-ZА-Яа-яЁё]+$', l_name):
            raise forms.ValidationError('Неккоректный ввод имени', code='invalid')
        return l_name
    

class LoginForm(forms.Form):
    username = forms.CharField(required=True, help_text="Введите имя пользователя", min_length=5, max_length=25, widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Имя пользователя'} ))
    password = forms.CharField(required=True, help_text="Укажите пароль от аккаунта", widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Пароль', 'type': 'password'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Неправильное имя пользователя или пароль", code='invalid')
        return cleaned_data
    
class ChangeForm(forms.Form):
    username = forms.CharField(required=False, help_text="Введите имя пользователя", min_length=5, max_length=25, widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Имя пользователя'} ))
    email = forms.CharField(required=False, help_text="Укажите почту аккаунта", min_length=6, widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Почта'}))
    phone_number = forms.CharField(required=False, help_text="Укажите ващ номер телефона", initial="+37529", max_length=13, widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Номер телефона'}))
    age = forms.IntegerField(required=False, help_text="Укажите ваш возраст", widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Возраст'}))
    f_name = forms.CharField(required=False, help_text="Укажите ваше имя", widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Имя'}))
    l_name = forms.CharField(required=False, help_text="Укажите вашу фамилию", widget=forms.TextInput(attrs={'class': 'def_input', 'placeholder': 'Фамилия'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number == "+37529":
            return phone_number

        if not re.match(r'\+37529[0-9]{7}', phone_number):
            raise forms.ValidationError('Неправильный номер телефона', code='invalid')
        return phone_number
    
    def clean_age(self):
        age = self.cleaned_data.get('age')

        if age == None:
            return age

        if age < 18:
            raise forms.ValidationError('Несовершеннолетним нельзя создавать аккаунт', code='invalid')
        elif age > 100:
            raise forms.ValidationError('Введенный возраст слишком велик', code='invalid')
        return age
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email == "":
            return email
        
        if not re.match(r'[a-zA-Z@_\-.]+', email):
            raise forms.ValidationError('Неправильная почта', code='invalid')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Имя пользователя уже существует")
    
        return username
    
    def clean_f_name(self):
        f_name = self.cleaned_data.get('f_name')

        if f_name == "":
            return f_name
        
        if not re.match(r'^[a-zA-ZА-Яа-яЁё]+$', f_name):
            raise forms.ValidationError('Неккоректный ввод имени', code='invalid')
        return f_name
    
    def clean_l_name(self):
        l_name = self.cleaned_data.get('l_name')

        if l_name == "":
            return l_name
        
        if not re.match(r'^[a-zA-ZА-Яа-яЁё]+$', l_name):
            raise forms.ValidationError('Неккоректный ввод фамилии', code='invalid')
        return l_name
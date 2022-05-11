
from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class':'form-control','type':'password','placeholder':'password'}),
        
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'class':'form-control','type':'password','placeholder':'Confirm password'}),
        
        )
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        
        
        widgets = {
            'username': forms.TextInput(
                attrs={'name': 'username', 'class': 'form-control'}),
            'email': forms.EmailInput(
                attrs={'name': 'email', 'class': 'form-control', 'placeholder': 'Email kiriting'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Tel kiriting'}),
             
        }
        
class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'last_name', 'first_name', 'email',
                  'phone_number', 'image', 'birthday', 'bio', 'address']
        
        widgets = {
            'username': forms.TextInput(
                attrs={'name': 'username', 'class': 'form-control'}),
            'last_name': forms.TextInput(
                attrs={'name': 'last_name', 'class': 'form-control', 'placeholder': 'Familiya kiriting'}),
            'first_name': forms.TextInput(
                attrs={'name': 'first_name','class': 'form-control', 'placeholder': 'Ism kiriting'}),
             'email': forms.EmailInput(
                attrs={'name': 'email', 'class': 'form-control',  'placeholder': 'Email kiriting'}),
            'phone_number': forms.TextInput(
                attrs={'name': 'phone_number', 'class': 'form-control', 'placeholder': 'Nomer kiriting'}),
            'image': forms.TextInput(
                attrs={'name': 'image','type':'file', 'class': 'form-control', 'placeholder': 'Rasm kiriting'}),
            'birthday': forms.TextInput(
                attrs={'name': 'birthday','class': 'form-control', 'placeholder': 'Tugulgan yilingizni kiriting'}),
            'bio': forms.TextInput(
                attrs={'name': 'bio','class': 'form-control', 'placeholder': 'Bio kiriting'}),
            'address': forms.TextInput(
                attrs={'name': 'address','class': 'form-control', 'placeholder': 'Address kiriting'}),
             
        }
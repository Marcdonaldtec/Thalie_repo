from typing import Any
from django import forms
from .models import Product, Category, Brand,Inventory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'brand', 'image']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
        
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['quantity']
        
class StockAdjustmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product_choices = [(product.pk, product.title) for product in Product.objects.all()]
        self.fields['product_data'] = forms.MultipleChoiceField(
            choices=product_choices,
            widget=forms.CheckboxSelectMultiple()
        )
        self.fields['quantity'] = forms.IntegerField(min_value=0, initial=0)
class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(max_length=255)
    whatsapp_number = forms.CharField(max_length=15)

class SignUpfum(forms.ModelForm):
    last_name = forms.CharField(max_length=255, required=True)
    first_name = forms.CharField(max_length=255, required=True)
    email = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.TextInput(max_length=255, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name', 'phone', 'address','password1','password2']
    def clean(self) :
       cleaned_data =super().clean()
       username = cleaned_data.get('username')
       email = cleaned_data.get('email')
       phone = cleaned_data.get('phone')
       
       if User.objects.filter(username__iexact=username).exists():
           self.add_error('username','This username is already exist')
           
       if User.objects.filter(email__iexact=email).exists():
           self.add_error('email','This email is already exist')
           
       if len(phone) < 8 :
           self.add_error('phone', 'Phone number incorrect')
       
       return cleaned_data
   
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
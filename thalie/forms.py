from django import forms
from .models import Product, Category, Brand,Inventory
from django.contrib.auth.models import User


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
    shipping_address = forms.CharField(widget=forms.Textarea, required=True)
    payment_details = forms.CharField(widget=forms.Textarea, required=True)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(max_length=255)
    whatsapp_number = forms.CharField(max_length=15)

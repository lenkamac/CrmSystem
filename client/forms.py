from django import forms

from .models import Client, Comment, ClientFile, Purchase
from product.models import Product


class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class AddFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ('file',)


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'quantity', 'notes']  # Remove purchase_price
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_product',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'id': 'id_quantity',
            }),
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add notes about this purchase...',
                                           'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show all products (no quantity restriction)
        self.fields['product'].queryset = Product.objects.all()
        # Display product name with price
        self.fields['product'].label_from_instance = lambda obj: f"{obj.name} - ${obj.net_price}"
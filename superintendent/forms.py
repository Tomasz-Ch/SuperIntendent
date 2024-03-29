from datetime import datetime

from django import forms

from superintendent.models import School, Products, Inventory

from superintendent.models import TYPES


class SchoolModelForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'


class NewMenuForm(forms.Form):
    date = forms.DateField(label="Data obiadu", initial=datetime.now())
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 85}))


class AddProductFormModel(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'


class InvoiceForm(forms.Form):
    operation_date = forms.DateField(label="Data przyjęcia", initial=datetime.now())
    operation_type = forms.IntegerField(widget=forms.Select(choices=TYPES), initial=TYPES[0])
    quantity = forms.FloatField()
    price = forms.DecimalField()
    product = forms.ModelChoiceField(queryset=Products.objects.all())


class UsedForm(forms.Form):
    operation_date = forms.DateField(label="Data wydania", initial=datetime.now())
    operation_type = forms.IntegerField(widget=forms.Select(choices=TYPES), initial=TYPES[1])
    quantity = forms.FloatField()
    price = forms.DecimalField()
    product = forms.ModelChoiceField(queryset=Products.objects.all())


# class ReportForm(forms.Form):
#     name = forms.CharField()


class SearchProductForm(forms.Form):
    name = forms.CharField(label="Nazwa produktu", max_length=128)


class ContactForm(forms.Form):
    from_email = forms.EmailField(label="E-mail", required=True)
    subject = forms.CharField(label="Temat wiadomości", required=True)
    message = forms.CharField(label="Treść wiadomości", widget=forms.Textarea, required=True)


class DateForm(forms.Form):
    date_from = forms.DateField(label="Okres od:")
    date_to = forms.DateField(label="Okres do:", initial=datetime.now())


class MealNumberForm(forms.Form):
    meal_date = forms.DateField(label="Data obiadu")
    meal_number = forms.IntegerField(label="Liczba posiłków")

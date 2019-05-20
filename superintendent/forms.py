from datetime import datetime

from django import forms

from superintendent.models import School, Products


class SchoolModelForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'


class NewMenuForm(forms.Form):
    date = forms.DateField(label="Data obiadu", initial=datetime.now())
    name = forms.CharField(widget=forms.Textarea)


class AddProductFormModel(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'

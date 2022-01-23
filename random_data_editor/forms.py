from django import forms

class CleanForm(forms.Form):
    string = forms.CharField(max_length=150)
from django import forms


class SearchForm(forms.Form):
    full_name = forms.CharField(label="Пошук за повним ім'ям", max_length=100)

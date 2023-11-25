from django import forms


class SearchForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your name"}
        ),
    )

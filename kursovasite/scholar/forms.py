from django import forms


class SearchForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your name"}
        ),
    )
class SearchForm_Elsevier(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter first name"}
        ),
    )
    
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter last name"}
        ),
    )
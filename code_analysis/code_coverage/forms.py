from django import forms

class RepositoryForm (forms.Form):
    url = forms.CharField(max_length=256)

"""
class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)
"""
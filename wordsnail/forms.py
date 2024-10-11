from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
	username = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ("username", "password1", "password2")

	def save(self, commit=True):
		user = super(RegisterUserForm, self).save(commit=False)
		user.username = self.cleaned_data['username']
		if commit:
			user.save()
		return user

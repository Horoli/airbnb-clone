from django import forms
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data  # 입력된 password가 일치하면 self.cleaned_data를 return
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ("email",)

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        user.username = email
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    # username = forms.EmailField(label="Email")

    # class Meta:
    #     model = models.User
    #     fields = ("first_name", "last_name", "email")

    # password = forms.CharField(widget=forms.PasswordInput)
    # password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # def clean_password1(self):

    #     password = self.cleaned_data.get("password")
    #     password1 = self.cleaned_data.get("password1")

    #     if password != password1:
    #         raise forms.ValidationError("Password confirmation does not match")
    #     else:
    #         return password

    # def save(self, *args, **kwargs):
    #     user = super().save(commit=False)  # commit=False 로 database에 업로드를 차단함
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     user.username = email
    #     user.set_password(password)
    #     user.save()

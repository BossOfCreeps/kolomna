from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Почта")
    last_name = forms.CharField(label="Фамилия")
    first_name = forms.CharField(label="Имя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Почта")
    last_name = forms.CharField(label="Фамилия")
    first_name = forms.CharField(label="Имя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))


class LoginForm(forms.Form):
    email = forms.EmailField(label="Почта")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))


class MassEmailForm(forms.Form):
    title = forms.CharField(label="Заголовок письма")
    text = forms.CharField(widget=forms.Textarea, label="Текст письма")
    emails = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={"checked": "checked"}), label="Почты")

    def __init__(self, *args, **kwargs):
        self.emails = kwargs.pop("emails", None)
        super(MassEmailForm, self).__init__(*args, **kwargs)
        self.fields["emails"].choices = self.emails

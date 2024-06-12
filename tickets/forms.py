from django import forms


class BuyForm(forms.Form):
    schedule = forms.IntegerField()
    visitor_standard = forms.IntegerField()
    visitor_child = forms.IntegerField()
    visitor_student = forms.IntegerField()
    visitor_retiree = forms.IntegerField()
    next = forms.CharField()

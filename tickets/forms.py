from django import forms


class BuyForm(forms.Form):
    event_id = forms.IntegerField()
    schedule = forms.IntegerField()
    visitor_standard = forms.IntegerField()
    visitor_child = forms.IntegerField()
    visitor_student = forms.IntegerField()
    visitor_retiree = forms.IntegerField()
    next = forms.CharField()

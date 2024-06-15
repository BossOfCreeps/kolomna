from django import forms
from django.db import transaction

from helpers import MultipleFileField
from tickets.models import Review, ReviewImage


class BuyForm(forms.Form):
    schedule = forms.IntegerField()
    visitor_standard = forms.IntegerField()
    visitor_child = forms.IntegerField()
    visitor_student = forms.IntegerField()
    visitor_retiree = forms.IntegerField()
    next = forms.CharField()


class ReviewForm(forms.ModelForm):
    files = MultipleFileField(required=False, label="Изображения")
    rate = forms.IntegerField(min_value=0, max_value=5, label="Рейтинг")

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop("event", [])
        self.user = kwargs.pop("user")
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["event"].choices = [(p.id, p.name) for p in self.event]

    @transaction.atomic()
    def save(self, commit=True):
        result = super(ReviewForm, self).save(commit=False)
        result.user = self.user
        result.save()

        for file in self.cleaned_data["files"]:
            ReviewImage.objects.create(review=result, file=file)

        return result

    class Meta:
        model = Review
        fields = ["event", "text", "rate", "files"]


class PurchaseVisitForm(forms.Form):
    pass

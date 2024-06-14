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

    @transaction.atomic()
    def save(self, commit=True):
        result = super(ReviewForm, self).save(commit=commit)

        for file in self.cleaned_data["files"]:
            ReviewImage.objects.create(review=result, file=file)

        return result

    class Meta:
        model = Review
        fields = "__all__"

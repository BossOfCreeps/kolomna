from django import forms
from django.db import transaction

from events.models import Event, EventImage, EventSchedule
from helpers import MultipleFileField, DateTimeLocalField


class EventForm(forms.ModelForm):
    files = MultipleFileField(
        required=False,
        label="Изображения",
        help_text="Если новые прикрепить изображения - старые удаляться. Будьте внимательны. "
        "Оставьте поле пустым - и ничего измениться",
    )

    @transaction.atomic()
    def save(self, commit=True):
        result = super(EventForm, self).save(commit=commit)

        if self.cleaned_data["files"]:
            result.images.all().delete()

        for file in self.cleaned_data["files"]:
            EventImage.objects.create(event=result, file=file)

        return result

    class Meta:
        model = Event
        fields = "__all__"


class EventScheduleCreateForm(forms.Form):
    event_id = forms.IntegerField()
    period = forms.CharField(label="Период")

    datetime_start = DateTimeLocalField(label="Дата и время начало", required=False)
    datetime_end = DateTimeLocalField(label="Дата и время конца", required=False)

    price_standard = forms.IntegerField(required=True)
    price_student = forms.IntegerField(required=True)
    price_child = forms.IntegerField(required=True)
    price_retiree = forms.IntegerField(required=True)

    visitors_standard = forms.IntegerField(required=False)
    visitors_student = forms.IntegerField(required=False)
    visitors_child = forms.IntegerField(required=False)
    visitors_retiree = forms.IntegerField(required=False)

    time_start = forms.TimeField(label="Время начала", required=False)
    time_end = forms.TimeField(label="Время конца", required=False)
    date_start = forms.DateField(label="Дата начала", required=False)
    date_end = forms.DateField(label="Дата конца", required=False)

    weekday = forms.MultipleChoiceField(
        choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("0", "0")], required=False
    )


class EventScheduleUpdateForm(forms.Form):
    pass

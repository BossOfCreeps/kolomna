from django.contrib import admin

from events.models import Event, EventImage, Organization, EventSchedule, EventSchedulePrice


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    class EventImageInline(admin.TabularInline):
        model = EventImage

    inlines = [EventImageInline]


@admin.register(EventSchedule)
class EventScheduleAdmin(admin.ModelAdmin):
    class EventSchedulePriceInline(admin.TabularInline):
        model = EventSchedulePrice

    model = EventSchedule
    inlines = [EventSchedulePriceInline]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

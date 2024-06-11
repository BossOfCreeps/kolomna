from django.contrib import admin

from events.models import Event, EventImage, Organization, EventSchedule


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    class EventImageInline(admin.TabularInline):
        model = EventImage

    class EventScheduleInline(admin.TabularInline):
        model = EventSchedule

    inlines = [EventImageInline, EventScheduleInline]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

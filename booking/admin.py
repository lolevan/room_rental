from django.contrib import admin

from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Booking, Advertisement, Room

from datetime import datetime

from decimal import Decimal


class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'customer_name', 'date', 'start_time', 'end_time', 'total_cost', 'confirmed')
    list_filter = ('room', 'date', 'customer_name')
    search_fields = ('room__name', 'customer_name', 'customer_email')

    def total_cost(self, obj):
        start_datetime = datetime.combine(obj.date, obj.start_time)
        end_datetime = datetime.combine(obj.date, obj.end_time)
        duration = end_datetime - start_datetime
        total_hours = duration.total_seconds() / 3600
        return obj.room.price_per_hour * Decimal(total_hours)

    total_cost.short_description = 'Total Cost'


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('booking', 'title', 'price')
    search_fields = ('booking__room__name', 'title')


class RoomAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Room
        fields = '__all__'


class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm
    list_display = ('name', 'capacity', 'price_per_hour', 'start_time', 'end_time')
    list_filter = ('capacity', 'price_per_hour')


admin.site.register(Booking, BookingAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Room, RoomAdmin)

# Register your models here.

from django import forms
from .models import Booking, Advertisement, Room


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'customer_name', 'customer_email']


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'image']


class AdditionalDetailsForm(forms.Form):
    event_name = forms.CharField(max_length=200, required=True)
    advertise = forms.BooleanField(required=False)

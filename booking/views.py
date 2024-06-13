from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Room, Booking, Advertisement

from .forms import BookingForm, AdvertisementForm, AdditionalDetailsForm

from datetime import datetime, timedelta

from decimal import Decimal


def home(request):
    return render(request, 'booking/home.html')


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'booking/room_list.html', {'rooms': rooms})


def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'booking/advertisement_list.html', {'advertisements': advertisements})


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'booking/room_detail.html', {'room': room})


def advertisement_detail(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    return render(request, 'booking/advertisement_detail.html', {'advertisement': advertisement})


def book_room(request, pk, date):
    room = get_object_or_404(Room, pk=pk)
    selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    confirmed_bookings = Booking.objects.filter(room=room, date=selected_date, confirmed=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.date = selected_date

            # Ensure the booking is within the working hours of the room
            if room.start_time <= booking.start_time and booking.end_time <= room.end_time:

                # Ensure the booking is at least one hour long
                booking_duration = datetime.combine(datetime.min, booking.end_time) - datetime.combine(datetime.min,
                                                                                                       booking.start_time)
                if booking_duration < timedelta(hours=1):
                    form.add_error(None, 'The booking must be at least one hour long.')
                else:
                    # Check for overlapping bookings
                    overlapping_bookings = Booking.objects.filter(
                        room=room, date=selected_date,
                        start_time__lt=booking.end_time,
                        end_time__gt=booking.start_time,
                        confirmed=True
                    )
                    if overlapping_bookings.exists():
                        form.add_error(None, 'The booking overlaps with an existing booking.')
                    else:
                        booking.save()
                        return redirect('additional_details', pk=booking.pk)
            else:
                form.add_error(None, 'Booking time must be within the working hours of the room.')
    else:
        form = BookingForm(initial={'date': selected_date})
    return render(request, 'booking/book_room.html', {'form': form, 'room': room, 'confirmed_bookings': confirmed_bookings,
                                              'selected_date': selected_date})


def additional_details(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    room = booking.room
    booking_duration = datetime.combine(datetime.min, booking.end_time) - datetime.combine(datetime.min,
                                                                                           booking.start_time)
    price = Decimal(booking_duration.total_seconds() / 3600) * room.price_per_hour

    if request.method == 'POST':
        form = AdditionalDetailsForm(request.POST)
        if form.is_valid():
            booking.event_name = form.cleaned_data['event_name']
            booking.advertise = form.cleaned_data['advertise']
            booking.save()

            # Отправка уведомления о принятии заявки
            user_email = booking.customer_email  # Предполагается, что у Booking есть поле customer_email
            mail_sent = send_mail(
                'Ваша заявка принята',
                'Ваш запрос на бронирование был успешно обработан. Спасибо за использование наших услуг.',
                settings.EMAIL_HOST_USER,
                [user_email],
                fail_silently=True,
            )

            if mail_sent:
                messages.success(request, 'Заявка принята и письмо отправлено пользователю')
                print('Mail sent')
            else:
                messages.error(request, 'Заявка принята, но письмо не было отправлено')
                print('Mail not sent')

            return redirect('index')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = AdditionalDetailsForm()

    return render(request, 'booking/additional_details.html', {'form': form, 'price': price, 'booking': booking})


def select_date(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        return redirect('book_room', pk=room.pk, date=selected_date)
    return render(request, 'booking/select_date.html', {'room': room})

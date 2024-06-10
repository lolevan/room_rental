from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/<int:pk>/select_date/', views.select_date, name='select_date'),
    path('rooms/<int:pk>/book/<str:date>/', views.book_room, name='book_room'),
    path('advertisements/', views.advertisement_list, name='advertisement_list'),
    path('advertisements/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('additional_details/<int:pk>/', views.additional_details, name='additional_details'),
]

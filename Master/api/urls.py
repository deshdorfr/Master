# api/urls.py
from django.urls import path
from .views import (
    ESP32DeviceListCreateView,
    ESP32DeviceRetrieveUpdateDestroyView,
    ChannelListCreateView,
    ChannelRetrieveUpdateDestroyView,
    AlarmListCreateView,
    AlarmRetrieveUpdateDestroyView
)

urlpatterns = [
    path('esp_devices/', ESP32DeviceListCreateView.as_view(), name='esp-device-list-create'),
    path('esp_devices/<int:pk>/', ESP32DeviceRetrieveUpdateDestroyView.as_view(), name='esp-device-detail'),
    path('channels/<int:esp_device_id>/', ChannelListCreateView.as_view(), name='channel-list-create'),
    path('channels/<int:esp_device_id>/channels/<int:pk>/', ChannelRetrieveUpdateDestroyView.as_view(), name='channel-detail'),
    path('alarms/', AlarmListCreateView.as_view(), name='alarm-list-create'),
    path('alarms/<int:pk>/', AlarmRetrieveUpdateDestroyView.as_view(), name='alarm-detail'),
]

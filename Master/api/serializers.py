# api/serializers.py
from rest_framework import serializers
from .models import ESP32Device, Channel

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'esp_device', 'name', 'command']
        read_only_fields = ['id']

class ESP32DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESP32Device
        fields = ['id', 'name']

class ChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['name', 'command', 'esp_device']

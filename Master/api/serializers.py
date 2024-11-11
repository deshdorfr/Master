# api/serializers.py
from rest_framework import serializers
from .models import ESP32Device, Channel, Alarm

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'esp_device', 'name', 'command']
        # read_only_fields = ['id']

class ESP32DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESP32Device
        fields = ['id', 'name']

class ChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['name', 'command', 'esp_device']


class AlarmSerializer(serializers.ModelSerializer):
    # Override the repeat field to accept a list of days
    repeat = serializers.ListField(
        child=serializers.ChoiceField(choices=[
            'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'
        ]),
        allow_empty=True
    )

    class Meta:
        model = Alarm
        fields = '__all__'

    def validate_repeat(self, value):
        # Convert list to a comma-separated string as required by MultiSelectField
        return ",".join(value)

    def to_representation(self, instance):
        # Convert the comma-separated string back to a list for API output
        representation = super().to_representation(instance)
        representation['repeat'] = instance.repeat.split(",") if instance.repeat else []
        return representation

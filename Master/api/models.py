# api/models.py
from django.db import models
from multiselectfield import MultiSelectField
from django.utils import timezone

class ESP32Device(models.Model):
    """Model to store ESP32 device information."""
    name = models.CharField(max_length=100, unique=True)  # Unique ESP32 device name

    def __str__(self):
        return self.name


class Channel(models.Model):
    """Model to store channel information associated with an ESP32 device."""
    esp_device = models.ForeignKey(ESP32Device, related_name='channels', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Name of the channel
    command = models.CharField(max_length=10, default="OFF")  # Command state (ON/OFF)

    class Meta:
        unique_together = ('esp_device', 'name')  # Ensure that each channel name is unique per ESP32

    def __str__(self):
        return f"{self.esp_device.name} - {self.name}: {self.command}"
    
class Alarm(models.Model):
    """Model to store alarm information for channels."""
    
    # Days of the week choices
    WEEKDAYS = (
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    )

    description = models.CharField(max_length=200)  # Alarm description
    repeat = MultiSelectField(choices=WEEKDAYS)  # Days of the week to repeat
    start_date = models.DateField()  # Start date of the alarm
    time = models.TimeField()  # Time of the alarm
    channel = models.ForeignKey(Channel, related_name='alarms', on_delete=models.CASCADE)
    command = models.CharField(max_length=10)  # Command to set on the channel (e.g., ON/OFF)

    def __str__(self):
        return f"Alarm {self.id} - {self.description}"

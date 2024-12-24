# api/models.py
from django.db import models
from multiselectfield import MultiSelectField
from django.utils import timezone
from django.utils.timezone import make_aware, localtime, now
import datetime

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
    
    # New fields
    identification_id = models.IntegerField(null=True, blank=True)  # Optional unique identifier
    led_pin = models.IntegerField(null=True, blank=True)  # Optional GPIO pin for LED
    input_pin = models.IntegerField(null=True, blank=True)  # Optional GPIO pin for input signal

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

    description = models.CharField(max_length=200)
    repeat = MultiSelectField(choices=WEEKDAYS)
    start_date = models.DateField()
    time = models.TimeField()  # Time of the alarm (naive)
    channel = models.ForeignKey(Channel, related_name='alarms', on_delete=models.CASCADE)
    command = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        # Combine the time with today's date to make it timezone-aware
        naive_time = datetime.datetime.combine(now().date(), self.time)
        aware_time = make_aware(naive_time)  # Convert to timezone-aware datetime
        utc_time = aware_time.astimezone(datetime.timezone.utc)  # Convert to UTC
        
        # Extract and store only the time part back into the time field
        self.time = utc_time.time()
        super().save(*args, **kwargs)

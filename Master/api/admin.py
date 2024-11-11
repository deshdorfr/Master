from django.contrib import admin
from .models import ESP32Device, Channel, Alarm

# Register your models here.

# Register ESP32Device model
@admin.register(ESP32Device)
class ESP32DeviceAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the 'name' field in the list view
    search_fields = ('name',)  # Allow searching by name
    list_filter = ('name',)  # Add filters based on 'name'

# Register Channel model
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('esp_device', 'name', 'command')  # Display esp_device, name, and command
    search_fields = ('esp_device__name', 'name')  # Allow searching by device name or channel name
    list_filter = ('command',)  # Add filter options based on the 'command' field
    
@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'start_date', 'time', 'channel', 'command')
    search_fields = ('description', 'channel__name')
    list_filter = ('start_date', 'command', 'repeat')
    # filter_horizontal = ('repeat',)  # For easier multiple day selection in the admin

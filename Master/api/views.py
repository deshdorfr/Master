# api/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import ESP32Device, Channel, Alarm
from .serializers import ESP32DeviceSerializer, ChannelSerializer, ChannelCreateSerializer, AlarmSerializer
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from django.utils.timezone import now
from django.utils.timezone import now, localtime, make_aware

import datetime

class ESP32DeviceListCreateView(generics.ListCreateAPIView):
    """API to list all ESP32 devices or create a new one."""
    queryset = ESP32Device.objects.all()
    serializer_class = ESP32DeviceSerializer
    permission_classes = [AllowAny]


class ESP32DeviceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """API to retrieve, update, or delete a specific ESP32 device."""
    queryset = ESP32Device.objects.all()
    serializer_class = ESP32DeviceSerializer
    permission_classes = [AllowAny]

class ChannelListCreateView(generics.ListCreateAPIView):
    """
    API to list all channels for a specific ESP32 device or create a new channel.
    """
    serializer_class = ChannelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Filter channels by the associated ESP32 device."""
        esp_device_id = self.kwargs.get('esp_device_id')
        if not ESP32Device.objects.filter(id=esp_device_id).exists():
            raise NotFound(f"ESP32 Device with id {esp_device_id} not found.")
        return Channel.objects.filter(esp_device_id=esp_device_id)

    def list(self, request, *args, **kwargs):
        """Override the list method to check and apply alarms."""
        queryset = self.get_queryset()
        # Check and apply alarms before returning the queryset
        for channel in queryset:
            self.check_and_apply_alarms(channel)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, esp_device_id, *args, **kwargs):
        """Create a new channel for a specific ESP32 device."""
        esp_device = generics.get_object_or_404(ESP32Device, id=esp_device_id)
        serializer = ChannelCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(esp_device=esp_device)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_and_apply_alarms(self, channel):
        """Check and apply alarms for a given channel."""
        current_time = now()  # Convert UTC to local timezone (Asia/Kolkata)
        current_day = current_time.strftime('%A').lower()  # e.g., 'monday'

        # Fetch alarms for this channel that are active
        alarms = channel.alarms.filter(
            start_date__lte=current_time.date(),  # Start date is in the past or today
            repeat__contains=current_day  # Today is included in repeat days
        )
        

        for alarm in alarms:
            # Combine date and time to create a naive datetime for the alarm time
            alarm_time_naive = datetime.datetime.combine(current_time.date(), alarm.time)
            # Make alarm_time timezone-aware
            alarm_time = make_aware(alarm_time_naive, timezone=current_time.tzinfo)

            # Check if alarm time is within the last 10 seconds
            # breakpoint()
            if 0 <= (current_time - alarm_time).total_seconds() <= 50:
                # Update channel command
                channel.command = alarm.command
                channel.save()

class ChannelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """API to retrieve, update, or delete a specific channel."""
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [AllowAny]
    
class AlarmListCreateView(generics.ListCreateAPIView):
    """API to list all alarms or create a new alarm."""
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    permission_classes = [AllowAny]


class AlarmRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """API to retrieve, update, or delete a specific alarm."""
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    permission_classes = [AllowAny]

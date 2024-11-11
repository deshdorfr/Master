# api/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import ESP32Device, Channel, Alarm
from .serializers import ESP32DeviceSerializer, ChannelSerializer, ChannelCreateSerializer, AlarmSerializer
from rest_framework.permissions import AllowAny

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
    """API to list all channels for a specific ESP32 device or create a new channel."""
    serializer_class = ChannelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Filter channels by the associated ESP32 device."""
        esp_device_id = self.kwargs['esp_device_id']
        return Channel.objects.filter(esp_device_id=esp_device_id)

    def post(self, request, esp_device_id, *args, **kwargs):
        """Create a new channel for a specific ESP32 device."""
        esp_device = generics.get_object_or_404(ESP32Device, id=esp_device_id)
        serializer = ChannelCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(esp_device=esp_device)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

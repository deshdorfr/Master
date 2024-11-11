# api/tasks.py
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Alarm

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

def execute_alarms():
    now = timezone.localtime(timezone.now())
    
    current_time = now.strftime('%H:%M')
    current_date = now.date()
    current_weekday = now.strftime('%A').lower()

    # Fetch alarms that need to be executed
    # logger.info(f"Executing alarms task at {current_weekday} {now}, {current_time+':00'},=======>>> {Alarm.objects.get(id=1).time}")  # Log the execution time
    alarms = Alarm.objects.filter(
        start_date__lte=current_date,
        time=current_time+':00'
    )
    for alarm in alarms:
        if current_weekday in alarm.repeat:
            alarm.channel.command = alarm.command
            alarm.channel.save()

# Set up APScheduler
scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.add_job(execute_alarms, 'interval', minutes=1)  # Run every minute
scheduler.start()

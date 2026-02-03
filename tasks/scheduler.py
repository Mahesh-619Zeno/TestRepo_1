from apscheduler.schedulers.background import BackgroundScheduler
from services.notification_service import NotificationService
import time

def start_scheduler():
    """Start the reminder scheduler (TDRS-001-C)"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=NotificationService.process_reminders,
        trigger="interval",
        minutes=1
    )
    scheduler.start()
    print("Reminder scheduler started (runs every minute)")
    
    # Keep the service running
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    start_scheduler()
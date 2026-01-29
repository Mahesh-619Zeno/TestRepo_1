from datetime import datetime, timedelta
import pytz

def validate_due_date(due_date):
    """Validate that due_date is a datetime object in the future."""
    now = datetime.now(pytz.UTC)
    if due_date is None:
        return True  # due_date optional
    if not isinstance(due_date, datetime):
        return False
    if due_date <= now:
        return False
    return True

def validate_reminder_time(due_date, reminder_minutes):
    """Validate that reminder time is before due date."""
    if due_date is None:
        # Cannot have reminder without due_date
        return reminder_minutes is None or reminder_minutes == 0
    if reminder_minutes is None or reminder_minutes == 0:
        return True  # No reminder set
    reminder_datetime = due_date - timedelta(minutes=reminder_minutes)
    now = datetime.now(pytz.UTC)
    if reminder_datetime <= now or reminder_datetime >= due_date:
        return False
    return True

def compute_next_due_date_for_recurring(task):
    # Simplified example for daily/weekly/monthly recurrence
    from dateutil.relativedelta import relativedelta
    if not task.is_recurring or not task.due_date or not task.recurrence_pattern:
        return None
    freq = task.recurrence_pattern.get('frequency')
    interval = task.recurrence_pattern.get('interval', 1)
    current_due = task.due_date
    if freq == 'daily':
        return current_due + relativedelta(days=interval)
    elif freq == 'weekly':
        return current_due + relativedelta(weeks=interval)
    elif freq == 'monthly':
        return current_due + relativedelta(months=interval)
    return None
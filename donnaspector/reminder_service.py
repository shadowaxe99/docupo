import datetime

class ReminderService:
    def set_reminder(self, message, datetime_str):
        reminder_time = datetime.datetime.now() + datetime.timedelta(hours=1)
        print(f'Setting reminder for {reminder_time}')

    def check_reminders(self):
        return []
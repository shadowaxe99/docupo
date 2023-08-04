import unittest
from calendar_integration import CalendarIntegration
from chat_interface import ChatInterface
from nlp_functions import NLPProcessor
from reminder_service import ReminderService

class TestSuite(unittest.TestCase):
    def test_calendar_integration(self):
        creds = 'your-credentials'  # replace with actual credentials
        calendar = CalendarIntegration(creds)
        event = {'summary': 'Test Event'}
        result = calendar.schedule_event(event)
        self.assertIsNotNone(result)

    def test_chat_interface(self):
        api_key = 'your-api-key'  # replace with actual API key
        chat = ChatInterface(api_key)
        prompt = 'Hello, how are you?'
        response = chat.chat(prompt)
        self.assertIsNotNone(response)

    def test_nlp_functions(self):
        nlp = NLPProcessor()
        user_input = 'I am feeling happy'
        result = nlp.classify_task(user_input)
        self.assertEqual(result, 'POSITIVE')

    def test_reminder_service(self):
        reminder = ReminderService()
        message = 'Test Reminder'
        datetime_str = '2023-08-03 10:00:00'
        reminder.set_reminder(message, datetime_str)
        reminders = reminder.check_reminders()
        self.assertIn(message, reminders)

if __name__ == '__main__':
    unittest.main()
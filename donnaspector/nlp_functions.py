from transformers import pipeline

class NLPProcessor:
    def __init__(self):
        self.classifier = pipeline('sentiment-analysis')

    def classify_task(self, user_input):
        result = self.classifier(user_input)[0]
        if result['label'] == 'POSITIVE' and result['score'] > 0.5:
            return 'schedule_meeting'
        elif result['label'] == 'NEGATIVE' and result['score'] > 0.5:
            return 'set_reminder'
        else:
            return 'send_email'
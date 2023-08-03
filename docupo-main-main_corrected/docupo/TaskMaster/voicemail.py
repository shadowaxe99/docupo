class Voicemail:
    def __init__(self, account):
        self.account = account

    def record_message(self, message):
        self.message = message
        return 'Message recorded'

    def call(self):
        return 'Calling...'
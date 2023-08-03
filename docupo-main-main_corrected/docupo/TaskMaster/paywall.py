class Paywall:
    def __init__(self, user):
        self.user = user

    def check_subscription(self):
        if self.user.subscription:
            return True
        else:
            return False
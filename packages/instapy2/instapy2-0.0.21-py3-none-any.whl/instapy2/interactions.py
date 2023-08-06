class InteractionsUtility:
    def __init__(self):
        self.amount = 0
        self.enabled = False
        self.percentage = 0
        self.randomize = False

    def set_amount(self, amount: int):
        self.amount = amount

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_percentage(self, percentage: int):
        self.percentage = percentage

    def set_randomize(self, randomize: bool):
        self.randomize = randomize
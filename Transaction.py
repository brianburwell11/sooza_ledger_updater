class Transaction():
    def __init__(self, date, transaction_id, credit, amount, to_from, note):
        self.date       = date
        self.id         = transaction_id
        self.credit     = credit
        self.amount     = amount
        self.to_from    = to_from
        self.note       = note

    def __str__(self):
        if self.credit:
            return f'{self.id}: Received {self.amount} from {self.to_from} on {self.date} with message "{self.note}"'
        else:
            return f'{self.id}: Sent {self.amount} to {self.to_from} on {self.date} with message "{self.note}"'
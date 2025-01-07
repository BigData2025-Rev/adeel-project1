import datetime

class Order:
    def __init__(self, id, account, items, total, delivery_date, points_earned, points_used, status = "1"):
        self.id = id
        self.account = account
        self.items = items
        self.total = total
        self.delivery_date = delivery_date
        self.points_earned = points_earned
        self.points_used = points_used
        self.status = status
        self.time_placed = datetime.now()().strftime("%m/%d/%Y, %H:%M:%S")
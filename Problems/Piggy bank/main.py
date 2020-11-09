class PiggyBank:
    def __init__(self,dollars,cents):
        if cents < 100:
            self.dollars = dollars
            self.cents = cents
        else:
            self.dollars = dollars + cents // 100
            self.cents = cents - 100 * (cents//100)
    def add_money(self,dollars,cents):
        self.dollars += dollars
        self.cents += cents
        if self.cents >= 100:
            self.dollars = self.dollars + self.cents // 100
            self.cents = self.cents - 100 * (self.cents//100)

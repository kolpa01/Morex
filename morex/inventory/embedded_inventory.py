class MorexInventory:
    def __init__(self, user):
        self.user = user
        self._inventory = {}

    async def add_item(self, item_id, amount: int):
        try:
            self._inventory[item_id] += amount
        except KeyError:
            self._inventory.update({item_id: amount})

    async def remove_item(self, item_id, amount: int):
        try:
            self._inventory[item_id] -= amount
        except KeyError:
            pass

    async def get_amount(self, item_id):
        amount = 0
        try:
            amount = self._inventory[item_id]
        except KeyError:
            amount = 0

        return amount

    @property
    def items(self):
        return self._inventory

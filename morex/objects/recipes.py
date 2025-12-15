from morex import MorexItem
import morex.inventory.utils as inv_utils
import morex.logging as logging


class MorexRecipe:
    def __init__(
        self, 
        recipe_id: str,
        item: MorexItem, 
        available: bool,
        amount: int,
        ingredients: list 
    ):
        self.id = recipe_id
        self.item = item
        self.amount = amount
        self.available = available
        self.ingredients = ingredients

    def __bool__(self):
        return True

    async def get_items_amount_from_inv(self, user):
        item_ids = []
        for ingredient in self.ingredients:
            item_ids.append(ingredient['item'].id)
        amounts = await inv_utils.items_amount.get_bulk_amount(user, items=item_ids)

        return amounts

    async def get_all(self, user):
        amounts = await self.get_items_amount_from_inv(user)

        possible_items = 0
        for ingredient in self.ingredients:
            amount = amounts[ingredient['item'].id]
            possible_items_candidate = amount // ingredient['amount']
            logging.success(str(possible_items_candidate))
            if not possible_items_candidate:
                return 1
            if possible_items_candidate < possible_items or not possible_items:
                possible_items = possible_items_candidate
        return possible_items

    async def get_missing_items(self, user, amount):
        amounts = await self.get_items_amount_from_inv(user)

        missing_items = []
        for ingredient in self.ingredients:
            if ingredient['amount'] * amount > amounts[ingredient['item'].id]:
                missing_items.append({'item': ingredient['item'], "amount": (ingredient['amount'] * amount) - amounts[ingredient['item'].id]})

        return missing_items

    async def craft(self, user, amount):
        missing_items = await self.get_missing_items(user, amount)

        if missing_items:
            return missing_items

        for ingredient in self.ingredients:
            await ingredient['item'].remove_item(user, amount * ingredient['amount'])
        await self.item.add_item(user, amount * self.amount)
        
        return 

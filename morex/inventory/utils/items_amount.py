import json


async def get_bulk_amount(user, exclude: list = None, items=None):
    """
    Returns specific items in form of a dict
    {
        item: amount,
    }
    """
    with open("userdb/inventories.json", "r") as f:
        users = json.load(f)
    
    if exclude is None:
        exclude = []
    
    amounts = {}
    for item in users[str(user.id)]["bag"]:
        if (item['item'] in items if items is not None else True) and (item['item'] not in exclude) and ((('i' not in item['item'] and 'a' not in item['item']) if item['item'] not in (items if items is not None else []) else True)):
            amounts.update({item['item']: item['amount']})
            if item['item'] in items if items is not None else False:
                items.remove(item['item'])
    if items:
        for lacking_item in items:
            amounts.update({lacking_item: 0})

    return amounts

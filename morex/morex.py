import json
import morex.enums as enums


class CustomUser:
    def __init__(self, iid, name, avatar, bot):
        self.id = iid
        self.name = name
        self.display_avatar = avatar
        self.bot = bot

# Parent Class


class MorexItem:
    def __init__(self, item: dict, lang: list, language=None) -> None:
        self.sid = item["name"]
        self.id = item["id"]
        self.emoji = item["emoji"]
        self.image = item["image"]
        self.disname = lang[0]
        self.displayname = f"{item['emoji']} {lang[0]}"
        self.description = lang[1]
        self.rarity = item["rarity"]
        self.price = item["price"] if item["price"] != "n" else False
        self.sellprice = item["sellprice"] if item["sellprice"] != "n" else False
        self.tradeable = True if item["tradeable"] != "n" else False
        self.useable = True if item["useable"] != "n" else False
        self.language = language
            
        self.raw = item
        
    def __str__(self) -> str:
        return self.displayname

    def __bool__(self) -> bool:
        return True

    def __eq__(self, other) -> bool:
        try:
            if self.id == other.id:
                return True
        except AttributeError:
            return False
        return False

    @property
    def toolartibutes(self):
        """Do not use it!!! It's a typo!!!"""
        return self.toolatributes

    @property
    def toolatributes(self):
        if self.raw["toolatributes"] == "n":
            return False
        elif self.raw["toolatributes"]['type'] == "bundle":
            return Bundle(self.raw['toolatributes'])
        elif self.raw["toolatributes"]['type'] == "container":
            return Container(self.raw['toolatributes'])
        elif self.raw["toolatributes"]['type'] == "smeltable":
            return Fuel(self.raw['toolatributes'])
        elif self.raw["toolatributes"]['type'] == "useable":
            if self.raw["toolatributes"]['itemtype'] == "note":
                return Note(self.raw['toolatributes'], [self.language['items']['notetitle'][self.id], self.language['items']['notecontent'][self.id]])
            elif self.raw["toolatributes"]['itemtype'] == "map":
                return Map(self.raw['toolatributes'], self.language['items']['map_legend'][self.id])
        elif self.raw["toolatributes"]['type'] == "unlockorb":
            return Orb(self.raw['toolatributes'])
        elif self.raw["toolatributes"]['type'] == "none":
            if self.raw["toolatributes"]['itemtype'] == "awaiting":
                return Awaiting(self.raw['toolatributes'])
        elif self.raw["toolatributes"]['type'] == "weapon":
            if self.raw["toolatributes"]['itemtype'] == "spellbook":
                return Spellbook(self.raw['toolatributes'], [self.language['items']['powersname'][self.id], self.language['items']['powersdescription'][self.id]])
            else:
                return Weapon(self.raw['toolatributes'])

    async def add_item(self, user, amount: int):
        with open("userdb/inventories.json", "r") as f:
            users = json.load(f)

        for item_id in users[str(user.id)]["bag"]:
            if item_id['item'] == self.id:
                item_id['amount'] += amount
                break
        else:
            obj = {"item": self.id, "amount": amount}
            users[str(user.id)]["bag"].append(obj)

        with open("userdb/inventories.json", "w") as f:
            json.dump(users, f)

    async def remove_item(self, user, amount: int):
        with open("userdb/inventories.json", "r") as f:
            users = json.load(f)

        for item_id in users[str(user.id)]["bag"]:
            if item_id['item'] == self.id:
                chk = item_id['amount'] - amount
                if chk < 0:
                    break
                item_id['amount'] -= amount
                break

        with open("userdb/inventories.json", "w") as f:
            json.dump(users, f)

    async def get_amount(self, user, amount):
        """
        returns None if user doesn't have an item
        returns False for invalid input
        """
        await self.add_item(user, 0)
        with open("userdb/inventories.json", "r") as f:
            users = json.load(f)
        try:
            amount = int(amount)
            if amount <= 0:
                return False
            else:
                for ina in users[str(user.id)]["bag"]:
                    if ina["item"] == self.id:
                        old_amt = ina["amount"]
                        new_amt = old_amt - amount
                        if new_amt < 0:
                            return None
                        break
                return amount
        except ValueError:
            if amount == "all":
                for ii in users[str(user.id)]["bag"]:
                    if self.id == ii["item"]:
                        a = ii["amount"]
                        if a == 0:
                            return None
                        return a
            else:
                return False
        except TypeError:
            for ina in users[str(user.id)]["bag"]:
                if ina["item"] == self.id:
                    old_amt = ina["amount"]
                    if old_amt < 1:
                        return None
                    return 1


class ToolAtributes:
    def __init__(self, toolatributes: dict) -> None:
        self.type = toolatributes["type"]
        self.itemtype = toolatributes["itemtype"]
        self.cursed = False if toolatributes["cursed"] == 0 else toolatributes["cursed"]


class Power:
    def __init__(self, power: dict, language):
        self.name = language[0]
        self.description = language[1]
        self.emoji = power['emoji']
        self.type = power['type']
        self.value = power['value']


class BundlePower:
    def __init__(self, power: dict):
        self.type = power['type']
        self.value = power['value']
        self.chance = power['chance'] if 'chance' in power else 10000

        
# Children


class Weapon(ToolAtributes):
    def __init__(self, toolatributes: dict) -> None:
        super().__init__(toolatributes)
        self.attack = toolatributes['attack']


class Bundle(ToolAtributes):
    """item that can be used in bundle!!!!"""

    def __init__(self, toolatributes: dict) -> None:
        super().__init__(toolatributes)
        self.power: BundlePower = BundlePower(toolatributes['power'])
        self.ta = toolatributes

    @property
    def bonus(self):
        bonus_powers = []
        if 'bonus' in self.ta:
            for i in self.ta['bonus']:
                bonus_powers.append(BundlePower(i))
            return bonus_powers
        else:
            return None


class Container(ToolAtributes):
    def __init__(self, toolatributes: dict) -> None:
        super().__init__(toolatributes)
        self.contains: list = toolatributes['contains']


class Fuel(ToolAtributes):
    def __init__(self, toolatributes: dict) -> None:
        super().__init__(toolatributes)
        self.xp_reaward = toolatributes['xp_reaward']
        self.fuel: list = toolatributes['fuel']
        self.lvl_required = toolatributes['lvl_required']
        self.item_smelted = toolatributes['item_smelted']
        self.amount = toolatributes['amount']


class Note(ToolAtributes):
    def __init__(self, toolatributes: dict, language) -> None:
        super().__init__(toolatributes)
        self.title = language[0]
        self.text = language[1]


class Map(ToolAtributes):
    def __init__(self, toolatributes: dict, map_legend) -> None:
        super().__init__(toolatributes)
        self.legend = map_legend
        self.map = toolatributes['map']


class Orb(ToolAtributes):
    def __init__(self, toolatributes: dict) -> None:
        super().__init__(toolatributes)
        self.value = toolatributes['value']


class Awaiting(ToolAtributes):
    def __init__(self, toolatributes: dict) -> None:
        super().__init__(toolatributes)
        self.timestamp = toolatributes['time']


class Spellbook(Weapon):
    def __init__(self, toolatributes, language) -> None:
        super().__init__(toolatributes)
        self.power: Power = Power(toolatributes['power'], language)


class MorexDigsite:
    def __init__(self, place: dict, disname):
        self.name = place['name']
        self.displayname = disname
        self.usages = place['usages']
        self.background = place['background']
        self.color = int(place['color'], 16)
        self.layers = place['layers']
        self.required_item = False if place['req_item'] == "n" else place['req_item']
        self.treasure = DigTreasure(place['treasure'])

    def __str__(self):
        return self.displayname


class MorexHuntlocation:
    def __init__(self, place: dict, disname):
        self.name = place['name']
        self.displayname = disname
        self.enemies = place['enemies']
        self.color = int(place['color'], 16)

    def __str__(self):
        return self.displayname


class MorexPlace:
    def __init__(self, place: dict, disname):
        self.name = place['name']
        self.displayname = disname
        self.color = int(place['color'], 16)
        self.loottable = place['items']

    def __str__(self):
        return self.displayname


class DigTreasure:
    def __init__(self, treasure: dict):
        self.can_replace = treasure['canreplace']
        self.layers = treasure['replacablelayers']
        self.rewards = treasure['contents']


class MorexEnemy:
    def __init__(self, data: dict):
        self.sid = data['name']
        self.id = data['id']
        self.emoji = data['emoji']
        self.disname = data['disname']
        self.displayname = f"{data['emoji']} {data['disname']}"
        self.attack = data['attack']
        self.weapon = data['weapon'] if data['weapon'] != "n" else None
        self.flags = enums.enemies.MorexEnemyFlags(data['flags'])
        self.type = enums.enemies.MorexEnemyTypes(data['type'])
        self.image = data['image']
        self.hp = data['hp']
        self.xp = data['xpreaward'] if 'xpreaward' in data else None
        self.drops = data['drops'] if 'drops' in data else None
        self.meetup = data['meetup']
        self.user_attacks = data['uattacks']
        self.enemy_attacks = data['eattacks']
        self.deaths = data['deaths']
        self.spells = data['spells']
        self.has_default_meetup = data['is_meetup_default']


class MorexQuest:
    def __init__(self, data: dict, langs: list):
        self.name = data['name']
        self.chapter = data['chapter']
        self.chapter_title = langs[0]
        self.disname = langs[1]
        self.description = langs[2]
        self.stage = data['stage']
        self.etaps = data['etaps']
        self.rewards = data['rewards']
        self.unlocks = data['unlocks']


class MorexStructure:
    def __init__(self, data: dict, disname):
        self.id = data['id']
        self.disname = disname
        self.displayname = disname
        self.enemies = data["oponents"]
        self.danger = data["danger_status"]
        self.chest_normal = data['normal']
        self.chest_treasure = data['treasure']

    def __str__(self):
        return f"<MorexStructure Object: id {self.id}, name {self.displayname}>"


class MorexMerchant:
    def __init__(self, data: dict, name, bought, question, in_shop, left, exit_shop):
        self.id = data['id']
        self.displayname = name
        self.icon = data['icon']
        self.times = data['times']
        self.offer = data['items']
        self.bought = bought
        self.question = question
        self.in_shop = in_shop
        self.left = left
        self.exit_shop = exit_shop


class MorexTask:
    def __init__(self, task_id, data: dict, langs: list):
        self.id = task_id
        self.type = data['type']
        self.disname = langs[0]
        self.displayname = self.disname
        self.description = langs[1]
        self.rarity = data['rarity']
        self.quest = data['quest']
        self.rewards = data['rewards']


class MorexMerchantTask:
    def __init__(self, merchant_id, kind, task_id, data: dict, langs: list):
        self.id = task_id
        self.merchant_id = int(merchant_id)
        self.type = kind

        self.disname = langs[0]
        self.displayname = self.disname
        self.description = langs[1]

        self.quest = data['quest']
        self.rewards = data['rewards']

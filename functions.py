import json
import buttons
import main
from morex import CustomUser, MorexItem, MorexDigsite, MorexHuntlocation, MorexEnemy, MorexQuest, MorexPlace, MorexStructure, MorexMerchant, MorexTask, MorexMerchantTask
from morex.objects.recipes import MorexRecipe
from morex.objects import MorexEvent
from morex.enums import utils
import datetime
import nextcord
import random
import custom_errors
import re
from nextcord import Interaction
from functools import cache
import morex.logging as logging


async def badges():
    with open("database/badges.json", "r") as f:
        aassad = json.load(f)

    return aassad


async def otherinfo():
    with open("userdb/otherdatabase.json", "r") as f:
        a = json.load(f)

    return a


async def recipies():
    with open("database/recipes.json", "r") as f:
        aassad = json.load(f)

    return aassad


async def skillz():
    with open("userdb/skills.json", "r") as f:
        sad = json.load(f)

    return sad


async def opponenttable():
    with open("database/opponents.json", "r") as f:
        opo = json.load(f)

    return opo


async def places():
    with open("database/places.json", "r") as f:
        opoa = json.load(f)

    return opoa


async def bossroom():
    with open("database/bossrooms.json", "r") as f:
        opoa = json.load(f)

    return opoa


async def boss():
    with open("database/bosses.json", "r") as f:
        opoa = json.load(f)

    return opoa


async def huntlocations():
    with open("database/huntlocations.json", "r") as f:
        opoa = json.load(f)

    return opoa


async def playerinfo():
    with open("userdb/playerdata.json", "r") as f:
        asd = json.load(f)

    return asd


async def itemsinfo():
    with open("database/itemsinfo.json", "r") as f:
        itemz = json.load(f)

    return itemz


async def get_farms_data():
    with open("userdb/farmlands.json", "r") as f:
        farm_land = json.load(f)

    return farm_land


async def get_inv_data():
    with open("userdb/inventories.json", "r") as f:
        users = json.load(f)

    return users


async def get_daily_tasks():
    with open("userdb/dailytasks.json", "r") as f:
        users = json.load(f)

    return users


async def tasks():
    with open("database/tasks.json", "r") as f:
        dtasks = json.load(f)

    return dtasks


async def get_merchant_tasks():
    with open("userdb/merchanttasks.json", "r") as f:
        users = json.load(f)

    return users


async def merchant_tasks():
    with open("database/merchanttasks.json", "r") as f:
        dtasks = json.load(f)

    return dtasks


async def stats():
    with open("userdb/stats.json", "r") as f:
        status = json.load(f)

    return status


async def structure():
    with open("database/structures.json", "r") as f:
        statusa = json.load(f)

    return statusa


async def merchant():
    with open("database/merchants.json", "r") as f:
        statusab = json.load(f)

    return statusab


async def quests():
    with open("userdb/quests.json", "r") as f:
        quest = json.load(f)

    return quest


async def questlist():
    with open("database/questlist.json", "r") as f:
        quest = json.load(f)

    return quest


async def custommobs():
    with open("userdb/custommobs.json", "r") as f:
        mobs = json.load(f)

    return mobs


async def digging():
    with open("database/digsites.json", "r") as f:
        digger = json.load(f)

    return digger


async def dialogues(dialogue, language):
    with open(f"dialogues/{language}/{dialogue}.json", "r") as f:
        aassad = json.load(f)

    return aassad


async def setting():
    with open("userdb/settings.json", "r") as f:
        settings = json.load(f)

    return settings


async def lang(language: str = "pl"):
    with open(f"lang/{language}.json", "r") as f:
        ll = json.load(f)

    return ll


async def beg_rewards():
    """finally beg rewards, not some stupid digDrops"""
    with open("database/beg.json", "r") as f:
        beg = json.load(f)

    return beg


async def isdebug(user):
    if user is None:
        return None
    if str(user.id) == "826792866776219709" and main.debug_account is True:
        usera = CustomUser(1, "Debug Account 1", "https://cdn.discordapp.com/attachments/1134067893840126012/1134067977839456276/Untitled_03-08-2023_10-39-45_11.png", False)
        return usera
    else:
        if str(user.id) == "1":
            return user
        return user


async def update_skill(user, skill, amount, max_amount):
    u_skills = await skillz()

    u_skills[str(user.id)][skill] += amount

    with open('userdb/skills.json', "w") as f:
        json.dump(u_skills, f)


async def update_stat(user, stat: str, amount: int):
    status = await stats()
    status[str(user.id)][stat] += amount
    with open("userdb/stats.json", "w") as f:
        json.dump(status, f)


async def add_location(user, location, mode):
    oti = await otherinfo()
    if location in oti[str(user.id)][mode]:
        return
    oti[str(user.id)][mode].append(location)
    with open("userdb/otherdatabase.json", "w") as f:
        json.dump(oti, f)
    return


async def has_event(user, event):
    oti = await otherinfo()
    if event in oti[str(user.id)]['events']:
        return True
    return False


async def check_location(user, location, mode):
    oti = await otherinfo()
    if location in oti[str(user.id)][mode]:
        return location
    else:
        if location is None:
            loc = oti[str(user.id)][f"{mode}_defaultlocation"]
            if loc in oti[str(user.id)][mode]:
                return loc
            else:
                return False
        else:
            if mode == "dig":
                a = get_dig_locations(location)
                if a is None:
                    return None
                else:
                    return False
            elif mode == "search":
                a = get_search_locations(location)
                if a is None:
                    return None
                else:
                    return False
            elif mode == "hunt":
                a = get_hunt_locations(location)
                if a is None:
                    return None
                else:
                    return False
    return False


@cache
def get_item(item: str, mode: str = "id", lang_str: str = "pl"):
    with open("database/itemsinfo.json", "r") as f:
        itemz = json.load(f)
    with open(f"lang/{lang_str}.json", "r") as f:
        language = json.load(f)

    for i in itemz:
        if i[mode] == item:
            sustem = i
            break
    else:
        return

    long = language["items"]["name"][sustem['id']]
    long2 = language["items"]["description"][sustem['id']]
    items: MorexItem = MorexItem(sustem, [long, long2], language)

    return items


@cache
def get_strucure(structure_id: int, lang_str: str = "pl"):
    with open("database/structures.json", "r") as f:
        itemz = json.load(f)
    with open(f"lang/{lang_str}.json", "r") as f:
        language = json.load(f)

    for i in itemz:
        if i['id'] == structure_id:
            sustem = i
            break
    else:
        return

    long = language["structures"]["name"][str(structure_id)]
    items: MorexStructure = MorexStructure(sustem, long)

    return items


@cache
def get_merchant(merchant_id: int, lang_str: str = "pl"):
    with open("database/merchants.json", "r") as f:
        itemz = json.load(f)
    with open(f"lang/{lang_str}.json", "r") as f:
        language = json.load(f)

    for i in itemz:
        if i['id'] == merchant_id:
            sustem = i
            break
    else:
        return

    name = language["merchants"]["name"][str(merchant_id)]
    bought = language["merchants"]["bought"][str(merchant_id)]
    question = language["merchants"]["question"][str(merchant_id)]
    in_shop = language["merchants"]["inshop"][str(merchant_id)]
    left = language["merchants"]["left"][str(merchant_id)]
    exit_shop = language["merchants"]["exit"][str(merchant_id)]
    items: MorexMerchant = MorexMerchant(sustem, name, bought, question, in_shop, left, exit_shop)

    return items


@cache
def get_quest(chapter: str, quest: str, lang_str: str = "pl"):
    with open("database/questlist.json", "r") as f:
        itemz = json.load(f)
    with open(f"lang/{lang_str}.json", "r") as f:
        language = json.load(f)

    for i in itemz:
        if i['chapter'] == chapter:
            for ii in i['quests']:
                if ii['name'] == quest:
                    sustem = ii
                    sustem.update({'chapter': chapter})
                    break
            else:
                return
            break
    else:
        return

    long = language['quests']["title"][sustem['chapter']]
    long2 = language['quests']["name"][sustem['name']]
    long3 = language['quests']["description"][sustem['name']]
    items: MorexQuest = MorexQuest(sustem, [long, long2, long3])

    return items


@cache
def get_task(task: str, lang_str: str = "pl"):
    with open("database/tasks.json", "r") as f:
        itemz = json.load(f)
    with open(f"lang/{lang_str}.json", "r") as f:
        language = json.load(f)

    try:
        sustem = itemz[task]
    except KeyError:
        return

    long = language['tasks']["name"][task]
    long2 = language['tasks']["description"][task]
    items: MorexTask = MorexTask(task, sustem, [long, long2])

    return items


@cache
def get_merchant_task(task_id: str, merchant_id, kind, lang_str: str = "pl"):
    with open("database/merchanttasks.json", "r") as f:
        itemz = json.load(f)
    with open(f"lang/{lang_str}.json", "r") as f:
        language = json.load(f)

    try:
        sustem = itemz[merchant_id][kind][task_id]
    except KeyError:
        return

    # long = language['merchant_tasks']["name"][f"{merchant_id}:{kind}:{task_id}"]
    # long2 = language['merchant_tasks']["description"][f"{merchant_id}:{kind}:{task_id}"]
    long = "Placeholder Name"
    long2 = "Placeholder description :3"
    items: MorexMerchantTask = MorexMerchantTask(merchant_id, kind, task_id, sustem, [long, long2])

    return items


@cache
def get_morex_oponent(data, mode: str = "id", lang_str: str = "pl"):
    with open(f"lang/{lang_str}.json", "r") as f:
        language = json.load(f)

    if mode == "list":
        with open("userdb/custommobs.json", "r") as f:
            mobs = json.load(f)
        for i in mobs:
            if mobs[i]['id'] == data[0]:
                for mob in mobs[i]['mobs']:
                    if mob['id'] == data[1]:
                        sustem = mob
                        break
                else:
                    return
                break
        else:
            return

        emojis = re.findall("^<.*>", sustem['displayname'])
        sustem.update({"emoji": emojis[0]})

        sustem.update({"is_meetup_default": False})
        if 'meetup' not in sustem:
            sustem.update({"meetup": language["mobs"]["meetup"]["default"]})
            sustem.update({"is_meetup_default": True})

        # TODO: add this to custom mob creation
        sustem['weapon'] = 'n'
        sustem['flags'] = 0
        sustem['type'] = 8

        sustem['uattacks'] = {}
        sustem['eattacks'] = {}
        sustem['deaths'] = {}
        sustem['spells'] = {}
        for i in language["mobs"]['uattacks']:
            sustem['uattacks'].update({i: language["mobs"]['uattacks'][i]['default']})

        for i in language["mobs"]['eattacks']:
            sustem['eattacks'].update({i: language["mobs"]['eattacks'][i]['default']})

        for i in language["mobs"]['deaths']:
            sustem['deaths'].update({i: language["mobs"]['deaths'][i]['default']})

        for i in language["mobs"]['spells']:
            sustem['spells'].update({i: language["mobs"]['spells'][i]['default']})
    else:
        with open("database/opponents.json", "r") as f:
            mobs = json.load(f)
        for i in mobs:
            if i[mode] == data:
                sustem: dict = i
                break
        else:
            return
        sustem.update({"disname": language["mobs"]["name"][sustem['id']]})
        try:
            sustem.update({"meetup": language["mobs"]["meetup"][sustem['id']]})
            sustem.update({"is_meetup_default": False})
        except KeyError:
            sustem.update({"meetup": language["mobs"]["meetup"]["default"]})
            sustem.update({"is_meetup_default": True})

        sustem['uattacks'] = {}
        sustem['eattacks'] = {}
        sustem['deaths'] = {}
        sustem['spells'] = {}
        for i in language["mobs"]['uattacks']:
            try:
                sustem['uattacks'].update({i: language["mobs"]['uattacks'][i][sustem['id']]})
            except KeyError:
                sustem['uattacks'].update({i: language["mobs"]['uattacks'][i]['default']})
        for i in language["mobs"]['eattacks']:
            try:
                sustem['eattacks'].update({i: language["mobs"]['eattacks'][i][sustem['id']]})
            except KeyError:
                sustem['eattacks'].update({i: language["mobs"]['eattacks'][i]['default']})
        for i in language["mobs"]['deaths']:
            try:
                sustem['deaths'].update({i: language["mobs"]['deaths'][i][sustem['id']]})
            except KeyError:
                sustem['deaths'].update({i: language["mobs"]['deaths'][i]['default']})
        for i in language["mobs"]['spells']:
            try:
                sustem['spells'].update({i: language["mobs"]['spells'][i][sustem['id']]})
            except KeyError:
                sustem['spells'].update({i: language["mobs"]['spells'][i]['default']})

    oponent: MorexEnemy = MorexEnemy(sustem)
    logging.info(utils.format_enum(oponent.flags))
    logging.info(utils.format_enum(oponent.type))

    return oponent


@cache
def get_dig_locations(item: str, lang_str: str = "pl"):
    with open("database/digsites.json", "r") as f:
        sites = json.load(f)
    with open(f"lang/{lang_str}.json", "r") as f:
        language = json.load(f)

    for i in sites:
        if i['name'] == item:
            sustem = i
            break
    else:
        return

    location: MorexDigsite = MorexDigsite(sustem, language['dig']['name'][sustem['name']])

    return location


@cache
def get_search_locations(item: str, lang_str: str = "pl"):
    with open("database/places.json", "r") as f:
        sites = json.load(f)
    with open(f"lang/{lang_str}.json", "r") as f:
        language = json.load(f)

    for i in sites:
        if i['name'] == item:
            sustem = i
            break
    else:
        return

    location: MorexPlace = MorexPlace(sustem, language['search']['name'][sustem['name']])

    return location


@cache
def get_hunt_locations(item: str, lang_str: str = "pl"):
    with open("database/huntlocations.json", "r") as f:
        sites = json.load(f)
    with open(f"lang/{lang_str}.json", "r") as f:
        language = json.load(f)

    for i in sites:
        if i['name'] == item:
            sustem = i
            break
    else:
        return

    location: MorexHuntlocation = MorexHuntlocation(sustem, language['hunt']['name'][sustem['name']])

    return location


@cache
def get_recipe(item_name, mode, langu):
    item = get_item(item_name, mode, langu)
    with open("database/recipes.json", "r") as f:
        itemz = json.load(f)

    for i in itemz:
        if i["item"] == item.sid:
            sustem = i
            break
    else:
        return

    ingredients = []
    for ingredient in sustem['recipe']:
        ingredients.append({"item": get_item(ingredient['name'], 'name', langu), "amount": ingredient['amount']})

    recipe: MorexRecipe = MorexRecipe(sustem['id'], item, True if sustem['available'] == "y" else False, sustem['amount'], ingredients)

    return recipe


async def create_account(user, checker=None, request_language=None):
    """
    **user** - normal user\n
    **checker** - you can put there anything as long it isn't None to enable check mode

    Returns:
    I have no idea
    """
    user = await isdebug(user)

    user_stats = await stats()
    if str(user.id) not in user_stats:
        if checker is not None:
            return False

        user_stats[str(user.id)] = {}
        user_stats[str(user.id)]["beg"] = 0
        user_stats[str(user.id)]["hunt"] = 0
        user_stats[str(user.id)]["search"] = 0
        user_stats[str(user.id)]["fight"] = 0
        with open("userdb/stats.json", "w") as f:
            json.dump(user_stats, f)

    playerdata = await playerinfo()
    if str(user.id) not in playerdata:
        day = datetime.datetime.now().timestamp()
        timestamp = round(day, None)

        playerdata[str(user.id)] = {}
        playerdata[str(user.id)]["wallet"] = 0
        playerdata[str(user.id)]["bank"] = 0
        playerdata[str(user.id)]["weapon_equiped"] = ["none", "none", "none"]
        playerdata[str(user.id)]["hp"] = 100
        playerdata[str(user.id)]["level"] = 0
        playerdata[str(user.id)]["xp"] = 0
        playerdata[str(user.id)]["total_xp"] = 0
        playerdata[str(user.id)]["beta"] = "none"
        playerdata[str(user.id)]["premium"] = "none"
        playerdata[str(user.id)]["badges"] = []
        playerdata[str(user.id)]["banned"] = "none"
        playerdata[str(user.id)]["version"] = main.version_number
        playerdata[str(user.id)]["timestamp"] = timestamp

        with open("userdb/playerdata.json", "w") as f:
            json.dump(playerdata, f)

    inventory = await get_inv_data()
    if str(user.id) in inventory:
        if "bundle" not in inventory[str(user.id)]:
            inventory[str(user.id)]["bundle"] = [{"item": "none", "amount": 0}, {"item": "none", "amount": 0}, {"item": "none", "amount": 0}, {"item": "none", "amount": 0}]
            with open("userdb/inventories.json", "w") as f:
                json.dump(inventory, f)
    else:
        inventory[str(user.id)] = {}
        inventory[str(user.id)]["bag"] = []
        inventory[str(user.id)]["bundle"] = [{"item": "none", "amount": 0}, {"item": "none", "amount": 0}, {"item": "none", "amount": 0}, {"item": "none", "amount": 0}]
        with open("userdb/inventories.json", "w") as f:
            json.dump(inventory, f)

    otherdata = await otherinfo()
    if str(user.id) not in otherdata:
        otherdata[str(user.id)] = {}
        otherdata[str(user.id)]["skillpoint"] = 0
        otherdata[str(user.id)]["search_defaultlocation"] = "forest"
        otherdata[str(user.id)]["dig_defaultlocation"] = "pit"
        otherdata[str(user.id)]["hunt_defaultlocation"] = "slime_valley"
        otherdata[str(user.id)]["search"] = ["forest"]
        otherdata[str(user.id)]["dig"] = ["pit"]
        otherdata[str(user.id)]["hunt"] = ["slime_valley"]
        otherdata[str(user.id)]["events"] = []
        otherdata[str(user.id)]["shop"] = ["main"]
        with open("userdb/otherdatabase.json", "w") as f:
            json.dump(otherdata, f)

    farmlands = await get_farms_data()
    if str(user.id) not in farmlands:
        farmlands[str(user.id)] = {}
        farmlands[str(user.id)]["farms"] = {"0": [{"crop": "none", "finish_timestamp": 0, "death_timestamp": 0, "blocktype": "0028", "state": "normal", "watered": False, "fertilized": False}, {"crop": "none", "finish_timestamp": 0, "death_timestamp": 0, "blocktype": "0028", "state": "normal", "watered": False, "fertilized": False}, {"crop": "none", "finish_timestamp": 0, "death_timestamp": 0, "blocktype": "0028", "state": "normal", "watered": False, "fertilized": False}, {"crop": "none", "finish_timestamp": 0, "death_timestamp": 0, "blocktype": "0028", "state": "normal", "watered": False, "fertilized": False}, {"crop": "none", "finish_timestamp": 0, "death_timestamp": 0, "blocktype": "0028", "state": "normal", "watered": False, "fertilized": False}, {"crop": "none", "finish_timestamp": 0, "death_timestamp": 0, "blocktype": "0028", "state": "normal", "watered": False, "fertilized": False}, {"crop": "none", "finish_timestamp": 0, "death_timestamp": 0, "blocktype": "0028", "state": "normal", "watered": False, "fertilized": False}, {"crop": "none", "finish_timestamp": 0, "death_timestamp": 0, "blocktype": "0028", "state": "normal", "watered": False, "fertilized": False}, {"crop": "none", "finish_timestamp": 0, "death_timestamp": 0, "blocktype": "0028", "state": "normal", "watered": False, "fertilized": False}]}
        farmlands[str(user.id)]["skins"] = {"0": "normal_farm"}
        farmlands[str(user.id)]["farms_unlocked"] = 1
        with open("userdb/farmlands.json", "w") as f:
            json.dump(farmlands, f)

    skills = await skillz()
    if str(user.id) not in skills:
        skills[str(user.id)] = {}
        skills[str(user.id)]['hp'] = 0
        skills[str(user.id)]['rob'] = 0
        skills[str(user.id)]['magic'] = 0
        skills[str(user.id)]['attack'] = 0
        # skills[str(user.id)]['java'] = 0
        # skills[str(user.id)]['python'] = 0
        with open("userdb/skills.json", "w") as f:
            json.dump(skills, f)

    questdata = await quests()
    if str(user.id) not in questdata:
        questdata[str(user.id)] = {}
        questdata[str(user.id)]["completedquests"] = []
        questdata[str(user.id)]["mainquestline"] = []
        questdata[str(user.id)]["otherquests"] = []
        with open("userdb/quests.json", "w") as f:
            json.dump(questdata, f)

    await create_quest(user, ["chapter1", "tutorial"])

    custommob = await custommobs()
    if str(user.id) not in custommob:
        custommob[str(user.id)] = {}
        customs = await custommobs()
        a = list(customs)[-1]
        ina = int(customs[a]["id"]) + 1
        ina = str(ina)
        sus = ""
        for i in range(4 - len(ina)):
            sus += "0"
        sus += ina
        custommob[str(user.id)]["id"] = sus
        custommob[str(user.id)]["rank"] = "d"
        custommob[str(user.id)]["points"] = 0
        custommob[str(user.id)]["kills"] = 0
        custommob[str(user.id)]["mobs"] = []
        with open("userdb/custommobs.json", "w") as f:
            json.dump(custommob, f)

    settings = await setting()
    if str(user.id) in settings:
        settings = await check_settings(settings, user.id)
        with open("userdb/settings.json", "w") as f:
            json.dump(settings, f)
    else:
        settings[str(user.id)] = {}
        settings = await check_settings(settings, user.id)
        with open("userdb/settings.json", "w") as f:
            json.dump(settings, f)

        if request_language is not None:
            embed = nextcord.Embed(title="Language/Język", description="Wybierz domyślny język w jakim będzie wyświetlany.\n\nChoose the default language in which bot will be displayed.\n# **Warning/Ostrzeżenie**\n**Jeżeli nic nie zrobisz bot będzie po polsku.\n\nIf you do nothing bot will be in polish.**", color=main.color_normal)
            embed.set_footer(text=main.version['en'])

            view = buttons.LanguageStartButtons(user)

            try:
                await user.send(embed=embed, view=view)
            except nextcord.Forbidden:
                print("Uhh...")

    daily_tasks = await get_daily_tasks()
    if str(user.id) not in daily_tasks:
        daily_tasks[str(user.id)] = {}
        daily_tasks[str(user.id)]["day"] = -1
        daily_tasks[str(user.id)]['pity'] = 0
        daily_tasks[str(user.id)]['quests'] = {}
        with open("userdb/dailytasks.json", "w") as f:
            json.dump(daily_tasks, f)

    await make_daily_tasks(user)

    merchant_task = await get_merchant_tasks()
    if str(user.id) not in merchant_task:
        merchant_task[str(user.id)] = {}
        with open("userdb/merchanttasks.json", "w") as f:
            json.dump(merchant_task, f)


async def has_enabled(user, setting_name):
    settings = await setting()
    a = settings[str(user.id)][setting_name]
    if a == "disabled":
        return False
    else:
        return True


async def get_lang(user) -> str:
    sethig = await setting()
    return sethig[str(user.id)]["language"]


async def check_settings(json_f, user_id):
    if "multiplayer" not in json_f[str(user_id)]:
        json_f[str(user_id)]["multiplayer"] = "enabled"
    if "debug_info" not in json_f[str(user_id)]:
        json_f[str(user_id)]["debug_info"] = "disabled"
    if "dm_notifications" not in json_f[str(user_id)]:
        json_f[str(user_id)]["dm_notifications"] = "enabled"
    if "language" not in json_f[str(user_id)]:
        json_f[str(user_id)]["language"] = "pl"
    return json_f


async def text_replacer(text: str, *lists):
    for i in lists:
        text = text.replace(i[0], str(i[1]))

    return text


async def make_daily_tasks(user):
    daily_tasks = await get_daily_tasks()

    origin = 1735772400
    one_day = 86400
    looks_like_we_gotta_do_quests_now = False

    day = datetime.datetime.now().timestamp()
    timestamp = round(day, None)
    
    event_obj = main.event['current_event']

    # okay what is this thing supposed to do?
    # it removes the event tasks after event ends okay
    dummy = []
    for id_task, potential_task in daily_tasks[str(user.id)]['quests'].items(): 
        if potential_task['type'] == 'classic':
            continue
        if event_obj:
            if event_obj.sid == potential_task['event']:
                continue
        dummy.append(id_task)
    for id_task in dummy:
        daily_tasks[str(user.id)]['quests'].pop(id_task)

    if daily_tasks[str(user.id)]["day"] < origin:
        daily_tasks[str(user.id)]["day"] = timestamp
        looks_like_we_gotta_do_quests_now = True

    if datetime.date.today() != datetime.date.fromtimestamp(daily_tasks[str(user.id)]["day"]):
        daily_tasks[str(user.id)]["day"] = timestamp
        looks_like_we_gotta_do_quests_now = True

    if looks_like_we_gotta_do_quests_now:
        cur_lan = await get_lang(user)
        with open("database/tasksrarity.json", "r") as f:
            rarities_table = json.load(f)

        daily_tasks[str(user.id)]["quests"] = {}
        # 6000 - common | 3000 - rare | 990 - epic | 10
        for useless in range(2):
            if daily_tasks[str(user.id)]["pity"] >= 15:
                current_rarity = 9999
                daily_tasks[str(user.id)]["pity"] = 0
            else:
                current_rarity = random.randint(1, 10000)

            for rar in rarities_table["table"]:
                if rarities_table["table"][rar][0] <= current_rarity <= rarities_table["table"][rar][1]:
                    rarity = rar
                    logging.info(f'{user.name} ({user.id}) got {rar} task.')
                    break
            else:
                continue

            task_id = random.choice(rarities_table['tasks'][rarity])
            rarities_table['tasks'][rarity].remove(task_id)

            task_to_add = get_task(task_id, cur_lan)
            daily_tasks[str(user.id)]["quests"][task_id] = {}
            daily_tasks[str(user.id)]["quests"][task_id]["progress"] = {quest: 0 for quest in task_to_add.quest}  # something complitacted e.g. somehting that actually requires some logic
            daily_tasks[str(user.id)]["quests"][task_id]["type"] = task_to_add.type
            daily_tasks[str(user.id)]["quests"][task_id]["completed"] = False
        if event_obj:
            if event_obj.has_quests:
                if event_obj.sid not in rarities_table['tasks']['event']:
                    logging.critical(f"Attempted to add {event_obj.sid} event quest, but none were found.")
                else:
                    task_id = random.choice(rarities_table['tasks']['event'][event_obj.sid])
                    rarities_table['tasks']['event'][event_obj.sid].remove(task_id)

                    task_to_add = get_task(task_id, cur_lan)
                    daily_tasks[str(user.id)]["quests"][task_id] = {}
                    daily_tasks[str(user.id)]["quests"][task_id]["progress"] = {quest: 0 for quest in task_to_add.quest}  # something complitacted e.g. somehting that actually requires some logic
                    daily_tasks[str(user.id)]["quests"][task_id]["type"] = task_to_add.type
                    daily_tasks[str(user.id)]["quests"][task_id]["event"] = event_obj.sid
                    daily_tasks[str(user.id)]["quests"][task_id]["completed"] = False

    with open("userdb/dailytasks.json", "w") as f:
        json.dump(daily_tasks, f)


async def update_daily_task(user, t_type, t_objective, amount):
    cur_lan = await get_lang(user)
    daily_tasks = await get_daily_tasks()
    changes = False
    was_completed = False
    completed_before = False
    for task in daily_tasks[str(user.id)]['quests']:
        if daily_tasks[str(user.id)]['quests'][task]['completed']:
            completed_before = True
            continue
        if f"{t_type}:{t_objective}" not in daily_tasks[str(user.id)]['quests'][task]["progress"]:
            continue
        changes = True
        daily_tasks[str(user.id)]['quests'][task]["progress"][f"{t_type}:{t_objective}"] += amount
        the_task = get_task(task, cur_lan)
        ctr = 0
        for i in daily_tasks[str(user.id)]['quests'][task]["progress"]:
            if daily_tasks[str(user.id)]['quests'][task]["progress"][i] > the_task.quest[i]:
                daily_tasks[str(user.id)]['quests'][task]["progress"][i] = the_task.quest[i]
            if daily_tasks[str(user.id)]['quests'][task]["progress"][i] == the_task.quest[i]:
                ctr += 1

        if ctr != len(the_task.quest):
            continue

        daily_tasks[str(user.id)]['quests'][task]["completed"] = True
        was_completed = True

        given_rewards = await rewards(user, the_task.rewards)
    if was_completed and not completed_before:
        daily_tasks[str(user.id)]["pity"] += 1
    if changes:
        with open("userdb/dailytasks.json", "w") as f:
            json.dump(daily_tasks, f)


async def rewards(user, reward_pool):
    """
    rewards aka normalized reward redeeming system to avoid repetition

    was it really that hard to do???
    """
    text = []
    cur_lan = await get_lang(user)

    try:
        u = reward_pool[0]['name']
        key = "name"
    except KeyError:
        try:
            u = reward_pool[0]['item']
            key = "item"
        except KeyError:
            raise ValueError

    for reward in reward_pool:
        if reward[key] == "coins":
            await update_bank(user, reward["amount"], "wallet")
            text.append(f"{reward["amount"]} {main.coin}")
        elif reward[key] == "event":
            await add_event(user, reward['amount'])
        elif reward[key] == "dig":
            await add_location(user, reward['amount'], 'dig')
            location = get_dig_locations(reward['amount'], cur_lan)
            text.append(location.displayname)
        else:
            item = get_item(reward[key], 'name', cur_lan)
            await item.add_item(user, reward['amount'])
            text.append(f"{reward['amount']} {item}")

    return "\n".join(text)


async def list_rewards(reward_pool, cur_lan):
    text = []

    try:
        u = reward_pool[0]['name']
        key = "name"
    except KeyError:
        try:
            u = reward_pool[0]['item']
            key = "item"
        except KeyError:
            raise ValueError

    for reward in reward_pool:
        if reward[key] == "coins":
            text.append(f"{reward["amount"]} {main.coin}")
        elif reward[key] == "event":
            continue
        else:
            item = get_item(reward[key], 'name', cur_lan)
            text.append(f"{reward['amount']} {item}")

    return "\n".join(text)


async def create_quest(user, quest, value=None, cur_lan='en'):
    """No Documentation?\n
⢿⣿⡻⣝⢯⡻⣝⢯⡻⣝⡯⣟⢯⡻⣝⢯⢟⡯⣟⡯⣟⡯⣟⢯⢟⡯⣟⣟⡽⣻⣻⢽⣻⢝⡯⣻⢝⡽⣝⢽
⡿⡾⣝⢮⡳⣝⢮⡳⣝⣞⢮⢯⣳⡫⣗⢯⡳⣝⣞⢮⢗⡽⣺⢽⢝⣞⡵⣳⣝⢷⢽⢕⡯⣗⢽⣪⡳⣝⢮⡳
⣿⣻⡪⣗⢝⢮⡳⣝⣞⢮⡫⣗⢗⡽⣪⢗⡽⣺⡪⡯⣳⢝⡮⡯⣳⡳⣝⣗⣗⢽⣝⣗⢽⣪⢳⢵⢝⡮⣳⢝
⣿⡳⣝⢎⢧⡳⣝⣞⢮⡳⣝⢮⡳⣝⢮⡳⣝⢞⢮⡫⣞⢵⡫⣞⢵⡫⣞⣞⢮⣳⡳⣕⢯⢮⡳⣝⢵⢝⡮⡳
⡿⣝⢜⢮⡳⣝⣞⢮⣳⢝⡮⡳⣝⢮⡳⣝⢮⣫⡳⣝⢮⡳⣝⢮⡳⣝⢞⡮⣳⡳⣝⢮⡳⡳⣝⢮⡳⣝⢮⡫
⡫⣞⢽⢕⡯⣺⣪⣗⣗⡯⣞⣝⢮⡳⣝⢮⡳⡵⣝⢮⡳⣝⢮⡣⡫⡎⣗⢝⢮⡺⣕⢗⢽⡱⣣⡳⣝⢮⡳⣹
⣮⢷⣝⣷⢽⡷⣷⣟⣗⢯⢞⢾⡵⣝⢮⡳⣝⢞⡮⣳⢝⢮⡳⣝⢮⡣⣳⢹⢕⡝⣎⢗⢵⡹⣜⢞⢮⡳⣝⣞
⣿⣻⡿⣾⢿⣻⣻⡺⣪⢯⡫⣗⣟⢯⣷⣽⣪⣗⡽⣪⢯⣳⣝⢮⡳⣝⢮⡳⣕⢝⡜⣎⢧⡫⡮⣫⡳⣝⣞⣞
⣿⣻⣽⡺⣝⣞⢮⢞⡵⣫⢞⡵⣳⢽⢵⡻⣷⣟⣿⣟⣿⡷⣟⣯⣟⣮⢗⣝⢮⢪⢎⢮⢺⡪⡯⣺⢪⣾⣺⣳
⢷⣟⣷⣯⣞⢮⢯⣳⢽⣕⢯⡺⡵⣫⢗⡽⣺⣪⢯⣻⣫⢿⢿⣟⣯⣿⡽⡮⣳⢱⢕⡕⣗⡽⣝⣮⢿⣺⡿⣽
⢿⣯⣷⡿⣾⣯⣷⢯⣷⣯⣗⢯⡫⣗⡯⡯⣞⡮⣗⣗⣗⡽⣝⣞⢯⢷⢿⡯⣺⢸⢸⣪⢗⣽⣾⣽⡿⣯⣟⣷
⣻⣷⣟⣿⣯⣿⢣⣓⣿⣽⢿⣳⢝⡷⡽⣝⣗⣯⣷⣷⣳⡯⣗⣗⢯⢯⢯⣻⡪⡎⣗⣵⢿⡻⣻⣯⢿⣳⣟⣾
⣿⣾⣟⣿⣾⢿⣲⢸⡿⣿⣻⣗⢽⣺⢽⣳⢯⢳⡽⣟⣿⣿⣿⣺⢽⣝⣗⢗⡕⣽⣺⣺⢗⣿⣟⣿⣻⣽⣾⣳
⢿⣾⣿⣿⣿⢕⡯⣷⣻⡯⣟⢮⢯⢞⡽⣯⡣⣳⣿⣯⣷⣿⡝⣿⡳⡳⡝⡕⡵⣗⡷⣫⣿⣿⣿⣯⡿⣷⣻⣾
⣿⣿⣿⣟⣿⢧⡻⣺⡪⣏⢮⡳⡯⡯⡯⣟⣮⣎⢯⣯⣿⣺⢵⢯⢪⢣⢣⢳⣽⢷⣿⣿⣿⣿⣿⣿⣿⣿⣽⣾
⣞⣷⣯⢿⡽⡷⣝⢞⡜⡮⣳⢯⢯⢯⢯⣻⣺⢞⣯⣗⡯⡾⣝⢎⢇⢇⢧⣿⣟⣿⣟⣿⣟⣿⣿⣽⣿⣟⣿⣾
⣿⣷⢿⣻⣿⢿⡪⣳⢹⡪⣗⢯⢯⢯⣳⣳⡳⣫⣞⢮⢯⡺⡮⣳⢝⢮⣿⡽⣯⡿⣯⣿⣻⣯⣿⣯⣿⣿⣿⣿
⣯⣿⡿⣽⢾⡳⡹⣜⢵⢹⢪⢳⡹⣕⢗⣗⡽⣳⣳⣫⢟⣞⢽⡪⣏⡯⡾⣯⢷⣟⡿⣽⣟⣷⣹⣿⢿⣾⣿⣾
⣻⣽⣿⣽⡻⡸⡕⡵⡱⡱⡱⡱⡕⡧⣳⡳⡯⣗⣗⣗⣟⢮⡳⣝⣾⣯⣟⡾⡽⡾⣽⣻⣯⢷⣻⡿⣿⣿⣽⣿
⣟⣿⣽⢞⢎⢎⢎⢎⢎⢎⢎⢮⡺⡼⡮⡯⡯⣗⣗⣗⢵⡳⡹⣾⣿⣿⣾⣿⣟⣿⣽⣾⡽⣯⡷⣟⣿⢷⣿⡿
⣿⣻⣽⡯⣮⡣⣣⢣⣣⡳⣝⢵⢹⢪⢫⡺⣝⣗⣗⢵⡣⣳⣽⣿⣿⣿⣻⣿⣿⣻⣾⣷⣿⣿⣽⣟⣾⣻⣽⣿
⡾⣿⣿⣽⣾⡾⣕⣟⣞⣞⣮⡺⣜⢮⣎⢞⢼⡺⡮⡳⣝⣾⣿⢿⣯⣿⣿⣿⢿⣿⣿⣿⣿⣾⣿⣽⣯⣿⢷⡿
    """
    true_quest = get_quest(quest[0], quest[1], cur_lan)

    leng = await lang(cur_lan)
    text = leng['commands']['quests']

    q = await quests()
    for asifj in q[str(user.id)]["mainquestline"]:
        if asifj["chapter"] == quest[0] and quest[1] == asifj["name"]:
            return
    for aasifj in q[str(user.id)]["completedquests"]:
        if aasifj[0] == quest[0] and quest[1] == aasifj[1]:
            return True
    if value != "checker":
        q[str(user.id)]["mainquestline"].append({"chapter": quest[0], "name": quest[1], "current": 0})
        with open("userdb/quests.json", "w") as f:
            json.dump(q, f)
        try:
            if quest[0] == "chapter1" and quest[1] == "tutorial":
                return
            embed = nextcord.Embed(title=true_quest.chapter_title, description=f"**{text['unlocked']} {true_quest.disname} {true_quest.stage}**\n\n{true_quest.description}", color=main.color_normal)
            embed.set_footer(text=main.version[cur_lan])
            reas = await has_enabled(user, "dm_notifications")
            if reas is True:
                await user.send(embed=embed)
        except Exception as e:
            print(e)
    return


async def sheild(number):
    if number == 0:
        return ""
    bars = ['<:MX_Shield6:1221159173602021546>', '<:MX_Shield5:1221159198654726276>', '<:MX_Shield4:1221159216681586840>', '<:MX_Shield3:1221159233874038934>', '<:MX_Shield2:1221159255646797956>', '<:MX_Shield1:1221159280925872299>']
    new_bar = ""
    our = number // 30
    oura = number % 30
    lin = our
    if oura != 0:
        lin += 1
    cnt = 0
    for i in range(our):
        if cnt == 10:
            if lin > 10:
                new_bar = new_bar[:-1]
                new_bar += "..."
                return new_bar
        if (i + 1) % 5 == 0:
            new_bar += f"{bars[0]}\n"
        else:
            new_bar += f"{bars[0]} "
        cnt += 1

    if oura > 0:
        if 1 <= oura <= 6:
            new_bar += f"{bars[5]} "
        elif 7 <= oura <= 12:
            new_bar += f"{bars[4]} "
        elif 13 <= oura <= 18:
            new_bar += f"{bars[3]} "
        elif 19 <= oura <= 24:
            new_bar += f"{bars[2]} "
        elif 25 <= oura <= 29:
            new_bar += f"{bars[1]} "

    return new_bar


async def progress_bar(minimal, maximum):
    bars = ["<:MX_BarLeftEmpty:1220681832346030182>", "<:MX_BarLeftHalf:1220681859814395936>", "<:MX_BarLeftFull:1220681891708014592>", "<:MX_BarMiddleEmpty:1220681956136718437>", "<:MX_BarMiddleHalf:1220681991889096776>", "<:MX_BarMiddleFull:1220682021819519071>", "<:MX_BarRightEmpty:1220682078778294312>", "<:MX_BarRightHalf:1220682123308957806>", "<:MX_BarRightFull:1220682153579380817>"]
    try:
        precent = (minimal / maximum) * 100
    except ZeroDivisionError:
        precent = random.randint(0, 100)
    precent = int(precent)
    new_bar = ""

    if precent == 0:
        new_bar += bars[0]
        for i in range(6):
            new_bar += bars[3]
        new_bar += bars[6]
        return new_bar
    elif 1 <= precent <= 10:
        new_bar += bars[1]
        for i in range(6):
            new_bar += bars[3]
        new_bar += bars[6]
        return new_bar
    elif 11 <= precent <= 23:
        new_bar += bars[2]
        new_bar += bars[4]
        for i in range(5):
            new_bar += bars[3]
        new_bar += bars[6]
        return new_bar
    elif 24 <= precent <= 36:
        new_bar += bars[2]
        new_bar += bars[5]
        new_bar += bars[4]
        for i in range(4):
            new_bar += bars[3]
        new_bar += bars[6]
        return new_bar
    elif 37 <= precent <= 49:
        new_bar += bars[2]
        for i in range(2):
            new_bar += bars[5]
        new_bar += bars[4]
        for i in range(3):
            new_bar += bars[3]
        new_bar += bars[6]
        return new_bar
    elif 50 <= precent <= 62:
        new_bar += bars[2]
        for i in range(3):
            new_bar += bars[5]
        new_bar += bars[4]
        for i in range(2):
            new_bar += bars[3]
        new_bar += bars[6]
        return new_bar
    elif 63 <= precent <= 75:
        new_bar += bars[2]
        for i in range(4):
            new_bar += bars[5]
        new_bar += bars[4]
        for i in range(1):
            new_bar += bars[3]
        new_bar += bars[6]
        return new_bar
    elif 76 <= precent <= 88:
        new_bar += bars[2]
        for i in range(5):
            new_bar += bars[5]
        new_bar += bars[4]
        new_bar += bars[6]
        return new_bar
    elif 89 <= precent <= 99:
        new_bar += bars[2]
        for i in range(6):
            new_bar += bars[5]
        new_bar += bars[7]
        return new_bar
    else:
        new_bar += bars[2]
        for i in range(6):
            new_bar += bars[5]
        new_bar += bars[8]
        return new_bar


async def add_event(user, event):
    otherdb = await otherinfo()
    if event in otherdb[str(user.id)]["events"]:
        return
    otherdb[str(user.id)]["events"].append(event)
    with open("userdb/otherdatabase.json", "w") as f:
        json.dump(otherdb, f)


async def update_quest(user, quest, amount, cur_lan):
    a = await create_quest(user, quest, "checker", cur_lan)

    leng = await lang(cur_lan)
    text = leng['commands']['quests']

    if a is True:
        return
    true_quest = get_quest(quest[0], quest[1], cur_lan)
    q = await quests()
    for asifj in q[str(user.id)]["mainquestline"]:
        if asifj["chapter"] == quest[0] and quest[1] == asifj["name"]:
            bob = asifj["current"] + amount
            if bob >= true_quest.etaps:
                # Do something
                q[str(user.id)]["mainquestline"].remove(asifj)
                q[str(user.id)]["completedquests"].append([quest[0], quest[1]])
                txt = ""
                for iiii in true_quest.rewards:
                    if iiii["name"] == "coins":
                        await update_bank(user, iiii["amount"], "wallet")
                        txt += f"{iiii['amount']} {main.coin}\n"
                    elif iiii["name"] == "event":
                        await add_event(user, iiii['amount'])
                    elif iiii['name'] == 'dig':
                        await add_location(user, iiii['amount'], 'dig')
                    elif iiii['name'] == 'hunt':
                        await add_location(user, iiii['amount'], 'hunt')
                    else:
                        item = get_item(iiii['name'], 'name', cur_lan)
                        await item.add_item(user, iiii['amount'])
                        txt += f"{iiii['amount']} {item}"

                with open("userdb/quests.json", "w") as f:
                    json.dump(q, f)
                try:
                    embed = nextcord.Embed(title=f"{text['finished']} {true_quest.disname} {true_quest.stage}", description=f"{text['got']}:\n{txt}", color=main.color_normal)
                    embed.set_footer(text=main.version[cur_lan])
                    reas = await has_enabled(user, "dm_notifications")
                    if reas is True:
                        await user.send(embed=embed)
                except Exception as e:
                    print(e)
                for gow in true_quest.unlocks:
                    if gow["quest"] == "none":
                        continue
                    await create_quest(user, [gow["chapter"], gow["quest"]], cur_lan=cur_lan)
                return
            asifj["current"] += amount
            with open("userdb/quests.json", "w") as f:
                json.dump(q, f)
            return


async def player_icon(user):
    user = await isdebug(user)
    a = await playerinfo()
    if str(user.id) == "826792866776219709":
        return "<:MX_OwnerIcon:1212133169818632304>"
    elif a[str(user.id)]["premium"] == "true" and a[str(user.id)]["beta"] == "true":
        return "<:MX_BetaPremiumIcon:1212133181172752464>"
    elif a[str(user.id)]["premium"] == "true":
        return "<:MX_PremiumIcon:1212133177947197580>"
    elif a[str(user.id)]["beta"] == "true":
        return "<:MX_BetaIcon:1212133175250395247>"
    else:
        return "<:MX_DefaultIcon:1212133172188291082>"


async def get_weapon(user):
    i = await playerinfo()
    g = await get_inv_data()
    counter = 0

    for auia in i[str(user.id)]["weapon_equiped"]:
        if auia != "none":
            oi = get_item(auia, 'name')
            if bool(await oi.get_amount(user, 1)) is True:
                return auia
        if counter != 2:
            counter += 1
            continue
        return False


async def get_from_value(listed: list[dict]):
    """
    This will choose one thing from list shaped like:
    [
      {"enemy": "greenslime", "min_value": 1,"max_value": 5000},
      {"enemy": "blueslime", "min_value": 5001,"max_value": 7500},
      {"enemy": "pinkslime", "min_value": 7501,"max_value": 9000},
      {"enemy": "goldslime", "min_value": 9001,"max_value": 9990},
      {"enemy": "morexslime", "min_value": 9991,"max_value": 10000}
    ]
    returns dict that matches
    """
    choice = random.randint(1, 10000)
    for i in listed:
        if i["min_value"] <= choice <= i["max_value"]:
            return i.copy()

    raise custom_errors.WhatHaveIDone


async def text_formatting_battle(text: str, user: nextcord.Member, enemy_name: str, cur_lan):
    items = list(set(re.findall('{i:....}', text)))
    item_emojis = list(set(re.findall('{ie:....}', text)))
    progress_bars = list(set(re.findall('{pb:[0-9]+:[1-9][0-9]*}', text)))
    text = text.replace("{e}", f"{enemy_name}")
    text = text.replace("{u}", f"{user.name}")
    for chance in items:
        item = get_item(chance[3:7], "id", cur_lan)
        if item is None:
            continue
        text = text.replace(chance, item.displayname)
    for chance in item_emojis:
        item = get_item(chance[4:8], "id", cur_lan)
        if item is None:
            continue
        text = text.replace(chance, item.emoji)
    for bar in progress_bars:
        prime = bar[1:-1].split(":")
        text = text.replace(bar, await progress_bar(int(prime[1]), int(prime[2])))
    return text


async def get_weapons(user: nextcord.Member):
    i = await playerinfo()
    g = await get_inv_data()
    c = g[str(user.id)]["bag"]
    ganga = []

    for xo, auia in enumerate(i[str(user.id)]["weapon_equiped"]):
        if auia != "none":
            oi = get_item(auia, "name")
            for cin in c:
                if cin["item"] != oi.id:
                    continue
                if cin["amount"] >= 1:
                    ganga.append(auia)
                else:
                    i[str(user.id)]["weapon_equiped"][xo] = "none"
                    with open("userdb/playerdata.json", "w") as f:
                        json.dump(i, f)
                    ganga.append("none")
                break
            else:
                i[str(user.id)]["weapon_equiped"][xo] = "none"
                with open("userdb/playerdata.json", "w") as f:
                    json.dump(i, f)
                ganga.append("none")
            continue
        ganga.append("none")

    return ganga


async def get_user_hp(user):
    pd = await playerinfo()
    sz = await skillz()

    return pd[str(user.id)]['hp'] + (sz[str(user.id)]['hp'] * 5)


async def isnt_beta(interaction):
    embed = nextcord.Embed(title="Musisz poczekać", description="To funkcja beta. Dostęp do niej będzie wkrótce.", color=main.color_normal)
    embed.set_footer(text=main.version)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    return


async def decode_rarity(i, leng):
    return leng['items']['rarity'][i]


async def get_rarity_color(ras):
    if ras == "common":
        kolor = 0xa6a6a6
    elif ras == "uncommon":
        kolor = 0x25ba20
    elif ras == "rare":
        kolor = 0x0296e0
    elif ras == "epic":
        kolor = 0x9f4ede
    elif ras == "legendary":
        kolor = 0xf7d40c
    elif ras == "mythic":
        kolor = 0xdb183c
    elif ras == "premium":
        kolor = 0xeb9f26
    else:
        kolor = main.color_normal

    return kolor


async def update_bank(user, change=0, mode="wallet"):
    users = await playerinfo()
    user = await isdebug(user)
    users[str(user.id)][mode] += change

    with open("userdb/playerdata.json", "w") as f:
        json.dump(users, f)

    return change


async def get_user_badges(user):
    badzie = await badges()
    playerdata = await playerinfo()
    badger = []
    for item in badzie:
        if item["name"] in playerdata[str(user.id)]["badges"]:
            badger.append(item["displayname"])

    if not badger:
        return " "
    else:
        return "\u200b".join(badger)


async def add_level(user):
    cur_lan = await get_lang(user)
    leng = await lang(cur_lan)
    abc = await otherinfo()
    users = await playerinfo()
    user = await isdebug(user)
    cts = await custommobs()
    users[str(user.id)]["xp"] -= 100
    users[str(user.id)]["level"] += 1
    with open("userdb/playerdata.json", "w") as f:
        json.dump(users, f)
    a = users[str(user.id)]["level"]
    text = f"{leng['other']['levels']['rewards']}:\n1000 {main.coin}"
    embed = nextcord.Embed(title=leng['other']['levels']['level'].replace('{a}', str(a)), color=main.color_normal)
    embed.set_footer(text=main.version[cur_lan])
    await update_bank(user, 1000, "wallet")
    if a <= 100:
        text += f"\n1 {main.skillpoint}"
        abc[str(user.id)]["skillpoint"] += 1
        with open("userdb/otherdatabase.json", "w") as f:
            json.dump(abc, f)

    if a == 5:
        limit = main.custom_mobs_limits['c']
        text += f"\n{leng['other']['levels']['increase']} {limit}"
        cts[str(user.id)]["rank"] = "c"
        with open('userdb/custommobs.json', 'w') as f:
            json.dump(cts, f)
    elif a == 10:
        limit = main.custom_mobs_limits['b']
        text += f"\n{leng['other']['levels']['increase']} {limit}"
        cts[str(user.id)]["rank"] = "b"
        with open('userdb/custommobs.json', 'w') as f:
            json.dump(cts, f)
    elif a == 20:
        limit = main.custom_mobs_limits['a']
        text += f"\n{leng['other']['levels']['increase']} {limit}"
        cts[str(user.id)]["rank"] = "a"
        with open('userdb/custommobs.json', 'w') as f:
            json.dump(cts, f)
    elif a == 50:
        limit = main.custom_mobs_limits['s']
        text += f"\n{leng['other']['levels']['increase']} {limit}"
        cts[str(user.id)]["rank"] = "s"
        with open('userdb/custommobs.json', 'w') as f:
            json.dump(cts, f)
    embed.description = text
    try:
        reas = await has_enabled(user, "dm_notifications")
        if reas is True:
            await user.send(embed=embed)
    except Exception as e:
        print(e)
    return users[str(user.id)]["xp"]


async def add_xp(user, amount):
    users = await playerinfo()
    users[str(user.id)]["xp"] += amount
    users[str(user.id)]["total_xp"] += amount

    with open("userdb/playerdata.json", "w") as f:
        json.dump(users, f)

    if users[str(user.id)]["xp"] >= 100:
        while users[str(user.id)]["xp"] >= 100:
            c = await add_level(user)
            if c < 100:
                break
        return
    else:
        return


async def sell_this(user, item: MorexItem, amount):
    user = await isdebug(user)

    cost = item.sellprice * amount

    await item.remove_item(user, amount)

    await update_bank(user, cost, "wallet")
    return True


async def buy_this(user, item: MorexItem, amount: int):
    user = await isdebug(user)
    playerdata = await playerinfo()

    cost = item.price * amount

    if playerdata[str(user.id)]['wallet'] < cost:
        return False

    await item.add_item(user, amount)

    await update_bank(user, cost * -1, "wallet")
    return True


async def trade_for_coins_check(interaction: Interaction, coin_user: nextcord.Member, item_user: nextcord.Member, coins, item: MorexItem, amount, language, cur_lan, eph, view, message_id=None, wb=None):
    res1 = await get_amount(coins, coin_user, "wallet")
    res2 = await item.get_amount(item_user, amount)
    if res1 is None or res2 is False:
        embed = nextcord.Embed(description=language['other']['invalid_value']['description'], color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
        embed.set_footer(text=main.version[cur_lan])
        if view is None:
            await interaction.response.send_message(embed=embed, ephemeral=eph)
        else:
            await interaction.edit(embed=embed)
        return False

    if res1 is False and res2 is not None:
        embed = nextcord.Embed(title=language['commands']['trade_money']['trade'], description=f"{coin_user} {language['commands']['trade_money']['no_coins']}", color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        if view is None:
            await interaction.response.send_message(embed=embed, ephemeral=eph)
        else:
            if wb is None:
                await interaction.followup.edit_message(embed=embed, view=None, message_id=message_id, content=None)
            else:
                await wb.edit(embed=embed, view=None, content=None)
        return False
    elif res1 is not False and res2 is None:
        embed = nextcord.Embed(title=language['commands']['trade_money']['trade'], description=f"{item_user} {language['commands']['trade_money']['no_items']}", color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        if view is None:
            await interaction.response.send_message(embed=embed, ephemeral=eph)
        else:
            if wb is None:
                await interaction.followup.edit_message(view=None, embed=embed, message_id=message_id, content=None)
            else:
                await wb.edit(embed=embed, view=None, content=None)
        return False
    elif res1 is False and res2 is None:
        embed = nextcord.Embed(title=language['commands']['trade_money']['trade'], description=f"{coin_user} {language['commands']['trade_money']['no_coins']}\n{item_user} {language['commands']['trade_money']['no_items']}", color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        if view is None:
            await interaction.response.send_message(embed=embed, ephemeral=eph)
        else:
            if wb is None:
                await interaction.followup.edit_message(embed=embed, view=None, message_id=message_id, content=None)
            else:
                await wb.edit(embed=embed, view=None, message_id=message_id, content=None)
        return False
    elif res1 is not False and res2 is not None:
        return True
    else:
        raise custom_errors.WhatHaveIDone


async def trade_for_items_check(interaction: Interaction, author: nextcord.Member, member: nextcord.Member, item1: MorexItem, item2: MorexItem, amount1, amount2, language, cur_lan, eph, view, message_id=None, wb=None):
    res1 = await item1.get_amount(author, amount1)
    res2 = await item2.get_amount(member, amount2)
    if res1 is False or res2 is False:
        embed = nextcord.Embed(description=language['other']['invalid_value']['description'], color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
        embed.set_footer(text=main.version[cur_lan])
        if view is None:
            await interaction.response.send_message(embed=embed, ephemeral=eph)
        else:
            await interaction.edit(embed=embed)
        return False

    if res1 is None and res2 is not None:
        embed = nextcord.Embed(title=language['commands']['trade_item']['trade'], description=f"{author} {language['commands']['trade_item']['no_items']}", color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        if view is None:
            await interaction.response.send_message(embed=embed, ephemeral=eph)
        else:
            if wb is None:
                await interaction.followup.edit_message(embed=embed, view=None, message_id=message_id, content=None)
            else:
                await wb.edit(embed=embed, view=None, content=None)
        return False
    elif res1 is not None and res2 is None:
        embed = nextcord.Embed(title=language['commands']['trade_item']['trade'], description=f"{member} {language['commands']['trade_item']['no_items']}", color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        if view is None:
            await interaction.response.send_message(embed=embed, ephemeral=eph)
        else:
            if wb is None:
                await interaction.followup.edit_message(view=None, embed=embed, message_id=message_id, content=None)
            else:
                await wb.edit(embed=embed, view=None, content=None)
        return False
    elif res1 is None and res2 is None:
        embed = nextcord.Embed(title=language['commands']['trade_item']['trade'], description=f"{author} {language['commands']['trade_item']['and']} {member} {language['commands']['trade_item']['both_no_items']}", color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        if view is None:
            await interaction.response.send_message(embed=embed, ephemeral=eph)
        else:
            if wb is None:
                await interaction.followup.edit_message(embed=embed, view=None, message_id=message_id, content=None)
            else:
                await wb.edit(embed=embed, view=None, message_id=message_id, content=None)
        return False
    elif res1 is not None and res2 is not None:
        return True
    else:
        raise custom_errors.WhatHaveIDone


async def user_dm_handler_trade_for_coins(c_user, itemp: str, amount: int, coins: int, i_user=None):
    if c_user is None:
        c_user = i_user
    cur_lan_c = await get_lang(c_user)
    leng_c = await lang(cur_lan_c)
    text_c = leng_c['commands']['trade_money']
    item_c = get_item(itemp, 'id', cur_lan_c)
    embed = nextcord.Embed(title=text_c['trade'], description=text_c['successful'], color=main.color_normal)
    if i_user is None:
        embed.add_field(name=text_c['you_got'], value=f"{amount} {item_c.displayname}", inline=False)
        embed.add_field(name=text_c['you_gave'], value=f"{coins} {main.coin}", inline=False)
    else:
        embed.add_field(name=text_c['you_got'], value=f"{coins} {main.coin}", inline=False)
        embed.add_field(name=text_c['you_gave'], value=f"{amount} {item_c.displayname}", inline=False)
    embed.set_footer(text=main.version[cur_lan_c])
    await c_user.send(embed=embed)


async def user_dm_handler_trade_for_items(c_user, item1: MorexItem, amount: int, item2: MorexItem, amount2: int, i_user=None):
    if c_user is None:
        c_user = i_user
    cur_lan_c = await get_lang(c_user)
    leng_c = await lang(cur_lan_c)

    text_c = leng_c['commands']['trade_item']

    embed = nextcord.Embed(title=text_c['trade'], description=text_c['successful'], color=main.color_normal)
    if i_user is None:
        embed.add_field(name=text_c['you_got'], value=f"{amount2} {item2.displayname}", inline=False)
        embed.add_field(name=text_c['you_gave'], value=f"{amount} {item1.displayname}", inline=False)
    else:
        embed.add_field(name=text_c['you_got'], value=f"{amount} {item1.displayname}", inline=False)
        embed.add_field(name=text_c['you_gave'], value=f"{amount2} {item2.displayname}", inline=False)
    embed.set_footer(text=main.version[cur_lan_c])
    await c_user.send(embed=embed)


async def get_amount(amount, user: nextcord.Member, mode: str):
    """_summary_

    Args:
        amount : numer
        user (nextcord.Member): osoba
        mode (str): wallet | bank

    Returns:
        None if invalid input
        False if not enough coins
        ~why~
    """
    user = await isdebug(user)
    player_info = await playerinfo()
    if mode == "wallet":
        user_coins = player_info[str(user.id)]["wallet"]
    else:
        user_coins = player_info[str(user.id)]["bank"]

    try:
        amount = int(amount)
        if amount <= 0:
            return None
        else:
            if user_coins < amount:
                return False
            else:
                return amount
    except ValueError:
        if amount == "all":
            if user_coins == 0:
                return False
            else:
                return user_coins
        return None


async def get_amount_item(user, item: MorexItem, amount):
    playerdata = await playerinfo()
    try:
        amount = int(amount)
        if amount <= 0:
            return None
        if amount*item.price > playerdata[str(user.id)]['wallet']:
            return False
        return amount
    except ValueError:
        if amount == "all":
            final_cost = playerdata[str(user.id)]['wallet'] // item.price
            if final_cost <= 0:
                return False
            return final_cost
        return None
    except TypeError:
        if item.price > playerdata[str(user.id)]['wallet']:
            return False
        return 1  # returns 1


async def try_amount(amount):
    try:
        amount = int(amount)
        if amount <= 0:
            return None
        return amount
    except ValueError:
        if amount == "all":
            return "all"
        return None
    except TypeError:
        return 1


async def bundle_add_item(user, item, amount, src, slot):
    user = await isdebug(user)

    users = await get_inv_data()

    if users[str(user.id)]["bundle"][slot]["item"] == item.sid:
        remaining = 6 - users[str(user.id)]["bundle"][slot]["amount"]
        if amount - remaining > 0:
            addition = remaining
        else:
            addition = amount
        if await item.get_amount(user, str(addition)):
            await item.remove_item(user, addition)
            users = await get_inv_data()
            users[str(user.id)]["bundle"][slot]["amount"] += addition
            with open("userdb/inventories.json", "w") as f:
                json.dump(users, f)
            return [item, addition, users[str(user.id)]["bundle"][slot]["amount"]]
        else:
            return False
    elif users[str(user.id)]["bundle"][slot]["item"] == "none":
        remaining = 6 - users[str(user.id)]["bundle"][slot]["amount"]
        if amount - remaining > 0:
            addition = remaining
        else:
            addition = amount
        if await item.get_amount(user, str(addition)):
            await item.remove_item(user, addition)
            users = await get_inv_data()

            users[str(user.id)]["bundle"][slot]["amount"] += addition
            users[str(user.id)]["bundle"][slot]["item"] = item.sid

            with open("userdb/inventories.json", "w") as f:
                json.dump(users, f)
            return ["none", item, addition]
        else:
            return False
    else:
        remaining = 6
        if amount - remaining > 0:
            addition = remaining
        else:
            addition = amount
        if await item.get_amount(user, str(addition)):
            await item.remove_item(user, addition)
            ajte = users[str(user.id)]["bundle"][slot]["item"]
            ajte = get_item(ajte, 'name')
            amt = users[str(user.id)]["bundle"][slot]["amount"]
            await ajte.add_item(user, users[str(user.id)]["bundle"][slot]["amount"])

            users = await get_inv_data()

            users[str(user.id)]["bundle"][slot]["amount"] = addition
            users[str(user.id)]["bundle"][slot]["item"] = item.sid

            with open("userdb/inventories.json", "w") as f:
                json.dump(users, f)
            return [ajte.id, amt, item, addition]
        else:
            return False


async def bundle_remove_item(user, amount, src, slot):
    """_summary_

    Args:
        user (_type_): _description_
        amount (_type_): _description_
        src (_type_): _description_
        slot (_type_): _description_

    Returns:
        [the item["name"], removed amount, new amount]
    """
    users = await get_inv_data()

    if users[str(user.id)]["bundle"][slot]["item"] == "none":
        return None
    else:
        amt = users[str(user.id)]["bundle"][slot]["amount"]
        ajte = users[str(user.id)]["bundle"][slot]["item"]
        ajte = get_item(ajte, 'name', 'en')

        c = None
        if amt <= amount:
            c = amount - amt
            amount = amt

        if src == "equipment":
            await ajte.add_item(user, amount)
            users = await get_inv_data()

        if c is None:
            users[str(user.id)]["bundle"][slot]["amount"] -= amount
            with open("userdb/inventories.json", "w") as f:
                json.dump(users, f)
            return [users[str(user.id)]["bundle"][slot]["item"], amount, amt - amount]
        else:
            users[str(user.id)]["bundle"][slot]["amount"] = 0
            users[str(user.id)]["bundle"][slot]["item"] = "none"
            with open("userdb/inventories.json", "w") as f:
                json.dump(users, f)
            return ["none", amt, ajte.sid]


async def no_account(interaction: Interaction, language):
    leng = await lang(language)
    embed = nextcord.Embed(title=leng['other']['no_account']['title'], description=leng['other']['no_account']['description'], color=main.color_normal)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1134067893840126012/1226297031203487896/65939r.png")
    embed.set_footer(text=main.version[language])
    await interaction.response.send_message(embed=embed, ephemeral=True)


async def mperr(interaction: Interaction, language):
    leng = await lang(language)
    embed = nextcord.Embed(title=leng['other']['mperr']['title'], description=leng['other']['mperr']['description'], color=main.color_normal)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1134067893840126012/1226297031203487896/65939r.png")
    embed.set_footer(text=main.version[language])
    await interaction.response.send_message(embed=embed, ephemeral=True)


async def pmerr(interaction: Interaction, language):
    leng = await lang(language)
    embed = nextcord.Embed(title=leng['other']['pmerr']['title'], description=leng['other']['pmerr']['description'], color=main.color_normal)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1134067893840126012/1226297031203487896/65939r.png")
    embed.set_footer(text=main.version[language])
    await interaction.response.send_message(embed=embed, ephemeral=True)


async def firsttime(user, second_user=None):
    user = await isdebug(user)
    second_user = await isdebug(second_user)

    await create_account(user, None, True)
    playerdata = await playerinfo()
    if playerdata[str(user.id)]["banned"] == "yes":
        raise custom_errors.ToMakeCodeWorkError
    # with open("randomevent.json", "r") as f:
    #   asda = json.load(f)
    # if str(user.id) not in asda:
    #   if str(user.id) == "826792866776219709":
    #     await self.add_item(user, "field", 1)
    #     await self.add_item(user, "strre", 1)
    #     await user.send("UwU")

    #     asda.append(str(user.id))
    #     with open("randomevent.json", "w") as f:
    #       json.dump(asda, f)

    if second_user is None:
        return user
    else:
        a = await create_account(second_user, True)
        tset = await setting()
        aaa = tset[str(user.id)]["multiplayer"]
        if aaa == "disabled":
            return "pmerr"
        if a is False:
            return False

        playerdata = await playerinfo()
        if playerdata[str(second_user.id)]["banned"] == "yes":
            raise custom_errors.ToMakeCodeWorkError

        dd = tset[str(second_user.id)]["multiplayer"]
        if dd == "disabled":
            return "mperr"

        return [user, second_user]


async def short_user_info(user):
    playerdata = await playerinfo()
    p_icon = await player_icon(user)
    pd = playerdata[str(user.id)]

    info = f"Level: {pd['level']} ({pd['xp']}/100)\nXP: {pd['total_xp']}\nCoins: {pd['bank'] + pd['wallet']} {main.coin}"

    return {"info": info, "icon": p_icon, "acc_creation": [pd['version'], pd['timestamp']]}


async def get_row():
    lista = []
    table = ["<:MX_Cash:1198436125279256576>", "<:MX_Diamond:1241071516410581002>", "<:MX_GolenEssence:1222205491728351344>"]
    for i in range(3):
        rnd = random.randint(0, 2)
        if rnd == 1:
            ornd = random.randint(1, 20)
            if ornd != 17:
                rnd = random.choice([0, 2])
        lista.append(table[rnd])

    return lista


async def dead_row():
    lista = []
    table = ["<:MX_Cash:1198436125279256576>", "<:MX_Diamond:1241071516410581002>", "<:MX_GolenEssence:1222205491728351344>"]
    for i in range(3):
        it = random.choice(table)
        lista.append(it)
        table.remove(it)

    return lista


async def create_text(top_row, middle_row, bottom_row):
    rows = [top_row, middle_row, bottom_row]
    text = []
    for row in rows:
        text.append("".join(row))

    return "\n".join(text)


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


async def validate_amount_input(interaction, user_language, amount):
    language_file = await lang(user_language)
    if isinstance(amount, int):
        if amount >= 0:
            return amount
        amount = "-1"
    try:
        amount = int(amount)
        if amount <= 0:
            embed = nextcord.Embed(description=language_file['other']['too_small_value']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[user_language])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return amount
    except ValueError:
        if amount == "all":
            return "all"
        embed = nextcord.Embed(description=language_file['other']['invalid_value']['description'], color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=main.version[user_language])
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return False
    except TypeError:
        return 1


async def missing_item(interaction, user_language):
    language_file = await lang(user_language)
    embed = nextcord.Embed(description=language_file['other']['bad_item']['description'], color=main.color_normal)
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=main.version[user_language])
    await interaction.response.send_message(embed=embed, ephemeral=True)
    return False


async def missing_recipe(interaction, user_language):
    language_file = await lang(user_language)
    embed = nextcord.Embed(description=language_file['other']['missing_recipe']['description'], color=main.color_normal)
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=main.version[user_language])
    await interaction.response.send_message(embed=embed, ephemeral=True)
    return False


async def unavailable_recipe(interaction, user_language):
    language_file = await lang(user_language)
    embed = nextcord.Embed(description=language_file['other']['unavailable_recipe']['description'], color=main.color_normal)
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=main.version[user_language])
    await interaction.response.send_message(embed=embed, ephemeral=True)
    return False


async def untradeable_item(interaction, user_language):
    language_file = await lang(user_language)
    embed = nextcord.Embed(description=language_file['other']['untradeable_item']['description'], color=main.color_normal)
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=main.version[user_language])
    await interaction.response.send_message(embed=embed, ephemeral=True)
    return False


async def get_item_with_handling(item, mode, cur_lan, interaction):
    item = get_item(item, mode, cur_lan)
    if not item:
        await missing_item(interaction, cur_lan)
        return False
    if 'a' in item.id or 'i' in item.id:
        await missing_item(interaction, cur_lan)
        return False
    return item


async def has_event_boost(boost):
    if not main.event['current_event']:
        return 1
    if main.event['current_event'].default_features[boost]:
        return main.event['current_event'].default_features[boost]
    return 1

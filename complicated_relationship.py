import nextcord
from nextcord import Interaction
from morex import MorexEnemy
import functions as fns
from PIL import Image
import custom_errors
import buttons
import random
import main
import json


async def hunter(mode, interaction: Interaction, place, color):
    g = await fns.get_inv_data()
    cur_lan = await fns.get_lang(interaction.user)
    leng = await fns.lang(cur_lan)
    text = leng['commands']['hunt']

    weapon = await fns.get_weapon(interaction.user)

    if weapon is False:
        if mode[0] == "search" or mode[0] == "enemy":
            return False
        errorembed = nextcord.Embed(description=text['noweapon'], color=main.color_normal)
        errorembed.set_author(name=f"{interaction.user.name}", icon_url=str(interaction.user.display_avatar))
        errorembed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=errorembed, ephemeral=True)
        return

    weapon = fns.get_item(weapon, "name", cur_lan)

    user_bundle = g[str(interaction.user.id)]["bundle"]
    user_weapons = await fns.get_weapons(interaction.user)
    weapon_pack = []
    for weapons in user_weapons:
        wep = fns.get_item(weapons, "name", cur_lan)
        weapon_pack.append(wep)

    is_rewarded = True

    if mode[0] == "slime":
        res = await fns.get_from_value(place.enemies)
        save_identifier = res["enemy"]
        if save_identifier == "nothing":
            return
        enemy = fns.get_morex_oponent(save_identifier, "name", cur_lan)
    elif mode[0] == "search":
        save_identifier = random.choice(place.enemies)
        enemy = fns.get_morex_oponent(save_identifier, "name", cur_lan)
    elif mode[0] == "enemy":
        save_identifier = mode[2]
        enemy = fns.get_morex_oponent(save_identifier, "name", cur_lan)
    elif mode[0] == "custom":
        save_identifier = place
        enemy = fns.get_morex_oponent(save_identifier, "list", cur_lan)
        is_rewarded = False
    else:
        raise custom_errors.WhatHaveIDone("/hunt weird mode")

    if not enemy:
        save_identifier = "m000"
        is_rewarded = False
        data = {
            'id': 'm000',
            'name': 'null', 
            'emoji': '<:MX_QuestionMark:1266370987474288764>', 
            'attack': [11, 0, 1], 
            'weapon': 'n', 
            'flags': 0, 
            'type': 548, 
            'image': 'https://kolpa01.github.io/do_you_miss_me.png', 
            'xpreaward': [-10, -1], 
            'hp': 1000, 
            'drops': [{'item': 'voidcrystal', 'min_value': -1, 'max_value': -1, 'chance': 10000}], 
            'disname': 'Null', 
            'meetup': 'Something is wrong.', 
            'is_meetup_default': True, 
            'uattacks': {
                'baseuserattack': {'default': 'Some thing are better left alone.'}, 
                'faileduserattack': {'default': 'Can you hear its scream?'}
            }, 
            'eattacks': {
                'failedmobattack': '0.', 
                'hpmobattack': '{ahp}.', 
                'shmobattack': '{ash}.', 
                'bshmobattack': 'It is pointless.', 
                'bshandhpmobattack': 'You can hear it cracking.'
            }, 
            'deaths': {
                'hpdeath': 'Don\'t come back.', 
                'beerdeath': 'Disappointing.', 
                'curseddeath': 'Disappoiting.', 
                'hpandshdeath': 'Was it always you?', 
                'escape': 'It cannot escape.'
            }, 
            'spells': {
                'atk': 'You can see it sparkling.', 
                'reb': 'You can feel it.'
            }
        }
        enemy = MorexEnemy(data)

    meetup_text = await fns.text_formatting_battle(enemy.meetup, interaction.user, enemy.displayname, cur_lan)

    icon = await fns.player_icon(interaction.user)
    full_bar = await fns.progress_bar(1, 1)
    user_hp = await fns.get_user_hp(interaction.user)

    embed = nextcord.Embed(title=text['fight'], color=color)
    embed.add_field(name=f"{enemy.displayname}", value=f"{full_bar}\n{enemy.hp}/{enemy.hp} HP\n0 SH", inline=False)
    embed.add_field(name=f"{icon} {interaction.user.name}", value=f"{full_bar}\n{user_hp}/{user_hp} HP\n0 SH", inline=False)
    embed.add_field(name=text['info'], value=meetup_text, inline=False)
    embed.set_thumbnail(url=enemy.image)
    embed.set_footer(text=main.version[cur_lan])

    view = buttons.HuntButtons(360, user_hp, enemy.hp, user_hp, enemy.hp, save_identifier, enemy.image, weapon, weapon_pack, 0, 3, 0, 0, 3, 9, user_bundle, is_rewarded, False, True, mode, icon, False, enemy, text, cur_lan, color, 0, {}, 0, None, interaction.user)
    if weapon.toolatributes.itemtype == "spellbook":
        view.atks.disabled = False
    else:
        view.atks.disabled = True

    if mode[0] == "custom":
        await interaction.response.edit_message(embed=embed, view=view)
    else:
        await interaction.response.send_message(embed=embed, view=view)


async def init_dialogues(interaction: Interaction, current_language, dialogue, default=None, new_message=True):
    with open(f'dialogues/{current_language}/{dialogue}.json') as f:
        dialogues = json.load(f)
    mapper = {}

    for i in dialogues:
        a = dialogues[i]['choices']
        mapper.update({f"{i}": a})

    if default is None:
        starting_point = 'firsttime'
    else:
        starting_point = default

    if 'exec' in dialogues[starting_point]:
        for execution in dialogues[starting_point]['exec']:
            if execution == 'add_event':
                await fns.add_event(interaction.user, dialogues[starting_point]['exec'][execution])
            if execution == 'add_item':
                item = fns.get_item(dialogues[starting_point]['exec'][execution][0], 'name', current_language)
                await item.add_item(interaction.user, dialogues[starting_point]['exec'][execution][1])
            if execution == 'add_xp':
                await fns.add_xp(interaction.user, dialogues[starting_point]['exec'][execution])
            if execution == 'update_quest':
                await fns.update_quest(interaction.user, dialogues[starting_point]['exec'][execution][0], dialogues[starting_point]['exec'][execution][1], current_language)

    cur_choice = []
    view = buttons.Dialogues(180, interaction.user, mapper, dialogues, current_language)
    for i, choice in enumerate(mapper[starting_point]):
        if i == 0:
            view.one.label = choice
            cur_choice.append(mapper[starting_point][choice])
        elif i == 1:
            view.two.label = choice
            cur_choice.append(mapper[starting_point][choice])
        elif i == 2:
            view.three.label = choice
            cur_choice.append(mapper[starting_point][choice])
        elif i == 3:
            view.four.label = choice
            cur_choice.append(mapper[starting_point][choice])
    view.current_choices = cur_choice
    view.children = view.children[:len(mapper[starting_point])]

    embed = nextcord.Embed(title=dialogues[starting_point]['name'], description=dialogues[starting_point]['text'], color=int(dialogues[starting_point]['color'], 16))
    embed.set_thumbnail(dialogues[starting_point]['icon'])
    embed.set_footer(text=main.version[current_language])

    if new_message:
        await interaction.response.send_message(embed=embed, view=view)
    else:
        await interaction.response.edit_message(embed=embed, view=view)


async def pages_helper(embeds: list[nextcord.Embed], user: nextcord.Member):
    cur_lan = await fns.get_lang(user)
    leng = await fns.lang(cur_lan)

    return buttons.Pages(60, len(embeds), embeds, user, main.version[cur_lan], leng['other']['pages']['page'], leng)

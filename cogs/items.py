import nextcord
from nextcord.ext import commands
import main
import buttons
from nextcord import Interaction, SlashOption
import functions as fns
import random
from autocompletes import item_autocompletes, recipe_autocompletes


class ItemsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="inventory", description="View user's inventory.", description_localizations={"pl": "Wyświetl ekwipunek użytkownika."}, integration_types=main.integrations, contexts=main.contexts)
    async def inventory(
            self,
            interaction: Interaction,
            member: nextcord.Member = SlashOption(
                name="member",
                name_localizations={"pl": "osoba"},
                description="Select a member.",
                description_localizations={"pl": "Wybierz osobę."},
                required=False
            )
    ):
        if member is None:
            member = await fns.firsttime(interaction.user)
            cur_lan = await fns.get_lang(member)
        else:
            aa = await fns.firsttime(interaction.user, member)
            cur_lan = await fns.get_lang(interaction.user)

            if aa is False:
                await fns.no_account(interaction, cur_lan)
                return
            elif aa == "pmerr":
                await fns.pmerr(interaction, cur_lan)
                return
            elif aa == "mperr":
                await fns.mperr(interaction, cur_lan)
                return
            member = aa[1]

        leng = await fns.lang(cur_lan)
        text = leng['commands']['inventory']

        user_inventory = await fns.get_bulk_amount(member)

        items = {}
        for item, amount in user_inventory.items():
            if amount == 0:
                continue
            full_item = fns.get_item(item, "id", cur_lan)
            items.update({full_item.id: [full_item, amount]})
        items = {k: v for k, v in sorted(items.items(), key=lambda item: item[1][0].disname)}
        
        if not items:
            if member == interaction.user:
                txt = text['self_no_items']
            else:
                txt = text['member_no_items']
            embed = nextcord.Embed(description=txt, color=main.color_normal)
            embed.set_author(name=f"{text['title']} {member.name}", icon_url=member.display_avatar.url)
            embed.set_footer(text=f"{leng['other']['pages']['page']} 0/0 | {main.version[cur_lan]}")
            await interaction.response.send_message(embed=embed)
            return

        bomb = []
        embed = None
        d = 0
        for item, amount in items.values():
            if d == 0:
                embed = nextcord.Embed(color=main.color_normal)
                embed.set_author(name=f"{text['title']} {member.name}", icon_url=member.display_avatar.url)
            rarity = await fns.decode_rarity(item.rarity, leng)

            embed.add_field(name=f"{item.displayname} - {amount}", value=f"{rarity} | `{item.id}`", inline=False)

            d += 1
            if d == 5:
                bomb.append(embed)
                d = 0

        if d != 5 and d != 0:
            bomb.append(embed)

        aaa = len(bomb)
        embed = bomb[0]
        if aaa == 1:
            embed.set_footer(text=f"{leng['other']['pages']['page']} 1/1 | {main.version[cur_lan]}")
            await interaction.response.send_message(embed=embed)
            return
        embed.set_footer(text=f"{leng['other']['pages']['page']} 1/{aaa} | {main.version[cur_lan]}")
        await interaction.response.send_message(embed=embed, view=buttons.Pages(60, aaa, bomb, interaction.user, main.version[cur_lan], leng['other']['pages']['page'], leng))

    @nextcord.slash_command(name="item", description="View informations about an item.", description_localizations={"pl": "Wyświetl informacje o przedmiocie."}, integration_types=main.integrations, contexts=main.contexts)
    async def item(
            self,
            interaction=Interaction,
            itemp: str = SlashOption(
                name="item",
                name_localizations={"pl": "przedmiot"},
                description="Choose the item.",
                description_localizations={"pl": "Wybierz przedmiot."},
                required=True,
            ),
    ):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text_cmd = leng['commands']['item']

        item = fns.get_item(itemp, 'id', cur_lan)

        if item is None:
            return
        if 'i' in item.id or 'a' in item.id:
            return

        amount = await item.get_amount(interaction.user, 'all')
        amount = 0 if amount is None else amount

        price = main.deny if item.price is False else item.price
        sellprice = main.deny if item.sellprice is False else item.sellprice
        tradeable = main.deny if item.tradeable is False else main.accept

        embed = nextcord.Embed(title=item.disname,
                               description=f"```\n{item.description}```\n{await fns.decode_rarity(item.rarity, leng)}\n\n**{text_cmd['price']}:** {price}\n**{text_cmd['sellprice']}:** {sellprice}\n**{text_cmd['tradeable']}:** {tradeable}\n**{text_cmd['owned']}:** {amount}",
                               color=await fns.get_rarity_color(item.rarity))
        embed.set_thumbnail(url=item.image)
        if item.toolartibutes is not False:
            cursed = main.deny if item.toolartibutes.cursed is False else main.accept  # item.toolartibutes.cursed
            if item.toolartibutes.type == "weapon":
                itype = text_cmd['weapon']

                nattack = item.toolatributes.attack[0]
                kattack = item.toolatributes.attack[1]
                mattack = item.toolatributes.attack[2]
                if item.toolatributes.itemtype == "sword":
                    typ = text_cmd['sword']
                elif item.toolatributes.itemtype == "trident":
                    typ = text_cmd['trident']
                elif item.toolatributes.itemtype == "spellbook":
                    typ = text_cmd['spellbook']
                else:
                    typ = "Unidentified"

                embed.add_field(name=text_cmd['ta_title'],
                                value=f"**{text_cmd['type']}**: {itype} / {typ}\n**{text_cmd['attack']}**: {mattack} / {nattack} / {kattack}\n**{text_cmd['cursed']}**: {cursed}",
                                inline=False)

                if item.toolatributes.itemtype == "spellbook":
                    nazwa = item.toolatributes.power.name
                    emoji = item.toolatributes.power.emoji
                    wartosc = item.toolatributes.power.value
                    desc = item.toolatributes.power.description

                    embed.add_field(name=text_cmd['power_info'],
                                    value=f"**{text_cmd['name']}:** {emoji} {nazwa}\n**{text_cmd['description']}:** {desc}\n**{text_cmd['value']}:** {wartosc}",
                                    inline=False)

            elif item.toolatributes.type == "container":
                itype = text_cmd['container']
                text = []
                if item.toolatributes.itemtype == "bundle":
                    typ = text_cmd['bundle']
                    for items in item.toolatributes.contains:
                        if items["item"] == "coins":
                            text.append(f"{items['value']} {main.coin}\n")
                            continue
                        bitem = fns.get_item(items['item'], 'name', cur_lan)
                        text.append(f"{items['value']} {bitem.displayname}\n")
                elif item.toolatributes.itemtype == "box":
                    typ = text_cmd['box']
                    for items in item.toolatributes.contains:
                        if items["item"] == "coins":
                            bitem = main.coin
                        else:
                            bitem = fns.get_item(items['item'], 'name', cur_lan)
                            bitem = bitem.displayname
                        amounta = items["min_value"]
                        amountb = items["max_value"]
                        aaa = items["chance"]
                        text.append(f"**{aaa / 100}%** ")
                        if amounta != amountb:
                            text.append(f"{amounta}-{amountb} ")
                        else:
                            text.append(f"{amounta} ")
                        text.append(f"{bitem}\n")
                else:
                    typ = "Unidentified"
                embed.add_field(name=text_cmd['ta_title'], value=f"**{text_cmd['type']}**: {itype} / {typ}\n**{text_cmd['cursed']}**: {cursed}", inline=False)
                embed.add_field(name=text_cmd['contains'], value="".join(text), inline=False)
            elif item.toolartibutes.type == "smeltable":
                itype = text_cmd['smeltable']
                if item.toolartibutes.itemtype == "ore":
                    typ = text_cmd['ore']
                elif item.toolartibutes.itemtype == "other":
                    typ = text_cmd['other']
                else:
                    typ = "Unidentified"

                itata = fns.get_item(item.toolartibutes.item_smelted, 'name', cur_lan)

                embed.add_field(name=text_cmd['ta_title'],
                                value=f"**{text_cmd['type']}:** {itype} / {typ}\n**{text_cmd['lvl_req']}:** {item.toolartibutes.lvl_required}\n**{text_cmd['after_smelting']}:** {item.toolartibutes.amount} {itata.displayname}\n**{text_cmd['xp']}:** {item.toolartibutes.xp_reaward[0]}-{item.toolartibutes.xp_reaward[1]}\n**{text_cmd['cursed']}:** {cursed}",
                                inline=False)
                text = []

                for ambat in item.toolartibutes.fuel:
                    it = fns.get_item(ambat['fuel'], 'name', cur_lan)
                    text.append(f'{ambat["amount"]} {it.displayname} - {ambat["smelt_time"]}s\n')
                embed.add_field(name=text_cmd['fuel'], value="".join(text), inline=False)
            elif item.toolatributes.type == "bundle":
                if item.toolatributes.power.type == "satk":
                    embed.add_field(name=text_cmd['power_info'], value=f"**{text_cmd['type']}:** {text_cmd['satk']}\n**{text_cmd['value']}:** {item.toolatributes.power.value}\n**{text_cmd['chance']}:** {item.toolatributes.power.chance / 100}%", inline=False)
                elif item.toolatributes.power.type == "reg":
                    embed.add_field(name=text_cmd['power_info'], value=f"**{text_cmd['type']}:** {text_cmd['reg']}\n**{text_cmd['value']}:** {item.toolatributes.power.value}\n**{text_cmd['chance']}:** {item.toolatributes.power.chance / 100}%", inline=False)
                elif item.toolatributes.power.type == "def":
                    embed.add_field(name=text_cmd['power_info'], value=f"**{text_cmd['type']}:** {text_cmd['def']}\n**{text_cmd['value']}:** {item.toolatributes.power.value}\n**{text_cmd['chance']}:** {item.toolatributes.power.chance / 100}%", inline=False)
                elif item.toolatributes.power.type == "time":
                    embed.add_field(name=text_cmd['power_info'], value=f"**{text_cmd['type']}:** {text_cmd['time']}\n**{text_cmd['chance']}:** {item.toolatributes.power.chance / 100}%", inline=False)
                elif item.toolatributes.power.type == "smw":
                    embed.add_field(name=text_cmd['power_info'], value=f"**{text_cmd['type']}:** {text_cmd['smw']}\n**{text_cmd['value']}:** {fns.get_item(item.toolatributes.power.value)}\n**{text_cmd['chance']}:** {item.toolatributes.power.chance / 100}%", inline=False)
                if item.toolatributes.bonus is not None:
                    new_text = []
                    for i in item.toolatributes.bonus:
                        if i.type == "smw":
                            new_text.append(f"**{text_cmd['smw']}**\n{main.empty}**{text_cmd['value']}:** {fns.get_item(i.value, "id", cur_lan)}\n{main.empty}**{text_cmd['chance']}:** {i.chance / 100}%")
                        elif i.type == "time":
                            new_text.append(f"**{text_cmd['time']}**\n{main.empty}**{text_cmd['chance']}:** {i.chance / 100}%")
                        elif i.type == "satk":
                            new_text.append(f"**{text_cmd['satk']}**\n{main.empty}**{text_cmd['value']}:** {i.value}\n{main.empty}**{text_cmd['chance']}:** {i.chance / 100}%")
                        elif i.type == "def":
                            new_text.append(f"**{text_cmd['def']}**\n{main.empty}**{text_cmd['value']}:** {i.value}\n{main.empty}**{text_cmd['chance']}:** {i.chance / 100}%")
                        elif i.type == "reg":
                            new_text.append(f"**{text_cmd['reg']}**\n{main.empty}**{text_cmd['value']}:** {i.value}\n{main.empty}**{text_cmd['chance']}:** {i.chance / 100}%")
                    embed.add_field(name=text_cmd['bp'], value="\n".join(new_text))
            elif item.toolatributes.type == "unlockorb":
                if item.toolatributes.itemtype == "search":
                    embed.add_field(name=text_cmd['ta_title'], value=f"**{text_cmd['command']}:** /{item.toolartibutes.itemtype}\n**{text_cmd['location']}:** {fns.get_search_locations(item.toolatributes.value, cur_lan)}")
            elif item.toolartibutes.type == "none":
                if item.toolartibutes.itemtype == "awaiting":
                    embed.add_field(name=text_cmd['ta_title'], value=f"**{text_cmd['in_days']}** <t:{item.toolartibutes.timestamp}:R>", inline=False)
            else:
                embed.add_field(name="Error",
                                value=f'Not Implemented {item.toolartibutes.type}/{item.toolartibutes.itemtype}',
                                inline=False)
        debug_info = await fns.has_enabled(interaction.user, "debug_info")
        if debug_info is True:
            embed.add_field(name=text_cmd['dev'], value=f"**ID:** `{item.id}`\n**SID:** `{item.sid}`", inline=False)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="use", description="Use items.", description_localizations={"pl": "Użyj przedmiotów."}, integration_types=main.integrations, contexts=main.contexts)
    async def use(
            self,
            interaction: Interaction,
            itemp: str = SlashOption(
                name="item",
                name_localizations={"pl": "przedmiot"},
                description="Choose the item.",
                description_localizations={"pl": "Wybierz przedmiot."},
                required=True,
            ),
            amount: str = SlashOption(
                name="amount",
                name_localizations={"pl": "ilość"},
                description="Choose an amount. (25, 3, all)",
                description_localizations={"pl": "Wybierz ilość. (25, 3, all)"},
                required=False
            )
    ):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['use']
        item = fns.get_item(itemp, "id", cur_lan)
        if item is None:
            return
        if item.useable is False:
            return

        amount = await item.get_amount(interaction.user, amount)

        if amount is False:
            embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        elif amount is None:
            embed = nextcord.Embed(description=leng['other']['not_enough_items']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if item.toolartibutes.itemtype == "map":
            embed = nextcord.Embed(title=text['map'], description=f"**{text['legend']}:**\n{item.toolartibutes.legend}", color=main.color_normal)
            embed.set_image(url=item.toolartibutes.map)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return
        elif item.toolartibutes.itemtype == "note":
            embed = nextcord.Embed(description=f"### {item.toolartibutes.title}\n{item.toolartibutes.text}", color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return
        elif item.toolartibutes.type == "unlockorb":
            otherdata = await fns.otherinfo()

            if item.toolartibutes.value in otherdata[str(interaction.user.id)]["search"]:
                embed = nextcord.Embed(description=text['owned'], color=main.color_normal)
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                embed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=embed)
                return

            await item.remove_item(interaction.user, 1)

            await fns.add_location(interaction.user, item.toolartibutes.value, item.toolartibutes.itemtype)

            if item.sid == "caveorb":
                await fns.update_quest(interaction.user, ["chapter1", "shopcraft"], 1, cur_lan)
            embed = nextcord.Embed(description=f"{text['unlocked']} {leng[item.toolartibutes.itemtype]['name'][item.toolartibutes.value]}", color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return
        elif item.toolartibutes.itemtype == "bundle":
            joining = []
            for i in item.toolartibutes.contains:
                if i["item"] == "coins":
                    await fns.update_bank(interaction.user, i["value"]*amount, "bank")
                    joining.append(f"{i['value']*amount} {main.coin}")
                else:
                    temp_item = fns.get_item(i['item'], "name", cur_lan)
                    await temp_item.add_item(interaction.user, i["value"] * amount)
                    joining.append(f"{i['value']*amount} {temp_item.displayname}")
            txt = '\n'.join(joining)
            await item.remove_item(interaction.user, amount)
            embed = nextcord.Embed(description=f"{text['open']} {amount} {item.displayname}\n**{text['get']}:**\n{txt}", color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return
        elif item.toolatributes.itemtype == "box":
            joinable = []
            for i in item.toolatributes.contains:
                temp_amt = 0
                if i['item'] == "coins":
                    for ii in range(amount):
                        chance = random.randint(1, 10000)
                        if chance <= i['chance']:
                            value = random.randint(i['min_value'], i['max_value'])
                            temp_amt += value
                    if temp_amt > 0:
                        await fns.update_bank(interaction.user, temp_amt, "wallet")
                        joinable.append(f"{temp_amt} {main.coin}")
                else:
                    for ii in range(amount):
                        chance = random.randint(1, 10000)
                        if chance <= i['chance']:
                            value = random.randint(i['min_value'], i['max_value'])
                            temp_amt += value
                    if temp_amt > 0:
                        temp_item = fns.get_item(i['item'], 'name', cur_lan)
                        await temp_item.add_item(interaction.user, temp_amt)
                        joinable.append(f"{temp_amt} {temp_item.displayname}")
            txt = "\n".join(joinable)
            await item.remove_item(interaction.user, amount)
            embed = nextcord.Embed(description=f"{text['open']} {amount} {item.displayname}\n**{text['get']}:**\n{txt}", color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return

    @item.on_autocomplete("itemp")
    async def item_autocomplete(self, interaction, current: str):
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        data = await item_autocompletes.all_items(leng, current)
        await interaction.response.send_autocomplete(data)

    @use.on_autocomplete("itemp")
    async def use_autocomplete(self, interaction, current: str):
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        data = await item_autocompletes.useable_items(leng, current)
        await interaction.response.send_autocomplete(data)


def setup(client):
    client.add_cog(ItemsCog(client))

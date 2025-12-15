import nextcord
from nextcord.ext import commands
import main
import json
from nextcord import Interaction, SlashOption
import functions as fns


class EquipmentCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="equipment")
    async def equipment(self, interaction: Interaction):
        pass

    @equipment.subcommand(name="view", description="View your equipment.", description_localizations={"pl": "Wyświetl swoje wyposażenie."})
    async def equipment_view(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['eq_view']
        users = await fns.get_inv_data()

        weapons = await fns.get_weapons(user)

        squad = []
        for i, weapon in enumerate(weapons, 1):
            if weapon == "none":
                squad.append(f"{i} - [Empty]")
            else:
                weapon_name = fns.get_item(weapon, "name", cur_lan)
                squad.append(f"{i} - {weapon_name.displayname}")

        squad = "\n".join(squad)

        squad2 = []

        for i, item in enumerate(users[str(user.id)]["bundle"], 1):
            if item["item"] == "none":
                squad2.append(f"{i} - [Empty]")
            else:
                item_name = fns.get_item(item['item'], 'name', cur_lan)
                squad2.append(f"{i} - {item['amount']} {item_name}")

        squad2 = "\n".join(squad2)

        embed = nextcord.Embed(description=f"{text['your_weapons']}\n{squad}\n{text['your_bundle']}\n{squad2}", color=main.color_normal)
        embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @equipment.subcommand(name="bundle")
    async def equipment_bundle(self, interaction: Interaction):
        pass

    @equipment.subcommand(name="weapon")
    async def equipment_weapon(self, interaction: Interaction):
        pass

    @equipment_bundle.subcommand(name="equip", description="Move items from inventory to bundle.", description_localizations={"pl": "Przenieś przedmioty z ekwipunku do sakwy."})
    async def bundle_equip(
            self,
            interaction: Interaction,
            itemp: str = SlashOption(
                name="item",
                name_localizations={"pl": "przedmiot"},
                description="Choose the item.",
                description_localizations={"pl": "Wybierz przedmiot."},
                required=True,
            ),
            slot: int = SlashOption(
                name="slot",
                description="Choose the slot.",
                description_localizations={"pl": "Wybierz slot."},
                required=True,
                choices={"1": 0, "2": 1, "3": 2, "4": 3}
            ),
            amount: int = SlashOption(
                name="amount",
                name_localizations={"pl": "ilość"},
                description="Choose the amount from the list.",
                description_localizations={"pl": "Wybierz ilość z listy."},
                required=True,
                choices={"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6}
            )
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['eq_b_eq']

        if slot not in [0, 1, 2, 3]:
            return

        if amount not in [1, 2, 3, 4, 5, 6]:
            return

        item = fns.get_item(itemp, "id", cur_lan)

        if item is None:
            return

        if item.toolatributes is False:
            return

        if item.toolatributes.type != "bundle":
            return

        res = await fns.bundle_add_item(user, item, amount, "equipment", slot)

        if res is False:
            embed = nextcord.Embed(description=leng['other']['not_enough_items']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        else:
            if res[0] == "none":
                embed = nextcord.Embed(
                    description=f"{text['added']} {res[2]} {item.displayname} {text['slot']} {slot + 1}\n\n**{text['current_slot']} {int(slot) + 1}:**\n{res[2]} {item.displayname}\n**{text['inventory']}:**\n-{res[2]} {item.displayname}",
                    color=main.color_normal)
                embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
                embed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=embed)

            elif res[0] == item:
                embed = nextcord.Embed(
                    description=f"{text['added']} {res[1]} {item.displayname} {text['slot']} {slot + 1}\n\n**{text['current_slot']} {slot + 1}:**\n{res[2]} {item.displayname}\n**{text['inventory']}:**\n-{res[1]} {item.displayname}",
                    color=main.color_normal)
                embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
                embed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=embed)

            else:
                disname2 = fns.get_item(res[0], 'id', cur_lan)
                embed = nextcord.Embed(
                    description=f"{text['changed']} {res[1]} {disname2.displayname} {text['to']} {res[3]} {item.displayname} {text['on_slot']} {slot + 1}\n\n**{text['current_slot']} {slot + 1}:**\n{res[3]} {item.displayname}\n**{text['inventory']}:**\n-{res[3]} {item.displayname}\n+ {res[1]} {disname2.displayname}",
                    color=main.color_normal)
                embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
                embed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=embed)

    @equipment_bundle.subcommand(name="unequip", description="Move items from bundle to inventory.", description_localizations={"pl": "Przenieś przedmioty z sakwy do ekwipunku."})
    async def bundle_unequip(
            self,
            interaction: Interaction,
            slot: int = SlashOption(
                name="slot",
                description="Choose the slot.",
                description_localizations={"pl": "Wybierz slot."},
                required=True,
                choices={"1": 0, "2": 1, "3": 2, "4": 3}
            ),
            amount: int = SlashOption(
                name="amount",
                name_localizations={"pl": "ilość"},
                description="Choose the amount from the list.",
                description_localizations={"pl": "Wybierz ilość z listy."},
                required=True,
                choices={"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6}
            )
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['eq_b_ue']

        if slot not in [0, 1, 2, 3]:
            return

        if amount not in [1, 2, 3, 4, 5, 6]:
            return

        res = await fns.bundle_remove_item(user, amount, "equipment", int(slot))
        if res is None:
            embed = nextcord.Embed(description=text['empty_slot'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return
        else:
            if res[0] != "none":
                item = fns.get_item(res[0], 'name', cur_lan)
                embed = nextcord.Embed(
                    description=f"{text['deleted']} {res[1]} {item.displayname} {text['from_slot']} {slot + 1}\n\n**{text['current_slot']} {int(slot) + 1}:**\n{res[2]} {item.displayname}\n**{text['inventory']}:**\n+ {res[1]} {item.displayname}",
                    color=main.color_normal)
                embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
                embed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=embed)
            else:
                item = fns.get_item(res[2], 'name', cur_lan)

                embed = nextcord.Embed(
                    description=f"{text['deleted']} {res[1]} {item.displayname} {text['from_slot']} {slot + 1}\n\n**{text['current_slot']} {slot + 1}:**\n[Empty]\n**{text['inventory']}:**\n+ {res[1]} {item.displayname}",
                    color=main.color_normal)
                embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
                embed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=embed)

    @equipment_weapon.subcommand(name="equip", description="Equip weapons on different slots.", description_localizations={"pl": "Wyposaż bronie na różnych slotach."})
    async def weapon_equip(
            self,
            interaction: Interaction,
            slot: int = SlashOption(
                name="slot",
                description="Choose the slot.",
                description_localizations={"pl": "Wybierz slot."},
                required=True,
                choices={"1": 0, "2": 1, "3": 2}
            ),
            itemp: str = SlashOption(
                name="weapon",
                name_localizations={"pl": "broń"},
                description="Choose the weapon.",
                description_localizations={"pl": "Wybierz broń."},
                required=True,
            )
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['eq_w_eq']

        if slot not in [0, 1, 2]:
            return

        item = fns.get_item(itemp, "id", cur_lan)

        if item is None:
            return

        if item.toolatributes is False:
            return

        if item.toolatributes.type != "weapon":
            return

        user_weapons = await fns.get_weapons(user)

        res = await item.get_amount(user, 1)

        if res is None:
            embed = nextcord.Embed(description=text['no_weapon'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return

        playerdata = await fns.playerinfo()

        if item.sid in user_weapons:
            if item.sid != user_weapons[slot]:
                old_weapon_slot = None
                for i, weapon_name in enumerate(user_weapons):
                    if weapon_name == item.sid:
                        old_weapon_slot = i
                        break

                old_weapon = user_weapons[slot]

                playerdata[str(user.id)]['weapon_equiped'][slot] = item.sid
                playerdata[str(user.id)]['weapon_equiped'][old_weapon_slot] = old_weapon

                with open("userdb/playerdata.json", "w") as f:
                    json.dump(playerdata, f)

                old_weapon_object = fns.get_item(old_weapon, 'name', cur_lan)

                if old_weapon_object is not None:
                    embed = nextcord.Embed(description=f"{text['swapped']}:\n{old_weapon_slot + 1} - {old_weapon_object.displayname}\n{slot + 1} - {item.displayname}", color=main.color_normal)
                    embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
                    embed.set_footer(text=main.version[cur_lan])
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = nextcord.Embed(description=f"{text['equiped']} {item.displayname} {text['on_slot']} {slot + 1}.", color=main.color_normal)
                    embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
                    embed.set_footer(text=main.version[cur_lan])
                    await interaction.response.send_message(embed=embed)
                return
            else:
                embed = nextcord.Embed(description=text['already_there'], color=main.color_normal)
                embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
                embed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=embed)
                return
        else:
            playerdata[str(user.id)]["weapon_equiped"][slot] = item.sid
            with open("userdb/playerdata.json", "w") as f:
                json.dump(playerdata, f)

            embed = nextcord.Embed(description=f"{text['equiped']} {item.displayname} {text['on_slot']} {slot + 1}.", color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)

    @equipment_weapon.subcommand(name="unequip", description="Unequip weapon from selected slot.", description_localizations={"pl": "Zdejmij broń z wybranego slotu."})
    async def weapon_unequip(
            self,
            interaction: Interaction,
            slot: int = SlashOption(
                name="slot",
                description="Choose the slot.",
                description_localizations={"pl": "Wybierz slot."},
                required=True,
                choices={"1": 0, "2": 1, "3": 2}
            )
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['eq_w_ue']

        if slot not in [0, 1, 2]:
            return

        weapons = await fns.get_weapons(user)
        playerdata = await fns.playerinfo()

        if playerdata[str(user.id)]["weapon_equiped"][slot] == "none":
            embed = nextcord.Embed(description=text['empty'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return
        else:
            item = fns.get_item(weapons[slot], "name", cur_lan)
            embed = nextcord.Embed(description=f"{text['unequiped']} {item.displayname} {text['from_slot']} {slot + 1}", color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)

            playerdata[str(user.id)]["weapon_equiped"][slot] = "none"
            with open("userdb/playerdata.json", "w") as f:
                json.dump(playerdata, f)

    @bundle_equip.on_autocomplete("itemp")
    async def equipment_bundle_equip_autocomplete(self, interaction, current: str):
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        language = await fns.lang(leng)
        data = {}
        i = 0
        if not current:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.toolatributes:
                    if chk_it.toolatributes.type == "bundle":
                        i += 1
                        data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.toolartibutes:
                    if chk_it.toolatributes.type == "bundle":
                        if str(current.lower()) in chk_it.disname.lower():
                            i += 1
                            data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))

    @weapon_equip.on_autocomplete("itemp")
    async def equipment_weapon_equip_autocomplete(self, interaction, current: str):
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        language = await fns.lang(leng)
        data = {}
        i = 0
        if not current:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if 'a' not in chk_it.id:
                    if chk_it.toolatributes:
                        if chk_it.toolatributes.type == "weapon":
                            i += 1
                            data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if 'a' not in chk_it.id:
                    if chk_it.toolartibutes:
                        if chk_it.toolatributes.type == "weapon":
                            if str(current.lower()) in chk_it.disname.lower():
                                i += 1
                                data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))


def setup(client):
    client.add_cog(EquipmentCog(client))

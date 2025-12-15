import asyncio
import nextcord
from nextcord.ext import commands
import main
import random
from nextcord import Interaction, SlashOption
import functions as fns


class Workstations(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="smelt", description="Smelt items to get smelted items.", description_localizations={"pl": "Przetop przedmioty, aby zdobyć przetopione przedmioty."})
    async def smelt(
            self,
            interaction: Interaction,
            itemp: str = SlashOption(
                name="item",
                name_localizations={"pl": "przedmiot"},
                description="Choose the item.",
                description_localizations={"pl": "Wybierz przedmiot."},
                required=True,
            ),
            amount: int = SlashOption(
                name="amount",
                name_localizations={"pl": "ilość"},
                description="Choose an amount.",
                description_localizations={"pl": "Wybierz ilość."},
                choices=[1, 2, 3, 4, 5, 6],
                required=True
            ),
            fuel: str = SlashOption(
                name="fuel",
                name_localizations={"pl": "paliwo"},
                description="Choose the item.",
                description_localizations={"pl": "Wybierz przedmiot."},
                required=True,
            ),
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['smelt']

        playerinfo = await fns.playerinfo()

        furnace = fns.get_item('i001', 'id')
        has_furnace = await furnace.get_amount(user, 1)
        if has_furnace is None:
            embed = nextcord.Embed(description=text['nofurnace'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if amount not in [1, 2, 3, 4, 5, 6]:
            return

        item = await fns.get_item_with_handling(itemp, "id", cur_lan, interaction)
        if not item:
            return

        if not item.toolatributes:
            embed = nextcord.Embed(description=text['baditem'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if item.toolatributes.type != 'smeltable':
            embed = nextcord.Embed(description=text['baditem'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        fuel = fns.get_item(fuel, 'id', cur_lan)
        if fuel is None:
            embed = nextcord.Embed(description=text['badfuel'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if "a" in fuel.id or "i" in fuel.id:
            embed = nextcord.Embed(description=text['badfuel'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if fuel.sid not in ['wood', 'coal']:
            embed = nextcord.Embed(description=text['notafuel'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        for i in item.toolatributes.fuel:
            if i['fuel'] == fuel.sid:
                fuel_payload = i
                break
        else:
            embed = nextcord.Embed(description=text['tooweak'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        has_enough_item = await item.get_amount(user, amount)
        if has_enough_item is None:
            embed = nextcord.Embed(description=leng['other']["not_enough_coins"], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        has_enough_fuel = await fuel.get_amount(user, amount * fuel_payload['amount'])
        if has_enough_fuel is None:
            embed = nextcord.Embed(description=text['notenoughfuel'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if playerinfo[str(interaction.user.id)]["level"] < item.toolartibutes.lvl_required:
            embed = nextcord.Embed(description=text['level'], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        time_remaining = fuel_payload['smelt_time'] * amount

        await item.remove_item(user, amount)
        await fuel.remove_item(user, fuel_payload['amount'] * amount)

        embed = nextcord.Embed(description=f"{text['smelting']} {amount} {item}\n{text['time']}: {time_remaining}", color=main.color_normal)
        embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)
        for i in range(1, time_remaining):
            embeda = nextcord.Embed(description=f"{text['smelting']} {amount} {item}\n{text['time']}: {time_remaining - i}", color=main.color_normal)
            embeda.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embeda.set_footer(text=main.version[cur_lan])
            await asyncio.sleep(1)
            await interaction.edit_original_message(embed=embeda)

        item_smelted = fns.get_item(item.toolatributes.item_smelted, 'name', cur_lan)
        await item_smelted.add_item(user, amount * item.toolatributes.amount)

        tot = 0
        for i in range(amount):
            xp_amount = random.randint(item.toolatributes.xp_reaward[0], item.toolatributes.xp_reaward[1])
            await fns.add_xp(user, xp_amount)
            tot += xp_amount

        embedc = nextcord.Embed(description=f"{text['smelted']} {amount} {item}\n\n{text['got']}\n{amount * item.toolatributes.amount} {item_smelted}\n{tot} XP", color=main.color_normal)
        embedc.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
        embedc.set_footer(text=main.version[cur_lan])
        await interaction.edit_original_message(embed=embedc)
        return

    @smelt.on_autocomplete("itemp")
    async def smelt_autocomplete(self, interaction, current: str):
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
                    if chk_it.toolatributes.type == 'smeltable':
                        i += 1
                        data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.toolatributes:
                    if chk_it.toolatributes.type == 'smeltable':
                        if str(current.lower()) in chk_it.disname.lower():
                            i += 1
                            data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))

    @smelt.on_autocomplete("fuel")
    async def smelt2_autocomplete(self, interaction, current: str):
        """
        This thing is trash
        """
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
                if chk_it.sid in ['wood', 'coal']:
                    i += 1
                    data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.sid in ['wood', 'coal']:
                    if str(current.lower()) in chk_it.disname.lower():
                        i += 1
                        data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))


def setup(client):
    client.add_cog(Workstations(client))

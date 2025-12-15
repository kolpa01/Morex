import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import functions as fns
import main
import json
import buttons
import dropdown


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="beta", description="Join Morex Beta to test new features early.", description_localizations={"pl": "Dołącz do Morex Beta, aby móc testować nowe funkcje wcześniej."})
    async def beta(self, interaction: Interaction):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['beta']

        embed = nextcord.Embed(description=await fns.text_replacer(text['warning'], ["{main.accept}", main.accept], ["{main.deny}", main.deny]), color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
        embed.set_footer(text=main.version[cur_lan])
        view = buttons.ConfirmationButtons(180, interaction.user)
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()
        if view.value is None:
            await interaction.edit_original_message(view=None)
            return

        playerdata = await fns.playerinfo()
        if view.value is False and playerdata[str(interaction.user.id)]['beta'] == "true":
            playerdata[str(interaction.user.id)]["beta"] = "none"
            with open("userdb/playerdata.json", "w") as f:
                json.dump(playerdata, f)
            embed = nextcord.Embed(description=text['left'], color=main.color_normal)
        elif view.value is False and playerdata[str(interaction.user.id)]['beta'] == "none":
            embed = nextcord.Embed(description=text['left_failed'], color=main.color_normal)
        elif view.value is True and playerdata[str(interaction.user.id)]['beta'] == "true":
            embed = nextcord.Embed(description=text['joined_failed'], color=main.color_normal)
        else:
            playerdata[str(interaction.user.id)]["beta"] = "true"
            with open("userdb/playerdata.json", "w") as f:
                json.dump(playerdata, f)
            embed = nextcord.Embed(description=text['joined'], color=main.color_normal)

        embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
        embed.set_footer(text=main.version[cur_lan])
        await interaction.edit_original_message(embed=embed, view=None)

    @nextcord.slash_command(name="settings", description="Manage your settings.", description_localizations={"pl": "Zarządzaj swoimi ustawieniami/"})
    async def settings(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['settings']
        sete = await fns.setting()
        stats = (lambda x: main.accept if x == "enabled" else main.deny)(sete[str(user.id)]["multiplayer"])
        embed = nextcord.Embed(title=text['settings'],
                               description=f"{text['multiplayer']} {stats}",
                               color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed, view=dropdown.SettingsDropdownInitializer(360, user, user, cur_lan, leng['dropdown']['settings']))

    @nextcord.slash_command(name="set")
    async def set_parent(self, interaction: Interaction):
        pass

    @set_parent.subcommand(name="default")
    async def set_default(self, interaction: Interaction):
        pass

    @set_default.subcommand(name="dig", description="Set the default location for /dig.", description_localizations={"pl": "Wybierz domyślną lokalizację dla /dig."})
    async def set_default_dig(
            self,
            interaction: Interaction,
            place=SlashOption(
                name="place",
                name_localizations={"pl": "miejsce"},
                description="Choose the place.",
                description_localizations={"pl": "Wybierz miejsce."},
                required=True,
            )
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['sd_dig']

        place = await fns.check_location(user, place, "dig")
        if place is None or place is False:
            return
        place = fns.get_dig_locations(place, cur_lan)

        otherinfo = await fns.otherinfo()

        if place.name == otherinfo[str(user.id)]["dig_defaultlocation"]:
            embed = nextcord.Embed(description=text['exists'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return

        otherinfo[str(interaction.user.id)]["dig_defaultlocation"] = place.name
        with open("userdb/otherdatabase.json", "w") as f:
            json.dump(otherinfo, f)

        embed = nextcord.Embed(description=await fns.text_replacer(text['set'], ["{place}", place.displayname]), color=main.color_normal)
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @set_default.subcommand(name="hunt", description="Set the default location for /hunt.", description_localizations={"pl": "Wybierz domyślną lokalizację dla /hunt."})
    async def set_default_hunt(
            self,
            interaction: Interaction,
            place=SlashOption(
                name="place",
                name_localizations={"pl": "miejsce"},
                description="Choose the place.",
                description_localizations={"pl": "Wybierz miejsce."},
                required=True,
            )
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['sd_hunt']

        place = await fns.check_location(user, place, "hunt")
        if place is None or place is False:
            return
        place = fns.get_hunt_locations(place, cur_lan)

        otherinfo = await fns.otherinfo()

        if place.name == otherinfo[str(user.id)]["hunt_defaultlocation"]:
            embed = nextcord.Embed(description=text['exists'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return

        otherinfo[str(interaction.user.id)]["hunt_defaultlocation"] = place.name
        with open("userdb/otherdatabase.json", "w") as f:
            json.dump(otherinfo, f)

        embed = nextcord.Embed(description=await fns.text_replacer(text['set'], ["{place}", place.displayname]), color=main.color_normal)
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @set_default.subcommand(name="search", description="Set the default location for /search.", description_localizations={"pl": "Wybierz domyślną lokalizację dla /search."})
    async def set_default_search(
            self,
            interaction: Interaction,
            place=SlashOption(
                name="place",
                name_localizations={"pl": "miejsce"},
                description="Choose the place.",
                description_localizations={"pl": "Wybierz miejsce."},
                required=True,
            )
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['sd_search']

        place = await fns.check_location(user, place, "search")
        if place is None or place is False:
            return
        place = fns.get_search_locations(place, cur_lan)

        otherinfo = await fns.otherinfo()

        if place.name == otherinfo[str(user.id)]["search_defaultlocation"]:
            embed = nextcord.Embed(description=text['exists'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return

        otherinfo[str(interaction.user.id)]["search_defaultlocation"] = place.name
        with open("userdb/otherdatabase.json", "w") as f:
            json.dump(otherinfo, f)

        embed = nextcord.Embed(description=await fns.text_replacer(text['set'], ["{place}", place.displayname]), color=main.color_normal)
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @set_default_dig.on_autocomplete("place")
    async def set_default_dig_autocomplete(self, interaction, current: str):
        digsites = await fns.digging()
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        data = {}
        i = 0
        if not current:
            for name in digsites:
                if await fns.check_location(interaction.user, name['name'], 'dig'):
                    chk_it = fns.get_dig_locations(name['name'], leng)
                    i += 1
                    data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for name in digsites:
                if await fns.check_location(interaction.user, name['name'], 'dig'):
                    chk_it = fns.get_dig_locations(name['name'], leng)
                    if str(current.lower()) in chk_it.displayname.lower():
                        i += 1
                        data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))

    @set_default_hunt.on_autocomplete("place")
    async def set_default_hunt_autocomplete(self, interaction, current: str):
        huntlocations = await fns.huntlocations()
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        data = {}
        i = 0
        if not current:
            for name in huntlocations:
                if await fns.check_location(interaction.user, name['name'], 'hunt'):
                    chk_it = fns.get_hunt_locations(name['name'], leng)
                    i += 1
                    data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for name in huntlocations:
                if await fns.check_location(interaction.user, name['name'], 'hunt'):
                    chk_it = fns.get_hunt_locations(name['name'], leng)
                    if str(current.lower()) in chk_it.displayname.lower():
                        i += 1
                        data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))

    @set_default_search.on_autocomplete("place")
    async def set_default_search_autocomplete(self, interaction, current: str):
        search_places = await fns.places()
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        data = {}
        i = 0
        if not current:
            for name in search_places:
                if await fns.check_location(interaction.user, name['name'], 'search'):
                    chk_it = fns.get_search_locations(name['name'], leng)
                    i += 1
                    data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for name in search_places:
                if await fns.check_location(interaction.user, name['name'], 'search'):
                    chk_it = fns.get_search_locations(name['name'], leng)
                    if str(current.lower()) in chk_it.displayname.lower():
                        i += 1
                        data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))


def setup(client):
    client.add_cog(Settings(client))

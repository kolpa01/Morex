import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import functions as fns
import main
import json
import morex
import complicated_relationship


class Informations(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="announcement", description="Show the latest announcement from the creator.", description_localizations={"pl": "Wyświetl najnowsze ogłoszenie od twórcy."})
    async def announcement(self, interaction: Interaction):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['announcement']

        with open('userdb/announcements.json', "r") as f:
            language = json.load(f)

        language = language[cur_lan]['announcement']

        if language == "":
            language = text['none']

        embed = nextcord.Embed(title=text['announcement'], description=language, color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="changelog", description="Display most important changes in different versions.", description_localizations={"pl": "Wyświetl najważniejsze zmiany w różnych wersjach."})
    async def changelog(
            self,
            interaction: nextcord.Interaction,
            changelog: str = SlashOption(
                name="version",
                name_localizations={"pl": "wersja"},
                description="Choose the version (2.0, 2.0.4.6)",
                description_localizations={"pl": "Wybierz wersję (2.0, 2.0.4.6)"},
                required=True
            )
    ):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)

        if changelog not in leng['changelogs']:
            return

        embed = nextcord.Embed(title=f"Changelog {changelog}", description=leng['changelogs'][changelog], color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        button = nextcord.ui.Button(style=nextcord.ButtonStyle.link, url=f"https://kolpa01.github.io/morex/changelog/{changelog.replace('.', '-')}", label=f"Changelog {changelog}")
        view = nextcord.ui.View(timeout=180)
        view.add_item(button)
        await interaction.response.send_message(embed=embed, view=view)

    @nextcord.slash_command(name="credits", description="Special thanks to all people that are listed in this command.", description_localizations={"pl": "Specjalne podziękowania dla wszystkich osób, które są wypisane na tej komendzie."})
    async def credits(self, interaction: Interaction):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['credits']

        embed = nextcord.Embed(title=text['credits'], description=f"**{text['source']}**\nkolpa01\n\n**{text['textures']}**\nPancake\nkolpa01\n\n**{text['lore']}**\nkolpa01\nSanteMateo\n\n**{text['translation']}**\nkolpa01\n\n**{text['thanks']}**\nAMOGUS\nkolpa01\n{interaction.user.name} {text['for']}", color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])

        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="event", description="Display information about current and upcoming events.", description_localizations={"pl": "Wyświetl informacje o obecnych i nadchodzących wydarzeniach."})
    async def event(self, interaction: Interaction):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['event']

        with open('ownerdb/event.json', "r") as f:
            events_data = json.load(f)

        embeds = []
        if not events_data['events'] and not events_data['current_event']:
            embed = nextcord.Embed(title=text['event'], description=text['none'], color=main.color_normal)
            embed.set_footer(text=f"{leng['other']['pages']['page']} 0/0 | {main.version[cur_lan]}")
            await interaction.response.send_message(embed=embed)
            return
        else:
            if events_data['current_event']:
                event_obj = morex.objects.MorexEvent(events_data['current_event'], cur_lan)
                embed = nextcord.Embed(
                    title=text['event'], 
                    description=f"**{event_obj.disname}**\n<t:{event_obj.start}> - <t:{event_obj.end}>\n{event_obj.description}", 
                    color=main.color_normal
                )
                embeds.append(embed)
            for k, event_data in events_data['events'].items():
                event_obj = morex.objects.MorexEvent(event_data, cur_lan)
                embed = nextcord.Embed(
                    title=text['event'], 
                    description=f"**{event_obj.disname}**\n<t:{event_obj.start}> - <t:{event_obj.end}>\n{event_obj.description}", 
                    color=main.color_normal
                )
                embeds.append(embed)
        embed = embeds[0]
        embed.set_footer(text=f"{leng['other']['pages']['page']} 1/{len(embeds)} | {main.version[cur_lan]}")
        view = await complicated_relationship.pages_helper(embeds, interaction.user)

        await interaction.response.send_message(embed=embed, view=view)

    @nextcord.slash_command(name="ping", description="Pong!", description_localizations={"pl": "Pong!"})
    async def ping(self, interaction: Interaction):
        member = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)

        embed = nextcord.Embed(title="Ping", description=f"Pong! {round(self.client.latency*1000)} ms", color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @changelog.on_autocomplete("changelog")
    async def changelog_autocomplete(self, interaction, current: str):
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        language = await fns.lang(leng)
        data = []
        i = 0
        if not current:
            for item in language['changelogs']:
                i += 1
                data.append(item)
                if i == 24:
                    break
            await interaction.response.send_autocomplete(data)
        else:
            for item in language['changelogs']:
                if str(current.lower()) in item:
                    i += 1
                    data.append(item)
                if i == 24:
                    break
            await interaction.response.send_autocomplete(data)


def setup(client):
    client.add_cog(Informations(client))

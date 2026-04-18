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

    @nextcord.slash_command(name="announcement", description="Show the latest announcement from the creator.", description_localizations={"pl": "Wyświetl najnowsze ogłoszenie od twórcy."}, integration_types=main.integrations, contexts=main.contexts)
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

    @nextcord.slash_command(name="changelog", description="Display most important changes in different versions.", description_localizations={"pl": "Wyświetl najważniejsze zmiany w różnych wersjach."}, integration_types=main.integrations, contexts=main.contexts)
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

    @nextcord.slash_command(name="credits", description="Special thanks to all people that are listed in this command.", description_localizations={"pl": "Specjalne podziękowania dla wszystkich osób, które są wypisane na tej komendzie."}, integration_types=main.integrations, contexts=main.contexts)
    async def credits(self, interaction: Interaction):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['credits']

        embed = nextcord.Embed(title=text['credits'], description=f"**{text['source']}**\nkolpa01\n\n**{text['textures']}**\nPancake\nkolpa01\n\n**{text['lore']}**\nkolpa01\nSanteMateo\n\n**{text['translation']}**\nkolpa01\n\n**{text['thanks']}**\nAMOGUS\nkolpa01\n{interaction.user.name} {text['for']}", color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])

        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="ping", description="Pong!", description_localizations={"pl": "Pong!"}, integration_types=main.integrations, contexts=main.contexts)
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

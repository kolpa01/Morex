import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import main
import functions as fns
import json
import buttons


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="help", description="Show all available commands.", description_localizations={"pl": "Wyświetl wszystkie dostępne komendy"}, integration_types=main.integrations, contexts=main.contexts)
    async def help(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['help']
# {cur_lan}
        with open(f"ownerdb/{cur_lan}.json", "r") as f:
            pages = json.load(f)

        embeds = []

        texts = []
        for i, page in enumerate(pages, 1):
            texts.append(page)
            if i % 5 == 0:
                embed = nextcord.Embed(title=text['help'], description="\n\n".join(texts), color=main.color_normal)
                texts = []
                embeds.append(embed)
            if i == len(pages) and not i % 5 == 0:
                embed = nextcord.Embed(title=text['help'], description="\n\n".join(texts), color=main.color_normal)
                texts = []
                embeds.append(embed)

        lenght = len(embeds)
        embed = embeds[0]
        embed.set_footer(text=f"{leng['other']['pages']['page']} 1/{lenght} | {main.version[cur_lan]}")
        # view = nextcord.ui.View(timeout=160)
        # view.add_item(nextcord.ui.Button(style=nextcord.ButtonStyle.url, url="https://discord.gg/NtNAwHD6fp", label="jajco"))
        await interaction.response.send_message(embed=embeds[0], view=buttons.Pages(60, lenght, embeds, user, main.version[cur_lan], leng['other']['pages']['page'], leng))


def setup(client):
    client.add_cog(Help(client))

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import functions as fns
import main


class DevTools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="dev", guild_ids=[927971482448060477, 1222203197834399794, 1198437946810974258, 1132073153510789292])
    async def dev_tools(self, interaction: Interaction):
        pass

    @dev_tools.subcommand(name="embed")
    async def embed_cmd(
            self,
            interaction: Interaction,
            title: str = SlashOption(required=False),
            desc: str = SlashOption(required=False),
            clr: str = SlashOption(required=False),
            fields: str = SlashOption(required=False),
            thumbnail: str = SlashOption(required=False),
            footer: str = SlashOption(required=False),
            lang: str = SlashOption(required=False, choices=["pl", "en"]),
    ):
        if clr is None:
            color = main.color_normal
        else:
            color = int(clr[1:], 16)
        if not lang:
            lang = "en"
        if desc:
            desc = await fns.text_formatting_battle(desc, interaction.user, "{e}", lang)
            desc = desc.replace("\\n", "\n")
        embed = nextcord.Embed(title=title, description=desc, color=color)
        if fields:
            for i in fields.split(";"):
                a = i.split(",")
                a[1] = await fns.text_formatting_battle(a[1], interaction.user, "{e}", lang)
                a[1] = a[1].replace("\\n", "\n")
                embed.add_field(name=a[0], value=a[1], inline=False)
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=footer)
        await interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(DevTools(client))

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import functions as fns
import main
import json


class Skills(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="skills")
    async def skills(self, interaction):
        pass

    @skills.subcommand(name="view", description="Show user's skills.", description_localizations={"pl": "Wyświetl umiejętności użytkownika."})
    async def skills_view(
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
            user = await fns.firsttime(interaction.user)
            cur_lan = await fns.get_lang(user)
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
            user = aa[1]

        leng = await fns.lang(cur_lan)
        text = leng['commands']['skills_view']

        skillz = await fns.skillz()
        otherinfo = await fns.otherinfo()

        embed = nextcord.Embed(description=f"{otherinfo[str(user.id)]['skillpoint']} {main.skillpoint}", color=main.color_normal)

        for k, v in skillz[str(user.id)].items():
            if k == 'rob':
                maxi = 10
            else:
                maxi = 20
            bar = await fns.progress_bar(v, maxi)

            if k == 'hp':
                info = f"+{v*5} HP"
            else:
                info = f"+0 [Empty]"

            embed.add_field(name=text[k], value=f"{bar} {v}/{maxi} {main.skillpoint}\n{info}", inline=False)

        empty_bar = await fns.progress_bar(0, 1)
        embed.add_field(name=text['soon'], value=f"{empty_bar} 0/10 {main.skillpoint}\n+0 [Empty]", inline=False)
        embed.add_field(name=text['soon'], value=f"{empty_bar} 0/20 {main.skillpoint}\n+0 [Empty]", inline=False)

        embed.set_author(name=f"{text['title']} {user.name}", icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])

        await interaction.response.send_message(embed=embed)

    @skills.subcommand(name='change', description="Raise certain Skill level.", description_localizations={"pl": "Zwiększ poziom wybranej umiejętności."})
    async def skills_raise(
        self,
        interaction: Interaction,
        skill=SlashOption(
            name="skill",
            name_localizations={"pl": "umiejętność"},
            description="Select a skill.",
            description_localizations={"pl": "Wybierz umiejętność."},
            choices={
                "HP": "hp"
            },
            choice_localizations={
                "pl": {"HP": "hp"}
            },
            required=True
        ),
        amount: str = SlashOption(
            name="amount",
            name_localizations={"pl": "ilość"},
            description="Choose an amount. (25, 3, all)",
            description_localizations={"pl": "Wybierz ilość. (25, 3, all)"},
            required=True
        )
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['skills_change']

        if skill != 'hp':
            return

        otherinfo = await fns.otherinfo()

        try:
            amount = int(amount)
            if amount > 20 or amount < 1:
                embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
                embed.set_author(name=user.name, icon_url=user.display_avatar.url)
                embed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        except ValueError:
            if amount == 'all':
                amount = otherinfo[str(user.id)]['skillpoint']
                if amount == 0:
                    embed = nextcord.Embed(description=text['notenough'], color=main.color_normal)
                    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
                    embed.set_footer(text=main.version[cur_lan])
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
            else:
                embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
                embed.set_author(name=user.name, icon_url=user.display_avatar.url)
                embed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

        skillz = await fns.skillz()

        add_amount = 20 - skillz[str(user.id)][skill]
        if amount >= add_amount:
            amount = add_amount

        if amount == 0:
            embed = nextcord.Embed(description=text['already_full'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if amount > otherinfo[str(user.id)]['skillpoint']:
            amount = otherinfo[str(user.id)]['skillpoint']

        if amount == 0:
            embed = nextcord.Embed(description=text['notenough'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        otherinfo[str(user.id)]['skillpoint'] -= amount
        with open('userdb/otherdatabase.json', "w") as f:
            json.dump(otherinfo, f)

        await fns.update_skill(user, skill, amount, 20)

        embed = nextcord.Embed(description=f"{text['raised']} {amount}.", color=main.color_normal)
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(Skills(client))

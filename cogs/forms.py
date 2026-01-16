import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import functions as fns
import main
import json


class RateModal(nextcord.ui.Modal):
    def __init__(self, user, channel, texts, rep):
        super().__init__(
            rep
        )

        self.place = nextcord.ui.TextInput(label=texts[0], min_length=10, max_length=4000, required=True, placeholder=texts[1])
        self.add_item(self.place)
        self.user = user
        self.channel = channel

    async def callback(self, interaction: Interaction) -> None:
        embed = nextcord.Embed(title=f"Od {self.user.name}", description=self.place.value)
        await self.channel.send(embed=embed)


class BugReport(nextcord.ui.Modal):
    def __init__(self, user, channel, texts, rep):
        super().__init__(
            rep,
        )

        self.place = nextcord.ui.TextInput(label=texts[0], min_length=1, max_length=128, required=True, placeholder=texts[4])
        self.add_item(self.place)
        self.placeb = nextcord.ui.TextInput(label=texts[1], min_length=10, max_length=1024, required=True, placeholder=texts[5])
        self.add_item(self.placeb)
        self.placea = nextcord.ui.TextInput(label=texts[2], min_length=10, max_length=4000, required=False, placeholder=texts[5])
        self.add_item(self.placea)
        self.placec = nextcord.ui.TextInput(label=texts[3], min_length=10, max_length=4000, required=False, placeholder=texts[5])
        self.add_item(self.placec)
        self.user = user
        self.channel = channel

    async def callback(self, interaction: Interaction) -> None:
        embed = nextcord.Embed(title=f"From {self.user.name} ({self.user.id})", color=main.color_normal)
        embed.add_field(name="Which system broke", value=self.place.value, inline=False)
        embed.add_field(name="What's the incorrect behavior", value=self.placeb.value, inline=False)
        embed.add_field(name="Steps to reproduce", value=self.placea.value, inline=False)
        embed.add_field(name="Other Informations", value=self.placec.value, inline=False)
        embed.set_footer(text=main.version['en'])
        await self.channel.send(embed=embed)


class RedeemModal(nextcord.ui.Modal):
    def __init__(self, user, channel, texts, rep):
        super().__init__(
            rep
        )

        self.place = nextcord.ui.TextInput(label=texts[0], min_length=3, max_length=20, required=True, placeholder=texts[1])
        self.add_item(self.place)
        self.user = user
        self.channel = channel

    async def callback(self, interaction: Interaction) -> None:
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        golden = leng['commands']['redeem']
        with open('ownerdb/codes.json', "r") as f:
            codes = json.load(f)
        try:
            the_thing = codes[self.place.value]
        except KeyError:
            embed = nextcord.Embed(description=golden['invalid'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if str(self.user.id) in the_thing['users']:
            embed = nextcord.Embed(description=golden['fail'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        the_thing['users'].append(str(self.user.id))
        with open('ownerdb/codes.json', "w") as f:
            json.dump(codes, f)

        text = []
        text = await fns.rewards(self.user, the_thing['rewards'])
        embed = nextcord.Embed(title=golden['redeemed'], description=f"{golden['got']}\n{text}", color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)


class Forms(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="bug", integration_types=main.integrations, contexts=main.contexts)
    async def bug(self, interaction: Interaction):
        pass

    @bug.subcommand(name="report", description="Report bugs to the developer.", description_localizations={"pl": "Zgłoś błędy do dewelopera."})
    async def bug_report(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['modals']['bug']

        channel = self.client.get_channel(1128664371342618674)
        await interaction.response.send_modal(BugReport(user=user, channel=channel, texts=[text['what'], text['define'], text['replica'], text['other'], text['sys'], text['write']], rep=text['report']))

    @nextcord.slash_command(name="rate", description="Rate the bot.", description_localizations={"pl": "Oceń bota."}, integration_types=main.integrations, contexts=main.contexts)
    async def rate(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['modals']['rate']

        channel = self.client.get_channel(1098283249446440981)
        await interaction.response.send_modal(RateModal(user=user, channel=channel, texts=[text['content'], text['write']], rep=text['opinion']))

    @nextcord.slash_command(name="redeem", description="Type codes to get free items.", description_localizations={"pl": "Wpisz kody, aby zdobyć darmowe przedmioty."}, integration_types=main.integrations, contexts=main.contexts)
    async def reedem(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['modals']['redeem']

        channel = self.client.get_channel(1098283249446440981)
        await interaction.response.send_modal(RedeemModal(user=user, channel=channel, texts=[text['label'], text['placeholder']], rep=text['title']))


def setup(client):
    client.add_cog(Forms(client))

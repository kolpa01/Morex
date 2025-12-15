import nextcord
from nextcord.ext import commands
import functions as fns
import main
from nextcord import Interaction, SlashOption


class Leaderboards(commands.Cog):
    def __init__(self, client):
        self.client = client     

    async def get_leaderboard(self, stat):
        users = await fns.playerinfo()
        leader_board = {}
        for user_id, user_details in users.items():
            if user_id == 1:
                continue
            if stat == "all":
                total_amount = user_details["wallet"] + user_details["bank"]
            else:
                total_amount = user_details[stat]
            leader_board[user_id] = total_amount

        leader_board = dict(sorted(leader_board.items(), key=lambda item: item[1], reverse=True))

        return leader_board

    @nextcord.slash_command(name="leaderboard")
    async def leaderboards(self, interaction: Interaction):
        pass

    @leaderboards.subcommand(name="coins", description="View users with most coins.", description_localizations={"pl": "Zobacz użytkowników z największą ilością monet."})
    async def lb_coins(
        self,
        interaction: Interaction,
        mode=SlashOption(
            name="type",
            name_localizations={"pl": "statystyka"},
            description="Choose the type of leaderboards.",
            description_localizations={"pl": "Wybierz rodzaj tabeli wyników."},
            required=True,
            choices={"All": "all", "Wallet": "wallet", "Bank": "bank"},
            choice_localizations={"pl": {"All": "all", "Wallet": "wallet", "Bank": "bank"}}
        )
    ):

        await interaction.response.defer()
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['leaderboards_coins']

        embed = nextcord.Embed(title=text[mode], color=main.color_normal)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1134067893840126012/1146845224321171486/coin.png")
        leader_board = await self.get_leaderboard(mode)
        index = 1
        for user_id, amount in leader_board.items():
            member = await self.client.fetch_user(int(user_id))
            if member is None:
                name = "???"
            else:
                name = member.name
            embed.add_field(name=f"{index}. {name}", value=f"{amount} {main.coin}", inline=False)
            if index == 10:
                break
            else:
                index += 1
        embed.set_footer(text=f"{text['position']} #{list(leader_board).index(str(interaction.user.id)) + 1} | {main.version[cur_lan]}")

        await interaction.followup.send(embed=embed)

    @leaderboards.subcommand(name="xp", description="View users with most XP.", description_localizations={"pl": "Zobacz użytkowników z największą ilością XP."})
    async def lb_level(
        self,
        interaction: Interaction
    ):

        await interaction.response.defer()
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['leaderboards_xp']

        embed = nextcord.Embed(title=text['all'], color=main.color_normal)
        leader_board = await self.get_leaderboard('total_xp')
        index = 1
        for user_id, amount in leader_board.items():
            member = await self.client.fetch_user(int(user_id))
            if member is None:
                name = "???"
            else:
                name = member.name
            embed.add_field(name=f"{index}. {name}", value=f"{amount // 100} LV | {amount} XP", inline=False)
            if index == 10:
                break
            else:
                index += 1
        embed.set_footer(text=f"{text['position']} #{list(leader_board).index(str(interaction.user.id)) + 1} | {main.version[cur_lan]}")

        await interaction.followup.send(embed=embed)
            
    
def setup(client):
    client.add_cog(Leaderboards(client))

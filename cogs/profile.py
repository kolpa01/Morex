import nextcord
from nextcord.ext import commands
import dropdown
import main
from nextcord import Interaction, SlashOption
import functions as fns


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="profile", description="Shows user's profile", description_localizations={"pl": "Wyświetla profil użytkownika."}, integration_types=main.integrations, contexts=main.contexts)
    async def profile(
            self,
            interaction: Interaction,
            osoba: nextcord.Member = SlashOption(
                name="member",
                name_localizations={"pl": "osoba"},
                description="Select a member.",
                description_localizations={"pl": "Wybierz osobę."},
                required=False
            )):
        if osoba is None:
            user = await fns.firsttime(interaction.user)
            cur_lan = await fns.get_lang(user)
        else:
            aa = await fns.firsttime(interaction.user, osoba)
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
        text = leng['commands']['profile']

        users = await fns.playerinfo()

        display_avatar = user.display_avatar.url
        badges = await fns.get_user_badges(user)
        icon = await fns.player_icon(user)

        wallet = users[str(user.id)]["wallet"]
        bank = users[str(user.id)]["bank"]
        exp = users[str(user.id)]["xp"]
        totexp = users[str(user.id)]["total_xp"]
        level = users[str(user.id)]["level"]
        vver = users[str(user.id)]["version"]
        dat = users[str(user.id)]["timestamp"]

        premium = (lambda x: main.accept if x == "true" else main.deny)(users[str(user.id)]["premium"])
        beta = (lambda x: main.accept if x == "true" else main.deny)(users[str(user.id)]["beta"])
        banned = (lambda x: main.deny if x == "none" else main.accept)(users[str(user.id)]["banned"])

        embed = nextcord.Embed(title=f"{text['profile']} {user.name}",
                               description=f"{badges}\n\n**{text['general']}**\n{wallet + bank} {main.coin}\n{level} {text['level']} | {exp}/100\n{totexp} XP\n\n**{text['creation']}** {vver}\n<t:{dat}>\n\n**{text['status']} {icon}**\nPremium: {premium}\nBeta: {beta}\n{text['banned']} {banned}",
                               color=main.color_normal)
        embed.set_thumbnail(url=display_avatar)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed, view=dropdown.ProfileDropdownInitializer(180, user, interaction.user, cur_lan, leng['dropdown']['profile']))


def setup(client):
    client.add_cog(Profile(client))

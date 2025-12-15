import nextcord
from nextcord.ext import commands
import main
import buttons
from nextcord import Interaction, SlashOption
import functions as fns


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="fight", description="Fight with different users using your weapons.", description_localizations={"pl": "Zawalcz z innymi osobami swoimi własnymi broniami."})
    async def fight(
            self,
            interaction: Interaction,
            osoba: nextcord.Member = SlashOption(
                name="member",
                name_localizations={"pl": "osoba"},
                description="Select a member.",
                description_localizations={"pl": "Wybierz osobę."},
                required=True
            ),
            mode=SlashOption(
                name="mode",
                name_localizations={"pl": "tryb"},
                description="Choose the battle mode.",
                description_localizations={"pl": "Wybierz tryb walki."},
                choices={"Classic": "classic"},
                choice_localizations={"pl": {"Klasyczny": "classic"}},
                required=True
            )
    ):
        aa = await fns.firsttime(interaction.user, osoba)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['fight']
        if aa is False:
            await fns.no_account(interaction, cur_lan)
            return
        elif aa == "mperr":
            await fns.mperr(interaction, cur_lan)
            return
        elif aa == "pmerr":
            await fns.pmerr(interaction, cur_lan)
            return
        user = aa[0]
        member = aa[1]

        if member.bot:
            return

        if member == user:
            return

        errorembed = nextcord.Embed(description=text['no_weapon'], color=main.color_normal)
        errorembed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
        errorembed.set_footer(text=main.version[cur_lan])

        errorembed2 = nextcord.Embed(description=text['user_weapon'], color=main.color_normal)
        errorembed2.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
        errorembed2.set_footer(text=main.version[cur_lan])

        errorembed3 = nextcord.Embed(description=text['both_weapon'], color=main.color_normal)
        errorembed3.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
        errorembed3.set_footer(text=main.version[cur_lan])

        if mode == "classic":
            user_weapon = await fns.get_weapon(user)
            member_weapon = await fns.get_weapon(member)

            if user_weapon is False and member_weapon is False:
                await interaction.response.send_message(embed=errorembed3)
                return
            elif user_weapon is False and member_weapon is True:
                await interaction.response.send_message(embed=errorembed)
                return
            elif user_weapon is True and member_weapon is False:
                await interaction.response.send_message(embed=errorembed2)
                return

            user_weapon = fns.get_item(user_weapon, 'name', cur_lan)
            member_weapon = fns.get_item(member_weapon, 'name', cur_lan)

            confirmationui = buttons.ConfirmationButtons(30, member)

            embed = nextcord.Embed(title=text['challenge'], description=f"{user.name} {text['challenges']}", color=main.color_normal)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(content=f"<@{member.id}>", embed=embed, view=confirmationui)
            await confirmationui.wait()

            if confirmationui.value is None or confirmationui.value is False:
                await interaction.edit_original_message(content=None, view=None)
                return

            ico1 = await fns.player_icon(user)
            ico2 = await fns.player_icon(member)
            u_hp = await fns.get_user_hp(user)
            e_hp = await fns.get_user_hp(member)

            pbar = await fns.progress_bar(1, 1)

            embed = nextcord.Embed(title=text['fight'], color=main.color_normal)
            embed.add_field(name=f"{ico1} {user.name}", value=f"{pbar} {u_hp}/{u_hp} HP\n0 SH", inline=False)
            embed.add_field(name=f"{ico2} {member.name}", value=f"{pbar} {e_hp}/{e_hp} HP\n0 SH", inline=False)
            embed.add_field(name=text['info'], value=await fns.text_replacer(text['chall'], ["{u}", user.name], ["{e}", member.name]), inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1198440482087379054/1220427058623156285/aaaa.aaaa.png")
            embed.set_footer(text=main.version[cur_lan])

            view = buttons.FightButtons(60, {"hp": u_hp, "user": user, "weapon": user_weapon, "icon": ico1}, {"hp": e_hp, "user": member, "weapon": member_weapon, "icon": ico2}, "classic", cur_lan, text)
            view.second_cancel.disabled = True
            view.second_defence2.disabled = True
            view.second_fight.disabled = True
            view.second_power.disabled = True
            if user_weapon.toolatributes.itemtype != "spellbook":
                view.powerb.disabled = True
            await interaction.edit_original_message(content=None, embed=embed, view=view)


def setup(client):
    client.add_cog(Games(client))

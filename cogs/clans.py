import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import main
import functions as fns
import buttons
import json
import uuid
import modals


class Clans(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def get_clans(self):
        with open("userdb/clans.json") as f:
            clans = json.load(f)

        return clans

    async def add_clan(self, user, clan_data):
        clans_data = await self.get_clans()

        clan_id = str(uuid.uuid4())
        clans_data[str(clan_id)] = clan_data

        with open("userdb/clans.json", "w") as f:
            json.dump(clans_data, f)

        relationships = await fns.u_relationships()
        relationships[str(user.id)]["clan"] = clan_id

        with open("userdb/relationships.json", "w") as f:
            json.dump(relationships, f)

    async def buy_clan(self, user, clan_data):
        user = await fns.isdebug(user)
        playerdata = await fns.playerinfo()

        cost = 500000

        if playerdata[str(user.id)]['wallet'] < cost:
            return False

        await fns.update_bank(user, cost * -1, "wallet")

        await self.add_clan(user, clan_data)

        return True

    async def can_buy_clan(self, interaction, user, text, cur_lan, msg=None, edit_mode=False):
        playerdata = await fns.playerinfo()
        wallet = playerdata[str(user.id)]["wallet"]

        if wallet < 500000:
            cost = 500000 - wallet
            no_coins = await fns.text_replacer(text["no_coins0"], ["{cost}", cost], ["{coin}", main.coin])
            if playerdata[str(user.id)]["bank"] >= cost:
                embed = nextcord.Embed(description=f"{no_coins}\n\n{text["no_coins1"]}", color=main.color_normal)
            else:
                embed = nextcord.Embed(description=no_coins, color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            if edit_mode:
                await msg.edit(embed=embed, view=None)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    @nextcord.slash_command(name="clans", integration_types=main.integrations, contexts=main.contexts)
    async def clans(self, interaction: Interaction):
        pass

    @clans.subcommand(name="create", description="Create your own clan.", description_localizations={"pl": "Stwórz swój własny klan."})
    async def clans_create(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['clans']

        relationships = await fns.u_relationships()
        current_clan = relationships[str(user.id)]["clan"]
        
        if current_clan:
            embed = nextcord.Embed(description=text["already_in"], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if not await self.can_buy_clan(interaction, user, text, cur_lan):
            return
    
        modal = modals.ClanCreationModal(user, leng, cur_lan)
        await interaction.response.send_modal(modal)
        await modal.wait()
        if not modal.can_proceed:
            return
        clan_data = modal.clan_data

        view = buttons.ConfirmationButtons(60, user)
        embed = nextcord.Embed(description=await fns.text_replacer(text['confirmation'], ['{clan}', clan_data["name"]], ['{cost}', 500000], ['{coin}', main.coin]), color=main.color_normal)
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        msg = await interaction.followup.send(embed=embed, view=view)
        await view.wait()
        if view.value is False or view.value is None:
            await msg.edit(view=None)
            return

        relationships = await fns.u_relationships()
        current_clan = relationships[str(user.id)]["clan"]
        if current_clan:
            embed = nextcord.Embed(description=text["already_in"], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await msg.edit(embed=embed, view=None)
            return

        res = await self.buy_clan(user, clan_data)

        if not res:
            await self.can_buy_clan(interaction, user, text, cur_lan, msg, True)
            return

        embed = nextcord.Embed(description=await fns.text_replacer(text["bought"], ["{clan}", clan_data["name"]]), color=main.color_normal)
        embed.set_author(name=user.name, icon_url=str(user.display_avatar))
        embed.set_footer(text=main.version[cur_lan])
        await msg.edit(embed=embed, view=None)


def setup(client):
    client.add_cog(Clans(client))

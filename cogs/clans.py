import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import main
import functions as fns
import buttons
import json
import uuid
import modals
from autocompletes import clan_autocompletes


class Clans(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def add_clan(self, user, clan_data):
        clans_data = await fns.get_clans()

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

    @clans.subcommand(name="join", description="Join someone's clan.", description_localizations={"pl": "Dołącz do czyjegoś klanu."})
    async def clans_join(
        self, 
        interaction: Interaction,
        clan_uuid: str = SlashOption(
            name="clan",
            name_localizations={"pl": "klan"},
            description="Choose the clan.",
            description_localizations={"pl": "Wybierz klan."},
            required=True,
        )
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['clans']

        relationships = await fns.u_relationships()
        current_clan = relationships[str(user.id)]["clan"]
        
        if current_clan:
            embed = nextcord.Embed(description=text["already_joined"], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        player_data = await fns.playerinfo()
        all_clans = await fns.get_clans()
        if clan_uuid not in all_clans:
            embed = nextcord.Embed(description=text["fake"], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        clan_data = all_clans[clan_uuid]
        if clan_data["level_required"] > player_data[str(user.id)]["level"]:
            embed = nextcord.Embed(description=text["no_level"], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if len(clan_data["members"]) >= clan_data["member_limit"]:
            embed = nextcord.Embed(description=text["full"], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        relationships[str(user.id)]["clan"] = clan_uuid

        with open("userdb/relationships.json", "w") as f:
            json.dump(relationships, f)

        all_clans[clan_uuid]["members"].append(str(user.id))

        with open("userdb/clans.json", "w") as f:
            json.dump(all_clans, f)

        embed = nextcord.Embed(description=await fns.text_replacer(text["joined"], ["{clan}", clan_data["name"]]), color=main.color_normal)
        embed.set_author(name=user.name, icon_url=str(user.display_avatar))
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @clans.subcommand(name="leave", description="Leave your current clan.", description_localizations={"pl": "Odejdź ze swojego obecnego klanu."})
    async def clans_leave(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['clans']

        relationships = await fns.u_relationships()
        current_clan = relationships[str(user.id)]["clan"]
        
        if not current_clan:
            embed = nextcord.Embed(description=text["not_in_clan"], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        all_clans = await fns.get_clans()
        clan_data = all_clans[relationships[str(user.id)]["clan"]]
        uuid = relationships[str(user.id)]["clan"]
        if clan_data["owner"] == str(user.id):
            embed = nextcord.Embed(description=text["is_owner"], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        relationships[str(user.id)]["clan"] = None

        with open("userdb/relationships.json", "w") as f:
            json.dump(relationships, f)

        all_clans[uuid]["members"].remove(str(user.id))

        with open("userdb/clans.json", "w") as f:
            json.dump(all_clans, f)

        embed = nextcord.Embed(description=await fns.text_replacer(text["left"], ["{clan}", clan_data["name"]]), color=main.color_normal)
        embed.set_author(name=user.name, icon_url=str(user.display_avatar))
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @clans_join.on_autocomplete("clan_uuid")
    async def clans_join_autocomplete(self, interaction, current: str):
        data = await clan_autocompletes.all_clans(interaction.user, current)
        await interaction.response.send_autocomplete(data)


def setup(client):
    client.add_cog(Clans(client))

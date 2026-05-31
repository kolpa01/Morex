import nextcord
from nextcord.ext import commands
import main
from nextcord import Interaction, SlashOption
from uuid import uuid4
import functions as fns
import buttons
import json
import complicated_relationship
from autocompletes import proposal_autocompletes
import datetime


MARRIAGE_REQ_LIMIT = 10


class Marriage(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def can_send_proposal(self, interaction, user, member, text, cur_lan, edit_mode):
        relationships = await fns.u_relationships()
        if len(relationships[str(user.id)]["marriages"]) >= relationships[str(user.id)]["marriage_slots"]:
            embed = nextcord.Embed(description=text["no_slots"], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            if edit_mode:
                await interaction.edit_original_message(embed=embed, view=None)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            return False

        if len(relationships[str(member.id)]["marriages"]) >= relationships[str(member.id)]["marriage_slots"]:
            embed = nextcord.Embed(description=text["no_member_slots"], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            if edit_mode:
                await interaction.edit_original_message(embed=embed, view=None)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            return False

        if str(member.id) in relationships[str(user.id)]["marriages"]:
            embed = nextcord.Embed(description=text["already_married"], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False

        if len(relationships[str(user.id)]["marriage_sent"]) >= MARRIAGE_REQ_LIMIT:
            embed = nextcord.Embed(description=text["too_much_requests"], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            if edit_mode:
                await interaction.edit_original_message(embed=embed, view=None)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            return False

        if len(relationships[str(member.id)]["marriage_received"]) >= MARRIAGE_REQ_LIMIT:
            embed = nextcord.Embed(description=text["too_member_requests"], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            if edit_mode:
                await interaction.edit_original_message(embed=embed, view=None)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            return False

        for req, req_id in relationships[str(user.id)]["marriage_sent"].items():
            if req_id == member.id:
                embed = nextcord.Embed(description=text["already_sent"], color=main.color_normal)
                embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
                embed.set_footer(text=main.version[cur_lan])
                if edit_mode:
                    await interaction.edit_original_message(embed=embed, view=None)
                else:
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                return False

        for req, req_id in relationships[str(member.id)]["marriage_sent"].items():
            if req_id == user.id:
                embed = nextcord.Embed(description=text["already_member_sent"], color=main.color_normal)
                embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
                embed.set_footer(text=main.version[cur_lan])
                if edit_mode:
                    await interaction.edit_original_message(embed=embed, view=None)
                else:
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                return False

        return True

    @nextcord.slash_command(name="marriage", integration_types=main.integrations, contexts=main.contexts)
    async def marriage(self, interaction: Interaction):
        pass

    @marriage.subcommand(name="propose", description="Propose to any user with an engagement ring.", description_localizations={"pl": "Oświadcz się danemu użytkownikowi za pomocą pierścionka zaręczynowego."})
    async def marriage_propose(
        self, 
        interaction: Interaction,
        member: nextcord.Member = SlashOption(
            name="member",
            name_localizations={"pl": "osoba"},
            description="Select a member.",
            description_localizations={"pl": "Wybierz osobę."},
        )
    ):
        aa = await fns.firsttime(interaction.user, member)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['marriage']
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

        if not await self.can_send_proposal(interaction, user, member, text, cur_lan, False):
            return
        
        ring = fns.get_item("placeholder", "name", cur_lan)
        res = await ring.get_amount(user, 1)
        if res is None:
            embed = nextcord.Embed(description=f"{text['dont_have']}{ring}\n{text["try_again"]}", color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = nextcord.Embed(description=await fns.text_replacer(text["confirmation"], ["{u}", f"<@{member.id}>"], ["{item}", ring]), color=main.color_normal)
        embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        view = buttons.ConfirmationButtons(60, user)
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()
        if view.value is None or view.value is False:
            await interaction.edit_original_message(view=None)
            return

        amount = await ring.get_amount(user, 1)
        if amount is None:
            await interaction.edit_original_message(view=None)
            return

        proposal_identifier = str(uuid4())
        if not await self.can_send_proposal(interaction, user, member, text, cur_lan, True):
            return

        relationships = await fns.u_relationships()

        relationships[str(user.id)]["marriage_sent"].update({proposal_identifier: member.id})
        relationships[str(member.id)]["marriage_received"].update({proposal_identifier: user.id})

        with open("userdb/relationships.json", "w") as f:
            json.dump(relationships, f)

        await ring.remove_item(user, 1)

        embed = nextcord.Embed(description=await fns.text_replacer(text["sent"], ["{u}", f"<@{member.id}>"]), color=main.color_normal)
        embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.edit_original_message(embed=embed, view=None)

    @marriage.subcommand(name="accept", description="Accept someone's marriage proposal.", description_localizations={"pl": "Zaakceptuj czyjeś oświadczyny."})
    async def marriage_accept(
        self,
        interaction: Interaction,
        proposal: str = SlashOption(
            name="proposal",
            name_localizations={"pl": "oświadczyny"},
            description="Choose the proposal.",
            description_localizations={"pl": "Wybierz oświadczyny."},
            required=True,
        ),
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['marriage']

        relationships = await fns.u_relationships()

        if proposal not in relationships[str(user.id)]["marriage_received"]:
            return

        member = await self.client.fetch_user(relationships[str(user.id)]["marriage_received"][proposal])

        if len(relationships[str(user.id)]["marriages"]) >= relationships[str(user.id)]["marriage_slots"]:
            embed = nextcord.Embed(description=text["no_slots"], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False

        if len(relationships[str(member.id)]["marriages"]) >= relationships[str(member.id)]["marriage_slots"]:
            embed = nextcord.Embed(description=text["no_member_slots"], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False

        if str(member.id) in relationships[str(user.id)]["marriages"]:
            embed = nextcord.Embed(description=text["already_married"], color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False

        day = datetime.datetime.now().timestamp()
        timestamp = round(day, None)

        relationships[str(member.id)]["marriage_sent"].pop(proposal)
        relationships[str(user.id)]["marriage_received"].pop(proposal)

        relationships[str(user.id)]["marriages"].update({str(member.id): {"since": timestamp}})
        relationships[str(member.id)]["marriages"].update({str(user.id): {"since": timestamp}})

        with open("userdb/relationships.json", "w") as f:
            json.dump(relationships, f)

        embed = nextcord.Embed(description=await fns.text_replacer(text["married"], ["{u}", f"<@{member.id}>"]), color=main.color_normal)
        embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @marriage.subcommand(name="decline")
    async def marriage_decline(
            self, 
            interaction: Interaction
    ):
        pass

    @marriage.subcommand(name="divorce")
    async def marriage_divorce(self, interaction: Interaction):
        pass

    @marriage.subcommand(name="requests", description="Show all of your marriage proposals.", description_localizations={"pl": "Wyświetl wszystkie swoje oświadczyny."})
    async def marriage_requests(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['marriage']

        relationships = await fns.u_relationships()

        requests = []
        counter = 1
        for uuid, user_id in relationships[str(user.id)]["marriage_sent"].items():
            requests.append(f"**{counter} - <@{user_id}> ({await self.client.fetch_user(user_id)})**\n{uuid}")
            counter += 1

        if requests:
            description = text["proposals_sent"] + "\n" + "\n".join(requests)
        else:
            description = text["no_proposals_sent"]

        embed = nextcord.Embed(description=description, color=main.color_normal)
        embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])

        received = []
        counter = 1
        for uuid, user_id in relationships[str(user.id)]["marriage_received"].items():
            received.append(f"**{counter} - <@{user_id}> ({await self.client.fetch_user(user_id)})**\n{uuid}")
            counter += 1

        if received:
            description = text["proposals_received"] + "\n" + "\n".join(received)
        else:
            description = text["no_proposals_received"]

        embed2 = nextcord.Embed(description=description, color=main.color_normal)
        embed2.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
        embed2.set_footer(text=f"{leng['other']['pages']['page']} 1/2 | {main.version[cur_lan]}")

        view = await complicated_relationship.pages_helper([embed2, embed], user)
        await interaction.response.send_message(embed=embed2, view=view)

    @marriage_accept.on_autocomplete("proposal")
    async def marriage_accept_autocomplete(self, interaction, current: str):
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            await interaction.response.send_autocomplete({})
            return

        data = await proposal_autocompletes.all_received(interaction.user, self.client, current)
        await interaction.response.send_autocomplete(data)


def setup(client):
    client.add_cog(Marriage(client))

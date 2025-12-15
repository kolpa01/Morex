import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import functions as fns
import complicated_relationship


class Hunting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="hunt", description="Grab your weapon and go hunt some enemies.", description_localizations={"pl": "Weź swoją broń i pójdź polować na wrogów."})
    async def hunt(
            self,
            interaction: Interaction,
            place=SlashOption(
                name="place",
                name_localizations={"pl": "miejsce"},
                description="Choose the place.",
                description_localizations={"pl": "Wybierz miejsce."},
                required=False,
            )
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)

        place = await fns.check_location(user, place, "hunt")
        if place is None or place is False:
            return
        place = fns.get_hunt_locations(place, cur_lan)

        if place.name == "training_arena":
            if await fns.has_event(user, "beatgirl"):
                return
            if await fns.has_event(user, "metguywithweirdname"):
                if not await fns.has_event(user, 'lazy'):
                    await complicated_relationship.init_dialogues(interaction, cur_lan, "v2_hunt_tutorial")
                    return
                await complicated_relationship.init_dialogues(interaction, cur_lan, "v2_hunt_tutorial", 'denial')
                return
        await complicated_relationship.hunter(["slime", 0], interaction, place, place.color)

    @hunt.on_autocomplete("place")
    async def hunt_autocomplete(self, interaction, current: str):
        huntlocations = await fns.huntlocations()
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        data = {}
        i = 0
        if not current:
            for name in huntlocations:
                if await fns.check_location(interaction.user, name['name'], 'hunt'):
                    chk_it = fns.get_hunt_locations(name['name'], leng)
                    i += 1
                    data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for name in huntlocations:
                if await fns.check_location(interaction.user, name['name'], 'hunt'):
                    chk_it = fns.get_hunt_locations(name['name'], leng)
                    if str(current.lower()) in chk_it.displayname.lower():
                        i += 1
                        data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))


def setup(client):
    client.add_cog(Hunting(client))

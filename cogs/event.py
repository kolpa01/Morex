import nextcord
from nextcord.ext import commands
from nextcord import Interaction 
import functions as fns
import main
import json
import morex
import complicated_relationship


class EventCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="event", integration_types=main.integrations, contexts=main.contexts)
    async def event(self, interaction: Interaction):
        pass

    @event.subcommand(name="counter", description="Display global counter with milestones for users to complete.", description_localizations={"pl": "Display global counter with milestones for users to complete."})
    async def event_counter(self, interaction: Interaction):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['event_counter']

        with open("ownerdb/global_counter.json", "r") as f:
            counters = json.load(f)

        if not len(counters):
            embed = nextcord.Embed(title=text['counter'], description=text['none'], color=main.color_normal)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return

        # do this in a better way please
        current_counter = list(counters.items())[0]
        embed = nextcord.Embed(title=text['counter'], description=str(current_counter), color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @event.subcommand(name="list", description="Display information about current and upcoming events.", description_localizations={"pl": "Wyświetl informacje o obecnych i nadchodzących wydarzeniach."})
    async def event_list(self, interaction: Interaction):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['event_list']

        with open('ownerdb/event.json', "r") as f:
            events_data = json.load(f)

        embeds = []
        if not events_data['events'] and not events_data['current_event']:
            embed = nextcord.Embed(title=text['event'], description=text['none'], color=main.color_normal)
            embed.set_footer(text=f"{leng['other']['pages']['page']} 0/0 | {main.version[cur_lan]}")
            await interaction.response.send_message(embed=embed)
            return
        else:
            if events_data['current_event']:
                event_obj = morex.objects.MorexEvent(events_data['current_event'], cur_lan)
                embed = nextcord.Embed(
                    title=text['event'], 
                    description=f"**{event_obj.disname}**\n<t:{event_obj.start}> - <t:{event_obj.end}>\n{event_obj.description}", 
                    color=main.color_normal
                )
                embeds.append(embed)
            for k, event_data in events_data['events'].items():
                event_obj = morex.objects.MorexEvent(event_data, cur_lan)
                embed = nextcord.Embed(
                    title=text['event'], 
                    description=f"**{event_obj.disname}**\n<t:{event_obj.start}> - <t:{event_obj.end}>\n{event_obj.description}", 
                    color=main.color_normal
                )
                embeds.append(embed)
        embed = embeds[0]
        embed.set_footer(text=f"{leng['other']['pages']['page']} 1/{len(embeds)} | {main.version[cur_lan]}")
        view = await complicated_relationship.pages_helper(embeds, interaction.user)

        await interaction.response.send_message(embed=embed, view=view)


def setup(client):
    client.add_cog(EventCommands(client))

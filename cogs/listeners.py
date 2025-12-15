import nextcord
from nextcord import Interaction, ApplicationInvokeError
from nextcord.ext import commands, tasks
import custom_errors
import main
from morex import logging
from morex.objects import MorexEvent
import json
import datetime


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cached_data = {"time": 0, "starts": [], "current_event": None, "sent_notifs": [False, False, False]}
        self.reload_cache = False
        self.notification_channel = None
        self._notif_channel_id = 1371570817283915836
        self.role = "<@&1371570940600782960>"
        self.loop_is_running = False

    @commands.Cog.listener()
    async def on_application_command_error(
        self, interaction: Interaction, error: ApplicationInvokeError
    ) -> None:
        if isinstance(error.original, custom_errors.ToMakeCodeWorkError):
            return
        if main.mode == "dev":
            return
        log_channel = await self.client.fetch_channel(1332861604194160700)
        if interaction.guild:
            g_name = f"{interaction.guild.name} ({interaction.guild.id})"
        else:
            g_name = "guild_not_found"
        whole_cmd = [interaction.application_command.name]
        try:
            whole_cmd.append(interaction.application_command.parent_cmd.name)
            try:
                whole_cmd.append(interaction.application_command.parent_cmd.parent_cmd.name)
            except AttributeError:
                pass
        except AttributeError:
            pass
        whole_cmd.reverse()
        embed = nextcord.Embed(title="New error has occured :OOO", description=f"In server {g_name} by {interaction.user} ({interaction.user.id})\nUsing **/{' '.join(whole_cmd)}**\n```{error}```", color=main.color_normal)
        embed.set_footer(text=main.version["en"])
        await log_channel.send(embed=embed)
        await interaction.response.send_message(content="Something went wrong...", ephemeral=True)
        return

    @tasks.loop(minutes=1)
    async def event_handler(self):
        if self.cached_data["time"] == 0 or self.reload_cache:
            try:
                self.notification_channel = await self.client.fetch_channel(self._notif_channel_id)
            except nextcord.Forbidden:
                logging.warn("Event notification channel wasn't found.")

            with open('ownerdb/event.json', 'r') as f:
                event_data = json.load(f)
            self.cached_data['starts'] = [a for a in event_data['events']]
            self.cached_data['starts'].sort()
                
            self.cached_data['time'] = datetime.datetime.now().timestamp()

            if event_data['current_event']:
                self.cached_data['current_event'] = MorexEvent(event_data['current_event'], 'en')
                self.cached_data['sent_notifs'] = event_data['sent_notifs']

            main.event = self.cached_data                
            self.reload_cache = False
            logging.success('Updated event cache')
        this_day = round(datetime.datetime.now().timestamp())
        if (False if len(self.cached_data['starts']) < 1 else int(self.cached_data['starts'][0]) <= this_day) and not self.cached_data['current_event']:
            with open('ownerdb/event.json', 'r') as f:
                event_data = json.load(f)

            self.cached_data['current_event'] = MorexEvent(event_data['events'][self.cached_data['starts'][0]], 'en')  # event object

            event_data['current_event'] = event_data['events'][self.cached_data['starts'][0]]
            event_data['events'].pop(str(self.cached_data['current_event'].start), None)
            event_data['sent_notifs'] = self.cached_data['sent_notifs']

            with open('ownerdb/event.json', 'w') as f:
                json.dump(event_data, f)

            self.cached_data['starts'].pop(0)
            main.event = self.cached_data                
        if self.cached_data['current_event']:
            if self.cached_data['current_event'].notify_start:
                if not self.cached_data['sent_notifs'][0]:
                    if self.cached_data['current_event'].start <= this_day:
                        embed = nextcord.Embed(title='New Event', description=f'The {self.cached_data['current_event'].disname} has just started!', color=main.color_normal)
                        embed.set_footer(text=main.version['en'])
                        try:
                            await self.notification_channel.send(content=self.role, embed=embed)
                        except AttributeError:
                            logging.critical('Attempted to send notification to None')
                        self.cached_data['sent_notifs'][0] = True
                        main.event = self.cached_data                
                        with open('ownerdb/event.json', 'r') as f:
                            event_data = json.load(f)

                        event_data['sent_notifs'] = self.cached_data['sent_notifs']

                        with open('ownerdb/event.json', 'w') as f:
                            json.dump(event_data, f)
            if self.cached_data['current_event'].notify_before_end:
                if not self.cached_data['sent_notifs'][1]:
                    if self.cached_data['current_event'].notify_before_end <= this_day:
                        embed = nextcord.Embed(title='Event', description=f'The {self.cached_data['current_event'].disname} ends <t:{self.cached_data['current_event'].end}:R>!', color=main.color_normal)
                        embed.set_footer(text=main.version['en'])
                        try:
                            await self.notification_channel.send(content=self.role, embed=embed)
                        except AttributeError:
                            logging.critical('Attempted to send notification to None')
                        self.cached_data['sent_notifs'][1] = True
                        main.event = self.cached_data                
                        with open('ownerdb/event.json', 'r') as f:
                            event_data = json.load(f)

                        event_data['sent_notifs'] = self.cached_data['sent_notifs']

                        with open('ownerdb/event.json', 'w') as f:
                            json.dump(event_data, f)
            if self.cached_data['current_event'].end <= this_day:
                if self.cached_data['current_event'].notify_end:
                    if not self.cached_data['sent_notifs'][2]:
                        embed = nextcord.Embed(title='Event Ended', description=f'The {self.cached_data['current_event'].disname} has ended.', color=main.color_normal)
                        embed.set_footer(text=main.version['en'])
                        try:
                            await self.notification_channel.send(content=self.role, embed=embed)
                        except AttributeError:
                            logging.critical('Attempted to send notification to None')
                        self.cached_data['sent_notifs'][2] = True
                        main.event = self.cached_data                
                        with open('ownerdb/event.json', 'r') as f:
                            event_data = json.load(f)

                        event_data['sent_notifs'] = self.cached_data['sent_notifs']

                        with open('ownerdb/event.json', 'w') as f:
                            json.dump(event_data, f)
                self.cached_data['current_event'] = None
                self.cached_data['sent_notifs'] = [False, False, False]
                main.event = self.cached_data                
                with open('ownerdb/event.json', 'r') as f:
                    event_data = json.load(f)

                event_data['sent_notifs'] = self.cached_data['sent_notifs']
                event_data['current_event'] = None

                with open('ownerdb/event.json', 'w') as f:
                    json.dump(event_data, f)

    @commands.Cog.listener()
    async def on_ready(self):
        logging.success(f"Logged in {self.client.user}")
        activity = nextcord.Activity(type=nextcord.ActivityType.watching, name="Slime Valley")
        await self.client.change_presence(activity=activity)
        if not self.loop_is_running:
            self.event_handler.start()
            self.loop_is_running = True


def setup(client):
    client.add_cog(Events(client))

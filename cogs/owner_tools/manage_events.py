import nextcord
from nextcord.ext import commands
import json
import main
import morex.logging as logging
import buttons
import functions as fns
import datetime
from uuid import uuid4


class SaveAsDraft(nextcord.ui.Modal):
    def __init__(self, view):
        super().__init__(
            "Save as Draft",
            timeout=600,  
        )

        self.text = nextcord.ui.TextInput(
            label="Draft Name",
            placeholder="Enter draft name.",
            min_length=1,
            max_length=64,
        )
        self.add_item(self.text)
        self.view = view

    async def callback(self, interaction: nextcord.Interaction) -> None:
        name = f"{uuid4()}.json"
        obj = {"metadata": {"name": self.text.value}, "data": self.view.event}
        with open(f'ownerdb/events/drafts/{name}', "w") as f:
            json.dump(obj, f)


class SaveAsPreset(nextcord.ui.Modal):
    def __init__(self, view):
        super().__init__(
            "Save as Preset",
            timeout=600,  
        )

        self.text = nextcord.ui.TextInput(
            label="Preset Name",
            placeholder="Enter preset name.",
            min_length=1,
            max_length=64,
        )
        self.add_item(self.text)
        self.view = view

    async def callback(self, interaction: nextcord.Interaction) -> None:
        name = f"{uuid4()}.json"
        obj = {"metadata": {"name": self.text.value}, "data": self.view.event}
        with open(f'ownerdb/events/presets/{name}', "w") as f:
            json.dump(obj, f)
        

class SaveButtons(nextcord.ui.View):
    def __init__(self, user, og_view):
        super().__init__(timeout=60)
        self.user = user
        self.value = None
        self.og_view = og_view

    @nextcord.ui.button(label="Save as Event", emoji='<:MX_Save:1220425821559455836>', style=nextcord.ButtonStyle.gray, row=1)
    async def save(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        missing = []
        if self.og_view.event['id'] is None:
            missing.append("id")
        if self.og_view.event['disname']['pl'] is None:
            missing.append("disname_pl")
        if self.og_view.event['disname']['en'] is None:
            missing.append('disname_en')
        if self.og_view.event['description']['en'] is None:
            missing.append('description_en')
        if self.og_view.event['description']['pl'] is None:
            missing.append('description_pl')
        if self.og_view.event['start'] is None:
            missing.append('start')
        if self.og_view.event['end'] is None:
            missing.append('end')
        if missing:
            embed = nextcord.Embed(title="Missing Options", description="\n".join(f"`{a}`" for a in missing), color=main.color_normal)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        self.value = "save"
        self.stop()

    @nextcord.ui.button(label="Discard", emoji=main.deny, style=nextcord.ButtonStyle.red, row=1)
    async def discard(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = "discard"
        self.stop()

    @nextcord.ui.button(label="Save as Draft", emoji='<:MX_Save:1220425821559455836>', style=nextcord.ButtonStyle.gray, row=2)
    async def draft(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(SaveAsDraft(self.og_view))
        self.value = "draft"
        self.stop()

    @nextcord.ui.button(label="Save as Preset", emoji='<:MX_Save:1220425821559455836>', style=nextcord.ButtonStyle.gray, row=2)
    async def preset(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        missing = []
        if self.og_view.event['id'] is None:
            missing.append("id")
        if self.og_view.event['disname']['pl'] is None:
            missing.append("disname_pl")
        if self.og_view.event['disname']['en'] is None:
            missing.append('disname_en')
        if self.og_view.event['description']['en'] is None:
            missing.append('description_en')
        if self.og_view.event['description']['pl'] is None:
            missing.append('description_pl')
        if self.og_view.event['start'] is None:
            missing.append('start')
        if self.og_view.event['end'] is None:
            missing.append('end')
        if missing:
            embed = nextcord.Embed(title="Missing Options", description="\n".join(f"`{a}`" for a in missing), color=main.color_normal)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        await interaction.response.send_modal(SaveAsPreset(self.og_view))
        self.value = "draft"
        self.stop()

    @nextcord.ui.button(label="Cancel", emoji=main.deny, style=nextcord.ButtonStyle.red, row=3)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.stop()

    async def interaction_check(self, interaction):
        if interaction.user != self.user:
            return False
        return True


class StrModal(nextcord.ui.Modal):
    def __init__(self, text, view):
        if text is None:
            text = ""
        super().__init__(
            "Edit string",
            timeout=600,  
        )
        self.view = view
        label = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(':')
        label = " ".join(text.capitalize() for text in label)

        self.text = nextcord.ui.TextInput(
            label=label,
            style=nextcord.TextInputStyle.paragraph,
            default_value=text,
            min_length=1,
            max_length=4000,
        )
        self.add_item(self.text)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        ids = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(":")
        if len(ids) == 1:
            self.view.event[ids[0]] = self.text.value
        elif len(ids) == 2:
            self.view.event[ids[0]][ids[1]] = self.text.value
        else:
            return
        await self.view.update_embeds()
        embed = self.view.embedz[self.view.current]
        embed.set_footer(text=f"Page {self.view.current + 1}/4 | {main.version['en']}")
        await interaction.edit(embed=embed)


class BoolModal(nextcord.ui.Modal):
    def __init__(self, text, view):
        if text is None:
            text = ""
        elif text:
            text = "1"
        elif not text:
            text = "0"
        super().__init__(
            "Edit bool",
            timeout=600,  
        )
        self.view = view
        label = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(':')
        label = " ".join(text.capitalize() for text in label)

        self.text = nextcord.ui.TextInput(
            label=label,
            default_value=text,
            min_length=1,
            max_length=1,
        )
        self.add_item(self.text)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        ids = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(":")
        if len(ids) == 1:
            self.view.event[ids[0]] = bool(int(self.text.value))
        elif len(ids) == 2:
            self.view.event[ids[0]][ids[1]] = bool(int(self.text.value))
        else:
            return
        await self.view.update_embeds()
        embed = self.view.embedz[self.view.current]
        embed.set_footer(text=f"Page {self.view.current + 1}/4 | {main.version['en']}")
        await interaction.edit(embed=embed)


class IntModal(nextcord.ui.Modal):
    def __init__(self, text, view):
        if text is None:
            text = ""
        elif not text:
            text = ""
        super().__init__(
            "Edit int",
            timeout=600,  
        )
        self.view = view
        label = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(':')
        label = " ".join(text.capitalize() for text in label)

        self.text = nextcord.ui.TextInput(
            label=label,
            default_value=text,
            placeholder="Leave empty for False or type '0'",
            required=False,
            max_length=1000,
        )
        self.add_item(self.text)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        ids = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(":")
        if self.text.value == '' or self.text.value == "0":
            value = False
        else:
            value = int(self.text.value)
        if len(ids) == 1:
            self.view.event[ids[0]] = value
        elif len(ids) == 2:
            self.view.event[ids[0]][ids[1]] = value
        else:
            return
        await self.view.update_embeds()
        embed = self.view.embedz[self.view.current]
        embed.set_footer(text=f"Page {self.view.current + 1}/4 | {main.version['en']}")
        await interaction.edit(embed=embed)


class TimeModal(nextcord.ui.Modal):
    def __init__(self, text, view):
        if text is None:
            text = ""
        elif text:
            date = datetime.datetime.fromtimestamp(text)
            text = f"{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}"
        super().__init__(
            "Edit time",
            timeout=600,  
        )
        self.view = view
        label = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(':')
        label = " ".join(text.capitalize() for text in label)

        self.text = nextcord.ui.TextInput(
            label=label,
            default_value=text,
            placeholder="DD/MM/YYYY HH:MM",
            min_length=1,
            max_length=1000,
        )
        self.add_item(self.text)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        ids = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(":")
        date, time = self.text.value.split(" ")
        day, month, year = date.split("/")
        hour, minute = time.split(":")
        timestamp = round(datetime.datetime(int(year), int(month), int(day), int(hour), int(minute)).timestamp())
        if len(ids) == 1:
            self.view.event[ids[0]] = timestamp
        elif len(ids) == 2:
            self.view.event[ids[0]][ids[1]] = timestamp
        else:
            return
        await self.view.update_embeds()
        embed = self.view.embedz[self.view.current]
        embed.set_footer(text=f"Page {self.view.current + 1}/4 | {main.version['en']}")
        await interaction.edit(embed=embed)


class BoolTimeModal(nextcord.ui.Modal):
    def __init__(self, text, view):
        if text is None:
            text = ""
        elif text:
            date = datetime.datetime.fromtimestamp(text)
            text = f"{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}"
        super().__init__(
            "Edit time",
            timeout=600,  
        )
        self.view = view
        label = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(':')
        label = " ".join(text.capitalize() for text in label)

        self.text = nextcord.ui.TextInput(
            label=label,
            default_value=text,
            placeholder="DD/MM/YYYY HH:MM",
            required=False,
            max_length=1000,
        )
        self.add_item(self.text)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        ids = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(":")
        if self.text.value == '':
            timestamp = False
        else:
            date, time = self.text.value.split(" ")
            day, month, year = date.split("/")
            hour, minute = time.split(":")
            timestamp = round(datetime.datetime(int(year), int(month), int(day), int(hour), int(minute)).timestamp())
        if len(ids) == 1:
            self.view.event[ids[0]] = timestamp
        elif len(ids) == 2:
            self.view.event[ids[0]][ids[1]] = timestamp
        else:
            return
        await self.view.update_embeds()
        embed = self.view.embedz[self.view.current]
        embed.set_footer(text=f"Page {self.view.current + 1}/4 | {main.version['en']}")
        await interaction.edit(embed=embed)


class TimeEndModal(nextcord.ui.Modal):
    def __init__(self, text, view):
        if text is None:
            text = ""
        elif text:
            date = datetime.datetime.fromtimestamp(text)
            text = f"{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}"
        super().__init__(
            "Edit time",
            timeout=600,  
        )
        self.view = view
        label = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(':')
        label = " ".join(text.capitalize() for text in label)

        self.text = nextcord.ui.TextInput(
            label=label,
            default_value=text,
            placeholder="DD/MM/YYYY HH:MM",
            min_length=1,
            max_length=1000,
        )
        self.add_item(self.text)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        ids = self.view.fields_ids[str(self.view.current)][self.view.current_page_pos[str(self.view.current)]['current'] - 1].split(":")
        if self.text.value.startswith("+"):
            a = self.text.value.lstrip("+")
            time = int(a) * 3600 
            timestamp = self.view.event['start'] + time
        else:
            date, time = self.text.value.split(" ")
            day, month, year = date.split("/")
            hour, minute = time.split(":")
            timestamp = round(datetime.datetime(int(year), int(month), int(day), int(hour), int(minute)).timestamp())
        if len(ids) == 1:
            self.view.event[ids[0]] = timestamp
        elif len(ids) == 2:
            self.view.event[ids[0]][ids[1]] = timestamp
        else:
            return
        await self.view.update_embeds()
        embed = self.view.embedz[self.view.current]
        embed.set_footer(text=f"Page {self.view.current + 1}/4 | {main.version['en']}")
        await interaction.edit(embed=embed)


class Up(nextcord.ui.Button):
    def __init__(self):
        super().__init__(style=nextcord.ButtonStyle.gray, emoji="<:MX_Up:1410564408123457667>", row=1)

    async def callback(self, interaction: nextcord.Interaction):
        if self.view.current_page_pos[str(self.view.current)]['current'] > 1:
            self.view.current_page_pos[str(self.view.current)]['current'] -= 1

        await self.view.update_embeds()
        embed = self.view.embedz[self.view.current]
        embed.set_footer(text=f"Page {self.view.current + 1}/4 | {main.version['en']}")
        await interaction.edit(embed=embed)


class Down(nextcord.ui.Button):
    def __init__(self):
        super().__init__(style=nextcord.ButtonStyle.gray, emoji="<:MX_Down:1410564401630679111>", row=1)

    async def callback(self, interaction: nextcord.Interaction):
        if self.view.current_page_pos[str(self.view.current)]['current'] < self.view.current_page_pos[str(self.view.current)]['max']:
            self.view.current_page_pos[str(self.view.current)]['current'] += 1

        await self.view.update_embeds()
        embed = self.view.embedz[self.view.current]
        embed.set_footer(text=f"Page {self.view.current + 1}/4 | {main.version['en']}")
        await interaction.edit(embed=embed)


class EventPages(buttons.Pages):
    def __init__(self, user, client, lang_file, skeleton):
        self.event = skeleton
        # <:MX_DotWhite:1410564398963097701>
        embed1 = nextcord.Embed(
            title="Event Creator",
            color=main.color_normal
        )
        embed1.add_field(
            name="ID",
            value=f"<:MX_DotWhite:1410564398963097701> | {self.event['id']}",
            inline=False
        )
        embed1.add_field(
            name="Name",
            value=f"<:MX_DotWhite:1410564398963097701> | :flag_pl: {self.event['disname']['pl']}\n<:MX_DotWhite:1410564398963097701> | :flag_gb: {self.event['disname']['en']}",
            inline=False

        )
        embed1.add_field(
            name="Description",
            value=f"<:MX_DotWhite:1410564398963097701> | :flag_pl: {self.event['description']['pl']}\n<:MX_DotWhite:1410564398963097701> | :flag_gb: {self.event['description']['en']}",
            inline=False
        )

        embed2 = nextcord.Embed(
            title="Event Creator",
            color=main.color_normal
        )
        embed2.add_field(
            name="Duration",
            value=f"<:MX_DotWhite:1410564398963097701> | Start: {None if self.event['start'] is None else f'<t:{self.event['start']}>'}\n<:MX_DotWhite:1410564398963097701> | End: {None if self.event['end'] is None else f'<t:{self.event['end']}>'}\nDuration: 0s",
            inline=False
        )
        embed2.add_field(
            name="Notifications",
            value=f"<:MX_DotWhite:1410564398963097701> | Start: {main.accept if self.event['notifications']['start'] else main.deny}\n<:MX_DotWhite:1410564398963097701> | End: {main.accept if self.event['notifications']['end'] else main.deny}\n<:MX_DotWhite:1410564398963097701> | Before End: {main.deny if not self.event['notifications']['before_end'] else f'<t:{self.event['notifications']['before_end']}>'}",
            inline=False
        )

        embed3 = nextcord.Embed(
            title="Event Creator",
            color=main.color_normal
        )
        embed3.add_field(
            name="Features",
            value=f"<:MX_DotWhite:1410564398963097701> | Hunt XP: {self.event['features']['hunt_xp'] if self.event['features']['hunt_xp'] else main.deny}\n<:MX_DotWhite:1410564398963097701> | Dig Coins: {self.event['features']['dig_chest_coins'] if self.event['features']['dig_chest_coins'] else main.deny}\n<:MX_DotWhite:1410564398963097701> | Beg coins: {self.event['features']['beg_coins'] if self.event['features']['beg_coins'] else main.deny}",
            inline=False
        )
        embed3.add_field(
            name="Quests",
            value=f"<:MX_DotWhite:1410564398963097701> | Quests: {main.deny if not self.event['quests'] else main.accept}",
            inline=False
        )
        embed4 = nextcord.Embed(title="Event Creator", color=main.color_normal)
        embed4.add_field(
            name="Search Overrides",
            value=f"<:MX_DotWhite:1410564398963097701> {self.event['location_overrides']}",
            inline=False
        )
        embeds = [
            embed1, embed2, embed3, embed4
        ] 
        self.current_page_pos = {"0": {"current": 0, "max": 5}, "1": {"current": 0, "max": 5}, "2": {"current": 0, "max": 4}, "3": {"current": 0, "max": 1}}
        self.field_types = {"0": ["str", "str", "str", "str", "str"], "1": ["time", "etime", "bool", "bool", "btime"], "2": ["int", "int", "int", "bool"], "3": ["search"]}
        self.fields_ids = {"0": ["id", "disname:pl", "disname:en", "description:pl", "description:en"], "1": ["start", "end", "notifications:start", "notifications:end", "notifications:before_end"], "2": ["features:hunt_xp", "features:dig_chest_coins", "features:beg_coins", "quests"], "3": ["location_overrides"]}
        self.client = client
        super().__init__(360, 4, embeds, user, leng=lang_file, custom_footer=main.version['en'])
        self.remove_item(self.farleft)
        self.remove_item(self.farright)
        self.add_item(Up())
        self.add_item(Down())

    async def get_event_duration(self):
        if self.event['start'] is None or self.event['end'] is None:
            return "0s"
        if self.event['end'] < self.event['start']:
            return "!!! Event cannot be ended before it starts !!!"
        time = self.event['end'] - self.event['start']
        return f"{time}s"

    async def update_embeds(self):
        name1_1 = f"<1> | {self.event['id']}".replace(f'<{self.current_page_pos["0"]["current"]}>', '<:MX_DotBlue:1410564396622807081>').replace('<1>', '<:MX_DotWhite:1410564398963097701>')
        name1_2 = f"<2> | :flag_pl: {self.event['disname']['pl']}\n<3> | :flag_gb: {self.event['disname']['en']}".replace(f'<{self.current_page_pos["0"]["current"]}>', '<:MX_DotBlue:1410564396622807081>').replace('<2>', '<:MX_DotWhite:1410564398963097701>').replace('<3>', '<:MX_DotWhite:1410564398963097701>')
        name1_3 = f"<4> | :flag_pl: {self.event['description']['pl']}\n<5> | :flag_gb: {self.event['description']['en']}".replace(f'<{self.current_page_pos["0"]["current"]}>', '<:MX_DotBlue:1410564396622807081>').replace('<4>', '<:MX_DotWhite:1410564398963097701>').replace('<5>', '<:MX_DotWhite:1410564398963097701>')
        embed1 = nextcord.Embed(title="Event Creator", color=main.color_normal)
        embed1.add_field(name="ID", value=name1_1, inline=False)
        embed1.add_field(name="Name", value=name1_2, inline=False)
        embed1.add_field(name="Description", value=name1_3, inline=False)

        name2_1 = f"<1> | Start: {None if self.event['start'] is None else f'<t:{self.event['start']}>'}\n<2> | End: {None if self.event['end'] is None else f'<t:{self.event['end']}>'}\nDuration: {await self.get_event_duration()}".replace(f'<{self.current_page_pos["1"]["current"]}>', '<:MX_DotBlue:1410564396622807081>').replace('<1>', '<:MX_DotWhite:1410564398963097701>').replace('<2>', '<:MX_DotWhite:1410564398963097701>')
        name2_2 = f"<3> | Start: {main.accept if self.event['notifications']['start'] else main.deny}\n<4> | End: {main.accept if self.event['notifications']['end'] else main.deny}\n<5> | Before End: {main.deny if not self.event['notifications']['before_end'] else f'<t:{self.event['notifications']['before_end']}>'}".replace(f'<{self.current_page_pos["1"]["current"]}>', '<:MX_DotBlue:1410564396622807081>').replace('<3>', '<:MX_DotWhite:1410564398963097701>').replace('<4>', '<:MX_DotWhite:1410564398963097701>').replace('<5>', '<:MX_DotWhite:1410564398963097701>')
        embed2 = nextcord.Embed(title="Event Creator", color=main.color_normal)
        embed2.add_field(name="Duration", value=name2_1, inline=False)
        embed2.add_field(name="Notifications", value=name2_2, inline=False)

        name3_1 = f"<1> | Hunt XP: {self.event['features']['hunt_xp'] if self.event['features']['hunt_xp'] else main.deny}\n<2> | Dig Coins: {self.event['features']['dig_chest_coins'] if self.event['features']['dig_chest_coins'] else main.deny}\n<3> | Beg coins: {self.event['features']['beg_coins'] if self.event['features']['beg_coins'] else main.deny}".replace(f'<{self.current_page_pos["2"]["current"]}>', '<:MX_DotBlue:1410564396622807081>').replace('<1>', '<:MX_DotWhite:1410564398963097701>').replace('<2>', '<:MX_DotWhite:1410564398963097701>').replace('<3>', '<:MX_DotWhite:1410564398963097701>')
        name3_2 = f"<4> | Quests: {main.deny if not self.event['quests'] else main.accept}".replace(f'<{self.current_page_pos["2"]["current"]}>', '<:MX_DotBlue:1410564396622807081>').replace('<4>', '<:MX_DotWhite:1410564398963097701>')
        embed3 = nextcord.Embed(title="Event Creator", color=main.color_normal)
        embed3.add_field(name="Features", value=name3_1, inline=False)
        embed3.add_field(name="Quests", value=name3_2, inline=False)
        
        name4_1 = f"<1> {self.event['location_overrides']}".replace(f'<{self.current_page_pos["3"]["current"]}>', '<:MX_DotBlue:1410564396622807081>')
        embed4 = nextcord.Embed(title="Event Creator", color=main.color_normal)
        embed4.add_field(
            name="Search Overrides",
            value=name4_1,
            inline=False
        )
        self.embedz[0] = embed1
        self.embedz[1] = embed2
        self.embedz[2] = embed3
        self.embedz[3] = embed4

    async def send_embed(self, interaction):
        await self.update_embeds()
        embed = self.embedz[self.current]
        embed.set_footer(text=f"Page {self.current + 1}/4 | {main.version['en']}")
        await interaction.edit(embed=embed)
        
    @nextcord.ui.button(emoji='<:MX_Plus:1410564406215180379>', style=nextcord.ButtonStyle.gray, row=2)
    async def plus(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        num = self.current_page_pos[str(self.current)]["current"]
        if num == 0:
            # raise error or smt
            return 
        if self.field_types[str(self.current)][num - 1] == "bool":
            field_id = self.fields_ids[str(self.current)][num - 1].split(":")
            if len(field_id) == 1:
                self.event[field_id[0]] = True
            elif len(field_id) == 2:
                self.event[field_id[0]][field_id[1]] = True
            else:
                return
            await self.send_embed(interaction)
            return
        elif self.field_types[str(self.current)][num - 1] == "int":
            field_id = self.fields_ids[str(self.current)][num - 1].split(":")
            if len(field_id) == 1:
                if not self.event[field_id[0]]:
                    self.event[field_id[0]] = 1
                else:
                    self.event[field_id[0]] += 1
            elif len(field_id) == 2:
                if not self.event[field_id[0]][field_id[1]]:
                    self.event[field_id[0]][field_id[1]] = 1
                else:
                    self.event[field_id[0]][field_id[1]] += 1
            else:
                return
            await self.send_embed(interaction)
            return

        await interaction.response.send_message(content="Cannot add to this field", ephemeral=True)

    @nextcord.ui.button(emoji='<:MX_Pencil:1269702293591294063>', style=nextcord.ButtonStyle.gray, row=2)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        num = self.current_page_pos[str(self.current)]["current"]
        if num == 0:
            return 

        field_id = self.fields_ids[str(self.current)][num - 1].split(":")
        if len(field_id) == 1:
            text = self.event[field_id[0]]
        elif len(field_id) == 2:
            text = self.event[field_id[0]][field_id[1]]
        else:
            return
        if self.field_types[str(self.current)][num - 1] == "str":
            await interaction.response.send_modal(StrModal(text, self))
        elif self.field_types[str(self.current)][num - 1] == "bool":
            await interaction.response.send_modal(BoolModal(text, self))
        elif self.field_types[str(self.current)][num - 1] == "int":
            await interaction.response.send_modal(IntModal(text, self))
        elif self.field_types[str(self.current)][num - 1] == "time":
            await interaction.response.send_modal(TimeModal(text, self))
        elif self.field_types[str(self.current)][num - 1] == "etime":
            await interaction.response.send_modal(TimeEndModal(text, self))
        elif self.field_types[str(self.current)][num - 1] == "btime":
            await interaction.response.send_modal(BoolTimeModal(text, self))

    @nextcord.ui.button(emoji='<:MX_Minus:1410564404604571670>', style=nextcord.ButtonStyle.gray, row=2)
    async def minus(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        num = self.current_page_pos[str(self.current)]["current"]
        if num == 0:
            # raise error or smt
            return 
        if self.field_types[str(self.current)][num - 1] == "bool":
            field_id = self.fields_ids[str(self.current)][num - 1].split(":")
            if len(field_id) == 1:
                self.event[field_id[0]] = False
            elif len(field_id) == 2:
                self.event[field_id[0]][field_id[1]] = False
            else:
                return
            await self.send_embed(interaction)
            return
        elif self.field_types[str(self.current)][num - 1] == "int":
            field_id = self.fields_ids[str(self.current)][num - 1].split(":")
            if len(field_id) == 1:
                if not self.event[field_id[0]]:
                    self.event[field_id[0]] = False
                elif self.event[field_id[0]] == 1:
                    self.event[field_id[0]] = False
                else:
                    self.event[field_id[0]] -= 1
            elif len(field_id) == 2:
                if not self.event[field_id[0]][field_id[1]]:
                    self.event[field_id[0]][field_id[1]] = False
                elif self.event[field_id[0]][field_id[1]] == 1:
                    self.event[field_id[0]][field_id[1]] = False
                else:
                    self.event[field_id[0]][field_id[1]] -= 1
            else:
                return
            await self.send_embed(interaction)
            return
        elif self.field_types[str(self.current)][num - 1] == "btime":
            field_id = self.fields_ids[str(self.current)][num - 1].split(":")
            if len(field_id) == 1:
                self.event[field_id[0]] = False
            elif len(field_id) == 2:
                self.event[field_id[0]][field_id[1]] = False
            else:
                return
            await self.send_embed(interaction)
            return

        await interaction.response.send_message(content="Cannot remove to this field", ephemeral=True)

    @nextcord.ui.button(label="Save", emoji='<:MX_Save:1220425821559455836>', style=nextcord.ButtonStyle.gray, row=2)
    async def save(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = SaveButtons(interaction.user, self)
        msg = await interaction.response.send_message(content="...", view=view, ephemeral=True)
        await view.wait()
        if view.value is None:
            await msg.delete()
            return
        elif view.value == "discard":
            await msg.delete()
            self.stop()
            return
        elif view.value == "draft":
            await msg.delete()
            return
        elif view.value == "preset":
            await msg.delete()
            return
        elif view.value == "save":
            missing = []
            if self.event['id'] is None:
                missing.append("id")
            if self.event['disname']['pl'] is None:
                missing.append("disname_pl")
            if self.event['disname']['en'] is None:
                missing.append('disname_en')
            if self.event['description']['en'] is None:
                missing.append('description_en')
            if self.event['description']['pl'] is None:
                missing.append('description_pl')
            if self.event['start'] is None:
                missing.append('start')
            if self.event['end'] is None:
                missing.append('end')
            if missing:
                embed = nextcord.Embed("Missing Options", description="\n".join(f"`{a}`" for a in missing), color=main.color_normal)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            await msg.delete()
            event_cog = self.client.get_cog('Events')
            with open('ownerdb/event.json', "r") as f:
                event_data = json.load(f)
            event_data['events'].update({self.event['start']: self.event})
            with open('ownerdb/event.json', "w") as f:
                json.dump(event_data, f)
            event_cog.reload_cache = True
            self.stop()
            return

    async def interaction_check(self, interaction):
        if interaction.user != self.user:
            return False
        return True


class DefaultUp(nextcord.ui.Button):
    def __init__(self):
        super().__init__(style=nextcord.ButtonStyle.gray, label="\u200b", emoji="", row=1)

    async def callback(self, interaction: nextcord.Interaction):
        if self.view.current_page_pos[str(self.view.current)]['current'] > 1:
            self.view.current_page_pos[str(self.view.current)]['current'] -= 1

        await self.view.update_embeds()
        embed = self.view.embedz[self.view.current]
        embed.set_footer(text=main.version['en'])
        await interaction.edit(embed=embed)


class DefaultDown(nextcord.ui.Button):
    def __init__(self):
        super().__init__(style=nextcord.ButtonStyle.gray, label="\u200b", emoji="", row=1)

    async def callback(self, interaction: nextcord.Interaction):
        if self.view.current_page_pos[str(self.view.current)]['current'] < self.view.current_page_pos[str(self.view.current)]['max']:
            self.view.current_page_pos[str(self.view.current)]['current'] += 1

        await self.view.update_embeds()
        embed = self.view.embedz[self.view.current]
        embed.set_footer(text=f"Page {self.view.current + 1}/4 | {main.version['en']}")
        await interaction.edit(embed=embed)


class SelectPreset(nextcord.ui.View):
    def __init__(self, user, client, choices, metadata):
        super().__init__(timeout=360)
        self.user = user
        self.client = client
        self.current = 1
        self.choices = choices
        self.event_metadata = metadata

    async def load_skel(self):
        return self.choices[self.current]

    async def get_embed(self, skel):
        embed = nextcord.Embed(
            title="Event Creator",
            color=main.color_normal
        )
        embed.add_field(
            name="ID",
            value=f"<:MX_DotWhite:1410564398963097701> | {skel['id']}",
            inline=False
        )
        embed.add_field(
            name="Name",
            value=f"<:MX_DotWhite:1410564398963097701> | :flag_pl: {skel['disname']['pl']}\n<:MX_DotWhite:1410564398963097701> | :flag_gb: {skel['disname']['en']}",
            inline=False

        )
        embed.add_field(
            name="Description",
            value=f"<:MX_DotWhite:1410564398963097701> | :flag_pl: {skel['description']['pl']}\n<:MX_DotWhite:1410564398963097701> | :flag_gb: {skel['description']['en']}",
            inline=False
        )
        embed.set_footer(text=f"Page 1/4 | {main.version['en']}")
        return embed

    @nextcord.ui.button(emoji="<:MX_Up:1410564408123457667>", style=nextcord.ButtonStyle.gray)
    async def up(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.current > 1:
            self.current -= 1

    @nextcord.ui.button(emoji="<:MX_Down:1410564401630679111>", style=nextcord.ButtonStyle.gray)
    async def down(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.current < len(self.choices):
            self.current += 1

    @nextcord.ui.button(emoji=main.accept, style=nextcord.ButtonStyle.green)
    async def accept(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        skel = await self.load_skel()

        embed = await self.get_embed(skel)
        leng = await fns.lang("en")
        view = EventPages(self.user, self.client, leng, skel)
        await interaction.edit(embed=embed, view=view)


class EventCreationChoicer(nextcord.ui.View):
    def __init__(self, user, client):
        super().__init__(timeout=360)
        self.user = user
        self.client = client

    async def load_skel(self):
        with open('ownerdb/events/skel.json', 'r') as f:
            skel = json.load(f)
        return skel

    async def get_embed(self, skel):
        embed = nextcord.Embed(
            title="Event Creator",
            color=main.color_normal
        )
        embed.add_field(
            name="ID",
            value=f"<:MX_DotWhite:1410564398963097701> | {skel['id']}",
            inline=False
        )
        embed.add_field(
            name="Name",
            value=f"<:MX_DotWhite:1410564398963097701> | :flag_pl: {skel['disname']['pl']}\n<:MX_DotWhite:1410564398963097701> | :flag_gb: {skel['disname']['en']}",
            inline=False

        )
        embed.add_field(
            name="Description",
            value=f"<:MX_DotWhite:1410564398963097701> | :flag_pl: {skel['description']['pl']}\n<:MX_DotWhite:1410564398963097701> | :flag_gb: {skel['description']['en']}",
            inline=False
        )
        embed.set_footer(text=f"Page 1/4 | {main.version['en']}")
        return embed

    @nextcord.ui.button(label="New", emoji=main.accept, style=nextcord.ButtonStyle.green)
    async def new(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        skel = await self.load_skel()

        embed = await self.get_embed(skel)
        leng = await fns.lang("en")
        view = EventPages(self.user, self.client, leng, skel)
        await interaction.edit(embed=embed, view=view)

    @nextcord.ui.button(label="From Preset", emoji='<:MX_Pencil:1269702293591294063>', style=nextcord.ButtonStyle.blurple)
    async def preset(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        logging.info('Edited')

    @nextcord.ui.button(label="From Draft", emoji='<:MX_Pencil:1269702293591294063>', style=nextcord.ButtonStyle.blurple)
    async def draft(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        logging.info('Edited')

    async def interaction_check(self, interaction):
        if interaction.user != self.user:
            return False
        return True


class MainEventsMenuView(nextcord.ui.View):
    def __init__(self, user, client):
        super().__init__(timeout=360)
        self.user = user
        self.client = client

    @nextcord.ui.button(label="Create", emoji=main.accept, style=nextcord.ButtonStyle.green)
    async def create(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="Event creator", description="How do you want to create your new event :3", color=main.color_normal)
        view = EventCreationChoicer(self.user, self.client)
        await interaction.edit(embed=embed, view=view)

    @nextcord.ui.button(label="Edit", emoji='<:MX_Pencil:1269702293591294063>', style=nextcord.ButtonStyle.blurple)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        logging.info('Edited')

    @nextcord.ui.button(label="Delete", emoji=main.deny, style=nextcord.ButtonStyle.red)
    async def remove(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        with open('ownerdb/event.json', 'r') as f:
            events = json.load(f)
        events_data = [events['current_event']]
        for k, v in events['events'].items():
            events_data.append(v)
        return events_data

    async def interaction_check(self, interaction):
        if interaction.user != self.user:
            return False
        return True


class OwnerToolsEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def get_cog_data(self):
        listeners = self.client.get_cog('Events')
        return listeners

    async def reload_caches(self):
        cog = await self.get_cog_data()
        cog.reload_cache = True

    async def get_events_data(self):
        with open('ownerdb/event.json', 'r') as f:
            events = json.load(f)
        events_data = [events['current_event']]
        for k, v in events['events'].items():
            events_data.append(v)
        return events_data

    async def any_event_exists(self):
        events_data = await self.get_events_data()
        for i in events_data:
            if i:
                return True
        return False

    async def get_events_embed(self):
        events_data = await self.get_events_data()
        text = []
        for i, event in enumerate(events_data):
            if not event:
                text.append(f'{main.deny} There are no current events.')
                continue
            if i == 0:
                text.append(f'{main.accept} **{event['disname']['en']} ({event['id']})**\n<t:{event['start']}> - <t:{event['end']}>')
                continue
            text.append(f'<:MX_DotWhite:1410564398963097701> **{event['disname']['en']} ({event['id']})**\n<t:{event['start']}> - <t:{event['end']}>')
        text = '\n\n'.join(text)
        embed = nextcord.Embed(title="Event Creator", description=text, color=main.color_normal)
        embed.set_footer(text=main.version['en'])
        return embed

    @nextcord.slash_command(
        name="events", 
        guild_ids=[
            927971482448060477,
            1222203197834399794,
            1198437946810974258,
            1132073153510789292,
            1315801334729146489
        ]
    )
    async def ot_events(self, interaction: nextcord.Interaction):
        pass
   
    @ot_events.subcommand(name="creator", description="Create new events!!!")
    async def ot_creator(self, interaction: nextcord.Interaction):
        if interaction.user.id != 826792866776219709:
            return
        embed = await self.get_events_embed()
        view = MainEventsMenuView(interaction.user, self.client)
        if not await self.any_event_exists():
            view.edit.disabled = True
            view.remove.disabled = True
        await interaction.response.send_message(embed=embed, view=view)


def setup(client):
    client.add_cog(OwnerToolsEvents(client))

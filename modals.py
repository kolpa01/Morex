import nextcord
import main
import functions as fnc
from nextcord import Interaction
import polishchars


class CustommobsCreationModal(nextcord.ui.Modal):
    def __init__(self, user, channel, cur_lan, leng):
        self.modal_lang = leng['modals']['custommobs_create']
        super().__init__(
            self.modal_lang['title'],
        )

        self.name = nextcord.ui.TextInput(
            label=self.modal_lang['label0'],
            min_length=3,
            max_length=32,
            required=True,
            placeholder=self.modal_lang['placeholder0']
        )
        self.disname = nextcord.ui.TextInput(
            label=self.modal_lang['label1'],
            min_length=3,
            max_length=32,
            required=True,
            placeholder=self.modal_lang['placeholder1']
        )
        self.atk = nextcord.ui.TextInput(
            label=self.modal_lang['label2'],
            min_length=1,
            max_length=19,
            required=True,
            placeholder=self.modal_lang['placeholder2']
        )
        self.hp = nextcord.ui.TextInput(
            label=self.modal_lang['label3'],
            min_length=1,
            max_length=5,
            required=True,
            placeholder=self.modal_lang['placeholder3']
        )
        self.meetup_message = nextcord.ui.TextInput(
            label=self.modal_lang['label4'],
            min_length=1,
            max_length=128,
            required=False,
            placeholder=self.modal_lang['placeholder4'],
            style=nextcord.enums.TextInputStyle.paragraph
        )
        self.add_item(self.name)
        self.add_item(self.disname)
        self.add_item(self.atk)
        self.add_item(self.hp)
        self.add_item(self.meetup_message)
        self.user = user
        self.channel = channel
        self.cur_lan = cur_lan
        self.leng = leng['commands']['custommobs_create']

    async def callback(self, interaction: Interaction) -> None:
        mobs = await fnc.custommobs()

        if len(mobs[str(self.user.id)]['mobs']) == 0:
            id_ = "c000"
        else:
            number = int(mobs[str(self.user.id)]['mobs'][-1]["id"][1:]) + 1
            if number > 99:
                id_ = "c" + str(number)
            else:
                id_ = "c" + ("0" * (3 - len(str(number)))) + str(number)

        atak = self.atk.value.split(",")
        attack = []
        for i in atak:
            try:
                if len(atak) != 3:
                    raise ValueError
                attack.append(int(i))
            except ValueError:
                response_embed = nextcord.Embed(description=self.leng['invalid_attack'], color=main.color_normal)
                response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
                response_embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=response_embed, ephemeral=True)
                return

        try:
            hp = int(self.hp.value)
            if hp <= 0 or hp > 65536:
                response_embed = nextcord.Embed(description=self.leng['int_invalid_hp'], color=main.color_normal)
                response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
                response_embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=response_embed, ephemeral=True)
                return
        except ValueError:
            response_embed = nextcord.Embed(description=self.leng['invalid_hp'], color=main.color_normal)
            response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
            response_embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.send_message(embed=response_embed, ephemeral=True)
            return

        nam = self.name.value.lower()
        if not polishchars.check_sid(nam):
            response_embed = nextcord.Embed(description=self.leng['sid'], color=main.color_normal)
            response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
            response_embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.send_message(embed=response_embed, ephemeral=True)
            return

        if not polishchars.check_string(self.disname.value):
            response_embed = nextcord.Embed(description=self.leng['disname'], color=main.color_normal)
            response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
            response_embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.send_message(embed=response_embed, ephemeral=True)
            return
        disname = polishchars.replace_unicode(self.disname.value)

        our_enemy = f'\u007b"id": "{id_}", "name": "{nam}", "disname": "{disname}", "displayname": "<:MX_Placeholder:1133387132766003210> {disname}", "attack": {attack}, "image": "https://cdn.discordapp.com/attachments/1134067893840126012/1134067977839456276/Untitled_03-08-2023_10-39-45_11.png", "hp": {hp}\u007d'

        if self.meetup_message.value != "":
            if not polishchars.check_string(self.meetup_message.value):
                response_embed = nextcord.Embed(description=self.leng['meetup'], color=main.color_normal)
                response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
                response_embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=response_embed, ephemeral=True)
                return
            mtp = polishchars.replace_unicode(self.meetup_message.value)
            our_enemy = our_enemy[:-1] + f', "meetup": "{mtp}"\u007d'

        embed = nextcord.Embed(title=f"Od {self.user.name}")
        embed.add_field(name="Id", value=self.user.id)
        await self.channel.send(content=str(our_enemy), embed=embed)

        response_embed = nextcord.Embed(description=self.leng['sent'], color=main.color_normal)
        response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
        response_embed.set_footer(text=main.version[self.cur_lan])
        await interaction.response.send_message(embed=response_embed, ephemeral=True)


class CustommobsEditModal(nextcord.ui.Modal):
    def __init__(self, user, aid, channel, name, disname, atk, hp, mob_id, emoji, image, cur_lan, leng, meetup=""):
        self.modal_lang = leng['modals']['custommobs_create']
        super().__init__(
            self.modal_lang['title2'],
        )

        self.name = nextcord.ui.TextInput(
            label=self.modal_lang['label0'],
            min_length=3,
            max_length=32,
            required=True,
            placeholder=self.modal_lang['placeholder0'],
            default_value=name
        )
        self.disname = nextcord.ui.TextInput(
            label=self.modal_lang['label1'],
            min_length=3,
            max_length=32,
            required=True,
            placeholder=self.modal_lang['placeholder1'],
            default_value=disname
        )
        self.atk = nextcord.ui.TextInput(
            label=self.modal_lang['label2'],
            min_length=1,
            max_length=19,
            required=True,
            placeholder=self.modal_lang['placeholder2'],
            default_value=atk
        )
        self.hp = nextcord.ui.TextInput(
            label=self.modal_lang['label3'],
            min_length=1,
            max_length=5,
            required=True,
            placeholder=self.modal_lang['placeholder3'],
            default_value=hp
        )
        self.meetup_message = nextcord.ui.TextInput(
            label=self.modal_lang['label4'],
            min_length=1,
            max_length=128,
            required=False,
            placeholder=self.modal_lang['placeholder4'],
            style=nextcord.enums.TextInputStyle.paragraph,
            default_value=meetup
        )
        self.add_item(self.name)
        self.add_item(self.disname)
        self.add_item(self.atk)
        self.add_item(self.hp)
        self.add_item(self.meetup_message)
        self.user = user
        self.channel = channel
        self.mob_id = mob_id
        self.emoji = emoji
        self.image = image
        self.author_id = aid
        self.cur_lan = cur_lan
        self.leng = leng['commands']['custommobs_create']

    async def callback(self, interaction: Interaction) -> None:
        id_ = self.mob_id

        attack = []
        atak = self.atk.value.split(",")
        for i in atak:
            try:
                if len(atak) != 3:
                    raise ValueError
                attack.append(int(i))
            except ValueError:
                response_embed = nextcord.Embed(description=self.leng['invalid_attack'], color=main.color_normal)
                response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
                response_embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=response_embed, ephemeral=True)
                return

        try:
            hp = int(self.hp.value)
            if hp <= 0 or hp > 65536:
                response_embed = nextcord.Embed(description=self.leng['int_invalid_hp'], color=main.color_normal)
                response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
                response_embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=response_embed, ephemeral=True)
                return
        except ValueError:
            response_embed = nextcord.Embed(description=self.leng['invalid_hp'], color=main.color_normal)
            response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
            response_embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.send_message(embed=response_embed, ephemeral=True)
            return

        nam = self.name.value.lower()
        if not polishchars.check_sid(nam):
            response_embed = nextcord.Embed(description=self.leng['sid'], color=main.color_normal)
            response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
            response_embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.send_message(embed=response_embed, ephemeral=True)
            return

        if not polishchars.check_string(self.disname.value):
            response_embed = nextcord.Embed(description=self.leng['disname'], color=main.color_normal)
            response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
            response_embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.send_message(embed=response_embed, ephemeral=True)
            return
        disname = polishchars.replace_unicode(self.disname.value)

        our_enemy = f'\u007b"id": "{id_}", "name": "{nam}", "disname": "{disname}", "displayname": "{self.emoji} {disname}", "attack": {attack}, "image": "{self.image}", "hp": {hp}\u007d'

        if self.meetup_message.value != "":
            if not polishchars.check_string(self.meetup_message.value):
                response_embed = nextcord.Embed(description=self.leng['meetup'], color=main.color_normal)
                response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
                response_embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=response_embed, ephemeral=True)
                return
            mtp = polishchars.replace_unicode(self.meetup_message.value)
            our_enemy = our_enemy[:-1] + f', "meetup": "{mtp}"\u007d'

        embed = nextcord.Embed(title=f"Od {self.user.name}", color=0x000aff)
        embed.add_field(name="User who used a command", value=self.user.id)
        embed.add_field(name="User who requested edit", value=self.author_id)
        await self.channel.send(content=str(our_enemy), embed=embed)

        response_embed = nextcord.Embed(description=f"{self.leng['request2']}\n{self.emoji} {disname}", color=main.color_normal)
        response_embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
        response_embed.set_footer(text=main.version[self.cur_lan])
        await interaction.response.send_message(embed=response_embed, ephemeral=True)

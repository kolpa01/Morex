import nextcord
import json
from nextcord import Interaction

import buttons
import main
import functions as fns


class ProfileDropdown(nextcord.ui.Select):
    def __init__(self, user, cur_lan, leng):
        self.user = user
        self.cur_lan = cur_lan
        self.leng = leng
        select_options = [
            nextcord.SelectOption(label=leng['label0'], description=leng['desc0']),
            nextcord.SelectOption(label=leng['label1'], description=leng['desc1']),
            nextcord.SelectOption(label=leng['label2'], description=leng['desc2']),
            nextcord.SelectOption(label=leng['label3'], description=leng['desc3'])
        ]
        super().__init__(placeholder=leng['placeholder'], min_values=1, max_values=1, options=select_options)
        
    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == self.leng['label0']:
            leng = await fns.lang(self.cur_lan)
            text = leng['commands']['profile']

            users = await fns.playerinfo()
            user = self.user

            display_avatar = str(user.display_avatar)
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
            embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == self.leng['label1']:
            leng = await fns.lang(self.cur_lan)
            text = leng['commands']['profile']
            name = self.user.name
            display_avatar = str(self.user.display_avatar)
            stats = await fns.stats()
            ouas = stats[str(self.user.id)]
            beg = ouas["beg"]
            search = ouas["search"]
            hunt = ouas["hunt"]

            badges = await fns.get_user_badges(self.user)

            embed = nextcord.Embed(title=f"{text['profile']} {name}", description=f"{badges}\n\n**{text['beg']}** {beg}\n\n**{text['fights']}** {hunt}\n\n**{text['search']}** {search}", color=main.color_normal)
            embed.set_thumbnail(url=display_avatar)
            embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.edit_message(embed=embed)
            
        elif self.values[0] == self.leng['label2']:
            leng = await fns.lang(self.cur_lan)
            text = leng['commands']['profile']
            users = await fns.get_inv_data()

            weapons = await fns.get_weapons(self.user)

            squad = []
            for i, weapon in enumerate(weapons, 1):
                if weapon == "none":
                    squad.append(f"{i} - [Empty]")
                else:
                    weapon_name = fns.get_item(weapon, "name", self.cur_lan)
                    squad.append(f"{i} - {weapon_name.displayname}")

            squad = "\n".join(squad)

            squad2 = []

            for i, item in enumerate(users[str(self.user.id)]["bundle"], 1):
                if item["item"] == "none":
                    squad2.append(f"{i} - [Empty]")
                else:
                    item_name = fns.get_item(item['item'], 'name', self.cur_lan)
                    squad2.append(f"{i} - {item['amount']} {item_name}")

            squad2 = "\n".join(squad2)

            hp = await fns.get_user_hp(self.user)
            embed = nextcord.Embed(title=f"{text['profile']} {self.user.name}", description=f"{hp} HP\n\n{text['your_weapons']}\n{squad}\n{text['your_bundle']}\n{squad2}", color=main.color_normal)
            embed.set_thumbnail(url=str(self.user.display_avatar))
            embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.edit_message(embed=embed)

        else:
            leng = await fns.lang(self.cur_lan)
            text = leng['commands']['profile']
            users = await fns.custommobs()
            user = self.user
            name = user.name
            lmit = main.custom_mobs_limits[users[str(user.id)]['rank']]
            embed = nextcord.Embed(title=f"{text['profile']} {name}", description=f"{text['imtoolazy']} {len(users[str(user.id)]['mobs'])}/{lmit}", color=main.color_normal)
            embed.set_thumbnail(url=str(self.user.display_avatar))
            reas = await fns.has_enabled(interaction.user, "debug_info")
            if reas is True:
                embed.add_field(name=text['dev'], value=f"**ID**: `{users[str(user.id)]['id']}`", inline=False)
                
            embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.edit_message(embed=embed)
            

class ProfileDropdownInitializer(nextcord.ui.View):
    def __init__(self, timeout, user, iuser, cur_lan, leng):
        self.iuser = iuser
        super().__init__(timeout=timeout)
        self.add_item(ProfileDropdown(user, cur_lan, leng))
        
    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.iuser:
            if interaction.user != self.iuser:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class QuestsDropdown(nextcord.ui.Select):
    def __init__(self, user, cur_lan, leng, embedz, parent, page):
        self.user = user
        self.cur_lan = cur_lan
        self.leng = leng
        self.parent = parent
        self.embedz = embedz
        self.page = page
        select_options = [
            nextcord.SelectOption(label=leng['label0']),
            nextcord.SelectOption(label=leng['label1']),
            nextcord.SelectOption(label=leng['label2']),
            nextcord.SelectOption(label=leng['label3'])
        ]
        super().__init__(placeholder=leng['placeholder'], min_values=1, max_values=1, options=select_options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == self.leng['label0']:
            num = 0
        elif self.values[0] == self.leng['label1']:
            num = 1
        elif self.values[0] == self.leng['label2']:
            num = 2
        else:
            num = 3

        embed = self.embedz[num][0]
        embed.set_footer(text=f"{self.page} 1/{len(self.embedz[num])} | {main.version[self.cur_lan]}")
        await self.parent.call_embed_change(num)
        if len(self.embedz[num]) == 1:
            for i in self.parent.children:
                if i == self:
                    continue
                i.disabled = True
        else:
            for i in self.parent.children:
                i.disabled = False
        await interaction.response.edit_message(embed=embed, view=self.parent)


class QuestsMenu(buttons.Pages):
    def __init__(self, timeout: float, lenght, embedz, user: nextcord.Member, custom_footer=None, page=None, leng=None, cur_lan=None):
        super().__init__(timeout, lenght, embedz[0], user, custom_footer, page, leng)
        self.embeds = embedz
        for i in self.children:
            i.row = 4
            if self.lenght == 1:
                i.disabled = True
        self.add_item(QuestsDropdown(user, cur_lan, leng['dropdown']['quests'], embedz, self, page))

    async def call_embed_change(self, index):
        self.embedz = self.embeds[index]
        self.current = 0
        self.lenght = len(self.embeds[index])

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True
   
   
class SettingsDropdown(nextcord.ui.Select):
    def __init__(self, user, cur_lan, leng, d):
        self.user = user
        self.cur_lan = cur_lan
        self.leng = leng
        self.parent = d
        select_options = [
            nextcord.SelectOption(label=leng['label0']),
            nextcord.SelectOption(label=leng['label1']),
            nextcord.SelectOption(label=leng['label2']),
            nextcord.SelectOption(label=leng['label3']),
        ]
        super().__init__(placeholder=leng['placeholder'], min_values=1, max_values=1, options=select_options)
        
    async def callback(self, interaction: nextcord.Interaction):
        settings = await fns.setting()
        leng = await fns.lang(self.cur_lan)
        text = leng['commands']['settings']

        if self.values[0] == self.leng['label0']:
            stats = (lambda x: main.accept if x == "enabled" else main.deny)(settings[str(self.user.id)]["multiplayer"])
            embed = nextcord.Embed(title=text['settings'], description=f"{text['multiplayer']} {stats}", color=main.color_normal)
            self.parent.value = 1
        elif self.values[0] == self.leng['label1']:
            stats = (lambda x: main.accept if x == "enabled" else main.deny)(settings[str(self.user.id)]["debug_info"])
            embed = nextcord.Embed(title=text['settings'], description=f"{text['dev_info']} {stats}", color=main.color_normal)
            self.parent.value = 2
        elif self.values[0] == self.leng['label2']:
            stats = (lambda x: main.accept if x == "enabled" else main.deny)(settings[str(self.user.id)]["dm_notifications"])
            embed = nextcord.Embed(title=text['settings'], description=f"{text['notif']} {stats}", color=main.color_normal)
            self.parent.value = 3
        else:
            stats = (lambda x: ":flag_pl:" if x == "pl" else ":flag_gb:")(settings[str(self.user.id)]["language"])
            embed = nextcord.Embed(title=text['settings'], description=f"{text['language']} {stats}", color=main.color_normal)
            self.parent.value = 4

        if self.values[0] == self.leng['label3']:
            self.parent.children[0].emoji = "🇵🇱"
            self.parent.children[1].emoji = "🇬🇧"
        else:
            self.parent.children[0].emoji = main.accept
            self.parent.children[1].emoji = main.deny

        embed.set_footer(text=main.version[self.cur_lan])
        await interaction.response.edit_message(embed=embed, view=self.parent)
    
        
class SettingsDropdownInitializer(nextcord.ui.View):
    def __init__(self, timeout, user, iuser, cur_lan, leng):
        self.iuser = iuser
        self.cur_lan = cur_lan
        super().__init__(timeout=timeout)
        self.add_item(SettingsDropdown(user, cur_lan, leng, self))
        self.value = 1
        self.list_of_settings = ["n", "multiplayer", "debug_info", "dm_notifications", "language"]
        
    @nextcord.ui.button(emoji=main.accept, style=nextcord.ButtonStyle.gray, row=2)
    async def yee(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        settings = await fns.setting()
        leng = await fns.lang(self.cur_lan)
        text = leng['commands']['settings']

        setting = self.list_of_settings[self.value]
        if setting != "language":
            settings[str(self.iuser.id)][setting] = "enabled"
        else:
            settings[str(self.iuser.id)][setting] = "pl"
        with open("userdb/settings.json", "w") as f:
            json.dump(settings, f)

        if self.value == 1:
            embed = nextcord.Embed(title=text['settings'], description=f"{text['multiplayer']} {main.accept}", color=main.color_normal)
            embed.set_footer(text=main.version[self.cur_lan])
        elif self.value == 2:
            embed = nextcord.Embed(title=text['settings'], description=f"{text['dev_info']} {main.accept}", color=main.color_normal)
            embed.set_footer(text=main.version[self.cur_lan])
        elif self.value == 3:
            embed = nextcord.Embed(title=text['settings'], description=f"{text['notif']} {main.accept}", color=main.color_normal)
            embed.set_footer(text=main.version[self.cur_lan])
        else:
            self.cur_lan = 'pl'
            leng = await fns.lang(self.cur_lan)
            text = leng['commands']['settings']
            embed = nextcord.Embed(title=text['settings'], description=f"{text['language']} :flag_pl:", color=main.color_normal)
            embed.set_footer(text=main.version[self.cur_lan])
        await interaction.response.edit_message(embed=embed)
    
    @nextcord.ui.button(emoji=main.deny, style=nextcord.ButtonStyle.gray, row=2)
    async def nah(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        settings = await fns.setting()
        leng = await fns.lang(self.cur_lan)
        text = leng['commands']['settings']

        setting = self.list_of_settings[self.value]
        if setting != "language":
            settings[str(self.iuser.id)][setting] = "disabled"
        else:
            settings[str(self.iuser.id)][setting] = "en"
        with open("userdb/settings.json", "w") as f:
            json.dump(settings, f)

        if self.value == 1:
            embed = nextcord.Embed(title=text['settings'], description=f"{text['multiplayer']} {main.deny}", color=main.color_normal)
            embed.set_footer(text=main.version[self.cur_lan])
        elif self.value == 2:
            embed = nextcord.Embed(title=text['settings'], description=f"{text['dev_info']} {main.deny}", color=main.color_normal)
            embed.set_footer(text=main.version[self.cur_lan])
        elif self.value == 3:
            embed = nextcord.Embed(title=text['settings'], description=f"{text['notif']} {main.deny}", color=main.color_normal)
            embed.set_footer(text=main.version[self.cur_lan])
        else:
            self.cur_lan = 'en'
            leng = await fns.lang(self.cur_lan)
            text = leng['commands']['settings']
            embed = nextcord.Embed(title=text['settings'], description=f"{text['language']} :flag_gb:", color=main.color_normal)
            embed.set_footer(text=main.version[self.cur_lan])
        await interaction.response.edit_message(embed=embed)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.iuser:
            if interaction.user != self.iuser:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True

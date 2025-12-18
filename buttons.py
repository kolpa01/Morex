import binascii
import nextcord
import json
import uuid
import base64
from nextcord import Interaction
import random
import main
import asyncio
import functions as fns
import morex
from morex import MorexItem, MorexEnemy
from morex.enums.enemies import MorexEnemyFlags, MorexEnemyTypes
import re


class Searching(nextcord.ui.Modal):
    def __init__(self, user, lenght, embedz, view, current=0, custom_footer=None, page=None, leng=None):
        super().__init__(
            leng[0],
        )

        self.place = nextcord.ui.TextInput(label=leng[1], min_length=1, max_length=3, required=True, placeholder=f"{leng[2]} {lenght}")
        self.add_item(self.place)
        self.user = user
        self.lenght = lenght
        self.embedz = embedz
        self.current = current
        self.view = view
        if custom_footer is None:
            self.footer = main.version
        else:
            self.footer = custom_footer
        if page is None:
            self.page = "Page"
        else:
            self.page = page
        self.language = leng[3]

    async def callback(self, interaction: Interaction):
        a = []
        for i in range(self.lenght):
            a.append(i)
        try:
            if int(self.place.value)-1 not in a:
                embed = nextcord.Embed(description=self.language, color=main.color_normal)
                embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
                embed.set_footer(text=self.footer)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        except (ValueError, TypeError):
            embed = nextcord.Embed(description=self.language, color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=self.footer)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        lol = self.place.value
        self.current = int(lol)-1

        a = self.current
        b = self.current + 1
        c = self.embedz[a]
        self.view.current = a
        c.set_footer(text=f"{self.page} {b}/{self.lenght} | {self.footer}")
        await interaction.response.edit_message(embed=c, view=self.view)


class LoadFight(nextcord.ui.Modal):
    """No Idea what i was drinking while decoding this
So Take this ASCII art of Morex
See source code to gaze upon Morex ASCII Art
In its full glory

        HHHH        HHHH
      HH  HH        HH  HH
    HH    HH        HH    HH
    HH  HH            HH  HH
  HH    HH            HH    HH
  HH    HH@@@@@@@@@@@@HH    HH
  HH  HH@@############@@HH  HH
  HHHH@@################@@HHHH
  HH@@####################@@HH
  @@######^^88####^^88######@@
  @@######^^88####^^88######@@
@@########8888####8888########@@
@@####IIII############IIII####@@
@@############################@@
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
    def __init__(self, user, interaction, cur_lan, leng):
        super().__init__(leng[0])

        self.place = nextcord.ui.TextInput(
            label=leng[1],
            min_length=0,
            max_length=4000,
            required=True,
            placeholder=leng[2]
        )
        self.add_item(self.place)
        self.user = user
        self.interaction = interaction
        self.cur_lan = cur_lan

    @staticmethod
    async def encode_int(thing, maximum):
        sus = ""
        temp = str(bin(thing)[2:])
        if len(temp) > maximum:
            raise ValueError
        for i in range(maximum - len(temp)):
            sus += "0"
        sus += temp
        return sus

    async def callback(self, interaction: Interaction) -> None:
        a = re.match("^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", self.place.value)
        if a is None:
            if str(interaction.user.id) == "826792866776219709":
                try:
                    saveobj = {"author": "0", "content": self.place.value, "version": "v1"}
                    cod = base64.b64decode(saveobj["content"].encode("utf-8")).decode("utf-8")
                    ddd = re.match("^[0-9a-f]{16}([0-9]{4}|f{4})[0-9]{4}[0-9a-f]{12}([0-9ia][0-9]{3}|f{4}){4}[0-9a-f]{2}([0-9ia][0-9]{3}|f{4}){4}[0-9a-f]{8}([0-9ia][0-9]{3}|f{4})[0-9a-f]{5}$", cod)

                    if ddd is None:
                        return
                    txt = cod
                except (binascii.Error, UnicodeDecodeError):
                    return
            else:
                return
        else:
            with open("userdb/battlesfrozenintime.json", "r") as f:
                sav = json.load(f)
            try:
                saveobj = sav[str(self.place.value)]
                txt = base64.b64decode(saveobj["content"].encode("utf-8")).decode("utf-8")
            except KeyError:
                return

        # 0066,0066,05dc,05dc,  \ffff/\0004/   0000,0300,0003,  \0035 FFFF 0035 0008/  09  \FFFF FFFF FFFF FFFF/ 000010
        # 77 | 0066,0066,00fa,00fa,  \ffff/\0002/   0000,0300,0003,  \0066 0066 0035 0008/  09  \ffff ffff ffff ffff/ 0000100
        # 87 | 0066,0066,00fa,00fa,  \ffff/\0002/   0000,0300,0003,  \0066 0066 0035 0008/  09  \ffff ffff ffff ffff/ 0000100 f \ffff/ 0066 0
        cpy = txt

        # u = [txt[i:i+4] for i in range(0, len(txt), 4)]
        # print(u)
        # hexin = ""
        stup = []
        cts = 4
        index = 0
        for i in txt:
            if index in [16, 17, 18, 19, 20, 21, 22, 23, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 78, 79, 80, 81]:
                if cts == 4:
                    stup.append(cpy[:4])
                    index += 1
                    cts = 3
                    cpy = cpy[1:]
                else:
                    index += 1
                    cts -= 1
                    cpy = cpy[1:]
                    if cts == 0:
                        # print("am i failure")
                        # index += 1
                        cts = 4
            else:
                if index in [74, 75, 76]:
                    if i == "1":
                        stup.append("0001")
                    else:
                        stup.append("0000")
                    cpy = cpy[1:]
                    index += 1
                else:
                    stup.append(await self.encode_int(int(i, 16), 4))
                    # print(await self.encode_int(int(i, 16), 4))
                    cpy = cpy[1:]

                    index += 1

        php = int(stup[0]+stup[1]+stup[2]+stup[3], 2)
        phpm = int(stup[4]+stup[5]+stup[6]+stup[7], 2)
        mhp = int(stup[8]+stup[9]+stup[10]+stup[11], 2)
        mhpm = int(stup[12]+stup[13]+stup[14]+stup[15], 2)

        if stup[16] == "ffff":
            mob = fns.get_morex_oponent("m"+stup[17][1:], 'id', self.cur_lan)
            mobo = mob.sid
            ctm = 0
            # mobs = await fnc.opponenttable()
            # for mob in mobs:
            #     if "m"+stup[17][1:] == mob["id"]:
            #         mgo = mob
            #         mobo = mob["name"]
            #         ctm = 0
            #         img = mob["image"]
            #         disname = mob["displayname"]
        else:
            mob = fns.get_morex_oponent((stup[16], "c"+stup[17][1:]), 'list', self.cur_lan)
            mobo = (stup[16], "c"+stup[17][1:])
            ctm = 1
            # mobs = await fnc.custommobs()
            # for usr in mobs:
            #     if mobs[usr]["id"] == stup[16]:
            #         for mob in mobs[usr]["mobs"]:
            #             if "c"+stup[17][1:] == mob["id"]:
            #                 mgo = mob
            #                 mobo = [stup[16], "c"+stup[17][1:]]
            #                 ctm = 1
            #                 img = mob["image"]
            #                 disname = mob["displayname"]

        # savefile.append(await self.encode_mob(self.opponent)) # 17 (16) (17)

        defe = int(stup[18]+stup[19]+stup[20]+stup[21], 2)
        defc = int(stup[22]+stup[23], 2)
        chur = int(stup[24]+stup[25], 2)
        wet = int(stup[26]+stup[27], 2)
        wetm = int(stup[28]+stup[29], 2)

        wep = fns.get_item(stup[30], 'id', self.cur_lan)

        if stup[31] == "ffff":
            wep1 = None
        else:
            wep1 = fns.get_item(stup[31], 'id', self.cur_lan)

        if stup[32] == "ffff":
            wep2 = None
        else:
            wep2 = fns.get_item(stup[32], 'id', self.cur_lan)

        if stup[33] == "ffff":
            wep3 = None
        else:
            wep3 = fns.get_item(stup[33], 'id', self.cur_lan)

        use = int(stup[34]+stup[35], 2)

        if stup[36] == "ffff":
            bun1 = "none"
        else:
            temp_item = fns.get_item(stup[36])
            bun1 = temp_item.sid

        if stup[37] == "ffff":
            bun2 = "none"
        else:
            temp_item = fns.get_item(stup[37])
            bun2 = temp_item.sid

        if stup[38] == "ffff":
            bun3 = "none"
        else:
            temp_item = fns.get_item(stup[38])
            bun3 = temp_item.sid

        if stup[39] == "ffff":
            bun4 = "none"
        else:
            temp_item = fns.get_item(stup[39])
            bun4 = temp_item.sid

        amt1 = int(stup[40], 2)
        amt2 = int(stup[41], 2)
        amt3 = int(stup[42], 2)
        amt4 = int(stup[43], 2)

        bun = [{"item": bun1, "amount": amt1}, {"item": bun2, "amount": amt2}, {"item": bun3, "amount": amt3}, {"item": bun4, "amount": amt4}]

        if stup[44] == "0001":
            eli = True
        else:
            eli = False

        if stup[45] == "0001":
            fro = True
        else:
            fro = False

        if stup[46] == "0001":
            fra = True
        else:
            fra = False

        if saveobj['version'] == 'v1':
            time_to = int(stup[47], 2)
            if stup[48] != 'ffff':
                weapon_back = fns.get_item(stup[48], 'id', self.cur_lan)
            else:
                weapon_back = None

            mob_sh = int(stup[49]+stup[50]+stup[51]+stup[52], 2)

            aasd = stup[53]
        else:
            time_to = 0
            weapon_back = None
            mob_sh = 0
            aasd = {}

        # mob_effects = {
        #     "e000": str(stup[53])
        # }

        ico = await fns.player_icon(interaction.user)

        bar1 = await fns.progress_bar(php, phpm)
        bar2 = await fns.progress_bar(mhp, mhpm)
        shbar = await fns.sheild(defe)
        leng = await fns.lang(self.cur_lan)
        xd = leng['commands']['hunt']
        embed = nextcord.Embed(title=xd['fight'], color=main.color_normal)
        embed.add_field(name=f"{mob.displayname}", value=f"{bar2}\n{mhp}/{mhpm} HP\n0 SH", inline=False)
        embed.add_field(name=f"{ico} {interaction.user.name}", value=f"{bar1}\n{php}/{phpm} HP\n{shbar} {defe} SH", inline=False)
        embed.add_field(name=xd['info'], value=xd['loaded'], inline=False)
        embed.set_thumbnail(url=mob.image)
        embed.set_footer(text=main.version[self.cur_lan])

        view = HuntButtons(360, php, mhp, phpm, mhpm, mobo, mob.image, wep, [wep1, wep2, wep3], defe, defc, chur, wet, wetm, use, bun, False, fro, eli, ["custom", ctm], ico, fra, mob, xd, self.cur_lan, main.color_normal, mob_sh, {}, time_to, weapon_back, interaction.user)
        for othervariable in view.children:
            if wep.toolatributes.itemtype != "spellbook" and othervariable == view.atks:
                othervariable.disabled = True
        await self.interaction.edit_original_message(embed=embed, view=view)


class HuntButtons(nextcord.ui.View):
    def __init__(
        self,
        timeout: float,
        player_hp: int,
        mob_hp: int,
        max_player_hp: int,
        max_mob_hp: int,
        mob_identifier,
        image_url: str,
        current_weapon: MorexItem,
        weapon_list: list,
        shield: int,
        shield_raise_remaining: int,
        spellbook_charge: int,
        weapon_changes: int,
        max_weapon_changes: int,
        bundle_item_uses: int,
        user_bundle: list,
        is_rewarded: bool,
        is_frozen: bool,
        is_eligible: bool,
        mode,
        icon: str,
        has_next_turn: bool,
        enemy_data: MorexEnemy,
        merged_langs: dict,
        current_lang: str,
        color,
        mob_sh,
        effects,
        weapon_disappears,
        temp_weapon,
        user: nextcord.Member = None,
        special=None
    ) -> None:
        super().__init__(timeout=timeout)

        self.player_hp = player_hp
        self.mob_hp = mob_hp
        self.player_max = max_player_hp
        self.mob_max = max_mob_hp

        self.opponent = mob_identifier
        self.user = user
        self.image = image_url
        self.defence = shield
        self.defence_count = shield_raise_remaining
        self.charging = spellbook_charge
        self.weapon_time = weapon_changes
        self.weapon = current_weapon
        self.pack = weapon_list
        self.mode = mode  # ["custom", 0] == customowa walka ze zwykłym mobem ["custom", 1] == customowa walka z customowym wrogiem
        self.icon = icon
        self.weapon_time_max = max_weapon_changes
        self.item_uses = bundle_item_uses
        self.bundle = user_bundle
        self.temporary_weapon = temp_weapon
        self.weapon_is_back = weapon_disappears

        self.mob_shield = mob_sh
        self.mob_effects = effects

        self.rewards = is_rewarded
        self.eligible = is_eligible
        self.nextturn = has_next_turn
        self.frozen = is_frozen
        self.enemy: MorexEnemy = enemy_data

        self.color = color
        self.cur_lan = current_lang
        self.language = merged_langs

        self.special = special

    async def get_correct_text(self, mode):
        mob_text = self.enemy.user_attacks[mode]

        try:
            text = mob_text[self.weapon.id]
        except KeyError:
            text = mob_text['default']

        return text

    async def get_info_text(self, text: str, ahp=None, ash=None, pw=None):
        text = text.replace('{u}', self.user.name)
        text = text.replace('{e}', self.enemy.disname)
        if ahp is not None:
            text = text.replace('{ahp}', str(ahp))
        if ash is not None:
            text = text.replace('{ash}', str(ash))
        if pw is not None:
            text = text.replace('{pw}', str(pw))
        if "{uw}" in text:
            text = text.replace('{uw}', self.weapon.displayname)
        return text

    async def manage_buttons(self, mode):
        if mode == "disable":
            for i in self.children:
                i.disabled = True
        else:
            for i in self.children:
                if self.weapon.toolatributes.itemtype != "spellbook" and i == self.atks:
                    continue
                i.disabled = False

    async def create_embed(self, interaction, details, embed_type=None):
        disname = self.enemy.displayname
        if embed_type == "death":
            self.image = "https://cdn.discordapp.com/attachments/1198440482087379054/1220427059029872690/Untitled_03-14-2024_10-52-26.png"
        bar1 = await fns.progress_bar(self.player_hp, self.player_max)
        bar2 = await fns.progress_bar(self.mob_hp, self.mob_max)
        shbar = await fns.sheild(self.defence)
        embed = nextcord.Embed(title=self.language['fight'], color=self.color)
        embed.add_field(name=f"{disname}", value=f"{bar2}\n{self.mob_hp}/{self.mob_max} HP\n0 SH", inline=False)
        embed.add_field(name=f"{self.icon} {interaction.user.name}", value=f"{bar1}\n{self.player_hp}/{self.player_max} HP\n{shbar} {self.defence} SH", inline=False)
        if embed_type == "krd":
            embed.add_field(name=self.language['dialogue'], value=self.special['idontwannadie']['text'], inline=False)
            self.image = self.special['idontwannadie']['icon']
        embed.add_field(name=self.language['info'], value=details, inline=False)
        embed.set_thumbnail(url=self.image)
        embed.set_footer(text=main.version[self.cur_lan])
        return embed

    async def player_death(self, interaction, mode):
        dis = self.enemy.disname
        if mode == "hp":
            embed = await self.create_embed(interaction, await self.get_info_text(self.enemy.deaths['hpdeath']), embed_type="death")
            await interaction.edit(embed=embed, view=self)
            self.stop()
        elif mode == "cursed":
            self.player_hp = 0
            await self.manage_buttons("disable")
            embed = await self.create_embed(interaction, await self.get_info_text(self.enemy.deaths['curseddeath']), embed_type="death")
            await interaction.edit(embed=embed, view=self)
            self.stop()
        elif mode == "beer":
            self.player_hp = 0
            await self.manage_buttons("disable")
            embed = await self.create_embed(interaction, await self.get_info_text(self.enemy.deaths['beerdeath']), embed_type="death")
            await interaction.edit(embed=embed, view=self)
            self.stop()
        else:
            embed = await self.create_embed(interaction, await self.get_info_text(self.enemy.deaths['hpandshdeath']), embed_type="death")
            await interaction.edit(embed=embed, view=self)
            self.stop()

    async def get_invincible_rewards(self):
        txt = []
        for i in self.enemy.drops:
            rnd = random.randint(1, 10000)
            if i["chance"] >= rnd:
                amount = random.randint(i["min_value"], i["max_value"])
                amount = amount // 2
                if amount:
                    reward = fns.get_item(i['item'], "name", self.cur_lan)
                    await reward.add_item(self.user, amount)
                    txt.append(f"{amount} {reward.displayname}")
        level = random.randint(self.enemy.xp[0], self.enemy.xp[1])
        level = level // 2
        if not level:
            level = 1
        await fns.add_xp(user=self.user, amount=level)
        txt.append(f"{level} XP")
        text = "\n".join(txt)

        return text

    async def get_structure(self, interaction, timeout_seconds: int):
        if self.mode[0] == "search":
            await asyncio.sleep(timeout_seconds)
            structure = fns.get_strucure(self.mode[1], self.cur_lan)
            embed = nextcord.Embed(title=structure.displayname, description=self.language['chest'], color=self.color)
            embed.set_footer(text=main.version[self.cur_lan])
            view = SearchChests(30, self.mode[2], self.user, structure, self.color)
            await interaction.edit(embed=embed, view=view)

    async def enemy_death(self, interaction):
        if self.mode[1] == 2 and self.mode[0] == "custom":
            self.mob_hp = 1
            embed = await self.create_embed(interaction, self.special['idontwannadie:followup']['text'], "krd")
            view = HuntTutorialButtons(360, interaction.user, self.icon, 4, self.cur_lan, self.color, self.special, self.language)
            view.atks.disabled = True
            await interaction.edit(embed=embed, view=view)
            self.stop()
            return
        if MorexEnemyFlags.INVINCIBLE in self.enemy.flags:
            self.mob_hp = 1
            embed = await self.create_embed(interaction, await self.get_info_text(self.enemy.deaths['escape']))
            rewards_text = await self.get_invincible_rewards()
            embed.add_field(name=self.language['rewards'], value=rewards_text, inline=False)
            await self.manage_buttons("disable")
            await interaction.edit(embed=embed, view=self)
            await self.get_structure(interaction, 5)
            self.stop()
            return
        self.mob_hp = 0
        for i in self.children:
            i.disabled = True
        disname = self.enemy.disname
        version = main.version[self.cur_lan]
        self.eligible = False
        if self.rewards is True:
            txt = []
            for i in self.enemy.drops:
                rnd = random.randint(1, 10000)
                if i["chance"] >= rnd:
                    reward = fns.get_item(i['item'], "name", self.cur_lan)
                    amount = random.randint(i["min_value"], i["max_value"])
                    await reward.add_item(interaction.user, amount)
                    txt.append(f"{amount} {reward.displayname}")
            level = random.randint(self.enemy.xp[0], self.enemy.xp[1])
            boost = await fns.has_event_boost('hunt_xp')
            level = boost * level
            await fns.add_xp(user=interaction.user, amount=level)
            txt.append(f"{level} XP")
            text = "\n".join(txt)

            embed = nextcord.Embed(title=f"{self.language['beaten']} {disname}", description=f"{self.language['got']}\n{text}", color=self.color)
            embed.set_thumbnail(url=self.image)
            embed.set_footer(text=version)
            await interaction.response.edit_message(embed=embed, view=None)

            await fns.update_stat(interaction.user, "hunt", 1)
            await fns.update_daily_task(interaction.user, "k", self.enemy.sid, 1)

            await self.get_structure(interaction, 2)
        else:
            embed = nextcord.Embed(title=f"{self.language['beaten']} {disname}", color=self.color)
            embed.set_thumbnail(url=self.image)
            embed.set_footer(text=version)
            await interaction.response.edit_message(embed=embed, view=None)

    async def enemy_turn(self, interaction, details=None):
        if self.nextturn is True:
            self.nextturn = False
            await self.manage_buttons("enable")
            await interaction.edit(view=self)
            return
        enemyatack = random.choice(self.enemy.attack)
        gg = None
        if enemyatack == 0:
            await self.manage_buttons("enable")
            embed = await self.create_embed(interaction, await self.get_info_text(self.enemy.enemy_attacks['failedmobattack']))
            await interaction.edit(embed=embed, view=self)
            return
        if self.defence == 0:
            gg = "hp"
        if gg == "hp":
            self.player_hp -= enemyatack
            if self.player_hp <= 0:
                self.player_hp = 0
                await self.player_death(interaction, "hp")
                return
            await self.manage_buttons("enable")
            embed = await self.create_embed(interaction, await self.get_info_text(self.enemy.enemy_attacks['hpmobattack'], ahp=enemyatack))
            await interaction.edit(embed=embed, view=self)
        else:
            self.defence -= enemyatack
            if self.defence == 0:
                await self.manage_buttons("enable")
                embed = await self.create_embed(interaction, await self.get_info_text(self.enemy.enemy_attacks['bshmobattack']))
                await interaction.edit(embed=embed, view=self)
            elif self.defence > 0:
                await self.manage_buttons("enable")
                embed = await self.create_embed(interaction, await self.get_info_text(self.enemy.enemy_attacks['shmobattack'], ash=enemyatack))
                await interaction.edit(embed=embed, view=self)
            else:
                bp = -1*self.defence
                self.player_hp += self.defence
                self.defence = 0
                if self.player_hp <= 0:
                    self.player_hp = 0
                    await self.player_death(interaction, "defence")
                else:
                    await self.manage_buttons("enable")
                    embed = await self.create_embed(interaction, await self.get_info_text(self.enemy.enemy_attacks['bshandhpmobattack'], ahp=bp))
                    await interaction.edit(embed=embed, view=self)

    async def get_shield(self, interaction):
        self.defence += 30
        self.defence_count -= 1
        await self.manage_buttons("disable")
        embed = await self.create_embed(interaction, await fns.text_replacer(self.language['sh_raise'], ['{u}', interaction.user.name]))
        await interaction.response.edit_message(embed=embed, view=self)
        await asyncio.sleep(2.5)
        await self.enemy_turn(interaction)
        return

    async def attack_mob_classic(self, interaction, atk, weapon_type, power=None):
        text = []
        if power is None:
            if atk == 0:
                text.append(await self.get_info_text(await self.get_correct_text('faileduserattack')))
            else:
                text.append(await self.get_info_text(await self.get_correct_text('baseuserattack'), ahp=atk))

            if weapon_type == "spellbook":
                if self.charging < 3:
                    self.charging += 1
                    if self.charging == 3:
                        text.append(await self.get_info_text(self.language['sp_charged']))
                    else:
                        text.append(await self.get_info_text(self.language['sp_charging']))
                else:
                    text.append(await self.get_info_text(self.language['sp_charged']))
        else:
            if weapon_type == "spellbookreb":
                text.append(await self.get_info_text(self.enemy.spells['reb'], ahp=atk))
            else:
                text.append(await self.get_info_text(self.enemy.spells['atk'], pw=power, ahp=atk))

        self.mob_hp -= atk
        if self.mob_hp > 0:
            await self.manage_buttons("disable")
            embed = await self.create_embed(interaction, "\n".join(text))
            await interaction.edit(embed=embed, view=self)
            await asyncio.sleep(2.5)
            await self.enemy_turn(interaction)
        else:
            await self.enemy_death(interaction)

    async def attack_handler(self, interaction, mode, item: MorexItem = None):
        version = main.version[self.cur_lan]

        if mode == "def":
            if self.defence_count != 0:
                await self.get_shield(interaction)
            else:
                embed = nextcord.Embed(description=self.language['sh_er'], color=self.color)
                embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
                embed.set_footer(text=version)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        elif mode == "atk":
            if self.weapon_is_back != 0:
                self.weapon_is_back -= 1
            else:
                if self.temporary_weapon is not None:
                    self.weapon = self.temporary_weapon
                    self.temporary_weapon = None

            if self.weapon.toolatributes.cursed == "y" or self.weapon.toolatributes.cursed in [1, 2, 3, 4, 5, 6]:
                x = random.randint(1, 10)
                if x in [1, 2, 3, 4]:
                    await self.player_death(interaction, "cursed")
                    return
            attack_value = random.choice(self.weapon.toolatributes.attack)
            type_weapon = self.weapon.toolatributes.itemtype

            await self.attack_mob_classic(interaction, attack_value, type_weapon)
        elif mode == "atk2":
            self.charging -= 3
            power_alias = f"{self.weapon.toolatributes.power.emoji} {self.weapon.toolatributes.power.name}"
            power_type = self.weapon.toolatributes.power.type
            if power_type == "atk":
                await self.attack_mob_classic(interaction, self.weapon.toolatributes.power.value, "spellbook", power_alias)
            elif power_type == "reb":
                attack_value = random.choice(self.weapon.toolatributes.attack)
                self.player_hp += attack_value
                await self.attack_mob_classic(interaction, attack_value, "spellbookreb", power_alias)
            elif power_type == "reg":
                reg_count = self.weapon.toolatributes.power.value
                self.player_hp += reg_count
                if self.player_hp > self.player_max:
                    reg_count = (self.player_max - self.player_hp) + reg_count
                    self.player_hp = self.player_max
                await self.manage_buttons("disable")
                if reg_count != 0:
                    tegzd = await self.get_info_text(self.language['regen'], ahp=reg_count)
                else:
                    tegzd = await self.get_info_text(self.language['regen_fail'])
                embed = await self.create_embed(interaction, tegzd)
                await interaction.edit(embed=embed, view=self)
                await asyncio.sleep(2.5)
                await self.enemy_turn(interaction)
        elif mode == "item":
            if item.toolatributes is False:
                return
            if item.toolatributes.type != "bundle":
                return

            result = [await self.on_bundle_item_use(item.toolatributes.power)]
            if item.toolatributes.bonus is not None:
                for power in item.toolatributes.bonus:
                    chance = random.randint(1, 10000)
                    if power.chance >= chance:
                        result.append(await self.on_bundle_item_use(power))

            ultimate_textbox = []
            prevent_enemy_turn = False
            for action in result:
                if action[0] == 'reg':
                    if action[1] is None:
                        ultimate_textbox.append(await self.get_info_text(self.language['regen_fail']))
                    else:
                        ultimate_textbox.append(await self.get_info_text(self.language['regen'], ahp=action[1]))
                elif action[0] == 'satk':
                    if action[1] is None:
                        await self.player_death(interaction, "beer")
                        return
                    else:
                        ultimate_textbox.append(await self.get_info_text(self.language['bundlehp'], ahp=action[1], pw=item.displayname))
                elif action[0] == 'time':
                    prevent_enemy_turn = True
                elif action[0] == 'def':
                    ultimate_textbox.append(await self.get_info_text(self.language['bundlesh'], ash=action[1], pw=item.displayname))
                elif action[0] == 'smw':
                    ultimate_textbox.append(await self.get_info_text(self.language['weaponreplace'], ash=action[1], pw=item.displayname))
            tegzd = " ".join(ultimate_textbox)
            embed = await self.create_embed(interaction, f"{await self.get_info_text(self.language['bundlebase'], pw=item.displayname)} {tegzd}")
            if not prevent_enemy_turn:
                await self.manage_buttons("disable")
            await interaction.edit(embed=embed, view=self)
            if not prevent_enemy_turn:
                await asyncio.sleep(2.5)
                await self.enemy_turn(interaction)

    async def on_bundle_item_use(self, power):
        if power.type == "reg":
            reg_count = power.value
            self.player_hp += reg_count
            if self.player_hp > self.player_max:
                reg_count = (self.player_max - self.player_hp) + reg_count
                self.player_hp = self.player_max
            if reg_count != 0:
                return ['reg', reg_count]
            else:
                return ['reg', None]
        elif power.type == "satk":
            self.player_hp -= power.value
            if self.player_hp <= 0:
                return ['satk', None]
            return ['satk', power.value]
        elif power.type == "time":
            self.nextturn = True
            return ['time', 1]
        elif power.type == "def":
            self.defence += power.value
            return ['def', power.value]
        elif power.type == "smw":
            # that's a bit complicated
            if self.temporary_weapon is None:
                self.temporary_weapon = self.weapon
            self.weapon_is_back = 5
            self.weapon = fns.get_item(power.value, 'id', self.cur_lan)
            return ['smw', 1]
        else:
            return

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_Sword:1220425813132836904>')
    async def fight(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.eligible is False:
            return
        await self.attack_handler(interaction, "atk")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_Shield:1220425815368400926>')
    async def defence(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.eligible is False:
            return
        await self.attack_handler(interaction, "def")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_NoIdeaWhatIsThis:1220425816794599604>')
    async def atks(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.eligible is False:
            return

        if self.weapon.toolatributes.itemtype == "spellbook" and self.charging >= 3:
            await self.attack_handler(interaction, "atk2")
            pass
        else:
            if self.weapon.toolatributes.itemtype == "spellbook":
                embed = nextcord.Embed(description=self.language['sp_wait'], color=self.color)
                embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
                embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            else:
                await interaction.response.send_message("Ta broń tego nie obsługuje", ephemeral=True)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_Bundle:1220425818321191004>', row=2)
    async def itembag(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.eligible is False:
            return
        if self.mode[0] != "custom":
            inventory = await fns.get_inv_data()
            if self.bundle != inventory[str(interaction.user.id)]["bundle"]:
                return
        if self.item_uses == 0:
            return
        await self.sisyphus_boom(interaction)

    async def sisyphus_boom(self, interaction, sis=False):
        confirmation_ui = BundleChoices(60, interaction.user)
        confirmation_ui.nahaa.label = self.language['cancel']
        if self.item_uses == 1:
            ran = f"1" + f" {self.language['time']}"
        else:
            ran = f"{self.item_uses}" + f" {self.language['times']}"

        bundle_list = []
        for i, bundle_items in enumerate(self.bundle):
            if bundle_items['item'] != "none":
                item = fns.get_item(self.bundle[i]["item"], "name", self.cur_lan)
                bundle_list.append(f"{i+1} - {str(self.bundle[i]['amount'])} " + item.displayname)
            else:
                bundle_list.append(f"{i+1} - [Empty]")

        text = '\n'.join(bundle_list)
        embed = nextcord.Embed(title=self.language['bundle'], description=f"{self.language['use']} {ran}\n\n{text}", color=self.color)
        embed.set_footer(text=main.version[self.cur_lan])
        if sis is False:
            await interaction.response.send_message(embed=embed, view=confirmation_ui, ephemeral=True)
            self.frozen = True
        elif sis is True:
            embed.add_field(name=self.language['error'], value=self.language['empty'])
            await interaction.edit_original_message(embed=embed, view=confirmation_ui)
        await confirmation_ui.wait()

        if confirmation_ui.value is None:
            try:
                await interaction.delete_original_message()
            except Exception as e:
                print(e)
            self.frozen = False
            return
        else:
            if self.item_uses == 0:
                return

            if self.bundle[confirmation_ui.value]["item"] == "none":
                await self.sisyphus_boom(interaction, True)
                return

            await interaction.delete_original_message()
            self.item_uses -= 1
            if self.mode[0] != "custom":
                a = await fns.get_inv_data()
                if self.bundle != a[str(interaction.user.id)]["bundle"]:
                    return
            self.frozen = False
            self.bundle[confirmation_ui.value]["amount"] -= 1
            its_a = fns.get_item(self.bundle[confirmation_ui.value]["item"], 'name', self.cur_lan)
            if self.bundle[confirmation_ui.value]["amount"] == 0:
                self.bundle[confirmation_ui.value]["item"] = "none"
            if self.mode[0] != "custom":
                await fns.bundle_remove_item(interaction.user, 1, False, confirmation_ui.value)
            await self.attack_handler(interaction, "item", its_a)
            return

    # What this function does is basically
    # https://youtube.com/shorts/x340VY4J6HQ
    # nothing more, nothing less

    async def sisyphus(self, interaction, sis):
        confirmation_ui = WeaponChoices(30, interaction.user)
        confirmation_ui.nahaa.label = self.language['cancel']

        if self.weapon_time_max - self.weapon_time == 1:
            ran = f"{self.weapon_time_max - self.weapon_time}" + f" {self.language['time']}"
        else:
            ran = f"{self.weapon_time_max - self.weapon_time}" + f" {self.language['times']}"

        weapons = []
        for i, weapon in enumerate(self.pack, 1):
            if weapon is None:
                weapons.append(f"{i} - [Empty]")
            else:
                weapons.append(f"{i} {weapon}")
        text = "\n".join(weapons)
        embed = nextcord.Embed(title=self.language['change'], description=f"{self.language['use_wp']} {ran}\n\n{text}\n\n{self.language['cur_wp']} {self.weapon}\n\n{self.language['reset']}", color=self.color)
        embed.set_footer(text=main.version[self.cur_lan])
        if sis is False:
            await interaction.response.send_message(embed=embed, view=confirmation_ui, ephemeral=True)
            self.frozen = True
        elif sis == "erm":
            embed.add_field(name=self.language['error'], value=self.language['empty'])
            await interaction.edit_original_message(embed=embed, view=confirmation_ui)
        else:
            embed.add_field(name=self.language['error'], value=self.language['equiped'])
            await interaction.edit_original_message(embed=embed, view=confirmation_ui)
        await confirmation_ui.wait()

        if confirmation_ui.value is None:
            try:
                await interaction.delete_original_message()
            except Exception as e:
                print(e)
            self.frozen = False
            return
        else:
            if self.weapon_time == self.weapon_time_max:
                return
            if self.weapon == self.pack[confirmation_ui.value]:
                await self.sisyphus(interaction, True)
            else:
                if self.pack[confirmation_ui.value] is None:
                    await self.sisyphus(interaction, "erm")
                    return
                self.weapon = self.pack[confirmation_ui.value]
                await interaction.delete_original_message()
                self.weapon_time += 1
                self.charging = 0
                self.temporary_weapon = None
                self.weapon_is_back = 0
                self.frozen = False
                return

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_Change:1220425820279931020>', row=2)
    async def weaponchange(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.eligible is False:
            return
        if self.weapon_time == self.weapon_time_max:
            return
        await self.sisyphus(interaction, False)

    @nextcord.ui.button(style=nextcord.ButtonStyle.red, emoji='<:MX_Shoe:1220425823555682404>', row=2)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.eligible is False:
            return
        if self.mode == ["custom", 2]:
            self.image = self.special['idontbitedoi']['icon']
            embed = await self.create_embed(interaction, self.special['idontbitedoi']['text'])
            self.image = self.special['idontbitedoi:followup']['icon']
            await interaction.response.edit_message(embed=embed)
            return

        view = ConfirmationButtons(60, self.user)
        embed = nextcord.Embed(title=self.language['warn'], description=self.language['run_confirm'], color=self.color)
        embed.set_footer(text=main.version[self.cur_lan])
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        self.frozen = True
        await view.wait()
        if view.value is None or view.value is False:
            self.frozen = False
            await interaction.delete_original_message()
            return

        self.frozen = False
        await interaction.delete_original_message()

        await self.manage_buttons("disable")
        self.eligible = False
        embed = await self.create_embed(interaction, self.language['ran'])
        await interaction.edit(embed=embed, view=self)
        self.stop()

    @staticmethod
    async def encode_itm(thing):
        if thing == "none" or thing is None:
            return "ffff"
        if type(thing) is MorexItem:
            return thing.id
        cd = fns.get_item(thing, "name")
        return cd.id

    @staticmethod
    async def encode_bol(thing):
        if thing is True:
            return "0001"
        elif thing is False:
            return "0000"

    @staticmethod
    async def encode_int(thing, maximum):
        sus = ""
        temp = str(bin(thing)[2:])
        if len(temp) > maximum:
            raise ValueError
        for i in range(maximum - len(temp)):
            sus += "0"
        sus += temp
        return sus

    async def encode_mob(self, thing):
        cd = ""
        if self.mode[0] != "custom":
            cd += "ffff"
            cd += "0"
            cd += str(self.enemy.id)[1:]
            return cd
        else:
            if self.mode[1] == 0:
                cd += "ffff"
                cd += "0"
                cd += str(self.enemy.id)[1:]
                return cd
            else:
                # I'll do it later
                cd += thing[0]
                cd += "0"
                cd += str(thing[1])[1:]
                return cd

    @nextcord.ui.button(style=nextcord.ButtonStyle.gray, emoji='<:MX_Save:1220425821559455836>', row=3)
    async def save(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.eligible is False:
            return
        if self.mode[1] == 2 and self.mode[0] == "custom":
            embed = await self.create_embed(interaction, self.language['tutorial'])
            await interaction.response.edit_message(embed=embed)
            return

        view = ConfirmationButtons(60, self.user)
        embed = nextcord.Embed(title=self.language['warn'], description=self.language['save_confirm'], color=self.color)
        embed.set_footer(text=main.version[self.cur_lan])
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        self.frozen = True
        await view.wait()
        if view.value is None or view.value is False:
            self.frozen = False
            await interaction.delete_original_message()
            return

        self.frozen = False
        await interaction.delete_original_message()
        savefile = [
            await self.encode_int(self.player_hp, 16),
            await self.encode_int(self.player_max, 16),
            await self.encode_int(self.mob_hp, 16),
            await self.encode_int(self.mob_max, 16),
            await self.encode_mob(self.opponent),
            await self.encode_int(self.defence, 16),
            await self.encode_int(self.defence_count, 8),
            await self.encode_int(self.charging, 8),
            await self.encode_int(self.weapon_time, 8),
            await self.encode_int(self.weapon_time_max, 8),
            await self.encode_itm(self.weapon),
            await self.encode_itm(self.pack[0]),
            await self.encode_itm(self.pack[1]),
            await self.encode_itm(self.pack[2]),
            await self.encode_int(self.item_uses, 8),
            await self.encode_itm(self.bundle[0]["item"]),
            await self.encode_itm(self.bundle[1]["item"]),
            await self.encode_itm(self.bundle[2]["item"]),
            await self.encode_itm(self.bundle[3]["item"]),
            await self.encode_int(self.bundle[0]["amount"], 4),
            await self.encode_int(self.bundle[1]["amount"], 4),
            await self.encode_int(self.bundle[2]["amount"], 4),
            await self.encode_int(self.bundle[3]["amount"], 4),
            await self.encode_bol(self.eligible),
            await self.encode_bol(self.frozen),
            await self.encode_bol(self.nextturn),
            await self.encode_int(self.weapon_is_back, 4),
            await self.encode_itm(self.temporary_weapon),
            await self.encode_int(self.mob_shield, 16),
            "0000"
        ]

        txt = ""
        for i in savefile:
            txt += i

        u = [txt[i:i+4] for i in range(0, len(txt), 4)]
        hexin = ""

        index = 0
        for i in u:
            if index in [16, 17, 30, 31, 32, 33, 36, 37, 38, 39, 48]:
                hexin += i
            else:
                te = int(i, 2)
                ouaa = str(hex(te))[2:]
                hexin += ouaa
            index += 1
        uu = hexin.encode("utf-8")
        code = base64.b64encode(uu)
        au = code.decode("utf-8")

        with open("userdb/battlesfrozenintime.json", "r") as f:
            sav = json.load(f)
        uid = uuid.uuid4()
        sav[str(uid)] = {}
        sav[str(uid)]["author"] = str(interaction.user.id)
        sav[str(uid)]["content"] = au
        sav[str(uid)]["version"] = "v1"

        with open("userdb/battlesfrozenintime.json", "w") as f:
            json.dump(sav, f)
        self.eligible = False
        embed = nextcord.Embed(title=self.language['saved'], description=str(uid), color=self.color)
        embed.set_footer(text=main.version[self.cur_lan])
        await interaction.edit(embed=embed, view=None)
        self.stop()

    @nextcord.ui.button(style=nextcord.ButtonStyle.gray, emoji='<:MX_Upload:1217191336449540247>', row=3)
    async def load(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.eligible is False:
            return
        if self.mode[1] == 2 and self.mode[0] == "custom":
            embed = await self.create_embed(interaction, self.language['tutorial'])
            await interaction.response.edit_message(embed=embed)
            return
        leng = await fns.lang(self.cur_lan)
        await interaction.response.send_modal(LoadFight(self.user, interaction, self.cur_lan, [leng['modals']['load_fight']['header'], leng['modals']['load_fight']['code'], leng['modals']['load_fight']['write']]))

    @nextcord.ui.button(style=nextcord.ButtonStyle.gray, emoji='<:MX_Info:1217191323015184536>', row=3)
    async def info(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.eligible is False:
            return
        if self.mode[1] == 2 and self.mode[0] == "custom":
            embed = await self.create_embed(interaction, self.language['tutorial'])
            await interaction.response.edit_message(embed=embed)
            return
        reas = await fns.has_enabled(interaction.user, "debug_info")
        if reas is False:
            return

        embed = nextcord.Embed(title="Debug Info", description=f"Name: {self.user.name}\nIcon: {self.icon}", color=self.color)
        embed.add_field(name="User Fight Data", value=f"<:MX_Heart:1259099939963666503> {self.player_hp}/{self.player_max}HP\n<:MX_Shield:1220425815368400926> {self.defence} SH\n<:MX_Shield:1220425815368400926> {self.defence_count} SHC\n<:MX_NoIdeaWhatIsThis:1220425816794599604> {self.charging} CRG\n<:MX_Change:1220425820279931020> {self.weapon_time}/{self.weapon_time_max} WPC")
        abc = (lambda x: main.accept if x is True else main.deny)
        embed.add_field(name="Booleans", value=f"{abc(self.rewards)} RAD\n{abc(self.eligible)} ELI\n{abc(self.nextturn)} NXT\n{abc(self.frozen)} FRZ", inline=False)
        embed.set_thumbnail(url=self.image)

        squad = f""
        xoxo = 0
        for i in self.pack:
            if i is None:
                squad += f"{xoxo+1} - [Empty]\n"
                pass
            else:
                squad += f"{xoxo+1} - {i.displayname}\n"

            xoxo += 1

        cntr = 0
        tegzd = f""
        for it in self.bundle:
            if it["item"] == "none":
                tegzd += f"{cntr+1} - [Empty]\n"
            else:
                item = fns.get_item(it['item'], "name", self.cur_lan)
                tegzd += f"{cntr+1} - {it['amount']} {item.displayname}\n"
            cntr += 1

        mewing = nextcord.Embed(title="Debug Info", color=self.color)
        mewing.add_field(name="Weapons", value=f"<:MX_Sword:1220425813132836904> {self.weapon}\n{squad}", inline=False)
        mewing.add_field(name="Swapped Weapons", value=f"<:MX_Sword:1220425813132836904> {self.temporary_weapon if self.temporary_weapon is not None else '[Empty]'}\n<:MX_QuestionMark:1266370987474288764> {self.weapon_is_back}", inline=False)
        mewing.add_field(name="Bundle", value=f"<:MX_Bundle:1220425818321191004> {self.item_uses} BNA\n{tegzd}", inline=False)

        embed3 = nextcord.Embed(title="Debug Info", description=f"<:MX_Heart:1259099939963666503> {self.mob_hp}/{self.mob_max}\n<:MX_QuestionMark:1266370987474288764> {self.opponent}", color=self.color)
        embed3.add_field(name=f"{self.enemy.disname}", value=f"```{self.enemy.meetup}```\n<:MX_Info:1217191323015184536> {self.enemy.displayname}\n<:MX_Heart:1259099939963666503> {self.enemy.hp}\n<:MX_Sword:1220425813132836904> {self.enemy.attack[0]}/{self.enemy.attack[1]}/{self.enemy.attack[2]}", inline=False)
        if self.enemy.drops is not None and self.enemy.xp is not None:
            # <:MX_XP:1266372378473005320>
            embed3.set_field_at(0, name=embed3.fields[0].name, value=str(embed3.fields[0].value) + f"\n<:MX_XP:1266372378473005320> {self.enemy.xp[0]}-{self.enemy.xp[1]}")
            p = []
            # {"item": "scorpclaw", "min_value": 1, "max_value": 3, "chance": 10000}
            for dumb in self.enemy.drops:
                item = fns.get_item(dumb['item'], "name", self.cur_lan)
                if dumb['min_value'] == dumb['max_value']:
                    drop_amount = str(dumb['min_value'])
                else:
                    drop_amount = f"{dumb['min_value']}-{dumb['max_value']}"
                tempstr = f"{item.displayname} {drop_amount} {dumb['chance']/100}%\n"
                p.append(tempstr)

            dasd = ''.join(p)

            embed3.add_field(name="Item", value=dasd, inline=False)
        embed3.add_field(name=f"Development Informations", value=f"**ID**: `{self.enemy.id}`\n**SID**: `{self.enemy.sid}`", inline=False)
        embed3.set_thumbnail(url=self.enemy.image)

        debme = nextcord.Embed(title="Debug Info", description=str(self.mode), color=self.color)
        ccc = nextcord.Embed(title="Debug Info", description=f"**EXPERIMENTAL**\n\nMOB_SH = {self.mob_shield}\n\nEFFECTS = {self.mob_effects}", color=self.color)

        leng = await fns.lang(self.cur_lan)
        pag = leng['other']['pages']['page']
        view = DebugCli(180, 5, [embed, mewing, embed3, debme, ccc], self.user, f"{main.version_number} | {self.user.id}", pag, leng, self)
        # view = Pages(180, 5, [embed, mewing, embed3, debme, ccc], self.user, f"{main.version_number} | {self.user.id}", pag, leng)

        embed.set_footer(text=f"Strona 1/5 | {main.version_number} | {self.user.id}")
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
            else:
                if self.frozen is True:
                    embed = nextcord.Embed(description=self.language['frozen'], color=self.color)
                    embed.set_author(name=self.user.name, icon_url=str(self.user.display_avatar))
                    embed.set_footer(text=main.version[self.cur_lan])
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return False
        return True


class Pages(nextcord.ui.View):
    def __init__(self, timeout: float, lenght, embedz, user: nextcord.Member, custom_footer=None, page=None, leng=None, row=None) -> None:
        super().__init__(timeout=timeout)
        self.lenght = int(lenght)
        self.embedz = embedz
        self.current = 0
        self.user = user
        if custom_footer is None:
            self.footer = main.version
        else:
            self.footer = custom_footer
        if page is None:
            self.page = "Page"
        else:
            self.page = page
        self.language = leng  # why are you being fed whole language file

    @nextcord.ui.button(emoji=main.farleft, style=nextcord.ButtonStyle.gray, row=1)
    async def farleft(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.current = 0
        a = self.current
        b = self.current + 1
        c = self.embedz[a]
        c.set_footer(text=f"{self.page} {b}/{self.lenght} | {self.footer}")
        await interaction.response.edit_message(embed=c, view=self)

    @nextcord.ui.button(emoji=main.left, style=nextcord.ButtonStyle.gray, row=1)
    async def left(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        if self.current == 0:
            self.current = self.lenght - 1
        else:
            self.current -= 1
        a = self.current
        b = self.current + 1
        c = self.embedz[a]
        c.set_footer(text=f"{self.page} {b}/{self.lenght} | {self.footer}")
        await interaction.response.edit_message(embed=c, view=self)

    @nextcord.ui.button(emoji=main.magnifier, style=nextcord.ButtonStyle.gray, row=1)
    async def skearch(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(modal=Searching(interaction.user, self.lenght, self.embedz, self, self.current, self.footer, self.page, [self.language['modals']['search']['title'], self.language['modals']['search']['label'], self.language['modals']['search']['placeholder'], self.language['other']['invalid_value']['description']]))

    @nextcord.ui.button(emoji=main.right, style=nextcord.ButtonStyle.gray, row=1)
    async def right(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.current == self.lenght-1:
            self.current = 0
        else:
            self.current += 1
        a = self.current
        b = self.current + 1
        c = self.embedz[a]
        c.set_footer(text=f"{self.page} {b}/{self.lenght} | {self.footer}")
        await interaction.response.edit_message(embed=c, view=self)

    @nextcord.ui.button(emoji=main.farright, style=nextcord.ButtonStyle.gray, row=1)
    async def farright(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.current = self.lenght-1
        a = self.current
        b = self.current + 1
        c = self.embedz[a]
        c.set_footer(text=f"{self.page} {b}/{self.lenght} | {self.footer}")
        await interaction.response.edit_message(embed=c, view=self)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class CliResolve(nextcord.ui.Modal):
    """
    I absolutely hate this feature.
    Not because it is hard or boring.
    Just because I'm not feeling too well right now.
    And I need to pour my hate somewhere.

    Update: It sucks. The feature obviously.
    """
    def __init__(self, user, parent):
        super().__init__(
            "Command Line",
        )
        self.user = user
        self.place = nextcord.ui.TextInput(label="Insert command", min_length=0, max_length=256, required=True, placeholder=f"{self.user.name}@morex:~$")
        self.parent = parent
        self.add_item(self.place)
        self.registered_commands = ["help", "echo", "cv", "secret"]
        self.options = {
            "cv": [
                "putsomethingheretoavoidoffbyoneerrors",
                "str",
                "any"
            ],
            "secret": [
                "a",
                "str"
            ]
        }
        self.please_kill_me_already = {
            "player_hp": [self.parent.player_hp, "int"],  # just player HP
            "mob_hp": [self.parent.mob_hp, "int"],  # just enemy HP
            "player_max": [self.parent.player_max, "int"],  # maximal HP that player can get
            "mob_max": [self.parent.mob_max, "int"],  # maximal HP that enemy can get
            "opponent": [self.parent.opponent, "str", "root"],  # that is the thing that figures out what mob to save; mob sid for normal mobs, tuple with custom mobs author id and mob id for custom mobs
            "user": [self.parent.user, "int", "root"],  # that the user who uses interaction... no idea why'd anyone want to change it
            "image": [self.parent.image, "str", "root"],  # image displayed during the fight
            "defence": [self.parent.defence, "int"],  # amount of SH that user has
            "defence_count": [self.parent.defence_count, "int"],  # how much times user can raise their shield
            "charging": [self.parent.charging, "int"],  # the charge of the user's spellbook; pretty much useless when user uses sword
            "weapon_time": [self.parent.weapon_time, "int"],  # im sorry for what ive done here... if this is the same as "weapon_time_max" you cannot change your weapon again... dont ask me why; increases by 1 everytime user swaps the weapon
            "weapon": [self.parent.weapon, "str", "root"],  # current weapon used by a user; item id gets turned into the MorexItem
            "pack": [self.parent.pack, "str", "root"],  # note: this isnt a bundle, its for some reason, the list that contains the user's weapons
            "mode": [self.parent.mode, "str", "root"],  # anything that will be put here will be turned into the list, i don't care what will happen
            "icon": [self.parent.icon, "str"],  # icon displayed next to a user's name during a battle
            "weapon_time_max": [self.parent.weapon_time_max, "int"],  # maximal amount of times that user can change their weapon
            "item_uses": [self.parent.item_uses, "int"],  # how much times you can use items from bundle
            "bundle": [self.parent.bundle, "str", "root"],
            "temporary_weapon": [self.parent.temporary_weapon, "str", "root"],
            "weapon_is_back": [self.parent.weapon_is_back, "int"],
            "mob_shield": [self.parent.mob_shield, "int"],
            "mob_effects": [self.parent.mob_effects, "str", "root"],
            "rewards": [self.parent.rewards, "bool", "root"],
            "eligible": [self.parent.eligible, "bool", "root"],
            "nextturn": [self.parent.nextturn, "bool"],
            "frozen": [self.parent.frozen, "bool", "root"],
            "enemy": [self.parent.enemy, "str", "root"],
            "color": [self.parent.color, "int"],
            "cur_lan": [self.parent.cur_lan, "str", "root"],
            "language": [self.parent.language, "str", "root"],
            "special": [self.parent.special, "str", "root"]
        }

    async def assign(self, variable, value):
        if variable not in self.please_kill_me_already:
            return None
        elif variable == 'player_hp':
            self.parent.player_hp = value
        elif variable == 'mob_hp':
            self.parent.mob_hp = value
        elif variable == 'player_max':
            self.parent.player_max = value
        elif variable == 'mob_max':
            self.parent.mob_max = value
        elif variable == 'opponent':
            a = value.split(";")
            if len(a) > 1:
                self.parent.opponent = (a[0], a[1])
            else:
                self.parent.opponent = a[0]
        elif variable == 'user':
            self.parent.user = value
        elif variable == 'image':
            self.parent.image = value
        elif variable == 'defence':
            self.parent.defence = value
        elif variable == 'defence_count':
            self.parent.defence_count = value
        elif variable == 'charging':
            self.parent.charging = value
        elif variable == 'weapon_time':
            self.parent.weapon_time = value
        elif variable == 'weapon':
            self.parent.weapon = value
        elif variable == 'pack':
            self.parent.pack = value
        elif variable == 'mode':
            self.parent.mode = value
        elif variable == 'icon':
            self.parent.icon = value
        elif variable == 'weapon_time_max':
            self.parent.weapon_time_max = value
        elif variable == 'item_uses':
            self.parent.item_uses = value
        elif variable == 'bundle':
            self.parent.bundle = value
        elif variable == 'temporary_weapon':
            self.parent.temporary_weapon = value
        elif variable == 'weapon_is_back':
            self.parent.weapon_is_back = value
        elif variable == 'mob_shield':
            self.parent.mob_shield = value
        elif variable == 'mob_effects':
            self.parent.mob_effects = value
        elif variable == 'rewards':
            self.parent.rewards = value
        elif variable == 'eligible':
            self.parent.eligible = value
        elif variable == 'nextturn':
            self.parent.nextturn = value
        elif variable == 'frozen':
            self.parent.frozen = value
        elif variable == 'enemy':
            self.parent.enemy = value
        elif variable == 'color':
            self.parent.color = value
        elif variable == 'cur_lan':
            self.parent.cur_lan = value
        elif variable == 'language':
            self.parent.language = value
        elif variable == 'special':
            self.parent.special = value

    async def stdout(self, output):
        embed = nextcord.Embed(description=f"```{self.user.name}@morex:~${self.place.value}\n{output}```", color=main.color_normal)
        embed.set_footer(text=main.version['en'])
        return embed

    async def validate_options(self, command):
        if len(self.options[command[0]]) < len(command):
            return "too_long"
        elif len(self.options[command[0]]) > len(command):
            return "too_short"
        parsed_values = []
        for i, v in enumerate(self.options[command[0]]):
            if v == "str":
                try:
                    str(command[i])
                except ValueError:
                    return f"wrong_type {i}"
            elif v == "int":
                try:
                    int(command[i])
                except ValueError:
                    return f"wrong_type {i}"
            elif v == "any":
                pass
            else:
                continue
            parsed_values.append(command[i])
        return parsed_values

    async def callback(self, interaction: Interaction):
        breakdown = self.place.value.split(" ")
        if breakdown[0] not in self.registered_commands:
            await interaction.response.send_message(embed=await self.stdout(f"{breakdown[0]}: command not found"), ephemeral=True)
            return
        elif breakdown[0] == "help":
            await interaction.response.send_message(embed=await self.stdout("This is a help message."), ephemeral=True)
            return
        elif breakdown[0] == "echo":
            await interaction.response.send_message(embed=await self.stdout(" ".join(breakdown[1:])), ephemeral=True)
            return
        a = await self.validate_options(breakdown)
        if breakdown[0] == "cv":
            if str(interaction.user.id) != "826792866776219709":
                self.parent.rewards = False
            try:
                the_thing = self.please_kill_me_already[breakdown[1]]
                try:
                    try:
                        _a = the_thing[2]
                        if str(interaction.user.id) != "826792866776219709":
                            await interaction.response.send_message(embed=await self.stdout(f"{breakdown[0]}: Permission denied"), ephemeral=True)
                            return
                    except IndexError:
                        pass
                    if the_thing[1] == "int":
                        value = int(breakdown[2])
                        display_value = value
                    elif the_thing[1] == "bool":
                        value = True if breakdown[2] == "1" or breakdown[2].lower() is True else False
                        display_value = value
                    else:
                        value = breakdown[2]
                        display_value = value
                    await self.assign(breakdown[1], value)
                    await interaction.response.send_message(embed=await self.stdout(f"Changed '{breakdown[1]}' to '{display_value}'"), ephemeral=True)
                    return
                except ValueError:
                    await interaction.response.send_message(embed=await self.stdout(f"{breakdown[0]}: '{breakdown[2]}' is not a valid value for {breakdown[1]}"), ephemeral=True)
                    return
            except KeyError:
                await interaction.response.send_message(embed=await self.stdout(f"{breakdown[0]}: variable '{breakdown[1]}' does not exist"), ephemeral=True)
                return
        elif breakdown[0] == "secret":
            if breakdown[1] == "act":
                await interaction.response.send_message(embed=await self.stdout(f"We shall meet soon... {interaction.user.name}..."), ephemeral=True)
                return
            await interaction.response.send_message(embed=await self.stdout(f"{breakdown[0]}: command not found"), ephemeral=True)
            return


class DebugCli(Pages):
    def __init__(self, timeout: float, lenght, embedz, user: nextcord.Member, custom_footer=None, page=None, leng=None, parent=None) -> None:
        super().__init__(timeout, lenght, embedz, user, custom_footer, page, leng)
        self.user = user
        self.parent = parent  # the battle ui
        self.language = leng  # just whole language file

    @nextcord.ui.button(emoji='<:MX_CommandLine:1322222539619176459>', style=nextcord.ButtonStyle.gray, row=2)
    async def command_line(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(CliResolve(self.user, self.parent))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class MerchantShop(nextcord.ui.View):
    def __init__(self, timeout: float, user: nextcord.Member, place, merchant, color, lang, lang_full) -> None:
        super().__init__(timeout=timeout)
        self.user = user
        self.merchant: morex.MorexMerchant = merchant
        self.place = place
        self.times = merchant.times
        self.color = color
        self.cur_lan = lang
        self.text = lang_full

    async def get_merchant_tasks(self):
        user_merchant_tasks = await fns.get_merchant_tasks()
        merchant_tasks = await fns.merchant_tasks()

        free_slots = 3
        add_quests = True

        if add_quests:
            for i in merchant_tasks[str(self.merchant.id)]['permanent']:
                if free_slots == 0:
                    add_quests = False
                    break
                if i in user_merchant_tasks[str(self.user.id)][str(self.merchant.id)]['pr']['completed']:
                    continue
                if i in user_merchant_tasks[str(self.user.id)][str(self.merchant.id)]['pr']['ongoing']:
                    continue
                free_slots -= 1

        if add_quests:
            for i in merchant_tasks[str(self.merchant.id)]['random']:
                if free_slots == 0:
                    break
                if i in user_merchant_tasks[str(self.user.id)][str(self.merchant.id)]['rd']:
                    continue
                free_slots -= 1

    async def get_merchant_offers(self):
        offers = []
        for i, item in enumerate(self.merchant.offer, 1):
            if i == 1:
                emote = main.one
            elif i == 2:
                emote = main.two
            elif i == 3:
                emote = main.three
            elif i == 4:
                emote = main.four
            elif i == 5:
                emote = main.five
            else:
                emote = main.six
            price_item = fns.get_item(item['priceitem'], 'name', self.cur_lan)
            m_item = fns.get_item(item['item'], 'name', self.cur_lan)
            offers.append(f"**{emote} {self.text['price']} - {item['price']} {price_item}**\n<:MX_Empty:1306308101389029478> {item['amount']} {m_item}")
        offers = "\n".join(offers)
        embed = nextcord.Embed(title=self.text['shop'], description=f"**{self.merchant.displayname}:**\n{random.choice(self.merchant.in_shop)}\n\n{offers}", color=self.color)
        embed.set_thumbnail(url=self.merchant.icon)
        embed.set_footer(text=main.version[self.cur_lan])
        return embed

    async def baj(self, item: int, interaction: nextcord.Interaction):
        offering = self.merchant.offer[item]

        price_item = fns.get_item(offering['priceitem'], 'name', self.cur_lan)
        has_item = await price_item.get_amount(interaction.user, offering['price'])

        if has_item is None or has_item is False:
            embed = nextcord.Embed(description=f"{self.text['notenough']} {price_item}", color=self.color)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        bought_item = fns.get_item(offering['item'], 'name', self.cur_lan)

        await bought_item.add_item(self.user, offering['amount'])
        await price_item.remove_item(self.user, offering['price'])

        self.times -= 1

        desc = [f"**{self.merchant.displayname}:**\n{random.choice(self.merchant.bought)}\n\n{self.text['bought']} {offering['amount']} {bought_item}"]

        if self.times != 0:
            if self.times == 1:
                desc.append(await fns.text_replacer(self.text['enter_again'], ["{amount}", self.times], ["{times}", self.text['time']]))
            else:
                desc.append(await fns.text_replacer(self.text['enter_again'], ["{amount}", self.times], ["{times}", self.text['times']]))

        desc = "\n\n".join(desc)
        embed = nextcord.Embed(title=self.text['shop'], description=desc, color=self.color)
        embed.set_thumbnail(url=self.merchant.icon)
        embed.set_footer(text=main.version[self.cur_lan])

        if bought_item.sid == "torch":
            await fns.update_quest(interaction.user, ["chapter1", "shoppbaj"], 1, self.cur_lan)
        await fns.update_daily_task(interaction.user, "s", "mer", 1)
        confirmationui = ConfirmationButtons(60, self.user)
        if self.times == 0:
            await interaction.edit(embed=embed, view=None)
            return
        await interaction.edit(embed=embed, view=confirmationui)
        await confirmationui.wait()

        if confirmationui.value is None or confirmationui.value is False:
            embed = nextcord.Embed(title=self.text['shop'], description=f"**{self.merchant.displayname}:**\n{random.choice(self.merchant.exit_shop)}", color=self.color)
            embed.set_thumbnail(url=self.merchant.icon)
            embed.set_footer(text=main.version[self.cur_lan])
            await interaction.edit_original_message(embed=embed, view=None)
            return
        else:
            new_embed = await self.get_merchant_offers()
            await interaction.edit_original_message(embed=new_embed, view=self)

    @nextcord.ui.button(emoji=main.one, style=nextcord.ButtonStyle.blurple)
    async def yee(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.baj(0, interaction)
        pass

    @nextcord.ui.button(emoji=main.two, style=nextcord.ButtonStyle.blurple)
    async def naha(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.baj(1, interaction)
        pass

    @nextcord.ui.button(emoji=main.three, style=nextcord.ButtonStyle.blurple)
    async def nahb(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.baj(2, interaction)
        pass

    @nextcord.ui.button(emoji=main.four, style=nextcord.ButtonStyle.blurple, row=2)
    async def nahc(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.baj(3, interaction)
        pass

    @nextcord.ui.button(emoji=main.five, style=nextcord.ButtonStyle.blurple, row=2)
    async def nahd(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.baj(4, interaction)
        pass

    @nextcord.ui.button(emoji=main.six, style=nextcord.ButtonStyle.blurple, row=2)
    async def nahe(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.baj(5, interaction)
        pass

    # @nextcord.ui.button(emoji=main.empty, style=nextcord.ButtonStyle.blurple, row=2)
    # async def get_tasks(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    #     pass

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class SearchChests(nextcord.ui.View):
    def __init__(self, timeout: float, mode, user: nextcord.Member, structure, color) -> None:
        super().__init__(timeout=timeout)
        self.user = user
        self.mode = mode
        self.structure = structure
        self.color = color

    async def give_items(self, interaction, chosen_chest):
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['search']

        if chosen_chest == 'empty':
            embed = nextcord.Embed(title=self.structure.disname, description=text['empty'], color=self.color)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.edit(embed=embed, view=None)
            return
        txt = []
        for reward in chosen_chest:
            if reward["item"] == "coins":
                coins = random.randint(reward["amount"][0], reward["amount"][1])
                if coins == 0:
                    continue
                await fns.update_bank(self.user, coins)
                txt.append(f"{coins} {main.coin}")
            else:
                amount = random.randint(reward["amount"][0], reward["amount"][1])
                if amount == 0:
                    continue
                item = fns.get_item(reward['item'], 'name', cur_lan)
                await item.add_item(self.user, amount)
                txt.append(f"{amount} {item}")
        txt = "\n".join(txt)
        embed = nextcord.Embed(title=self.structure.disname, description=f"{text['found']}\n\n{txt}", color=self.color)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.edit(embed=embed, view=None)
        await fns.update_stat(self.user, "search", 1)
        await fns.update_daily_task(self.user, "s", "chest", 1)

    @nextcord.ui.button(emoji=main.one, style=nextcord.ButtonStyle.blurple)
    async def one(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        random.shuffle(self.mode)
        numero = self.mode[0]
        await self.give_items(interaction, numero)

    @nextcord.ui.button(emoji=main.two, style=nextcord.ButtonStyle.blurple)
    async def two(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        random.shuffle(self.mode)
        numero = self.mode[1]
        await self.give_items(interaction, numero)

    @nextcord.ui.button(emoji=main.three, style=nextcord.ButtonStyle.blurple)
    async def three(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        random.shuffle(self.mode)
        numero = self.mode[2]
        await self.give_items(interaction, numero)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class FightButtons(nextcord.ui.View):
    def __init__(self, timeout: float, player, second_player, mode, cur_lan, language) -> None:
        super().__init__(timeout=timeout)
        self.player_hp = [player["hp"], second_player["hp"]]
        self.player_max = [player["hp"], second_player["hp"]]
        self.user = [player["user"], second_player["user"]]
        self.defence = [0, 0]
        self.defence_count = [5, 5]
        self.charging = [0, 0]
        self.weapon = [player["weapon"], second_player["weapon"]]
        self.icon = [player["icon"], second_player["icon"]]
        self.eligible = [True, True]

        self.image = "https://cdn.discordapp.com/attachments/1198440482087379054/1220427058623156285/aaaa.aaaa.png"

        self.turn = player["user"]

        self.cur_lan = cur_lan
        self.language = language

    async def get_info_text(self, text: str, ahp=None, ash=None, pw=None):
        if self.turn == self.user[0]:
            usr = self.user[0]
            enm = self.user[1]
            i = 0
        else:
            usr = self.user[1]
            enm = self.user[0]
            i = 1

        text = text.replace('{u}', usr.name)
        text = text.replace('{e}', enm.name)
        if ahp is not None:
            text = text.replace('{ahp}', str(ahp))
        if ash is not None:
            text = text.replace('{ash}', str(ash))
        if pw is not None:
            text = text.replace('{pw}', str(pw))
        if "{uw}" in text:
            text = text.replace('{uw}', self.weapon[i].displayname)
        return text

    async def change_turn(self, interaction):
        for i in self.children:
            i.disabled = True
        await interaction.edit(view=self)
        await asyncio.sleep(1)

        if self.turn == self.user[0]:
            self.second_fight.disabled = False
            self.second_defence2.disabled = False
            self.second_power.disabled = False
            self.second_cancel.disabled = False

            if self.weapon[1].toolatributes.itemtype != "spellbook":
                self.second_power.disabled = True

            self.turn = self.user[1]
        else:
            self.fight.disabled = False
            self.defence2.disabled = False
            self.powerb.disabled = False
            self.cancel.disabled = False

            if self.weapon[0].toolatributes.itemtype != "spellbook":
                self.second_power.disabled = True

            self.turn = self.user[0]

        await interaction.edit(view=self)

    async def manage_buttons(self):
        for i in self.children:
            i.disabled = True

    async def create_embed(self, details):
        bar1 = await fns.progress_bar(self.player_hp[0], self.player_max[0])
        bar2 = await fns.progress_bar(self.player_hp[1], self.player_max[1])
        shb1 = await fns.sheild(self.defence[0])
        shb2 = await fns.sheild(self.defence[1])
        embed = nextcord.Embed(title=self.language['fight'], color=main.color_normal)
        embed.add_field(name=f"{self.icon[0]} {self.user[0].name}", value=f"{bar1} {self.player_hp[0]}/{self.player_max[0]} HP\n{shb1} {self.defence[0]} SH", inline=False)
        embed.add_field(name=f"{self.icon[1]} {self.user[1].name}", value=f"{bar2} {self.player_hp[1]}/{self.player_max[1]} HP\n{shb2} {self.defence[1]} SH", inline=False)
        embed.add_field(name=self.language['info'], value=details, inline=False)
        embed.set_thumbnail(url=self.image)
        embed.set_footer(text=main.version[self.cur_lan])
        return embed

    async def player_death(self, interaction, mode):
        if self.turn == self.user[0]:
            victim = self.user[1]
            i = 0
        else:
            victim = self.user[0]
            i = 1
        if mode == "hp":
            await self.manage_buttons()
            embed = await self.create_embed(await self.get_info_text(self.language['hpdeath']))
            await interaction.edit(embed=embed, view=self)
            self.stop()
        elif mode == "cursed":
            self.player_hp[i] = 0
            await self.manage_buttons()
            embed = await self.create_embed(await self.get_info_text(self.language['cursed']))
            await interaction.edit(embed=embed, view=self)
            self.stop()
        else:
            await self.manage_buttons()
            embed = await self.create_embed(await self.get_info_text(self.language['hpandshdeath']))
            await interaction.edit(embed=embed, view=self)
            self.stop()

    async def attack_mob_classic(self, interaction, atk, weapon_type, power=None):
        if self.turn == self.user[0]:
            i = 1
            ii = 0
            victim = self.user[1]
        else:
            i = 0
            ii = 1
            victim = self.user[0]
        text = []
        if power is None:
            if atk == 0:
                await self.manage_buttons()
                embed = await self.create_embed(await self.get_info_text(self.language['faileduserattack']))
                await interaction.edit(embed=embed, view=self)
                return
            gg = None
            if self.defence[i] == 0:
                gg = "hp"
            if gg == "hp":
                self.player_hp[i] -= atk
                if self.player_hp[i] <= 0:
                    self.player_hp[i] = 0
                    await self.player_death(interaction, "hp")
                    return
                text.append(await self.get_info_text(self.language['hpmobattack'], ahp=atk))
            else:
                self.defence[i] -= atk
                if self.defence[i] == 0:
                    text.append(await self.get_info_text(self.language['bshmobattack']))
                elif self.defence[i] > 0:
                    text.append(await self.get_info_text(self.language['shmobattack'], ash=atk))
                else:
                    bp = -1 * self.defence[i]
                    self.player_hp[i] += self.defence[i]
                    self.defence[i] = 0
                    if self.player_hp[i] <= 0:
                        self.player_hp[i] = 0
                        await self.player_death(interaction, "defence")
                        return
                    else:
                        text.append(await self.get_info_text(self.language['bshandhpmobattack'], ahp=bp))

            if weapon_type == "spellbook":
                if self.charging[ii] < 3:
                    self.charging[ii] += 1
                    if self.charging[ii] == 3:
                        text.append(await self.get_info_text(self.language['sp_charged']))
                    else:
                        text.append(await self.get_info_text(self.language['sp_charging']))
                else:
                    text.append(await self.get_info_text(self.language['sp_charged']))
        else:
            if weapon_type == "spellbookreb":
                text.append(await self.get_info_text(self.language['reb'], ahp=atk))
            else:
                text.append(await self.get_info_text(self.language['atk'], pw=power, ahp=atk))

        await self.manage_buttons()
        embed = await self.create_embed("\n".join(text))
        await interaction.edit(embed=embed, view=self)
        await self.change_turn(interaction)

    async def get_shield(self, interaction):
        if self.turn == self.user[0]:
            i = 0
        else:
            i = 1
        self.defence[i] += 30
        self.defence_count[i] -= 1

        embed = await self.create_embed(await fns.text_replacer(self.language['sh_raise'], ["{u}", self.turn.name]))
        await interaction.edit(embed=embed)
        await self.change_turn(interaction)

    async def classic(self, interaction):
        if self.turn == self.user[0]:
            i = 0
        else:
            i = 1

        version = main.version[self.cur_lan]

        if self.defence_count[i] != 0:
            await self.get_shield(interaction)
        else:
            embed = nextcord.Embed(description=self.language['sh_er'], color=main.color_normal)
            embed.set_author(name=self.turn.name, icon_url=str(self.turn.display_avatar))
            embed.set_footer(text=version)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

    async def attack_handler(self, interaction, mode):
        if self.turn == self.user[0]:
            i = 0
            victim = self.user[1]
        else:
            i = 1
            victim = self.user[0]

        version = main.version[self.cur_lan]

        if mode == "atk":
            if self.weapon[i].toolatributes.cursed == "y" or self.weapon[i].toolatributes.cursed in [1, 2, 3, 4, 5, 6]:
                x = random.randint(1, 10)
                if x in [1, 2, 3, 4]:
                    await self.player_death(interaction, "cursed")
                    return
            attack_value = random.choice(self.weapon[i].toolatributes.attack)
            type_weapon = self.weapon[i].toolatributes.itemtype
            await self.attack_mob_classic(interaction, attack_value, type_weapon)
        elif mode == "atk2":
            self.charging[i] -= 3
            power_alias = f"{self.weapon[i].toolatributes.power.emoji} {self.weapon[i].toolatributes.power.name}"
            power_type = self.weapon[i].toolatributes.power.type
            if power_type == "atk":
                await self.attack_mob_classic(interaction, self.weapon[i].toolatributes.power.value, "spellbook", power_alias)
            elif power_type == "reb":
                attack_value = random.choice(self.weapon[i].toolatributes.attack)
                self.player_hp[i] += attack_value
                await self.attack_mob_classic(interaction, attack_value, "spellbookreb", power_alias)
            elif power_type == "reg":
                reg_count = self.weapon[i].toolatributes.power.value
                self.player_hp[i] += reg_count
                if self.player_hp[i] > self.player_max[i]:
                    reg_count = (self.player_max[i] - self.player_hp[i]) + reg_count
                    self.player_hp[i] = self.player_max[i]
                if reg_count != 0:
                    tegzd = await self.get_info_text(self.language['regen'], ahp=reg_count)
                else:
                    tegzd = await self.get_info_text(self.language['regen_fail'])
                embed = await self.create_embed(tegzd)
                await interaction.edit(embed=embed, view=self)
                await self.change_turn(interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_Sword:1220425813132836904>')
    async def fight(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.attack_handler(interaction, "atk")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_Shield:1220425815368400926>')
    async def defence2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.classic(interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_NoIdeaWhatIsThis:1220425816794599604>')
    async def powerb(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        print(self.charging)
        if self.weapon[0].toolatributes.itemtype == "spellbook" and self.charging[0] >= 3:
            await self.attack_handler(interaction, "atk2")
        else:
            if self.weapon[0].toolatributes.itemtype == "spellbook":
                await interaction.response.send_message(self.language['sp_wait'], ephemeral=True)
            else:
                await interaction.response.send_message("Ta broń tego nie obsługuje", ephemeral=True)

    @nextcord.ui.button(style=nextcord.ButtonStyle.red, emoji='<:MX_Shoe:1220425823555682404>')
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_buttons()
        embed = await self.create_embed(f"{self.turn.name} uciekł od walki.")
        await interaction.edit(embed=embed, view=self)
        self.stop()

    @nextcord.ui.button(style=nextcord.ButtonStyle.grey, emoji='<:MX_Sword:1220425813132836904>', row=2)
    async def second_fight(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.attack_handler(interaction, "atk")

    @nextcord.ui.button(style=nextcord.ButtonStyle.gray, emoji='<:MX_Shield:1220425815368400926>', row=2)
    async def second_defence2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.classic(interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.gray, emoji='<:MX_NoIdeaWhatIsThis:1220425816794599604>', row=2)
    async def second_power(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.weapon[1].toolatributes.itemtype == "spellbook" and self.charging[1] >= 3:
            await self.attack_handler(interaction, "atk2")
        else:
            if self.weapon[1].toolatributes.itemtype == "spellbook":
                await interaction.response.send_message(self.language['sp_wait'], ephemeral=True)
            else:
                await interaction.response.send_message("Ta broń tego nie obsługuje", ephemeral=True)

    @nextcord.ui.button(style=nextcord.ButtonStyle.red, emoji='<:MX_Shoe:1220425823555682404>', row=2)
    async def second_cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_buttons()
        embed = await self.create_embed(f"{self.turn.name} {self.language['ran']}")
        await interaction.edit(embed=embed, view=self)
        self.stop()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.turn:
            if interaction.user != self.turn:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class ConfirmationButtons(nextcord.ui.View):
    def __init__(self, timeout: float, user: nextcord.Member) -> None:
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None

    @nextcord.ui.button(emoji=main.accept, style=nextcord.ButtonStyle.gray)
    async def yee(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

    @nextcord.ui.button(emoji=main.deny, style=nextcord.ButtonStyle.gray)
    async def nah(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        self.stop()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class WeaponChoices(nextcord.ui.View):
    def __init__(self, timeout: float, user: nextcord.Member) -> None:
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None

    @nextcord.ui.button(emoji=main.one, style=nextcord.ButtonStyle.gray)
    async def yee(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 0
        self.stop()

    @nextcord.ui.button(emoji=main.two, style=nextcord.ButtonStyle.gray)
    async def nah(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 1
        self.stop()

    @nextcord.ui.button(emoji=main.three, style=nextcord.ButtonStyle.gray)
    async def naha(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 2
        self.stop()

    @nextcord.ui.button(label="Zrezygnuj", style=nextcord.ButtonStyle.red, row=2)
    async def nahaa(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = None
        self.stop()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class BundleChoices(nextcord.ui.View):
    def __init__(self, timeout: float, user: nextcord.Member) -> None:
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None

    @nextcord.ui.button(emoji=main.one, style=nextcord.ButtonStyle.gray)
    async def yee(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 0
        self.stop()

    @nextcord.ui.button(emoji=main.two, style=nextcord.ButtonStyle.gray)
    async def nah(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 1
        self.stop()

    @nextcord.ui.button(emoji=main.three, style=nextcord.ButtonStyle.gray)
    async def naha(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 2
        self.stop()

    @nextcord.ui.button(emoji=main.four, style=nextcord.ButtonStyle.gray)
    async def nahao(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 3
        self.stop()

    @nextcord.ui.button(label="Zrezygnuj", style=nextcord.ButtonStyle.red, row=2)
    async def nahaa(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = None
        self.stop()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class NineNumbers(nextcord.ui.View):
    def __init__(self, timeout: float, user: nextcord.Member) -> None:
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None

    @nextcord.ui.button(emoji=main.one, style=nextcord.ButtonStyle.gray)
    async def yee(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 0
        self.stop()

    @nextcord.ui.button(emoji=main.two, style=nextcord.ButtonStyle.gray)
    async def nah(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 1
        self.stop()

    @nextcord.ui.button(emoji=main.three, style=nextcord.ButtonStyle.gray)
    async def naha(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 2
        self.stop()

    @nextcord.ui.button(emoji=main.four, style=nextcord.ButtonStyle.gray, row=2)
    async def nahao(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 3
        self.stop()

    @nextcord.ui.button(emoji=main.five, style=nextcord.ButtonStyle.gray, row=2)
    async def nahaodsa(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 4
        self.stop()

    @nextcord.ui.button(emoji=main.six, style=nextcord.ButtonStyle.gray, row=2)
    async def nahaoasd(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 5
        self.stop()

    @nextcord.ui.button(emoji=main.seven, style=nextcord.ButtonStyle.gray, row=3)
    async def nahaobbbbb(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 6
        self.stop()

    @nextcord.ui.button(emoji=main.eight, style=nextcord.ButtonStyle.gray, row=3)
    async def nahaoaaaaa(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 7
        self.stop()

    @nextcord.ui.button(emoji=main.nine, style=nextcord.ButtonStyle.gray, row=3)
    async def nahaoaaaaaaaaaa(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = 8
        self.stop()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class Dialogues(nextcord.ui.View):
    def __init__(self, timeout: float, user, mapper, dict_a, cur_lan, choices=None, preservance=None) -> None:
        super().__init__(timeout=timeout)
        self.map = mapper
        if choices is None:
            self.current_choices = []
        else:
            self.current_choices = choices
        self.user = user
        self.dialogues = dict_a
        self.cur_lan = cur_lan
        if preservance is None:
            self.preserve = self.children
        else:
            self.preserve = preservance

    async def handler(self, choice, interaction: Interaction):
        self.current_choices = []
        self.children = self.preserve

        if choice != 'return:true':
            for i, choices in enumerate(self.map[choice]):
                if i == 0:
                    self.current_choices.append(self.map[choice][choices])
                elif i == 1:
                    self.current_choices.append(self.map[choice][choices])
                elif i == 2:
                    self.current_choices.append(self.map[choice][choices])
                elif i == 3:
                    self.current_choices.append(self.map[choice][choices])

                self.children = self.children[:len(self.map[choice])]

        if 'END' in self.current_choices:
            self.children = []

        if 'exec' in self.dialogues[choice]:
            for execution in self.dialogues[choice]['exec']:
                if execution == 'add_event':
                    await fns.add_event(interaction.user, self.dialogues[choice]['exec'][execution])
                elif execution == 'lock':
                    for button in self.dialogues[choice]['exec'][execution]:
                        self.children[button].disabled = True
                elif execution == 'add_item':
                    item: MorexItem = fns.get_item(self.dialogues[choice]['exec'][execution][0], 'name', self.cur_lan)
                    await item.add_item(interaction.user, self.dialogues[choice]['exec'][execution][1])
                elif execution == 'add_xp':
                    await fns.add_xp(interaction.user, self.dialogues[choice]['exec'][execution])
                elif execution == 'update_quest':
                    await fns.update_quest(interaction.user, self.dialogues[choice]['exec'][execution][0], self.dialogues[choice]['exec'][execution][1], self.cur_lan)

        if choice == 'return:true':
            await self.action_after_dialogue(interaction, self.dialogues[choice]['name'])
            return

        embed = nextcord.Embed(title=self.dialogues[choice]['name'], description=self.dialogues[choice]['text'], color=int(self.dialogues[choice]['color'], 16))
        embed.set_thumbnail(self.dialogues[choice]['icon'])
        embed.set_footer(text=main.version[self.cur_lan])
        await interaction.edit(embed=embed, view=self)

    async def action_after_dialogue(self, interaction, action):
        if action == 'hunt_tutorial':
            tutorial_text = await fns.dialogues('v1_hunt_tutorial', self.cur_lan)
            leng = await fns.lang(self.cur_lan)
            text = leng['commands']['hunt']
            plin = await fns.playerinfo()
            ico = await fns.player_icon(interaction.user)
            php = plin[str(interaction.user.id)]["hp"]
            bar1 = await fns.progress_bar(php, php)
            embed = nextcord.Embed(title=text['fight'], color=int(tutorial_text['firsttime']['color'], 16))
            embed.add_field(name=tutorial_text['firsttime']['name'], value=f"{bar1}\n200/200 HP\n0 SH", inline=False)
            embed.add_field(name=f"{ico} {interaction.user.name}", value=f"{bar1}\n{php}/{php} HP\n0 SH", inline=False)
            embed.add_field(name=text['dialogue'], value=tutorial_text['firsttime']['text'], inline=False)
            embed.add_field(name=text['info'], value=text['press_any'], inline=False)
            embed.set_thumbnail(url=tutorial_text['firsttime']['icon'])
            embed.set_footer(text=main.version[self.cur_lan])
            view = HuntTutorialButtons(360, interaction.user, ico, 0, self.cur_lan, int(tutorial_text['firsttime']['color'], 16), tutorial_text, text)
            view.atks.disabled = True
            await interaction.response.edit_message(embed=embed, view=view)

    @nextcord.ui.button(label=".")
    async def one(self, button: nextcord.ui.Button, interaction: Interaction):
        for i, choices in enumerate(self.map[self.current_choices[0]]):
            if i == 0:
                self.one.label = choices
            elif i == 1:
                self.two.label = choices
            elif i == 2:
                self.three.label = choices
            elif i == 3:
                self.four.label = choices
        await self.handler(self.current_choices[0], interaction)

    @nextcord.ui.button(label=".")
    async def two(self, button: nextcord.ui.Button, interaction: Interaction):
        for i, choices in enumerate(self.map[self.current_choices[1]]):
            if i == 0:
                self.one.label = choices
            elif i == 1:
                self.two.label = choices
            elif i == 2:
                self.three.label = choices
            elif i == 3:
                self.four.label = choices
        await self.handler(self.current_choices[1], interaction)

    @nextcord.ui.button(label=".")
    async def three(self, button: nextcord.ui.Button, interaction: Interaction):
        for i, choices in enumerate(self.map[self.current_choices[2]]):
            if i == 0:
                self.one.label = choices
            elif i == 1:
                self.two.label = choices
            elif i == 2:
                self.three.label = choices
            elif i == 3:
                self.four.label = choices
        await self.handler(self.current_choices[2], interaction)

    @nextcord.ui.button(label=".")
    async def four(self, button: nextcord.ui.Button, interaction: Interaction):
        for i, choices in enumerate(self.map[self.current_choices[3]]):
            if i == 0:
                self.one.label = choices
            elif i == 1:
                self.two.label = choices
            elif i == 2:
                self.three.label = choices
            elif i == 3:
                self.four.label = choices
        await self.handler(self.current_choices[3], interaction)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class HuntTutorialButtons(nextcord.ui.View):
    def __init__(self, timeout: float, user, ico, syp, cur_lan, color, defaults, parents) -> None:
        super().__init__(timeout=timeout)
        self.enabled = []
        self.step = syp
        self.enemy_max = 200
        self.enemy_hp = 200
        self.user = user
        self.icon = ico
        self.current_language = cur_lan
        self.color = color
        self.language = defaults
        self.texts = parents

    async def skip(self, interaction: Interaction):
        self.step = 1
        self.enabled = ["atk"]
        bar1 = await fns.progress_bar(1, 1)
        bar2 = await fns.progress_bar(self.enemy_hp, self.enemy_max)
        embed = nextcord.Embed(title=self.texts['fight'], color=int(self.language['beatmeupplease']['color'], 16))
        embed.add_field(name=self.language['beatmeupplease']['name'], value=f"{bar2}\n{self.enemy_hp}/200 HP\n0 SH", inline=False)
        embed.add_field(name=f"{self.icon} {interaction.user.name}", value=f"{bar1}\n100/100 HP\n0 SH", inline=False)
        embed.add_field(name=self.texts['dialogue'], value=self.language['beatmeupplease']['text'], inline=False)
        embed.add_field(name=self.texts['info'], value=self.language['beatmeupplease:followup']['text'], inline=False)
        embed.set_thumbnail(url=self.language['beatmeupplease']['icon'])
        embed.set_footer(text=main.version[self.current_language])
        await interaction.response.edit_message(embed=embed, view=self)

    async def figjt(self, interaction: Interaction):
        bar1 = await fns.progress_bar(1, 1)
        bar2 = await fns.progress_bar(self.enemy_hp, self.enemy_max)

        embed = nextcord.Embed(title=self.texts['fight'], color=int(self.language['waitareyouforreal']['color'], 16))
        embed.add_field(name=self.language['waitareyouforreal']['name'], value=f"{bar2}\n{self.enemy_hp}/200 HP\n0 SH", inline=False)
        embed.add_field(name=f"{self.icon} {interaction.user.name}", value=f"{bar1}\n100/100 HP\n<:MX_Shield6:1221159173602021546> 30 SH", inline=False)
        embed.add_field(name=self.texts['info'], value=self.language['waitareyouforreal']['text'], inline=False)
        embed.set_thumbnail(url=self.language['waitareyouforreal']['icon'])
        embed.set_footer(text=main.version[self.current_language])

        weapon = fns.get_item("ironsword", 'name', self.current_language)
        weapons = [weapon, None, None]

        enemy = fns.get_morex_oponent('m012', lang_str=self.current_language)

        view = HuntButtons(360, 100, 170, 100, 200, "kordelia", "https://cdn.discordapp.com/attachments/1222203424389599232/1260951036613492840/tutorialgworl.png", weapon, weapons, 30, 3, 0, 0, 3, 9, [{'item': 'none', 'amount': 0}, {'item': 'none', 'amount': 0}, {'item': 'none', 'amount': 0}, {'item': 'none', 'amount': 0}], False, False, True, ["custom", 2], self.icon, False, enemy, self.texts, self.current_language, self.color, 0, {}, 0, None, interaction.user, self.language)
        for othervariable in view.children:
            if othervariable == view.atks:
                othervariable.disabled = True

        await interaction.response.edit_message(embed=embed, view=view)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_Sword:1220425813132836904>')
    async def fight(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.step == 0:
            await self.skip(interaction)
        elif self.step == 1:
            self.step += 1
            self.enemy_hp -= 30
            bar1 = await fns.progress_bar(1, 1)
            bar2 = await fns.progress_bar(self.enemy_hp, self.enemy_max)
            embed = nextcord.Embed(title=self.texts['fight'], color=int(self.language['coverup']['color'], 16))
            embed.add_field(name=self.language['coverup']['name'], value=f"{bar2}\n{self.enemy_hp}/200 HP\n0 SH", inline=False)
            embed.add_field(name=f"{self.icon} {interaction.user.name}", value=f"{bar1}\n100/100 HP\n0 SH", inline=False)
            embed.add_field(name=self.texts['dialogue'], value=self.language['coverup']['text'], inline=False)
            embed.add_field(name=self.texts['info'], value=self.language['coverup:followup']['text'].replace('{u}', interaction.user.name), inline=False)
            embed.set_thumbnail(url=self.language['coverup']['icon'])
            embed.set_footer(text=main.version[self.current_language])
            await interaction.response.edit_message(embed=embed, view=self)
        elif self.step == 3:
            await self.figjt(interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_Shield:1220425815368400926>')
    async def defence(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.step == 0:
            await self.skip(interaction)
        elif self.step == 2:
            self.step += 1
            bar1 = await fns.progress_bar(1, 1)
            bar2 = await fns.progress_bar(self.enemy_hp, self.enemy_max)
            embed = nextcord.Embed(title=self.texts['fight'], color=int(self.language['comefightme']['color'], 16))
            embed.add_field(name=self.language['comefightme']['name'], value=f"{bar2}\n{self.enemy_hp}/200 HP\n0 SH", inline=False)
            embed.add_field(name=f"{self.icon} {interaction.user.name}", value=f"{bar1}\n100/100 HP\n<:MX_Shield6:1221159173602021546> 30 SH", inline=False)
            embed.add_field(name=self.texts['dialogue'], value=self.language['comefightme']['text'], inline=False)
            embed.add_field(name=self.texts['info'], value=self.language['comefightme:followup']['text'].replace('{u}', interaction.user.name), inline=False)
            embed.set_thumbnail(url=self.language['comefightme']['icon'])
            embed.set_footer(text=main.version[self.current_language])

            await interaction.response.edit_message(embed=embed, view=self)
        elif self.step == 3:
            await self.figjt(interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_NoIdeaWhatIsThis:1220425816794599604>')
    async def atks(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.step == 0:
            await self.skip(interaction)
        elif self.step == 3:
            await self.figjt(interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_Bundle:1220425818321191004>', row=2)
    async def itembag(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.step == 0:
            await self.skip(interaction)
        elif self.step == 3:
            await self.figjt(interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_Change:1220425820279931020>', row=2)
    async def weaponchange(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.step == 0:
            await self.skip(interaction)
        elif self.step == 3:
            await self.figjt(interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.red, emoji='<:MX_Shoe:1220425823555682404>', row=2)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.step == 0:
            await self.skip(interaction)
        elif self.step == 3:
            await self.figjt(interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.gray, emoji='<:MX_Save:1220425821559455836>', row=3)
    async def save(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.step == 0:
            await self.skip(interaction)
        elif self.step == 3:
            await self.figjt(interaction)
        elif self.step == 4:
            embed = nextcord.Embed(title=f"{self.language['tutcomplete']['name']}", description=f"{self.language['tutcomplete']['text']}", color=int(self.language['tutcomplete']['color'], 16))
            embed.set_thumbnail(url=self.language["tutcomplete"]["icon"])
            embed.set_footer(text=main.version[self.current_language])
            if await fns.has_event(interaction.user, "beatgirl") is False:
                await fns.update_quest(interaction.user, ["chapter1", "fighter"], 1, self.current_language)
            await interaction.response.edit_message(embed=embed, view=None)
            self.stop()

    @nextcord.ui.button(style=nextcord.ButtonStyle.gray, emoji='<:MX_Upload:1217191336449540247>', row=3)
    async def load(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.step == 0:
            await self.skip(interaction)
        elif self.step == 3:
            await self.figjt(interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.gray, emoji='<:MX_Info:1217191323015184536>', row=3)
    async def info(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.step == 0:
            await self.skip(interaction)
        elif self.step == 3:
            await self.figjt(interaction)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


# class reverseHuntButtons(nextcord.ui.View):
#     def __init__(
#             self,
#             timeout:float,
#             player_hp: int,
#             mob_hp: int,
#             player_max: int,
#             mob_max: int,
#             image: str,
#             weapon: str,
#             defonce: int,
#             defoncecout: int,
#             eli: bool,
#             icon: str,
#             guts: dict,
#             user: nextcord.Member=None
#     ) -> None:
#         super().__init__(timeout=timeout)
#
#         self.player_hp = player_hp
#         self.mob_hp = mob_hp
#         self.player_max = player_max
#         self.mob_max = mob_max
#
#         self.user = user
#         self.image = image
#         self.defence = defonce
#         self.defence_count = defoncecout
#         self.weapon = weapon
#         self.icon = icon
#
#         self.eligible = eli
#         self.enemy = guts
#
#     async def manage_buttons(self, mode):
#
#         if mode == "disable":
#             for i in self.children:
#                 i.disabled = True
#         else:
#             for i in self.children:
#                 i.disabled = False
#
#
#     async def create_embed(self, interaction, details, type=None):
#         disname = self.enemy["displayname"]
#         bar1 = await fnc.progress_bar(self.player_hp, self.player_max)
#         bar2 = await fnc.progress_bar(self.mob_hp, self.mob_max)
#         shbar = await fnc.sheild(self.defence)
#         embed = nextcord.Embed(title=f"Walka", color=main.color_normal)
#
#         embed.add_field(name=f"{self.icon} {interaction.user.name}", value=f"{bar2}\n{self.mob_hp}/{self.mob_max} HP",inline=False)
#         embed.add_field(name=f"{disname}", value=f"{bar1}\n{self.player_hp}/{self.player_max} HP\n{shbar} {self.defence} SH",inline=False)
#
#         embed.add_field(name="Informacje", value=details,inline=False)
#         embed.set_thumbnail(url=self.image)
#         embed.set_footer(text=main.version)
#         return embed
#
#     async def player_death(self, interaction, mode):
#         await self.manage_buttons("disable")
#         dis = self.enemy["disname"]
#         if mode == "hp":
#             embed=await self.create_embed(interaction, f"Nawet z tą mocą... Nie byłam w stanie ciebie pokonać... Haha...", type="death")
#             await interaction.edit(embed=embed, view=self)
#             self.stop()
#         else:
#             embed=await self.create_embed(interaction, f"Nawet z tą mocą... Nie byłam w stanie ciebie pokonać... Haha...", type="death")
#             await interaction.edit(embed=embed, view=self)
#             self.stop()
#
#     async def enemy_death(self, interaction):
#         self.mob_hp = 0
#         for i in self.children:
#             i.disabled = True
#         embed = nextcord.Embed(title=f"*Ujrzałeś mrok...*", color=main.color_normal)
#         embed.set_thumbnail(url=self.image)
#         embed.set_footer(text=main.version)
#         await interaction.edit(embed=embed, view=None)
#
#
#
#     async def enemy_turn(self, interaction, details=None):
#         dis = self.enemy["disname"]
#         enemyatack = self.enemy["attack"][random.randint(0,2)]
#         gg = None
#         if enemyatack == 0:
#             await self.manage_buttons("disable")
#             embed=await self.create_embed(interaction, f"{interaction.user.name} atakuje {dis}. Nie przyniosło to żadnych skutków.")
#             await interaction.edit(embed=embed, view=self)
#             return
#         if self.defence == 0:
#             gg = "hp"
#         if gg == "hp":
#             self.player_hp -= enemyatack
#             if self.player_hp <= 0:
#                 self.player_hp = 0
#                 await self.player_death(interaction, "hp")
#                 return
#             await self.manage_buttons("disable")
#             embed=await self.create_embed(interaction, f"{interaction.user.name} atakuje {dis}. {dis} traci {enemyatack} HP")
#             await interaction.edit(embed=embed, view=self)
#         else:
#             self.defence -= enemyatack
#             if self.defence == 0:
#                 await self.manage_buttons("disable")
#                 embed=await self.create_embed(interaction, f"{interaction.user.name} atakuje {dis}. {dis} traci wszystkie SH")
#                 await interaction.edit(embed=embed, view=self)
#             elif self.defence > 0:
#                 await self.manage_buttons("disable")
#                 embed=await self.create_embed(interaction, f"{interaction.user.name} atakuje {dis}. {dis} traci {enemyatack} SH")
#                 await interaction.edit(embed=embed, view=self)
#             else:
#                 bp = -1*self.defence
#                 self.player_hp += self.defence
#                 self.defence = 0
#                 if self.player_hp <= 0:
#                     self.player_hp = 0
#                     await self.player_death(interaction, "defence")
#                 else:
#                     await self.manage_buttons("disable")
#                     embed=await self.create_embed(interaction, f"{interaction.user.name} atakuje {dis}. {dis} traci wszystkie SH oraz {bp} HP.")
#                     await interaction.edit(embed=embed, view=self)
#
#         await asyncio.sleep(2.5)
#         if self.player_hp < self.enemy["attack"][2]:
#             await self.huntMobs(interaction, "def")
#         else:
#             lol = random.randint(1, 10)
#             if lol == 9:
#                 await self.huntMobs(interaction, "def")
#                 return
#             await self.huntMobs(interaction, "atk")
#
#
#
#
#
#     async def get_shield(self, interaction):
#         self.defence += 30
#         self.defence_count -= 1
#         await self.manage_buttons("enable")
#         dis = self.enemy["disname"]
#         embed = await self.create_embed(interaction, f"{dis} zdobywa 30 SH")
#         await interaction.edit(embed=embed, view=self)
#         return
#
#     async def attack_mob_classic(self, interaction, atk):
#         dis = self.enemy["disname"]
#         oo = await fnc.get_from_name(self.weapon, "displayname")
#         if atk == 0:
#             txt = f"{dis} atakuje {interaction.user.name} za pomocą {oo}. Nie przyniosło to żadnych skutków."
#         else:
#             txt = f"{dis} atakuje {interaction.user.name} za pomocą {oo} \n{interaction.user.name} traci {atk} HP"
#
#         self.mob_hp -= atk
#         if self.mob_hp > 0:
#             await self.manage_buttons("enable")
#             embed = await self.create_embed(interaction, txt)
#             await interaction.edit(embed=embed, view=self)
#             await asyncio.sleep(2.5)
#         else:
#             await self.enemy_death(interaction)
#
#
#     async def huntMobs(self, interaction, mode, details = None):
#         version = main.version
#         dd = await fnc.itemsinfo()
#
#         if mode == "def":
#             if self.defence_count != 0:
#                 await self.get_shield(interaction)
#             else:
#                 await self.huntMobs(interaction, "atk")
#         elif mode == "atk":
#             for ik in dd:
#                 if self.weapon == ik["name"]:
#                     attack_value = ik["toolatributes"]["attack"][random.randint(0,2)]
#                     await self.attack_mob_classic(interaction, attack_value)
#
#
#     @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:MX_Sword:1220425813132836904>')
#     async def fight(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
#         if self.eligible == False:
#             return
#         await self.enemy_turn(interaction)
#         pass
#
#
#
#
#     async def interaction_check(self, interaction: Interaction) -> bool:
#         if self.user:
#             if interaction.user != self.user:
#                 await interaction.response.send_message("Bruh",ephemeral=True)
#                 return False
#         return True


class LanguageStartButtons(nextcord.ui.View):
    def __init__(self, user: nextcord.Member) -> None:
        super().__init__(timeout=3600)
        self.user = user

    @nextcord.ui.button(emoji='🇵🇱', style=nextcord.ButtonStyle.gray)
    async def yee(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        settings = await fns.setting()

        settings[str(self.user.id)]["language"] = "pl"
        with open("userdb/settings.json", "w") as f:
            json.dump(settings, f)

        await interaction.response.send_message("Zmieniono Język na Polski", ephemeral=True)
        self.stop()

    @nextcord.ui.button(emoji='🇬🇧', style=nextcord.ButtonStyle.gray)
    async def nah(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        settings = await fns.setting()

        settings[str(self.user.id)]["language"] = "en"
        with open("userdb/settings.json", "w") as f:
            json.dump(settings, f)

        await interaction.response.send_message("Changed langauge to English", ephemeral=True)
        self.stop()
        self.stop()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True

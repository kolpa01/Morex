import nextcord
import morex.logging as logging
from morex.inventory import MorexInventory
from nextcord.ext import commands
import main
import buttons
import random
from nextcord import Interaction, SlashOption
import functions as fns
from PIL import Image
from io import BytesIO
from morex import MorexDigsite


class Mining(commands.Cog):
    def __init__(self, client):
        self.client = client

        # grid overlays 

        self.grid0 = None 
        self.grid1 = None
        self.grid2 = None 
        self.grid3 = None
        self.grid4 = Image.open('images/grid4_overlay.png')

        # numbers

        self.numbers = Image.open('images/numbers.png')
        self.n0 = Image.open('images/num0.png')
        self.n1 = Image.open('images/num1.png')
        self.n2 = Image.open('images/num2.png')
        self.n3 = Image.open('images/num3.png')
        self.n4 = Image.open('images/num4.png')
        self.n5 = Image.open('images/num5.png')
        self.n6 = Image.open('images/num6.png')
        self.debug_numbers = [self.n6, self.n5, self.n4, self.n3, self.n2, self.n1, self.n0]

        # blocks

        self.earth = Image.open('images/earth.png')
        self.stone = Image.open('images/stone.png')
        self.coal = Image.open('images/coalore.png')
        self.ironore = Image.open('images/ironore.png')
        self.goldore = Image.open('images/goldore.png')
        self.diamondore = Image.open('images/diamondore.png')
        self.candycorn = Image.open('images/candycorn.png')
        self.ice = Image.open('images/ice.png')
        self.candycane = Image.open('images/candycane.png')
        self.vines = Image.open('images/vines.png')
        self.placeholder = Image.open('images/placeholder.png')
        self.goldenegg = Image.open('images/goldenegg.png')
        self.spidershard = Image.open('images/spidershard.png')

        # block overlays

        self.o_vines = Image.open('images/o_vines.png')  

        # chest 

        self.treasure = Image.open('images/chest.png')
        self.two = Image.open('images/2.png')

        self.map = {
            "grid0.png": self.grid0,
            "grid1.png": self.grid1,
            "grid2.png": self.grid2,
            "grid3.png": self.grid3,
            "grid4.png": self.grid4,
            "numbers": self.numbers,
            "earth": self.earth,
            "stone": self.stone,
            "coal": self.coal,
            "ironore": self.ironore,
            "goldore": self.goldore,
            "diamondore": self.diamondore,
            "candycorn": self.candycorn,
            "ice": self.ice,
            "candycane": self.candycane,
            "vines": self.vines,
            "placeholder": self.placeholder,
            "goldenegg": self.goldenegg,
            ":vines": self.o_vines,
            "treasure": self.treasure,
            "2": self.two
        }

    @staticmethod
    async def create_world(place: MorexDigsite, lucky_mode: bool = False):
        layers = []
        for i in place.layers:
            tempdict = []
            for a in place.layers[i]:
                if a["class"] == "primary":
                    for aaa in range(9):
                        tempdict.append(a["item"])
                else:
                    for ran in range(a["guaranted_amount"]):
                        goodplacement = True
                        while goodplacement:
                            b = random.randint(0, 8)
                            if a["item"] == tempdict[b]:
                                continue
                            else:
                                tempdict[b] = a["item"]
                                goodplacement = False
                    for smt in range(a["amount"]):
                        aaaaaaa = random.randint(1, 100)
                        if lucky_mode:
                            aaaaaaa = 0
                        if a["chance"] >= aaaaaaa:
                            goodplacement = True
                            while goodplacement:
                                b = random.randint(0, 8)
                                if a["item"] == tempdict[b]:
                                    continue
                                else:
                                    tempdict[b] = a["item"]
                                    goodplacement = False
            layers.append(tempdict)
        lay = random.choice(place.treasure.layers)
        curlay = layers[int(lay)]

        true = True
        while true:
            ppp = random.randint(0, 8)
            if curlay[ppp] in place.treasure.can_replace:
                curlay[ppp] = "treasure"
                true = False
            else:
                continue
        layers.reverse()
        return layers

    @staticmethod
    async def get_shade(highest, layer):
        a = highest - (layer + 1)
        alpha = a * 16
        if alpha > 255:
            alpha = 255
        return Image.new("RGBA", (160, 160), (0, 0, 0, alpha))

    @nextcord.slash_command(name="dig", description="Go dig up ores and treasures.", description_localizations={"pl": "Pójdź wykopać rudy i skarby."}, integration_types=main.integrations, contexts=main.contexts)
    async def dig(
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
        leng = await fns.lang(cur_lan)
        text = leng['commands']['dig']

        place = await fns.check_location(user, place, "dig")
        if place is None or place is False:
            return
        place = fns.get_dig_locations(place, cur_lan)

        has_pickaxe = fns.get_item("0023", "id", cur_lan)
        if await has_pickaxe.get_amount(user, 1) is None:
            errorembed = nextcord.Embed(description=text['no_pickaxe'], color=main.color_normal)
            errorembed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            errorembed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=errorembed)
            return

        tutorial_mode = False

        if place.name == "mineshaft" and await fns.has_event(user, "metguywithweirdname") is False:
            return

        g = None

        if place.name == "mineshaft" and await fns.has_event(user, "digged") is False:
            tutorial_mode = True
        elif place.required_item is not False:
            req_item = fns.get_item(place.required_item, "name", cur_lan)
            res = await req_item.get_amount(user, 1)
            if res is None:
                errorembed = nextcord.Embed(description=f"{text['donthave']} {req_item}.\n{text['try_again']}", color=main.color_normal)
                errorembed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
                errorembed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=errorembed)
                return

            embed = nextcord.Embed(description=f"{text['have']} {req_item.displayname}.\n{text['visit']} {place.displayname} {text['for']} 1 {req_item}", color=main.color_normal)
            embed.set_author(name=f"{user.name}", icon_url=user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            view = buttons.ConfirmationButtons(60, user)
            await interaction.response.send_message(embed=embed, view=view)
            await view.wait()
            if view.value is None or view.value is False:
                await interaction.edit_original_message(view=None)
                return
            res = await req_item.get_amount(user, 1)
            if res is None:
                await interaction.edit_original_message(view=None)
                return
            await req_item.remove_item(user, 1)
            g = 1

        if tutorial_mode:
            world = await self.create_world(place, True)
            usages = 54
            digalog = await fns.dialogues("v1_dig_tutorial", cur_lan)
            action = "firsttime"
        else:
            world = await self.create_world(place)
            usages = place.usages
            action = None
            digalog = None
        max_usages = usages

        cur_layer = []
        for i in range(9):
            cur_layer.append(len(world) - 1)

        inventory = MorexInventory(user)
        game = True

        while game is True:
            background = Image.open(f'images/{place.background}')
            size1 = 170
            size2 = 170
            for i in range(9):
                if cur_layer[i] is not None:
                    numa_leja = cur_layer[i]
                    a = world[numa_leja][i]
                    if a == 'treasure' and place.name == 'icychasm':
                        pore = self.map['2']
                    else:
                        block_cutter = a.split(":")
                        pore = getattr(self, block_cutter[0], self.placeholder)
                        background.paste(pore, (size1, size2), pore)
                        if len(block_cutter) > 1:
                            pore_overlay = self.map[f":{block_cutter[1]}"]
                            background.paste(pore_overlay, (size1, size2), pore_overlay)
                    shading = await self.get_shade(len(world), numa_leja)
                    background.paste(shading, (size1, size2), shading)
                    reas = await fns.has_enabled(user, "debug_info")
                    if reas is True:
                        debug_nums = self.debug_numbers[-1:-1 * (len(world) + 1):-1]
                        debug_nums.reverse()
                        background.paste(debug_nums[numa_leja], (size1, size2), debug_nums[numa_leja])

                if size1 == 510:
                    size1 = 170
                    size2 += 170
                    continue
                size1 += 170

            view = buttons.NineNumbers(60, user)
            if self.map[place.background]:
                background.paste(self.map[place.background], (0, 0), self.map[place.background])
            background.paste(self.numbers, (0, 0), self.numbers)
            with BytesIO() as abecaf:
                text_inv = []
                background.save(abecaf, "PNG")
                abecaf.seek(0)
                for item_sid, amt in inventory.items.items():
                    if item_sid == "treasure":
                        text_inv.append(f"<:MX_Treasure:1237427125204549702> {text['chest_name']}")
                    else:
                        item_temp = fns.get_item(item_sid, 'name', cur_lan)
                        text_inv.append(f"{amt} {item_temp.displayname}")

                inv = '\n'.join(text_inv)
                pg_bar = await fns.progress_bar(usages, max_usages)
                disc = f"{text['durability']}\n{pg_bar} {(usages / max_usages) * 100:.0f}% ({usages}/{max_usages})\n\n{text['inventory']}\n{inv}"

                if tutorial_mode:
                    disc = ''.join((f"**{digalog[action]['name']}**\n{digalog[action]['text']}\n\n", disc))

                embed = nextcord.Embed(title=f"{place.displayname}", description=disc, color=place.color)
                embed.set_image(url='attachment://image.png')
                if tutorial_mode:
                    embed.set_thumbnail(url=digalog[action]['icon'])
                embed.set_footer(text=main.version[cur_lan])
                if tutorial_mode:
                    if action == "firsttime":
                        action = "notfirsttimeyouidiot"
                if g is None:
                    await interaction.response.send_message(embed=embed, file=nextcord.File(abecaf, filename="image.png"), view=view)
                    g = 1
                else:
                    await interaction.edit_original_message(embed=embed, file=nextcord.File(abecaf, filename="image.png"), view=view)

            await view.wait()
            if view.value is None:
                return
            else:
                if cur_layer[view.value] is not None:
                    usages -= 1

                    titem = world[cur_layer[view.value]][view.value]
                    titem = world[cur_layer[view.value]][view.value].split(":")[0]
                    
                    action = titem
                    await inventory.add_item(titem, 1)
                    if cur_layer[view.value] - 1 == -1:
                        cur_layer[view.value] = None
                    else:
                        cur_layer[view.value] -= 1

                if usages == 0:
                    break

                is_there_anything_left = False
                for block in cur_layer:
                    if block is not None:
                        is_there_anything_left = True
                        break
                if not is_there_anything_left:
                    break

        if tutorial_mode and await fns.has_event(user, "digged"): 
            logging.warn(f"{interaction.user.name} ({interaction.user.id}) Tried to scam you for M-Bucks!!")
            return

        invent = []
        chest = []
        chk = False
        for item_sid, amt in inventory.items.items():
            await fns.update_daily_task(user, "d", item_sid, amt)
            if item_sid == "treasure":
                chk = True
                for items in place.treasure.rewards:
                    choice = random.randint(1, 10000)
                    if choice <= items["choice"]:
                        if items["item"] == "coins":
                            dd = random.randint(items["min_value"], items["max_value"])
                            boost = await fns.has_event_boost("dig_chest_coins")
                            dd = boost * dd
                            await fns.update_bank(user, dd)
                            chest.append(f"{dd} {main.coin}")
                        else:
                            dd = random.randint(items["min_value"], items["max_value"])
                            itm = fns.get_item(items['item'], 'name', cur_lan)
                            await itm.add_item(user, dd)
                            chest.append(f"{dd} {itm}")

                continue
            item = fns.get_item(item_sid, 'name', cur_lan)
            await item.add_item(user, amt)
            invent.append(f"{amt} {item.displayname}")
        invent = "\n".join(invent)
        if chk:
            chest = "\n".join(chest)
            desc = f"{text['digup']}\n{invent}\n\n{text['chest']}\n{chest}"
        else:
            desc = f"{text['digup']}\n{invent}"

        if tutorial_mode:
            action = "byebye"
            desc = ''.join((f"**{digalog[action]['name']}**\n{digalog[action]['text']}\n\n", desc))
            await fns.update_quest(user, ["chapter1", "digger"], 1, cur_lan)
        embed = nextcord.Embed(title=place.displayname, description=desc, color=place.color)
        background = Image.new("RGBA", (1, 1), 0x00000000)
        with BytesIO() as a:
            background.save(a, "PNG")
            a.seek(0)
            embed.set_image(url='attachment://image.png')
            if tutorial_mode:
                embed.set_thumbnail(url=digalog[action]['icon'])
            embed.set_footer(text=main.version[cur_lan])
            await interaction.edit_original_message(embed=embed, file=nextcord.File(a, filename="image.png"), view=None)
            # await interaction.edit_original_message(embed=embed, view=None)
        await fns.update_daily_task(user, "d", "final", 1)

    @dig.on_autocomplete("place")
    async def dig_autocomplete(self, interaction, current: str):
        digsites = await fns.digging()
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        data = {}
        i = 0
        if not current:
            for name in digsites:
                if await fns.check_location(interaction.user, name['name'], 'dig'):
                    chk_it = fns.get_dig_locations(name['name'], leng)
                    i += 1
                    data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for name in digsites:
                if await fns.check_location(interaction.user, name['name'], 'dig'):
                    chk_it = fns.get_dig_locations(name['name'], leng)
                    if str(current.lower()) in chk_it.displayname.lower():
                        i += 1
                        data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))


def setup(client):
    client.add_cog(Mining(client))

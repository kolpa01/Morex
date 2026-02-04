import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import functions as fns
import main
import json
from PIL import Image
from io import BytesIO
import datetime
import random
import copy
import morex.inventory.utils as m_utils


class SeedSelector(nextcord.ui.Select):
    def __init__(self, user, cur_lan, select_options, text):
        self.user = user
        self.cur_lan = cur_lan
        super().__init__(
            placeholder=text, 
            min_values=1, 
            max_values=1, 
            options=select_options, 
            row=0
        )
        
            
class PlantUI(nextcord.ui.View):
    def __init__(self, timeout, user, cur_lan, dropdown, texture_data, text):
        super().__init__(timeout=timeout)
        self.add_item(dropdown)
        self.user = user
        self.cur_lan = cur_lan
        self.texture_data = texture_data
        self.text = text
        
        self.back.label = text["back"]

    async def plant_seed(self, interaction, tile_id, farm_id):
        if self.children[10].values == []:
            embed = nextcord.Embed(description=self.text["choice"], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        fm_data = await fns.get_farms_data()
        tile_data = fm_data[str(self.user.id)]["farms"][str(farm_id)][tile_id]
        if tile_data["crop"] != "none":
            embed = nextcord.Embed(description=self.text["something_there"], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if tile_data["state"] != "plowed":
            embed = nextcord.Embed(description=self.text["plow_needed"], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        seed = fns.get_item(self.children[10].values[0], "id", self.cur_lan)
        amount = await seed.get_amount(self.user, 1)
        if not amount:
            embed = nextcord.Embed(description=self.text["no_seed"], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[self.cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        await seed.remove_item(self.user, 1)
        grow_time = seed.toolatributes.growth_time

        if not tile_data["watered"]:
            grow_time = grow_time * 2
        else:
            if tile_data["fertilized"]:
                grow_time = grow_time // 2
        now = round(datetime.datetime.now().timestamp())
        finish = now + grow_time
        death = False
        if seed.toolatributes.wilt_time:
            death = finish + seed.toolatributes.wilt_time

        tile_data["crop"] = seed.id
        tile_data["start_timestamp"] = now
        tile_data["finish_timestamp"] = finish
        tile_data["death_timestamp"] = death

        with open("userdb/farmlands.json", "w") as f:
            json.dump(fm_data, f)

        descriptions = {}
        seeds = fns.get_seeds()
        seed_amounts = await m_utils.items_amount.get_bulk_amount(self.user, items=copy.copy(seeds))
        for seed in seeds:
            seed = fns.get_item(seed, "id", self.cur_lan)
            desc = await fns.text_replacer(self.text["you_own"], ["{amount}", seed_amounts[seed.id]])
            descriptions.update({seed.id: desc})
        for option in self.children[10].options:
            option.description = descriptions[option.value]
            option.default = False
            if option.value == self.children[10].values[0]:
                option.default = True
        
        await get_farm_image(interaction, self.user, self, self.texture_data, True, self.cur_lan, self.text)

    @nextcord.ui.button(emoji=main.one, style=nextcord.ButtonStyle.gray, row=1)
    async def one(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.plant_seed(interaction, 0, 0)

    @nextcord.ui.button(emoji=main.two, style=nextcord.ButtonStyle.gray, row=1)
    async def two(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.plant_seed(interaction, 1, 0)

    @nextcord.ui.button(emoji=main.three, style=nextcord.ButtonStyle.gray, row=1)
    async def three(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.plant_seed(interaction, 2, 0)

    @nextcord.ui.button(emoji=main.four, style=nextcord.ButtonStyle.gray, row=2)
    async def four(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.plant_seed(interaction, 3, 0)

    @nextcord.ui.button(emoji=main.five, style=nextcord.ButtonStyle.gray, row=2)
    async def five(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.plant_seed(interaction, 4, 0)

    @nextcord.ui.button(emoji=main.six, style=nextcord.ButtonStyle.gray, row=2)
    async def six(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.plant_seed(interaction, 5, 0)

    @nextcord.ui.button(emoji=main.seven, style=nextcord.ButtonStyle.gray, row=3)
    async def seven(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.plant_seed(interaction, 6, 0)

    @nextcord.ui.button(emoji=main.eight, style=nextcord.ButtonStyle.gray, row=3)
    async def eight(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.plant_seed(interaction, 7, 0)

    @nextcord.ui.button(emoji=main.nine, style=nextcord.ButtonStyle.gray, row=3)
    async def nine(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.plant_seed(interaction, 8, 0)

    @nextcord.ui.button(emoji=main.left, label="...", style=nextcord.ButtonStyle.gray, row=4)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = FarmView(self.user, self.texture_data, self.cur_lan, self.text)
        await get_farm_image(interaction, self.user, view, self.texture_data, True, self.cur_lan, self.text)
        self.stop()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class TextureData:
    def __init__(self):
        self.farm_skins = {
            "normal_farm": "images/farming/farm0.png"
        }
        self.crops = {
            "testseed": {
                "0": Image.open("images/farming/testseed_0.png"),
                "1": Image.open("images/farming/testseed_1.png"),
                "2": Image.open("images/farming/testseed_2.png"),
                "3": Image.open("images/farming/testseed_3.png"),
                "4": Image.open("images/farming/testseed_4.png")
            },
            "wheatseed": {
                "0": Image.open("images/farming/wheatseed_0.png"),
                "1": Image.open("images/farming/wheatseed_1.png"),
                "2": Image.open("images/farming/wheatseed_2.png"),
                "3": Image.open("images/farming/wheatseed_3.png"),
                "4": Image.open("images/farming/wheatseed_4.png")
            },
            "potatoseed": {
                "0": Image.open("images/farming/potatoseed_0.png"),
                "1": Image.open("images/farming/potatoseed_1.png"),
                "2": Image.open("images/farming/potatoseed_2.png"),
                "3": Image.open("images/farming/potatoseed_3.png"),
                "4": Image.open("images/farming/potatoseed_4.png")
            },
            "carrotseed": {
                "0": Image.open("images/farming/carrotseed_0.png"),
                "1": Image.open("images/farming/carrotseed_1.png"),
                "2": Image.open("images/farming/carrotseed_2.png"),
                "3": Image.open("images/farming/carrotseed_3.png"),
                "4": Image.open("images/farming/carrotseed_4.png")
            },
            "cornseed": {
                "0": Image.open("images/farming/cornseed_0.png"),
                "1": Image.open("images/farming/cornseed_1.png"),
                "2": Image.open("images/farming/cornseed_2.png"),
                "3": Image.open("images/farming/cornseed_3.png"),
                "4": Image.open("images/farming/cornseed_4.png")
            },
        }
        self.blocks = {
            "earth": {
                "normal": Image.open("images/farming/earth_normal.png"),
                "plowed": Image.open("images/farming/earth_plowed.png")
            }
        }
        self.watered = Image.open("images/farming/watered.png")
        self.fertilized = Image.open("images/farming/fertilized.png")


async def get_farm_image(interaction, user, view, texture_data, edit_mode, cur_lan, mx_text):
    fm_data = await fns.get_farms_data()
    farm_skin = Image.open(texture_data.farm_skins[fm_data[str(user.id)]["skins"]["0"]])
    canvas = Image.new("RGBA", (640, 640))
    text = []
    now = round(datetime.datetime.now().timestamp())
    for i, tile_data in enumerate(fm_data[str(user.id)]["farms"]["0"]):
        seed = fns.get_item(tile_data["crop"], "id", cur_lan)
        block = fns.get_item(tile_data["blocktype"], "id", cur_lan)
        pos = [80 + (160 * (i % 3)), 80 + (160 * (i // 3))]
        canvas.paste(texture_data.blocks[block.sid][tile_data["state"]], pos, texture_data.blocks[block.sid][tile_data["state"]])
        if tile_data["watered"]:
            canvas.paste(texture_data.watered, pos, texture_data.watered)
        if tile_data["fertilized"]:
            canvas.paste(texture_data.fertilized, pos, texture_data.fertilized)
        if seed is None:
            text.append(f"{i + 1}. [Empty]")
            continue
        texture_index = await get_tile_skin(tile_data, seed, now)
        canvas.paste(texture_data.crops[seed.sid][str(texture_index)], pos, texture_data.crops[seed.sid][str(texture_index)])
        if texture_index == 4:
            text.append(await fns.text_replacer(mx_text["plant_dead"], ["{number}", i + 1], ["{item}", seed.displayname], ["{timestamp}", tile_data["death_timestamp"]]))
        elif texture_index == 3:
            text.append(await fns.text_replacer(mx_text["plant_ready"], ["{number}", i + 1], ["{item}", seed.displayname]))
        else:
            text.append(await fns.text_replacer(mx_text["plant_growing"], ["{number}", i + 1], ["{item}", seed.displayname], ["{timestamp}", tile_data["finish_timestamp"]]))

    canvas.paste(farm_skin, [0, 0], farm_skin)
    text = "\n".join(text)
    title = await fns.text_replacer(mx_text["farm_title"], ["{user}", user.name])

    with BytesIO() as img_file:
        canvas.save(img_file, "PNG")
        img_file.seek(0)
        embed = nextcord.Embed(title=title, description=text, color=main.color_normal)
        embed.set_image(url='attachment://image.png')
        embed.set_footer(text=main.version[cur_lan])
        if not edit_mode:
            await interaction.response.send_message(embed=embed, file=nextcord.File(img_file, filename="image.png"), view=view)
        else:
            await interaction.edit(embed=embed, file=nextcord.File(img_file, filename="image.png"), view=view)


async def get_tile_skin(tile_data, item, timestamp):
    time = tile_data["finish_timestamp"] - tile_data["start_timestamp"]
    time_left = tile_data["finish_timestamp"] - timestamp
    if time_left > time:
        raise ValueError("time_left can't be bigger than time")

    how_much = 100 - round((time_left / time) * 100)

    if how_much < 11:
        return 0
    elif how_much < 40:
        return 1
    elif how_much < 99:
        return 2
    else:
        if tile_data["death_timestamp"]:
            if timestamp > tile_data["death_timestamp"]:
                return 4
        return 3


class FarmButtons(nextcord.ui.View):
    def __init__(self, user, texture_data, cur_lan, mode, text):
        super().__init__(timeout=60)
        self.user = user
        self.texture_data = texture_data
        self.cur_lan = cur_lan
        self.mode = mode
        self.text = text

        self.back.label = text["back"]
        
    async def plow_tile(self, farm_id, tile_id):
        fm_data = await fns.get_farms_data()
        tile_data = fm_data[str(self.user.id)]["farms"][str(farm_id)][tile_id]
        tile_data["crop"] = "none"
        tile_data["start_timestamp"] = 0
        tile_data["finish_timestamp"] = 0
        tile_data["death_timestamp"] = 0
        tile_data["state"] = "plowed"
        tile_data["watered"] = False
        tile_data["fertilized"] = False

        with open("userdb/farmlands.json", "w") as f:
            json.dump(fm_data, f)

    async def water_tile(self, farm_id, tile_id):
        fm_data = await fns.get_farms_data()
        fm_data[str(self.user.id)]["farms"][str(farm_id)][tile_id]["watered"] = True

        with open("userdb/farmlands.json", "w") as f:
            json.dump(fm_data, f)

    async def fertilize_tile(self, farm_id, tile_id):
        fm_data = await fns.get_farms_data()
        fm_data[str(self.user.id)]["farms"][str(farm_id)][tile_id]["fertilized"] = True

        with open("userdb/farmlands.json", "w") as f:
            json.dump(fm_data, f)

    async def harvest_crop(self, tile_data):
        text = []
        seed = fns.get_item(tile_data["crop"], "id", self.cur_lan)
        amount = random.randint(seed.toolatributes.amount[0], seed.toolatributes.amount[1])
        crop = fns.get_item(seed.toolatributes.crop, "name", self.cur_lan)
        await crop.add_item(self.user, amount)
        text.append(f"{amount} {crop.displayname}")

        chance = random.randint(1, 100)
        if chance <= seed.toolatributes.seed_chance:
            seed_amount = random.randint(seed.toolatributes.seed_amount[0], seed.toolatributes.seed_amount[1])
            await seed.add_item(self.user, seed_amount)
            text.append(f"{seed_amount} {seed.displayname}")

        return text

    async def harvest_tile(self, interaction, farm_id, tile_id):
        fm_data = await fns.get_farms_data()
        tile_data = fm_data[str(self.user.id)]["farms"][str(farm_id)][tile_id]

        now = round(datetime.datetime.now().timestamp())
        time = tile_data["finish_timestamp"] - tile_data["start_timestamp"]
        time_left = tile_data["finish_timestamp"] - now
        if time_left > time:
            raise ValueError("time_left can't be bigger than time")

        how_much = 100 - round((time_left / time) * 100)

        text = []
        if how_much < 99:
            seed = fns.get_item(tile_data["crop"], "id", self.cur_lan)
            chance = random.randint(1, 100)
            if chance <= seed.toolatributes.seed_chance:
                text.append(self.text["harvested"])
                await seed.add_item(self.user, 1)
                text.append(f"1 {seed.displayname}")
            else:
                text.append(self.text["no_no_harvest"])
        else:
            if tile_data["death_timestamp"]:
                if now > tile_data["death_timestamp"]:
                    text.append(self.text["no_no_harvest"])
                else:
                    text = [self.text["harvested"]] + await self.harvest_crop(tile_data)
            else:
                text = [self.text["harvested"]] + await self.harvest_crop(tile_data)

        tile_data["crop"] = "none"
        tile_data["start_timestamp"] = 0
        tile_data["finish_timestamp"] = 0
        tile_data["death_timestamp"] = 0
        tile_data["state"] = "normal"
        tile_data["watered"] = False
        tile_data["fertilized"] = False

        with open("userdb/farmlands.json", "w") as f:
            json.dump(fm_data, f)

        embed = nextcord.Embed(description="\n".join(text), color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=main.version[self.cur_lan])
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def get_tile_data(self, farm_id, tile_id):
        fm_data = await fns.get_farms_data()
        return fm_data[str(self.user.id)]["farms"][str(farm_id)][tile_id]

    async def manage_actions(self, interaction, tile_id):
        if self.mode == "plow":
            hoe = fns.get_item("hoe", "name", self.cur_lan)
            chance = random.randint(1, 20)
            amount = await hoe.get_amount(self.user, 1)
            if not amount:
                embed = nextcord.Embed(description=await fns.text_replacer(self.text['no_hoe'], ["{item}", hoe.displayname]), color=main.color_normal)
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            if chance == 1:
                await hoe.remove_item(self.user, 1)
                embed = nextcord.Embed(description=await fns.text_replacer(self.text['broken_hoe'], ["{item}", hoe.displayname]), color=main.color_normal)
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=embed, ephemeral=True)
            await self.plow_tile(0, tile_id)
            await get_farm_image(interaction, self.user, self, self.texture_data, True, self.cur_lan, self.text)
        elif self.mode == "water":
            tile_data = await self.get_tile_data(0, tile_id)
            if not tile_data["watered"] and tile_data["crop"] == "none" and tile_data["state"] == "plowed":
                watering_can = fns.get_item("wateringcan", "name", self.cur_lan)
                chance = random.randint(1, 15)
                amount = await watering_can.get_amount(self.user, 1)
                if not amount:
                    embed = nextcord.Embed(description=await fns.text_replacer(self.text['no_watering_can'], ["{item}", watering_can.displayname]), color=main.color_normal)
                    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=main.version[self.cur_lan])
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
                if chance == 1:
                    await watering_can.remove_item(self.user, 1)
                    embed = nextcord.Embed(description=await fns.text_replacer(self.text['broken_watering_can'], ["{item}", watering_can.displayname]), color=main.color_normal)
                    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=main.version[self.cur_lan])
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                await self.water_tile(0, tile_id)
                await get_farm_image(interaction, self.user, self, self.texture_data, True, self.cur_lan, self.text)
            else:
                embed = nextcord.Embed(description=self.text["unwaterable_tile"], color=main.color_normal)
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.mode == "fertilize":
            tile_data = await self.get_tile_data(0, tile_id)
            if tile_data["watered"] and tile_data["crop"] == "none" and tile_data["state"] == "plowed" and not tile_data["fertilized"]:
                fertilizer = fns.get_item("fertilizer", "name", self.cur_lan)
                amount = await fertilizer.get_amount(self.user, 1)
                if not amount:
                    embed = nextcord.Embed(description=await fns.text_replacer(self.text['no_fertilizer'], ["{item}", fertilizer.displayname]), color=main.color_normal)
                    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=main.version[self.cur_lan])
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
                await fertilizer.remove_item(self.user, 1)
                await self.fertilize_tile(0, tile_id)
                await get_farm_image(interaction, self.user, self, self.texture_data, True, self.cur_lan, self.text)
            else:
                embed = nextcord.Embed(description=self.text["unfertilizable_tile"], color=main.color_normal)
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.mode == "harvest":
            tile_data = await self.get_tile_data(0, tile_id)
            if tile_data["crop"] != "none":
                await self.harvest_tile(interaction, 0, tile_id)
                await get_farm_image(interaction, self.user, self, self.texture_data, True, self.cur_lan, self.text)
            else:
                embed = nextcord.Embed(description=self.text["no_harvest"], color=main.color_normal)
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                embed.set_footer(text=main.version[self.cur_lan])
                await interaction.response.send_message(embed=embed, ephemeral=True)

    @nextcord.ui.button(emoji=main.one, style=nextcord.ButtonStyle.gray)
    async def one(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, 0)

    @nextcord.ui.button(emoji=main.two, style=nextcord.ButtonStyle.gray)
    async def two(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, 1)

    @nextcord.ui.button(emoji=main.three, style=nextcord.ButtonStyle.gray)
    async def three(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, 2)

    @nextcord.ui.button(emoji=main.four, style=nextcord.ButtonStyle.gray, row=2)
    async def four(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, 3)

    @nextcord.ui.button(emoji=main.five, style=nextcord.ButtonStyle.gray, row=2)
    async def five(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, 4)

    @nextcord.ui.button(emoji=main.six, style=nextcord.ButtonStyle.gray, row=2)
    async def six(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, 5)

    @nextcord.ui.button(emoji=main.seven, style=nextcord.ButtonStyle.gray, row=3)
    async def seven(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, 6)

    @nextcord.ui.button(emoji=main.eight, style=nextcord.ButtonStyle.gray, row=3)
    async def eight(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, 7)

    @nextcord.ui.button(emoji=main.nine, style=nextcord.ButtonStyle.gray, row=3)
    async def nine(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, 8)

    @nextcord.ui.button(emoji=main.left, label="...", style=nextcord.ButtonStyle.gray, row=4)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = FarmView(self.user, self.texture_data, self.cur_lan, self.text)
        await get_farm_image(interaction, self.user, view, self.texture_data, True, self.cur_lan, self.text)
        self.stop()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class FarmView(nextcord.ui.View):
    def __init__(self, user: nextcord.Member, texture_data, cur_lan, text) -> None:
        super().__init__(timeout=600)
        self.user = user
        self.texture_data = texture_data
        self.cur_lan = cur_lan
        self.text = text

        self.plow.label = self.text["plow"]
        self.water.label = self.text["water"]
        self.fertilize.label = self.text["fertilize"]
        self.plant.label = self.text["plant"]
        self.harvest.label = self.text["harvest"]

    async def manage_actions(self, interaction, mode):
        view = FarmButtons(self.user, self.texture_data, self.cur_lan, mode, self.text)
        await get_farm_image(interaction, self.user, view, self.texture_data, True, self.cur_lan, self.text)
        self.stop()

    @nextcord.ui.button(label="...", style=nextcord.ButtonStyle.gray)
    async def plow(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, "plow")

    @nextcord.ui.button(label="...", style=nextcord.ButtonStyle.gray)
    async def water(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, "water")

    @nextcord.ui.button(label="...", style=nextcord.ButtonStyle.gray)
    async def fertilize(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, "fertilize")

    @nextcord.ui.button(label="...", style=nextcord.ButtonStyle.gray)
    async def plant(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        select_options = []
        seeds = fns.get_seeds()
        seed_amounts = await m_utils.items_amount.get_bulk_amount(self.user, items=copy.copy(seeds))
        for seed in seeds:
            seed = fns.get_item(seed, "id", self.cur_lan)
            desc = await fns.text_replacer(self.text["you_own"], ["{amount}", seed_amounts[seed.id]])
            select_options.append(nextcord.SelectOption(label=seed.disname, emoji=seed.emoji, value=seed.id, description=desc))

        dropdown = SeedSelector(self.user, self.cur_lan, select_options, self.text["choice"])
        view = PlantUI(60, self.user, self.cur_lan, dropdown, self.texture_data, self.text)
        await get_farm_image(interaction, self.user, view, self.texture_data, True, self.cur_lan, self.text)
        self.stop()

    @nextcord.ui.button(label="...", style=nextcord.ButtonStyle.gray)
    async def harvest(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.manage_actions(interaction, "harvest")

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
        return True


class Farming(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.texture_data = TextureData()

    @nextcord.slash_command(name="farm", description="View and manage your own farm.", description_localizations={"pl": "Wyświetl i zarządzaj swoją własną farmą."}, integration_types=main.integrations, contexts=main.contexts)
    async def farm(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['farm']

        await get_farm_image(interaction, user, FarmView(user, self.texture_data, cur_lan, text), self.texture_data, False, cur_lan, text)


def setup(client):
    client.add_cog(Farming(client))

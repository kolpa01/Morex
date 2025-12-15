import nextcord
from nextcord.ext import commands
import main
import json
import buttons
from nextcord import Interaction
import functions as fns
import asyncio
import complicated_relationship
import morex.logging as logging


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['help'])
    @commands.is_owner()
    async def asdafsfda(self, ctx):
        await ctx.send("m!test - sends progress bar (mina, maxa)\n\
m!add_quest_prg - updates quests progress (chapter, quest, amount)\n\
m!genfstab - generate help command (~~u~~, language, ~~els, files~~)\n\
**m!convertd - DO NOT USE IN PROD**\n\
m!xp - adds xp to author (xp)\n\
~~m!lmaolmao - sends random into about (0033) UNUSABLE~~\n\
m!db - prints info about a user (member)\n\
m!taks - updates author's dailt quesst\n\
m!reser - regen daily tasks\n\
m!itemz - sends all items\n\
m!itemztool - sends type and itemtype of all items\n\
m!divisionbyzero - generate 10 random progress bars\n\
~~**m!convert - DO NOT USE IN PROD** UNUSABLE~~\n\
~~**m!convertb - DO NOT USE IN PROD** UNUSABLE~~\n\
~~**m!convertc - DO NOT USE IN PROD** UNUSABLE~~\n\
~~m!dsa - adds bundle item PROBABLY UNUSABLE~~\n\
~~m!dsa2 - removes bundle item PROBABLY UNUSABLE~~\n\
m!sus - ping ada44 100 times\n\
m!barsss - sends 100 rising progres bars\n\
m!wwg - changes ur name (nick)\n\
m!mpg_cd - adds code to redeem\n\
m!itm_chgg - prints item info for changelog (first, last)\n\
m!omega_sus - forces bot to reload event cache\n\
m!enemiez - sends all oponents\
")

    async def resolve_rarity(self, i):
        if i == "common":
            i = "⚪ Pospolity"
        elif i == "uncommon":
            i = "🟢 Niepospolity"
        elif i == "rare":
            i = "🔵 Rzadki"
        elif i == "epic":
            i = "🟣 Epicki"
        elif i == "legendary":
            i = "🟡 Legendarny"
        elif i == "mythic":
            i = "🔴 Mityczny"
        elif i == "premium":
            i = "🟠 Premium"

        return i

    @commands.command()
    @commands.is_owner()
    async def enemiez(self, ctx):
        opo = await fns.opponenttable()
        for i in opo:
            await ctx.send(f'{i['emoji']} ({i['id']}) {i['name']} [.]({i['image']})')

    @commands.command()
    @commands.is_owner()
    async def itm_chgg(self, ctx, first, last):
        igems = await fns.itemsinfo()
        final_message = []
        send_mode = False
        for item in igems:
            if item['id'] != first and not send_mode:
                continue
            send_mode = True
            item = fns.get_item(item['id'], 'id', 'pl')
            final_message.append(f"<h3>{item.disname}</h3>")
            final_message.append(f"<p>\"{item.description.replace("\n", "<br>")}\"</p>")
            final_message.append(f"<p>Kupno: {item.price if item.price else '❌'}<br>Sprzedaż: {item.sellprice if item.sellprice else '❌'}<br>Rzadkość: {await self.resolve_rarity(item.rarity)}<br>Wymienialny: {'❌' if not item.tradeable else '✅'}</p>")
            if item.id == last:
                break
        logging.info("\n".join(final_message))
        await ctx.send("WuW")

    @commands.command()
    @commands.is_owner()
    async def mpg_cd(self, ctx, code):
        code_name, code = code.split("-")
        raw_rewards = code.split(";")
        rewards = []
        for code in raw_rewards:
            name, amount = code.split(":")
            amount = int(amount) if amount.isnumeric() else amount
            rewards.append({"item": name, "amount": amount})

        with open("ownerdb/codes.json", "r") as f:
            codes_file = json.load(f)

        codes_file.update({code_name: {"users": [], "rewards": rewards}})

        with open("ownerdb/codes.json", "w") as f:
            json.dump(codes_file, f)

    @commands.command()
    @commands.is_owner()
    async def omega_sus(self, ctx):
        randomsong = self.client.get_cog('Events')
        randomsong.reload_cache = True

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx, mina, maxa):
        res = await fns.progress_bar(float(mina), float(maxa))
        await ctx.send(f"{res}.")

    @commands.command()
    @commands.is_owner()
    async def wwg(self, ctx, *, nick=None):
        for member in ctx.guild.members:
            if member.id == self.client.user.id:
                await member.edit(nick=nick)
                break
        else:
            return
        await ctx.send("Removed Johnson Smith from database.")

    @nextcord.slash_command(name="test", guild_ids=[927971482448060477, 1222203197834399794, 1198437946810974258, 1132073153510789292])
    async def lmaoao(self, interaction: Interaction, one: str, two: str):
        dmd = await fns.playerinfo()
        csmb = await fns.opponenttable()
        embed = nextcord.Embed(title=f"Walka", color=main.color_normal)
        view = buttons.reverseHuntButtons(360, 200, 500, 200, 500,
                                          "https://cdn.discordapp.com/attachments/1228838259422138499/1264568639621828628/image.png?ex=669e58d2&is=669d0752&hm=5b241a2e54e2930111177ff625f34af0ae15fbb7558691a8cc2ecb72bfd5183f&",
                                          "woodensword", 0, 3, True, "U", csmb[0], interaction.user)

        await interaction.response.send_message(embed=embed, view=view)

    @nextcord.slash_command(name="d_t", guild_ids=[927971482448060477, 1222203197834399794, 1198437946810974258, 1132073153510789292])
    async def grep(self, interaction: Interaction):
        print(interaction.guild.get_role(934912007486971904))
        await complicated_relationship.init_dialogues(interaction, 'pl', "dialogues_v2")

    @commands.command()
    @commands.is_owner()
    async def add_quest_prg(self, ctx, chapter, quest, amount: int):
        await fns.update_quest(ctx.author, [chapter, quest], amount, 'pl')

    @commands.command()
    @commands.is_owner()
    async def genfstab(self, ctx, u, language, els, files):
        print(language)
        all_commandz = {}
        comand = self.client.get_application_commands()
        print(comand)
        if language == "/en":
            for i in comand:
                # await ctx.send(f"/{i.name} - {i.description}")
                if i.description != "No description provided.":
                    all_commandz.update({f"{i.name}": f"**/{i.name}** - {i.description}"})
                print(i.children)
                for k, ii in i.children.items():
                    # await ctx.send(f"/{i.name} {ii.name} - {ii.description}")
                    if ii.description != "No description provided.":
                        all_commandz.update({f"{i.name}{ii.name}": f"**/{i.name} {ii.name}** - {ii.description}"})
                    for kk, iii in ii.children.items():
                        # await ctx.send(f"/{i.name} {ii.name} {iii.name} - {iii.description}")
                        if iii.description != "No description provided.":
                            all_commandz.update({f"{i.name}{ii.name}{iii.name}": f"**/{i.name} {ii.name} {iii.name}** - {iii.description}"})
        else:
            for i in comand:
                # await ctx.send(f"/{i.name} - {i.description}")
                try:
                    all_commandz.update({f"{i.name}": f"**/{i.name}** - {i.description_localizations['pl']}"})
                except TypeError:
                    print("I DONT CARE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(i.children)
                for k, ii in i.children.items():
                    try:
                        # await ctx.send(f"/{i.name} {ii.name} - {ii.description}")
                        all_commandz.update({f"{i.name}{ii.name}": f"**/{i.name} {ii.name}** - {ii.description_localizations['pl']}"})
                    except TypeError:
                        print("I DONT CARE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    for kk, iii in ii.children.items():
                        # await ctx.send(f"/{i.name} {ii.name} {iii.name} - {iii.description}")
                        try:
                            all_commandz.update({f"{i.name}{ii.name}{iii.name}": f"**/{i.name} {ii.name} {iii.name}** - {iii.description_localizations['pl']}"})
                        except TypeError:
                            print("I DONT CARE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        saadsa = dict(sorted(all_commandz.items(), key=lambda item: item[0], reverse=False))
        my_treasure = []
        for k, i_dont_giev in saadsa.items():
            my_treasure.append(i_dont_giev)

        if language == "/en":
            b = 'en'
        else:
            b = 'pl'

        with open(f"ownerdb/{b}.json", "w") as f:
            json.dump(my_treasure, f)
        await ctx.send("X_X")

    @commands.command()
    @commands.is_owner()
    async def converd(self, ctx):
        a = await fns.playerinfo()

        for i in a:
            if a[i]['hp'] != 100:
                print(i)
            a[i]['hp'] = 100
            user = await self.client.fetch_user(i)
            await fns.create_account(user)

        with open('userdb/playerdata.json', "w") as f:
            json.dump(a, f)

        b = await fns.otherinfo()

        for i in b:
            if b[i]['skillpoint'] != a[i]['level']:
                print("asfsdf" + i)
            b[i]['skillpoint'] = a[i]['level']

        with open("userdb/otherdatabase.json", "w") as f:
            json.dump(b, f)

        await ctx.send("blututhdełajsizreditopear")

    @commands.command()
    @commands.is_owner()
    async def xp(self, ctx, xp: int):
        await fns.add_xp(ctx.author, xp)

    @nextcord.slash_command(name="lol", guild_ids=[927971482448060477, 1222203197834399794, 1198437946810974258, 1132073153510789292])
    async def lololol(self, interaction: Interaction):
        grid = [["D", "", "", "", "", "\n"],
                ["", "", "", "", "", "\n"],
                ["", "", "", "", "", "\n"],
                ["", "", "", "", "", "\n"],
                ["", "", "P", "", "", "\n"]]
        dpos = 0
        ppos = 2
        view = buttons.dodge(60, interaction.user)
        await interaction.response.send_message(content=str(grid), view=view)
        await asyncio.sleep(1)
        while True:

            dpos += 1
            if dpos == 5:
                dpos = 0
            grid[dpos][0] = "D"
            grid[dpos - 1][0] = ""
            await interaction.edit_original_message(content=str(grid))

            await asyncio.sleep(0.2)
            if view.value is True:
                grid[4][ppos] = ""
                grid[4][ppos - 1] = "P"
                ppos -= 1
                view.value = None
                await interaction.edit_original_message(content=str(grid))
            elif view.value is False:
                grid[4][ppos] = ""
                grid[4][ppos + 1] = "P"
                ppos += 1
                view.value = None
                await interaction.edit_original_message(content=str(grid))
            else:
                print("GRAB")

            await asyncio.sleep(0.2)
            if view.value is True:
                grid[4][ppos] = ""
                grid[4][ppos - 1] = "P"
                ppos -= 1
                view.value = None
                await interaction.edit_original_message(content=str(grid))
            elif view.value is False:
                grid[4][ppos] = ""
                grid[4][ppos + 1] = "P"
                ppos += 1
                view.value = None
                await interaction.edit_original_message(content=str(grid))
            else:
                print("GRAB")

            await asyncio.sleep(0.2)
            if view.value is True:
                grid[4][ppos] = ""
                grid[4][ppos - 1] = "P"
                ppos -= 1
                view.value = None
                await interaction.edit_original_message(content=str(grid))
            elif view.value is False:
                grid[4][ppos] = ""
                grid[4][ppos + 1] = "P"
                ppos += 1
                view.value = None
                await interaction.edit_original_message(content=str(grid))
            else:
                print("GRAB")

            await asyncio.sleep(0.2)
            if view.value is True:
                grid[4][ppos] = ""
                grid[4][ppos - 1] = "P"
                ppos -= 1
                view.value = None
                await interaction.edit_original_message(content=str(grid))
            elif view.value is False:
                grid[4][ppos] = ""
                grid[4][ppos + 1] = "P"
                ppos += 1
                view.value = None
                await interaction.edit_original_message(content=str(grid))
            else:
                print("GRAB")

            await asyncio.sleep(0.2)
            if view.value is True:
                grid[4][ppos] = ""
                grid[4][ppos - 1] = "P"
                ppos -= 1
                view.value = None
                await interaction.edit_original_message(content=str(grid))
            elif view.value is False:
                grid[4][ppos] = ""
                grid[4][ppos + 1] = "P"
                ppos += 1
                view.value = None
                await interaction.edit_original_message(content=str(grid))
            else:
                print("GRAB")

            # await interaction.edit_original_message(content=str(grid))

    @commands.command()
    @commands.is_owner()
    async def lmaolmao(self, ctx):
        item = await fns.get_item("0033", "id", "pl")

        await ctx.send(item.toolartibutes.power.type)
        # await ctx.send(item)
        # print(item)
        await ctx.send(str(item))
        await ctx.send(bool(item))

    @commands.command()
    @commands.is_owner()
    async def db(self, ctx, member: nextcord.Member):
        print(self.qualified_name)
        cts = await fns.custommobs()
        odb = await fns.otherinfo()
        mnb = await fns.get_inv_data()
        pld = await fns.playerinfo()
        qus = await fns.quests()
        sts = await fns.stats()

        print(f"custommobs.json: {cts[str(member.id)]}\n\n")
        print(f"otherdatabase.json: {odb[str(member.id)]}\n\n")
        print(f"mainbank.json: {mnb[str(member.id)]}\n\n")
        print(f"playerdata.json: {pld[str(member.id)]}\n\n")
        print(f"quests.json: {qus[str(member.id)]}\n\n")
        print(f"stats.json: {sts[str(member.id)]}\n\n")

    @commands.command()
    @commands.is_owner()
    async def taks(self, ctx):
        print("UwU")
        await fns.update_daily_task(ctx.author, "k", "greenslime", 3)

    @commands.command()
    @commands.is_owner()
    async def reser(self, ctx):
        a = await fns.get_daily_tasks()
        a[str(ctx.author.id)]['day'] = 0
        with open("userdb/dailytasks.json", "w") as f:
            json.dump(a, f)
        await fns.make_daily_tasks(ctx.author)

    @commands.command()
    @commands.is_owner()
    async def itemz(self, ctx):
        items = await fns.itemsinfo()

        for item in items:
            await ctx.send(f"{item['emoji']} ({item['id']}) {item['name']}")

    @commands.command()
    @commands.is_owner()
    async def itemztool(self, ctx):
        items = await fns.itemsinfo()
        seen = []
        for item in items:
            if item["toolatributes"] != "n":
                a = f"{item['toolatributes']['type']}/{item['toolatributes']['itemtype']}"
                if a not in seen:
                    seen.append(a)
                    await ctx.send(a)

    @commands.command()
    @commands.is_owner()
    async def divisionbyzero(self, ctx):
        for i in range(10):
            await ctx.send(f"{await fns.progress_bar(0, 0)} (0/0)")

    @commands.command()
    @commands.is_owner()
    async def convert(self, ctx):
        with open("newstats.json", "r") as f:
            status = json.load(f)

        sts = await fns.stats()

        for i in sts:
            uid = i
            beg = sts[i]["beg"]
            hunt = sts[i]["hunt"]
            shearvh = sts[i]["search"]

            status[str(uid)] = {}
            status[str(uid)]["beg"] = int(beg)
            status[str(uid)]["hunt"] = int(hunt)
            status[str(uid)]["search"] = int(shearvh)
            status[str(uid)]["fight"] = 0
            with open("newstats.json", "w") as f:
                json.dump(status, f)

    @commands.command()
    @commands.is_owner()
    async def convertb(self, ctx):
        with open("newplayerdata.json", "r") as f:
            player = json.load(f)

        psp = await fns.playerinfo()

        for i in psp:
            uid = i
            wallet = psp[i]["wallet"]
            bank = psp[i]["bank"]
            weapon_equiped = psp[i]["weapon_equiped"]
            hp = psp[i]["hp"]
            level = psp[i]["level"]
            xp = psp[i]["xp"]
            total_xp = psp[i]["total_xp"]
            beta = psp[i]["beta"]
            premium = psp[i]["premium"]
            badges = psp[i]["badges"]
            banned = psp[i]["banned"]
            version = psp[i]["version"]
            timestamp = psp[i]["timestamp"]

            player[str(uid)] = {}
            player[str(uid)]["wallet"] = wallet
            player[str(uid)]["bank"] = bank
            player[str(uid)]["weapon_equiped"] = [weapon_equiped, "none", "none"]
            player[str(uid)]["hp"] = hp
            player[str(uid)]["level"] = level
            player[str(uid)]["xp"] = xp
            # if level != 0:
            #   player[str(uid)]["total_xp"] = 100 * level + xp
            # else:
            player[str(uid)]["total_xp"] = total_xp
            player[str(uid)]["beta"] = beta
            player[str(uid)]["premium"] = premium
            player[str(uid)]["badges"] = badges
            player[str(uid)]["banned"] = banned
            player[str(uid)]["version"] = version
            player[str(uid)]["timestamp"] = timestamp

        with open("newplayerdata.json", "w") as f:
            json.dump(player, f)

    @commands.command()
    @commands.is_owner()
    async def convertc(self, ctx):
        with open("notb.json", "r") as f:
            oth = json.load(f)

        other = await fns.otherinfo()

        for i in other:
            uid = i
            skp = other[i]["skillpoint"]
            sdl = other[i]["search_defaultlocation"]
            ddl = other[i]["dig_defaultlocation"]
            hdl = ...
            slist = other[i]["search"]
            dlist = ...
            hlist = ...
            events = other[i]["events"]
            shop = other[i]["shop"]

            oth[str(uid)] = {}
            oth[str(uid)]["skillpoint"] = skp
            oth[str(uid)]["search_defaultlocation"] = sdl
            oth[str(uid)]["dig_defaultlocation"] = ddl
            oth[str(uid)]["hunt_defaultlocation"] = "slime_valley"
            oth[str(uid)]["search"] = slist
            oth[str(uid)]["dig"] = ["pit"]
            oth[str(uid)]["hunt"] = ["slime_valley"]
            oth[str(uid)]["events"] = events
            oth[str(uid)]["shop"] = shop
            with open("notb.json", "w") as f:
                json.dump(oth, f)

    @commands.command()
    @commands.is_owner()
    async def dsa(self, ctx, itm, amount: int, slot: int):
        a = await fns.bundle_add_item(ctx.author, itm, amount, "equipment", slot)
        await ctx.send(a)

    @commands.command()
    @commands.is_owner()
    async def dsa2(self, ctx, amount: int, slot: int):
        a = await fns.bundle_remove_item(ctx.author, amount, "equip", slot)
        await ctx.send(a)

    @commands.command()
    @commands.is_owner()
    async def sus(self, ctx):
        for i in range(100):
            await asyncio.sleep(0.5)
            await ctx.send("<@981287693268951090>")

    @commands.command()
    @commands.is_owner()
    async def barsss(self, ctx):
        for i in range(0, 100):
            await ctx.send(f"{await fns.progress_bar(i, 100)}")

   
def setup(client):
    client.add_cog(Dev(client))

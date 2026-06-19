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
import morex


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

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

    @commands.command(aliases=['help'])
    @commands.is_owner()
    async def asdafsfda(self, ctx):
        await ctx.send("m!test - sends progress bar (mina, maxa)\n\
m!add_quest_prg - updates quests progress (chapter, quest, amount)\n\
m!genfstab - generate help command (~~u~~, language, ~~els, files~~)\n\
m!reser - regen daily tasks\n\
m!itemz - sends all items\n\
m!itemztool - sends type and itemtype of all items\n\
m!barsss - sends 100 rising progres bars\n\
m!wwg - changes ur name (nick)\n\
m!mpg_cd - adds code to redeem\n\
m!itm_chgg - prints item info for changelog (first, last)\n\
m!omega_sus - forces bot to reload event cache\n\
m!enemiez - sends all oponents\n\
m!whattimeisit - gives you time and weather\n\
m!alphawolf - removes author from a clan\n\
m!aplacelikehome - shows probabilities of finding stuff (place)\
")

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
    async def barsss(self, ctx):
        for i in range(0, 100):
            await ctx.send(f"{await fns.progress_bar(i, 100)}")

    @commands.command()
    @commands.is_owner()
    async def whattimeisit(self, ctx):
        events_cog = self.client.get_cog("Events")
        if events_cog.time >= 1800 and events_cog.time < 5400:
            day_or_night = "day"
        else:
            day_or_night = "night"
        await ctx.send(f"It's {events_cog.time} and {day_or_night}")
        await ctx.send(f"Is it raining: {events_cog.is_raining}")

    @commands.command()
    @commands.is_owner()
    async def ilikenums(self, ctx, id, amount: int = 2):
        res = await fns.update_global_counter(id, ctx.author, amount)
        await ctx.send(res)

    @commands.command()
    @commands.is_owner()
    async def alphawolf(self, ctx):
        relationships = await fns.u_relationships()

        relationships[str(ctx.author.id)]["clan"] = None

        with open("userdb/relationships.json", "w") as f:
            json.dump(relationships, f)

        await ctx.send("left")

    @commands.command()
    @commands.is_owner()
    async def aplacelikehome(self, ctx, place):
        place: morex.MorexPlace = fns.get_search_locations(place, "en")
        if not place:
            await ctx.send("no.")

        for i in place.loottable:
            await ctx.send(f"{round((i["max_value"] - i["min_value"] + 1), 2) / 100}% {i["amount"]} {fns.get_item(i["item"], "name", "en")}")

        await ctx.send("JOHN")

    @commands.command()
    @commands.is_owner()
    async def create_counter(self, ctx, id):
        # im too lazy to add this shit to the event creation screen
        # temporary values too
        await fns.create_global_counter(
            id,
            {
                "1000": {
                    "rewards": [
                        {"name": "coins", "value": 21}
                    ],
                    "icon": "images/items/0005.png"
                }
            },
            {
                "1-1": [
                    {"name": "coins", "value": 21}
                ],
            }
        )
   

def setup(client):
    client.add_cog(Dev(client))

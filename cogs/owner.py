import nextcord
from nextcord.ext import commands
import functions as fns
import main
import json
from nextcord import Interaction
import re
from autocompletes.item_autocompletes import true_all
import complicated_relationship


class OwnerCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        name="owner",
        guild_ids=[
            927971482448060477,
            1222203197834399794,
            1198437946810974258,
            1132073153510789292,
            1315801334729146489
        ]
    )
    async def owner(self, interation: Interaction):
        pass

    @owner.subcommand(name="ban", description="Ban user from Morex :3")
    async def owner_ban(self, interaction: Interaction, user_id, reason, notify_user: bool = False):
        if interaction.user.id != 826792866776219709:
            return

        user = await self.client.fetch_user(int(user_id))
        await fns.create_account(user=user)
        player = await fns.playerinfo()

        player[str(user_id)]["banned"] = "yes"
        with open("userdb/playerdata.json", "w") as f:
            json.dump(player, f)

        embed = nextcord.Embed(title="Ban", description=f"You were banned from using Morex for:\n```{reason}```", color=main.color_normal)
        was_successful = None
        if notify_user:
            try:
                await user.send(embed=embed)
                was_successful = True
            except nextcord.Forbidden:
                was_successful = False

        await interaction.response.send_message(f"Ban't userr (this guy) -> {user.name}", ephemeral=True)
        user_data = await fns.short_user_info(user)
        channel = await self.client.fetch_channel(1333393576679178262)
        embed = nextcord.Embed(title=f"Banned {user.name}", description=f"{user_data['info']}\nStatus: {user_data['icon']}\nVersion: {user_data['acc_creation'][0]}\nTimestamp: <t:{user_data['acc_creation'][1]}>", color=0xff0000)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Notification", value=main.accept + ("" if was_successful else " (Failed)") if notify_user else main.deny, inline=False)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=main.version['en'])
        await channel.send(embed=embed)

    @owner.subcommand(name="unban", description="Unban user from Morex >:3")
    async def owner_unban(self, interaction: Interaction, user_id, notify_user: bool = False):
        if interaction.user.id != 826792866776219709:
            return

        user = await self.client.fetch_user(int(user_id))
        await fns.create_account(user=user)
        player = await fns.playerinfo()

        player[str(user_id)]["banned"] = "none"

        with open("userdb/playerdata.json", "w") as f:
            json.dump(player, f)

        embed = nextcord.Embed(title="Unban", description="You have been unbanned from Morex.", color=main.color_normal)
        was_successful = None
        if notify_user:
            try:
                await user.send(embed=embed)
                was_successful = True
            except nextcord.Forbidden:
                was_successful = False

        await interaction.response.send_message(f"Ubaned :#:###:#333#:#:#:#:3:#:3;#::3:#:##:3;3 {user.name}", ephemeral=True)
        user_data = await fns.short_user_info(user)
        channel = await self.client.fetch_channel(1333393576679178262)
        embed = nextcord.Embed(title=f"Unbanned {user.name}", description=f"{user_data['info']}\nStatus: {user_data['icon']}\nVersion: {user_data['acc_creation'][0]}\nTimestamp: <t:{user_data['acc_creation'][1]}>", color=0x00ff00)
        embed.add_field(name="Notification", value=main.accept + ("" if was_successful else " (Failed)") if notify_user else main.deny, inline=False)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=main.version['en'])
        await channel.send(embed=embed)

    @owner.subcommand(name="add_item", description="Dodaj przedmioty :3")
    async def owner_add_item(self, interaction: Interaction, user_id, itemp, amount: int):
        if interaction.user.id != 826792866776219709:
            return
        if user_id == "self":
            user_id = "826792866776219709"
        aa = await self.client.fetch_user(int(user_id))
        user = await fns.firsttime(aa)

        itemp = fns.get_item(itemp, 'name')

        await itemp.add_item(user, amount)
        embed = nextcord.Embed(title="Dodano item", description=f"Dodano {itemp} dla {aa}", color=main.color_normal)
        await interaction.response.send_message(embed=embed)
        
    @owner.subcommand(name="remove_item", description="Usuń przedmioty >:3")
    async def owner_add_remove(self, interaction: Interaction, user_id, itemp, amount: str):
        if interaction.user.id != 826792866776219709:
            return
        if user_id == "self":
            user_id = "826792866776219709"
        aa = await self.client.fetch_user(int(user_id))
        user = await fns.firsttime(aa)
        itemp = fns.get_item(itemp, "name")
        amount = await itemp.get_amount(user, amount)
        if amount is None:
            await interaction.response.send_message(content="Ziom itemu nie miał tyle (spróbuj all)")
            return
        elif amount is False:
            await interaction.response.send_message("idiot")
            return
        await itemp.remove_item(user, amount)
        
        embed = nextcord.Embed(title="Usunięto item", description=f"Usunięto {amount} {itemp} od {aa}", color=main.color_normal)
        await interaction.response.send_message(embed=embed)
        
    # @owner.subcommand(name="add_item", description="Dodaj przedmioty :3")
    # async def owner_add_item(self,interaction: Interaction, user_id,itemp, amount: int):
    #     if interaction.user.id != 826792866776219709:
    #         return
    #     if user_id == "self":
    #         user_id = "826792866776219709"
    #     aa = await self.client.fetch_user(int(user_id))
    #     user = await fnc.firsttime(aa)

    #     player = await fnc.playerinfo()
        
    #     await fnc.add_item(user, itemp, amount)
        
    #     embed=nextcord.Embed(title="Dodano item", description=f"Dodano {itemp} dla {aa}", color=main.color_normal)
    #     await interaction.response.send_message(embed=embed)
        
    # @owner.subcommand(name="add_item", description="Dodaj przedmioty :3")
    # async def owner_add_item(self,interaction: Interaction, user_id,itemp, amount: int):
    #     if interaction.user.id != 826792866776219709:
    #         return
    #     if user_id == "self":
    #         user_id = "826792866776219709"
    #     aa = await self.client.fetch_user(int(user_id))
    #     user = await fnc.firsttime(aa)

    #     player = await fnc.playerinfo()
        
    #     await fnc.add_item(user, itemp, amount)
        
    #     embed=nextcord.Embed(title="Dodano item", description=f"Dodano {itemp} dla {aa}", color=main.color_normal)
    #     await interaction.response.send_message(embed=embed)
  
    @owner.subcommand(name="database", description="Information about amount of users in each file")
    async def owner_db(self, interaction: Interaction):
        if interaction.user.id != 826792866776219709:
            return
        with open("userdb/custommobs.json", "r") as f:
            cts = json.load(f)
        with open("userdb/dailytasks.json", "r") as f:
            dts = json.load(f)
        with open("userdb/inventories.json", "r") as f:
            inv = json.load(f)
        with open("userdb/merchanttasks.json", "r") as f:
            mts = json.load(f)
        with open("userdb/otherdatabase.json", "r") as f:
            odb = json.load(f)
        with open("userdb/playerdata.json", "r") as f:
            pld = json.load(f)
        with open("userdb/quests.json", "r") as f:
            qts = json.load(f)
        with open("userdb/settings.json", "r") as f:
            stn = json.load(f)
        with open("userdb/skills.json", "r") as f:
            skl = json.load(f)
        with open("userdb/stats.json", "r") as f:
            sts = json.load(f)
        embed = nextcord.Embed(title="I used to roll the dice", description=f"custommobs.json - {len(cts)}\ndailytasks.json - {len(dts)}\ninventories.json - {len(inv)}\nmerchanttasks.json - {len(mts)}\notherdatabase.json - {len(odb)}\nplayerdata.json - {len(pld)}\nquests.json - {len(qts)}\nsettings.json - {len(stn)}\nskills.json - {len(skl)}\nstats.json - {len(sts)}")
        await interaction.response.send_message(embed=embed)
        
    @owner.subcommand(name="create_account", description="Wymuś utworzenie konta")
    async def owner_create_account(self, interaction: Interaction, uid: str):
        if interaction.user.id != 826792866776219709:
            return
        di = await self.client.fetch_user(int(uid))
        await fns.create_account(di)
        await interaction.response.send_message("Pomyślnie zmuszono użytkownika do konta", ephemeral=True)

    @nextcord.message_command(name="approve_mob", guild_ids=[927971482448060477])
    async def owner_create_accountt(self, interaction: Interaction, message):
        if interaction.user.id != 826792866776219709:
            return

        ussr_id = message.embeds[0].fields[0].value

        a = json.loads(message.content)

        cys = await fns.custommobs()
        if len(cys[str(ussr_id)]["mobs"]) == 0:
            a['id'] = "c000"
        else:
            number = int(cys[str(ussr_id)]['mobs'][-1]["id"][1:]) + 1
            if number > 99:
                a['id'] = "c" + str(number)
            else:
                a['id'] = "c" + ("0" * (3 - len(str(number)))) + str(number)
        
        cys[str(ussr_id)]["mobs"].append(a)
        
        with open("userdb/custommobs.json", "w") as f:
            json.dump(cys, f) 
            
        await interaction.response.send_message(f"Dodano {a['disname']} do {ussr_id}", ephemeral=True)
        if ussr_id != 1:
            cur_lan = await fns.get_lang(interaction.user)
            leng = await fns.lang(cur_lan)
            text = leng['commands']['custommobs_create']
            user = await self.client.fetch_user(ussr_id)
            embed = nextcord.Embed(title=text['accepted'], description=f"{text['accepted_info']}\n{a['displayname']}", color=main.color_normal)
            embed.set_footer(text=main.version[cur_lan])
            try:
                reas = await fns.has_enabled(user, "dm_notifications")
                if reas is True:
                    await user.send(embed=embed)
            except nextcord.Forbidden:
                pass 

    @nextcord.message_command(name="approve_mob_edit", guild_ids=[927971482448060477])
    async def owner_create_accountnnt(self, interaction: Interaction, message: nextcord.Message):
        if interaction.user.id != 826792866776219709:
            return

        # channel = self.client.get_channel(1259559255787442228)
        # message = await channel.fetch_message(int(id_message))
        ussr_id = message.embeds[0].fields[0].value

        print(message.content)
        print(ussr_id)
        a = json.loads(message.content)
        print(a)
        cys = await fns.custommobs()
        user_mob_id = cys[str(ussr_id)]['id']
        mob = fns.get_morex_oponent((user_mob_id, a['id']), "list", "en")
        for field, value in a.items():
            if field == "name":
                field = "sid"
            print(setattr(mob, field, value))

        mob = fns.get_morex_oponent((user_mob_id, a['id']), "list", "pl")
        for field, value in a.items():
            if field == "name":
                field = "sid"
            print(setattr(mob, field, value))

        for i in cys[str(ussr_id)]["mobs"]:
            print(i['id'] == a['id'])
            if i["id"] == a['id']:
                i.update(a)
                break
        
        with open("userdb/custommobs.json", "w") as f:
            json.dump(cys, f) 
            
        await interaction.response.send_message(f"Edytowano {a['disname']} do {ussr_id}", ephemeral=True)
        if ussr_id != 1:
            cur_lan = await fns.get_lang(interaction.user)
            leng = await fns.lang(cur_lan)
            text = leng['commands']['custommobs_create']
            user = await self.client.fetch_user(ussr_id)
            embed = nextcord.Embed(title=text['accepted'], description=f"{text['accepted_edit']}\n{mob.displayname}", color=main.color_normal)
            embed.set_footer(text=main.version[cur_lan])
            try:
                reas = await fns.has_enabled(user, "dm_notifications")
                if reas is True:
                    await user.send(embed=embed)
            except nextcord.Forbidden:
                print("didnt work")

    @owner.subcommand(name="add_image", description="Daj mobowi zdjęcie UwU")
    async def owner_create_accoadsunt(self, interaction: Interaction, user_id: str, mob_id: str, image_url: str, emoji: str):
        if interaction.user.id != 826792866776219709:
            return
        cys = await fns.custommobs()
        user_id = int(user_id)
        
        for mob in cys[str(user_id)]["mobs"]:
            if mob["id"] == mob_id:
                mob["image"] = image_url
            
                aaa = re.findall("^<.*>", mob['displayname'])
                mob['displayname'] = mob['displayname'].replace(aaa[0], emoji)
                zmienna = mob['displayname']
                break
        else:
            return

        with open("userdb/custommobs.json", "w") as f:
            json.dump(cys, f) 
            
        await interaction.response.send_message("Dodano zdjęcie do tego dziada", ephemeral=True)
        if user_id != 1:
            user = await self.client.fetch_user(user_id)
            embed = nextcord.Embed(title="Dodano zdjęcie", description=f"Stworzony przez ciebie wróg {zmienna} dostał zdjęcie.", color=main.color_normal)
            embed.set_thumbnail(url=image_url)
            embed.set_footer(text=main.version)
            try:
                reas = await fns.has_enabled(user, "dm_notifications")
                if reas is True:
                    await user.send(embed=embed)
            except nextcord.Forbidden:
                print("didnt work :")

    @owner.subcommand(name="item", description="View top 10 users in various categories.", description_localizations={"pl": "Zobacz 10 najelpszych osób w różnych dziedzinach."})
    async def item_lb(
        self, 
        interaction: Interaction,
        item=nextcord.SlashOption(
            name="item",
            description="item",
            required=True,
        )
    ):
        if interaction.user.id != 826792866776219709:
            return
        await interaction.response.defer()

        leader_board = {}
        total = 0
        users = await fns.get_inv_data()
        item = fns.get_item(item, "id", "en")
        for user_id, user_data in users.items():
            for itm in user_data['bag']:
                if item.id == itm['item']:
                    leader_board[user_id] = itm['amount']
                    total += itm['amount']
                    break

        leader_board = dict(sorted(leader_board.items(), key=lambda item: item[1], reverse=True))

        embed = nextcord.Embed(title="Nya", color=main.color_normal)
        embed.set_thumbnail(url=item.image)

        embeds = []
        index = 1
        please_not_10 = 0
        for user_id, amount in leader_board.items():
            please_not_10 += 1
            if please_not_10 == 11:
                embeds.append(embed)
                embed = nextcord.Embed(title="Nya", color=main.color_normal)
                embed.set_thumbnail(url=item.image)
                please_not_10 = 0

            member = await self.client.fetch_user(int(user_id))
            
            if member is None:
                name = "???"
                id_ = 0
            else:
                name = member.name
                id_ = member.id
            embed.add_field(name=f"{index}. {name} ({id_})", value=f"{amount} {item.displayname}", inline=False)
            index += 1
            
        if please_not_10 != 0:
            embeds.append(embed)

        embed = embeds[0]

        embed.set_footer(text=f"Page 1/{len(embeds)} | {main.version['en']}")

        view = await complicated_relationship.pages_helper(embeds, interaction.user)
        await interaction.followup.send(embed=embed, view=view)

    @item_lb.on_autocomplete("item")
    async def item_lb_autocomplete(self, interaction, current: str):
        data = await true_all(current)
        await interaction.response.send_autocomplete(data)


def setup(client):
    client.add_cog(OwnerCommands(client))

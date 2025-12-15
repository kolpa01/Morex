import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import random
import buttons
import functions as fns
import main


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="balance", description="View balance.", description_localizations={"pl": "Wyświetl stan konta."})
    async def balance(
            self,
            interaction: Interaction,
            osoba: nextcord.Member = SlashOption(
                name="member",
                name_localizations={"pl": "osoba"},
                description="Select a member.",
                description_localizations={"pl": "Wybierz osobę."},
                required=False
            )
    ):
        if osoba is None:
            user = await fns.firsttime(interaction.user)
            cur_lan = await fns.get_lang(user)
        else:
            aa = await fns.firsttime(interaction.user, osoba)
            cur_lan = await fns.get_lang(interaction.user)

            if aa is False:
                await fns.no_account(interaction, cur_lan)
                return
            elif aa == "pmerr":
                await fns.pmerr(interaction, cur_lan)
                return
            elif aa == "mperr":
                await fns.mperr(interaction, cur_lan)
                return
            user = aa[1]

        leng = await fns.lang(cur_lan)
        text = leng['commands']['balance']
        users = await fns.playerinfo()
        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        both = wallet_amt + bank_amt

        embed = nextcord.Embed(color=main.color_normal)
        embed.set_author(name=f"{text['title']} {user.name}", icon_url=str(user.display_avatar))
        embed.add_field(name=text['field1'], value=f"{wallet_amt} {main.coin}")
        embed.add_field(name=text['field2'], value=f"{bank_amt} {main.coin}", inline=False)
        embed.add_field(name=text['field3'], value=f"{both} {main.coin}", inline=False)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="beg", description="Beg to get a few coins.", description_localizations={"pl": "Żebraj, aby zdobyć kilka monet."})
    async def beg(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['beg']

        person = random.choice(text['person'])
        coin_txt = random.choice(text['coin'])
        item_txt = random.choice(text['item'])
        nocoin_txt = random.choice(text['nothing'])

        reward = await fns.beg_rewards()
        reward_dict = await fns.get_from_value(reward['drops'])

        if reward_dict["item"] == "nothing":
            embed = nextcord.Embed(title=person, description=nocoin_txt, color=main.color_normal)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return
        elif reward_dict["item"] == "coins":
            earnings = random.randint(reward_dict["amount"][0], reward_dict["amount"][1])
            boost = await fns.has_event_boost('beg_coins')
            earnings = boost * earnings
            await fns.update_bank(user, earnings, "wallet")
            await fns.update_stat(user, "beg", 1)
            embed = nextcord.Embed(title=person, description=f"{coin_txt} {earnings} {main.coin}", color=main.color_normal)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
        else:
            item = fns.get_item(reward_dict["item"], "name", cur_lan)

            earnings = random.randint(reward['passive_coins'][0], reward['passive_coins'][1])
            boost = await fns.has_event_boost('beg_coins')
            earnings = boost * earnings
            await item.add_item(user, reward_dict['amount'])
            await fns.update_bank(user, earnings, "wallet")
            await fns.update_stat(user, "beg", 1)
            embed = nextcord.Embed(title=person, description=f"{coin_txt} {earnings} {main.coin} {item_txt} {reward_dict['amount']} {item.displayname}", color=main.color_normal)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
        await fns.update_daily_task(user, "c", "beg", 1)

    @nextcord.slash_command(name="buy", description="Buy items from the shop using coins.", description_localizations={"pl": "Kup przedmioty ze sklepu za pomocą monet."})
    async def buy(
            self,
            interaction: Interaction,
            itemp: str = SlashOption(
                name="item",
                name_localizations={"pl": "przedmiot"},
                description="Choose the item.",
                description_localizations={"pl": "Wybierz przedmiot."},
                required=True
            ),
            amount: str = SlashOption(
                name="amount",
                name_localizations={"pl": "ilość"},
                description="Choose an amount. (25, 3, all)",
                description_localizations={"pl": "Wybierz ilość. (25, 3, all)"},
                required=False
            )
    ):
        playerdata = await fns.playerinfo()

        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['buy']

        item = fns.get_item(itemp, "id", cur_lan)
        if item is None:
            return
        if item.price is False:
            return

        result = await fns.get_amount_item(user, item, amount)

        if result is None:
            embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        elif result is False:
            if amount is None or amount == "all":
                amount = 1
            proice = item.price * int(amount)
            cost = proice - playerdata[str(user.id)]["wallet"]
            nocoins = await fns.text_replacer(text['no_coins0'], ['{item}', item.displayname], ['{cost}', cost], ['{coin}', main.coin], ['{amount}', amount])
            if playerdata[str(user.id)]["bank"] >= cost:
                embed = nextcord.Embed(
                    description=f"{nocoins}\n\n{text['no_coins1']}",
                    color=main.color_normal
                )
            else:
                embed = nextcord.Embed(
                    description=nocoins,
                    color=main.color_normal
                )
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return
        else:
            if "i" in item.id:
                has_station = await item.get_amount(interaction.user, "1")
                if has_station:
                    return
                else:
                    amount = 1
            else:
                amount = result
            view = buttons.ConfirmationButtons(60, user)
            embed = nextcord.Embed(
                description=await fns.text_replacer(text['confirmation'], ['{item}', item.displayname], ['{cost}', amount*item.price], ['{coin}', main.coin], ['{amount}', amount]),
                color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, view=view)
            await view.wait()
            if view.value is False or view.value is None:
                await interaction.edit_original_message(view=None)
                return

        res = await fns.buy_this(user, item, amount)

        if not res:
            proice = item.price * amount
            cost = proice - playerdata[str(user.id)]["wallet"]
            nocoins = await fns.text_replacer(text['no_coins0'], ['{item}', item.displayname], ['{cost}', cost], ['{coin}', main.coin], ['{amount}', amount])
            if playerdata[str(user.id)]["bank"] >= cost:
                embed = nextcord.Embed(
                    description=f"{nocoins}\n\n{text['no_coins1']}",
                    color=main.color_normal
                )
            else:
                embed = nextcord.Embed(
                    description=nocoins,
                    color=main.color_normal
                )
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.edit_original_message(embed=embed, view=None)
            return
        else:
            bought = await fns.text_replacer(text['bought'], ['{item}', item.displayname], ['{cost}', amount * item.price], ['{coin}', main.coin], ['{amount}', amount])
            embed = nextcord.Embed(description=bought, color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.edit_original_message(embed=embed, view=None)

    @nextcord.slash_command(name="deposit", description="Deposit coins into the bank.", description_localizations={"pl": "Wpłać monety do banku."})
    async def deposit(self, interaction=Interaction, amount: str = SlashOption(
            name="amount",
            name_localizations={"pl": "ilość"},
            description="Choose an amount. (25, 3, all)",
            description_localizations={"pl": "Wybierz ilość. (25, 3, all)"},
            required=True
    )):
        user = await fns.firsttime(interaction.user)
        result = await fns.get_amount(amount, user, "wallet")
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['deposit']

        if result is False:
            embed = nextcord.Embed(description=leng['other']['not_enough_coins']['description'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif result is None:
            embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await fns.update_bank(user, result, "bank")
            await fns.update_bank(user, -1 * result, "wallet")
            embed = nextcord.Embed(description=f"{text['bank']} {result} {main.coin}", color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="rob", description="Try to rob someone to earn some coins.", description_localizations={"pl": "Spróbuj kogoś okraść, aby zdobyć monety."})
    async def rob(self, interaction: Interaction, member: nextcord.Member = SlashOption(
        name="member",
        name_localizations={"pl": "osoba"},
        description="Select a member.",
        description_localizations={"pl": "Wybierz osobę."},
        required=True
    )):
        aa = await fns.firsttime(interaction.user, member)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['rob']
        if aa is False:
            await fns.no_account(interaction, cur_lan)
            return
        elif aa == "mperr":
            await fns.mperr(interaction, cur_lan)
            return
        elif aa == "pmerr":
            await fns.pmerr(interaction, cur_lan)
            return
        interaction.user = aa[0]
        member = aa[1]

        if str(member.id) == "826792866776219709":
            embed = nextcord.Embed(description=text['shield'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if member.bot is True:
            embed = nextcord.Embed(description=leng['other']['bot']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if member == interaction.user:
            embed = nextcord.Embed(description=text['is_himself'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        i = random.randint(1, 10)
        pd = await fns.playerinfo()
        if i >= 4:
            if pd[str(member.id)]["wallet"] == 0:
                amount = 0
            else:
                if pd[str(interaction.user.id)]["wallet"] == 0:
                    amount = 0
                else:
                    amount = random.randint(0, pd[str(member.id)]["wallet"])

            if amount == 0:
                embed = nextcord.Embed(description=text['fail0'], color=main.color_normal)
                embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
                embed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=embed)
                return
            embed = nextcord.Embed(description=f"{text['succes']} <@{member.id}> {amount} {main.coin}", color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            await fns.update_bank(interaction.user, amount, "wallet")
            await fns.update_bank(member, -1 * amount, "wallet")
        else:
            amount = random.randint(0, pd[str(interaction.user.id)]["wallet"])
            if amount == 0:
                embed = nextcord.Embed(description=text['fail0'], color=main.color_normal)
                embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
                embed.set_footer(text=main.version[cur_lan])
                await interaction.response.send_message(embed=embed)
                return
            embed = nextcord.Embed(description=await fns.text_replacer(text['fail1'], ['{user}', f'<@{member.id}>'], ['{amount}', amount], ['{coin}', main.coin]), color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            await fns.update_bank(interaction.user, -1 * amount, "wallet")
            await fns.update_bank(member, amount, "wallet")

    @nextcord.slash_command(name="sell", description="Sell your items to earn coins.", description_localizations={"pl": "Sprzedaj swoje przedmioty, aby zdobyć monety."})
    async def sell(
        self,
        interaction: Interaction,
        itemp: str = SlashOption(
            name="item",
            name_localizations={"pl": "przedmiot"},
            description="Choose the item.",
            description_localizations={"pl": "Wybierz przedmiot."},
            required=True,
        ),
        amount: str = SlashOption(
            name="amount",
            name_localizations={"pl": "ilość"},
            description="Choose an amount. (25, 3, all)",
            description_localizations={"pl": "Wybierz ilość. (25, 3, all)"},
            required=False
        )
    ):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['sell']
        item = fns.get_item(itemp, "id", cur_lan)
        if item is None:
            return
        if item.sellprice is False:
            return

        amount = await item.get_amount(interaction.user, amount)

        if amount is False:
            embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        elif amount is None:
            embed = nextcord.Embed(description=leng['other']['not_enough_items']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        view = buttons.ConfirmationButtons(60, interaction.user)
        embed = nextcord.Embed(
            description=await fns.text_replacer(text['confirmation'], ['{item}', item.displayname], ['{cost}', amount * item.sellprice], ['{coin}', main.coin], ['{amount}', amount]),
            color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()
        if view.value is False or view.value is None:
            await interaction.edit_original_message(view=None)
            return

        amount = await item.get_amount(interaction.user, amount)

        if amount is False:
            embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.edit_original_message(embed=embed)
            return
        elif amount is None:
            embed = nextcord.Embed(description=leng['other']['not_enough_items']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.edit_original_message(embed=embed)
            return

        await fns.sell_this(interaction.user, item, amount)

        embed = nextcord.Embed(
            description=await fns.text_replacer(text['sold'], ['{item}', item.displayname],
                                                ['{cost}', amount * item.sellprice], ['{coin}', main.coin],
                                                ['{amount}', amount]),
            color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar))
        embed.set_footer(text=main.version[cur_lan])
        await interaction.edit_original_message(embed=embed, view=None)

    @nextcord.slash_command(name="slots", description="Play at slots machine to win coins.", description_localizations={"pl": "Zagraj w automacie, aby wygrać monety."})
    async def slots(
            self,
            interaction: Interaction,
            bet: str = SlashOption(
                name="amount",
                name_localizations={"pl": "ilość"},
                description="Choose an amount. (25, 3, all)",
                description_localizations={"pl": "Wybierz ilość. (25, 3, all)"},
                required=True
            )
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text_cmd = leng['commands']['slots']
        bet = await fns.get_amount(bet, user, "wallet")
        if bet is False:
            embed = nextcord.Embed(description=leng['other']['not_enough_coins']['description'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif bet is None:
            embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)

        await fns.update_bank(user, -1 * bet)
        #  - 150%,  - 300%,  - 200%
        top_row = await fns.dead_row()
        bottom_row = await fns.dead_row()
        jj = [
            {"emoji": "<:MX_Cash:1198436125279256576>", "min_chance": 1, "max_chance": 80},
            {"emoji": "<:MX_GolenEssence:1222205491728351344>", "min_chance": 81, "max_chance": 95},
            {"emoji": "<:MX_Diamond:1241071516410581002>", "min_chance": 96, "max_chance": 100}
        ]
        middle_row = []
        for i in range(3):
            popp = random.randint(1, 100)
            for ii in jj:
                if ii["min_chance"] <= popp <= ii["max_chance"]:
                    middle_row.append(ii["emoji"])
                    continue
        if middle_row[0] == middle_row[1] == middle_row[2]:
            if middle_row[0] == "<:MX_Cash:1198436125279256576>":
                multi = 2
            elif middle_row[0] == "<:MX_GolenEssence:1222205491728351344>":
                multi = 5
            elif middle_row[0] == "<:MX_Diamond:1241071516410581002>":
                multi = 10
            else:
                multi = 1
            award = int(multi * bet)

            text = await fns.create_text(top_row, middle_row, bottom_row)
            text += f"\n{text_cmd['win']} {award} {main.coin}"
            await fns.update_bank(interaction.user, award, "wallet")
            embed = nextcord.Embed(title=text_cmd['machine'], description=text, color=main.color_normal)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
        else:
            text = await fns.create_text(top_row, middle_row, bottom_row)
            text += f"\n{text_cmd['lost']} {bet} {main.coin}"
            embed = nextcord.Embed(title=text_cmd['machine'], description=text, color=main.color_normal)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="shop", description="Displays a shop with every item you can buy.", description_localizations={"pl": "Wyświetla sklep z każdym przedmiotem, który można kupić."})
    async def shop(self, interaction: Interaction):
        interaction.user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['shop']

        txt = []
        for i in leng['items']['name']:
            item = fns.get_item(i, "id", cur_lan)
            if item.price:
                txt.append(f"{item.displayname} - {item.price} {main.coin}\n")

        embed = nextcord.Embed(title=text['shop'], description="".join(txt), color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])

        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="withdraw", description="Withdraw coins from the bank.", description_localizations={"pl": "Wypłać monety z banku."})
    async def withdraw(self, interaction=Interaction, amount: str = SlashOption(
            name="amount",
            name_localizations={"pl": "ilość"},
            description="Choose an amount. (25, 3, all)",
            description_localizations={"pl": "Wybierz ilość. (25, 3, all)"},
            required=True
    )):
        user = await fns.firsttime(interaction.user)
        result = await fns.get_amount(amount, user, "bank")
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['withdraw']

        if result is False:
            embed = nextcord.Embed(description=leng['other']['not_enough_coins']['description'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif result is None:
            embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await fns.update_bank(user, result, "wallet")
            await fns.update_bank(user, -1 * result, "bank")
            embed = nextcord.Embed(description=f"{text['wallet']} {result} {main.coin}", color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)

    @buy.on_autocomplete("itemp")
    async def buy_autocomplete(self, interaction, current: str):
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        language = await fns.lang(leng)
        data = {}
        i = 0
        if not current:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.price:
                    i += 1
                    data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.price:
                    if str(current.lower()) in chk_it.disname.lower():
                        i += 1
                        data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))

    @sell.on_autocomplete("itemp")
    async def sell_autocomplete(self, interaction, current: str):
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        language = await fns.lang(leng)
        data = {}
        i = 0
        if not current:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.sellprice:
                    i += 1
                    data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.sellprice:
                    if str(current.lower()) in chk_it.disname.lower():
                        i += 1
                        data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))


def setup(client):
    client.add_cog(Economy(client))

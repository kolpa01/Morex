import nextcord
from nextcord.ext import commands
import main
import buttons
from nextcord import Interaction, SlashOption
import functions as fns


class TradingCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="give")
    async def give(self, interaction: Interaction):
        pass

    @give.subcommand(name="item", description="Give items to the other person.", description_localizations={"pl": "Daj przedmioty innej osobie."})
    async def give_item(
            self,
            interaction: Interaction,
            member: nextcord.Member = SlashOption(
                name="member",
                name_localizations={"pl": "osoba"},
                description="Select a member.",
                description_localizations={"pl": "Wybierz osobę."},
                required=True
            ),
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
                required=True
            )
    ):
        aa = await fns.firsttime(interaction.user, member)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['give_item']
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

        item = await fns.get_item_with_handling(itemp, 'id', cur_lan, interaction)
        if not item:
            return

        if not item.tradeable:
            await fns.untradeable_item(interaction, cur_lan)
            return

        if member.bot is True:
            embed = nextcord.Embed(description=leng['other']['bot']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if member == interaction.user:
            embed = nextcord.Embed(description=text['is_himself'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        amount = await item.get_amount(interaction.user, amount)

        if amount is False:
            embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        elif amount is None:
            embed = nextcord.Embed(description=leng['other']['not_enough_items']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        view = buttons.ConfirmationButtons(60, interaction.user)
        embed = nextcord.Embed(description=await fns.text_replacer(text['confirmation'], ['{item}', item.displayname], ['{user}', f'<@{member.id}>'], ['{amount}', amount]), color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()
        if view.value is False or view.value is None:
            await interaction.edit_original_message(view=None)
            return

        amount = await item.get_amount(interaction.user, amount)

        if amount is False:
            embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.edit_original_message(embed=embed, view=None)
            return
        elif amount is None:
            embed = nextcord.Embed(description=leng['other']['not_enough_items']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.edit_original_message(embed=embed, view=None)
            return

        await item.add_item(member, amount)
        await item.remove_item(interaction.user, amount)
        embed = nextcord.Embed(description=f"{text['gave']} <@{member.id}> {amount} {item.displayname}", color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.edit_original_message(embed=embed, view=None)

    @give.subcommand(name="coins", description="Give coins to the other person.", description_localizations={"pl": "Daj monety innej osobie."})
    async def give_money(
            self,
            interaction: Interaction,
            member: nextcord.Member = SlashOption(
                name="member",
                name_localizations={"pl": "osoba"},
                description="Select a member.",
                description_localizations={"pl": "Wybierz osobę."},
                required=True
            ),
            amount: str = SlashOption(
                name="amount",
                name_localizations={"pl": "ilość"},
                description="Choose an amount. (25, 3, all)",
                description_localizations={"pl": "Wybierz ilość. (25, 3, all)"},
                required=True
            )
    ):
        aa = await fns.firsttime(interaction.user, member)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['give_money']
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

        if member.bot is True:
            embed = nextcord.Embed(description=leng['other']['bot']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if member == interaction.user:
            embed = nextcord.Embed(description=text['is_himself'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        amount = await fns.get_amount(amount, interaction.user, 'wallet')
        if amount is False:
            embed = nextcord.Embed(description=text['no_coins'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        elif amount is None:
            embed = nextcord.Embed(description=leng['other']['invalid_value']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        view = buttons.ConfirmationButtons(60, interaction.user)
        embed = nextcord.Embed(
            description=await fns.text_replacer(text['confirmation'], ['{coin}', main.coin],
                                                ['{user}', f'<@{member.id}>'], ['{amount}', amount]),
            color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()
        if view.value is False or view.value is None:
            await interaction.edit_original_message(view=None)
            return

        amount = await fns.get_amount(amount, interaction.user, 'wallet')

        if amount is False:
            embed = nextcord.Embed(description=text['no_coins'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.edit_original_message(embed=embed, view=None)
            return

        await fns.update_bank(interaction.user, -1 * amount)
        await fns.update_bank(member, amount)
        embed = nextcord.Embed(description=f"{text['gave']} <@{member.id}> {amount} {main.coin}", color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.edit_original_message(embed=embed, view=None)

    @nextcord.slash_command(name="trade")
    async def trade(self, interaction: Interaction):
        pass

    @trade.subcommand(name="for_coins", description="Trade coins for items and vice versa.", description_localizations={"pl": "Wymień się monetami za przedmioty i odwrotnie."})
    async def trade_for_coins(
            self,
            interaction: Interaction,
            member: nextcord.Member = SlashOption(
                name="member",
                name_localizations={"pl": "osoba"},
                description="Select a member.",
                description_localizations={"pl": "Wybierz osobę."},
                required=True
            ),
            mode=SlashOption(
                name="mode",
                name_localizations={"pl": "tryb"},
                description="Choose if you want to give coins and get items or give items and get coins.",
                description_localizations={"pl": "Wybierz czy chcesz dać monety i zdobyć przedmiot, czy dać przedmiot i zdobyć monety"},
                choices={"Give coins": "mine", "Give items": "yours"},
                choice_localizations={"pl": {"Dać monety": "mine", "Dać przedmiot": "yours"}},
                required=True
            ),
            coins: str = SlashOption(
                name="coins",
                name_localizations={"pl": "monety"},
                description="Choose the amount of coins. (500, 1250, all)",
                description_localizations={"pl": "Wybierz ilość monet. (500, 1250, all)"},
                required=True,
            ),
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
                required=True
            )):
        aa = await fns.firsttime(interaction.user, member)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['trade_money']
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

        if member.bot is True:
            embed = nextcord.Embed(description=leng['other']['bot']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if member == interaction.user:
            embed = nextcord.Embed(description=text['is_himself'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        item = await fns.get_item_with_handling(itemp, 'id', cur_lan, interaction)
        if not item:
            return

        if not item.tradeable:
            await fns.untradeable_item(interaction, cur_lan)
            return

        if mode == "mine":
            c_user = interaction.user
            i_user = member
        else:
            i_user = interaction.user
            c_user = member

        initial_check = await fns.trade_for_coins_check(interaction, c_user, i_user, coins, item, amount, leng, cur_lan, True, None)
        if initial_check is False:
            return

        amount = await item.get_amount(i_user, amount)
        coins = await fns.get_amount(coins, c_user, "wallet")

        view = buttons.ConfirmationButtons(60, interaction.user)
        embeda = nextcord.Embed(title=text['trade'], description=text['confirmation'], color=main.color_normal)
        if interaction.user == i_user:
            embeda.add_field(name=text['you_get'], value=f"{coins} {main.coin}", inline=False)
            embeda.add_field(name=text['you_give'], value=f"{amount} {item.displayname}", inline=False)
        else:
            embeda.add_field(name=text['you_get'], value=f"{amount} {item.displayname}", inline=False)
            embeda.add_field(name=text['you_give'], value=f"{coins} {main.coin}", inline=False)
        embeda.set_footer(text=main.version[cur_lan])
        msg = await interaction.response.send_message(content=interaction.user.mention, embed=embeda, view=view)
        await view.wait()
        if view.value is False or view.value is None:
            await interaction.edit_original_message(content=None, view=None)
            return
        msg = await msg.fetch()
        anotha_check = await fns.trade_for_coins_check(interaction, c_user, i_user, coins, item, amount, leng, cur_lan, False, view, msg.id)
        if anotha_check is False:
            return
        await interaction.edit_original_message(content=None, view=None)

        view = buttons.ConfirmationButtons(60, member)
        embeda = nextcord.Embed(title=text['trade'], description=text['confirmation'], color=main.color_normal)
        if member == c_user:
            embeda.add_field(name=text['you_get'], value=f"{amount} {item.displayname}", inline=False)
            embeda.add_field(name=text['you_give'], value=f"{coins} {main.coin}", inline=False)
        else:
            embeda.add_field(name=text['you_get'], value=f"{coins} {main.coin}", inline=False)
            embeda.add_field(name=text['you_give'], value=f"{amount} {item.displayname}", inline=False)
        embeda.set_footer(text=main.version[cur_lan])
        msg = await interaction.send(content=member.mention, embed=embeda, view=view)
        await view.wait()
        if view.value is False or view.value is None:
            await msg.edit(content=None, view=None)
            return

        anotha_check2 = await fns.trade_for_coins_check(interaction, c_user, i_user, coins, item, amount, leng, cur_lan, False, view, None, msg)
        if anotha_check2 is False:
            return

        await fns.update_bank(c_user, coins * -1, "wallet")
        await fns.update_bank(i_user, coins, "wallet")
        await item.add_item(c_user, amount)
        await item.remove_item(i_user, amount)

        await msg.edit(content=None, view=None)

        # USER MESSAGE HANDLER

        debug_info = await fns.has_enabled(c_user, "dm_notifications")
        if debug_info is True:
            await fns.user_dm_handler_trade_for_coins(c_user, itemp, amount, coins)

        debug_info2 = await fns.has_enabled(i_user, "dm_notifications")
        if debug_info2 is True:
            await fns.user_dm_handler_trade_for_coins(None, itemp, amount, coins, i_user)

        embed = nextcord.Embed(title=text['trade'], description=text['successful'], color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.send(embed=embed)

    @trade.subcommand(name="for_item", description="Trade your items for other user's items.", description_localizations={"pl": "Wymień się swoimi przedmiotami na przedmioty innego użytkownika."})
    async def trade_for_item(
            self,
            interaction: Interaction,
            member: nextcord.Member = SlashOption(
                name="member",
                name_localizations={"pl": "osoba"},
                description="Select a member.",
                description_localizations={"pl": "Wybierz osobę."},
                required=True
            ),
            item_author: str = SlashOption(
                name="your_item",
                name_localizations={"pl": "twój_przedmiot"},
                description="Choose the item.",
                description_localizations={"pl": "Wybierz przedmiot."},
                required=True,
            ),
            amount_author: str = SlashOption(
                name="your_amount",
                name_localizations={"pl": "twoja_ilość"},
                description="Choose an amount. (25, 3, all)",
                description_localizations={"pl": "Wybierz ilość. (25, 3, all)"},
                required=True
            ),
            item_member: str = SlashOption(
                name="member_item",
                name_localizations={"pl": "przedmiot_osoby"},
                description="Choose the item.",
                description_localizations={"pl": "Wybierz przedmiot."},
                required=True,
            ),
            amount_member: str = SlashOption(
                name="member_amount",
                name_localizations={"pl": "ilość_osoby"},
                description="Choose an amount. (25, 3, all)",
                description_localizations={"pl": "Wybierz ilość. (25, 3, all)"},
                required=True
            )
    ):
        aa = await fns.firsttime(interaction.user, member)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['trade_item']
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

        if member.bot is True:
            embed = nextcord.Embed(description=leng['other']['bot']['description'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if member == interaction.user:
            embed = nextcord.Embed(description=text['is_himself'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        item1 = await fns.get_item_with_handling(item_author, 'id', cur_lan, interaction)
        if not item1:
            return
        item2 = await fns.get_item_with_handling(item_member, 'id', cur_lan, interaction)
        if not item2:
            return

        if not item1.tradeable or not item2.tradeable:
            await fns.untradeable_item(interaction, cur_lan)
            return

        if item1 == item2:
            embed = nextcord.Embed(description=text['same'], color=main.color_normal)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        initial_check = await fns.trade_for_items_check(interaction, interaction.user, member, item1, item2, amount_author, amount_member, leng, cur_lan, True, None)
        if initial_check is False:
            return

        amount_author = await item1.get_amount(interaction.user, amount_author)
        amount_member = await item2.get_amount(member, amount_member)

        view = buttons.ConfirmationButtons(60, interaction.user)
        embeda = nextcord.Embed(title=text['trade'], description=text['confirmation'], color=main.color_normal)
        embeda.add_field(name=text['you_get'], value=f"{amount_member} {item2.displayname}", inline=False)
        embeda.add_field(name=text['you_give'], value=f"{amount_author} {item1.displayname}", inline=False)
        embeda.set_footer(text=main.version[cur_lan])
        msg = await interaction.response.send_message(content=interaction.user.mention, embed=embeda, view=view)
        await view.wait()
        if view.value is False or view.value is None:
            await interaction.edit_original_message(content=None, view=None)
            return
        msg = await msg.fetch()
        anotha_check = await fns.trade_for_items_check(interaction, interaction.user, member, item1, item2, amount_author, amount_member, leng, cur_lan, False, view, msg.id)
        if anotha_check is False:
            return
        await interaction.edit_original_message(content=None, view=None)

        view = buttons.ConfirmationButtons(60, member)
        embeda = nextcord.Embed(title=text['trade'], description=text['confirmation'], color=main.color_normal)
        embeda.add_field(name=text['you_get'], value=f"{amount_author} {item1.displayname}", inline=False)
        embeda.add_field(name=text['you_give'], value=f"{amount_member} {item2.displayname}", inline=False)
        embeda.set_footer(text=main.version[cur_lan])
        msg = await interaction.send(content=member.mention, embed=embeda, view=view)
        await view.wait()
        if view.value is False or view.value is None:
            await msg.edit(content=None, view=None)
            return

        anotha_check2 = await fns.trade_for_items_check(interaction, interaction.user, member, item1, item2, amount_author, amount_member, leng, cur_lan, False, view, None, msg)
        if anotha_check2 is False:
            return

        await item2.add_item(interaction.user, amount_member)
        await item1.remove_item(interaction.user, amount_author)
        await item1.add_item(member, amount_author)
        await item2.remove_item(member, amount_member)

        await msg.edit(content=None, view=None)

        # USER MESSAGE HANDLER

        debug_info = await fns.has_enabled(interaction.user, "dm_notifications")
        if debug_info is True:
            await fns.user_dm_handler_trade_for_items(interaction.user, item1, amount_author, item2, amount_member)

        debug_info2 = await fns.has_enabled(member, "dm_notifications")
        if debug_info2 is True:
            await fns.user_dm_handler_trade_for_items(None, item1, amount_author, item2, amount_member, member)

        embed = nextcord.Embed(title=text['trade'], description=text['successful'], color=main.color_normal)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.send(embed=embed)

    @give_item.on_autocomplete("itemp")
    async def give_item_autocomplete(self, interaction, current: str):
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
                if chk_it.tradeable:
                    i += 1
                    data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.tradeable:
                    if str(current.lower()) in chk_it.disname.lower():
                        i += 1
                        data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))

    @trade_for_coins.on_autocomplete("itemp")
    async def trade_for_coins_autocomplete(self, interaction, current: str):
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
                if chk_it.tradeable:
                    i += 1
                    data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.tradeable:
                    if str(current.lower()) in chk_it.disname.lower():
                        i += 1
                        data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))

    @trade_for_item.on_autocomplete("item_author")
    async def trade_for_item_autocomplete_author(self, interaction, current: str):
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
                if chk_it.tradeable:
                    i += 1
                    data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.tradeable:
                    if str(current.lower()) in chk_it.disname.lower():
                        i += 1
                        data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))

    @trade_for_item.on_autocomplete("item_member")
    async def trade_for_item_autocomplete_second(self, interaction, current: str):
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
                if chk_it.tradeable:
                    i += 1
                    data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for item in language['items']['name']:
                chk_it = fns.get_item(item, "id", leng)
                if chk_it.tradeable:
                    if str(current.lower()) in chk_it.disname.lower():
                        i += 1
                        data.update({chk_it.disname: chk_it.id})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))


def setup(client):
    client.add_cog(TradingCog(client))

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import functions as fns
import complicated_relationship
import random
import buttons
import main
import copy


class Searching(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="search", description="Search various places to get coins and items.", description_localizations={"pl": "Przeszukaj różne miejsca, aby zdobyć monety i przedmioty."})
    async def search(
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
        text = leng['commands']['search']

        if await fns.has_event(user, 'usedsearch') is False:
            await complicated_relationship.init_dialogues(interaction, cur_lan, 'v2_search_tutorial')
            return

        place = await fns.check_location(user, place, "search")
        if place is None or place is False:
            return
        place = fns.get_search_locations(place, cur_lan)

        # This thing should be removed. I'm not sure if I'll use it or not.
        # I'm going to rewrite it just in case.
        # Thankfully this is just normal dialogue.
        if await fns.has_event(user, "metkolpa") is False and place.name == "abandonedhouse":
            if await fns.has_event(user, 'inTheVoid'):
                await complicated_relationship.init_dialogues(interaction, cur_lan, 'rm_house_2')
            else:
                await complicated_relationship.init_dialogues(interaction, cur_lan, 'rm_house_1')
            return

        # wtf man
        if await fns.has_event(user, "nowayimgonnametkerreus") and await fns.has_event(user, 'metguywithweirdname') is False and place.name == "forest":
            kerreus_text = await fns.dialogues('v1_kerreus_meeting', cur_lan)
            embed = nextcord.Embed(
                title=kerreus_text['firsttime']['name'],
                description=kerreus_text['firsttime']['text'],
                color=int(kerreus_text['firsttime']['color'], 16)
            )
            embed.set_thumbnail(kerreus_text['firsttime']['icon'])
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            await fns.update_quest(user, ["chapter1", "wellmet"], 1, cur_lan)
            return
        # logic to change place.loottable
        event_obj = main.event['current_event']
        if event_obj:
            loot = event_obj.location_overrides(place)
        else:
            loot = copy.deepcopy(place.loottable)
            for i in loot:
                if i['item'] == 'event':
                    i.update(i['fallback'])

        somethin = await fns.get_from_value(loot)
        # somethin [item, amount, xp] - how that shit used to be of smt
        # no idea how hunter mode works
        # okay what even is hunter mode

        if somethin["item"] == "nothing":
            embed = nextcord.Embed(title=f"{text['searched']} {place.displayname}", description=text['nothing'], color=place.color)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
        elif somethin["item"] == "coins":
            coins = random.randint(420, somethin["amount"])
            xp = random.randint(somethin['xp'][0], somethin['xp'][1])
            embed = nextcord.Embed(title=f"{text['searched']} {place.displayname}", description=await fns.text_replacer(text['coins'], ['{main.coin}', main.coin], ['{xp}', xp], ['{coins}', coins]), color=place.color)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            await fns.add_xp(user, xp)
            await fns.update_bank(user, coins, "wallet")
            await fns.update_stat(user, 'search', 1)
            await fns.update_quest(user, ["chapter1", "searcher"], 1, cur_lan)
            await fns.update_daily_task(user, "s", "coins", 1)
        elif somethin["item"] == "mer":
            if somethin['amount'] == 6:
                await fns.update_quest(interaction.user, ["chapter1", "shopper"], 1, cur_lan)
                if await fns.has_event(user, "metguywithweirdname"):
                    if await fns.has_event(user, "broken") is False:
                        await fns.add_event(user, "broken")
                    if await fns.has_event(user, "fixed") is False:
                        if await fns.has_event(user, "metkusel") is False:
                            kusel_text = await fns.dialogues('v1_kusel', cur_lan)

                            embed = nextcord.Embed(title=f"{text['searched']} {place.displayname}", description=f"**{kusel_text['firsttime']['name']}**\n{kusel_text['firsttime']['text']}", color=place.color)
                            embed.set_thumbnail(url=kusel_text['firsttime']['icon'])
                            embed.set_footer(text=main.version[cur_lan])
                            await interaction.response.send_message(embed=embed)
                            await fns.add_event(user, 'metkusel')
                            return
                        else:
                            embed = nextcord.Embed(title=f"{text['searched']} {place.displayname}", description=text['fail'], color=place.color)
                            embed.set_footer(text=main.version[cur_lan])
                            await interaction.response.send_message(embed=embed)
                            return
                else:
                    embed = nextcord.Embed(title=f"{text['searched']} {place.displayname}", description=text['fail'], color=place.color)
                    embed.set_footer(text=main.version[cur_lan])
                    await interaction.response.send_message(embed=embed)
                    return

            merchant = fns.get_merchant(somethin['amount'], cur_lan)
            embed = nextcord.Embed(title=f"{text['searched']} {place.displayname}", description=f"**{merchant.displayname}:**\n{random.choice(merchant.question)}", color=place.color)
            embed.set_thumbnail(url=merchant.icon)
            embed.set_footer(text=main.version[cur_lan])

            view = buttons.MerchantQuestion(60, user, place, merchant, place.color, cur_lan, text)
            await interaction.response.send_message(embed=embed, view=view)
        elif somethin["item"] == "str":
            structure = fns.get_strucure(somethin['amount'], cur_lan)

            bbq = [
                'empty',
                structure.chest_treasure,
                structure.chest_normal
            ]

            status = random.randint(1, 5)
            if status > structure.danger:
                embed = nextcord.Embed(title=structure.disname, description=text['chest'], color=place.color)
                embed.set_footer(text=main.version[cur_lan])
                view = buttons.SearchChests(30, bbq, user, structure, place.color)
                await interaction.response.send_message(embed=embed, view=view)
            else:
                res = await complicated_relationship.hunter(["search", somethin['amount'], bbq], interaction, structure, place.color)
                if res is False:
                    embed = nextcord.Embed(title=f"{text['searched']} {place.displayname}", description=text['nothing'], color=place.color)
                    embed.set_footer(text=main.version[cur_lan])
                    await interaction.response.send_message(embed=embed)
        elif somethin["item"] == "enm":
            await complicated_relationship.hunter(["enemy", 1, somethin["amount"]], interaction, place, place.color)
        elif somethin["item"] == "boss":  # This one isn't done.
            # bsr = await fns.bossroom()
            # for sadsd in bsr:
            #     if sadsd["id"] == somethin[1]:
            #         # item_name = await fns.get_from_name(sadsd["token"], "displayname")
            #         item_name = 'foo'
            #         res = await fns.get_amount_items(interaction.user, await fns.get_from_name(sadsd["token"], "id"), str(sadsd["price"]))
            #         if res:
            #             embed = nextcord.Embed(title=sadsd["disname"],
            #                                    description="Posiadasz wystarczająco tokenów.\nCzy chcesz przywołać bossa?",
            #                                    color=place.color)
            #             embed.set_footer(text=main.version)
            #             view = buttons.ConfirmationButtons(60, interaction.user)
            #             await interaction.response.send_message(embed=embed, view=view)
            #             await view.wait()
            #             if view.value is None or view.value is False:
            #                 await interaction.edit_original_message(view=None)
            #                 return
            #             else:
            #                 bbs = await fns.boss()
            #                 pbos = bbs[sadsd["boss"]]
            #                 if pbos["id"] == 0:
            #                     ...
            #         else:
            #             embed = nextcord.Embed(title=sadsd["disname"],
            #                                    description="Brakuje Ci tokenów, aby przywołać bossa. Zdobądź ich więcej i wróć później",
            #                                    color=place.color)
            #             embed.set_footer(text=main.version)
            #             await interaction.response.send_message(embed=embed)
            #             return
            raise NotImplementedError
        else:
            # this thing sucks ass
            if somethin['item'] == 'metalshard':
                if await fns.has_event(user, "broken"):
                    if await fns.has_event(user, "fixed"):
                        somethin['item'] = 'wood'
                        somethin['amount'] = 1
                        somethin['xp'] = [1, 3]
                    else:
                        await fns.update_quest(user, ["chapter1", "shopperdis"], 1, cur_lan)
                else:
                    somethin['item'] = 'wood'
                    somethin['amount'] = 1
                    somethin['xp'] = [1, 3]
            item = fns.get_item(somethin['item'], 'name', cur_lan)
            xp = random.randint(somethin['xp'][0], somethin['xp'][1])
            embed = nextcord.Embed(title=f"{text['searched']} {place.displayname}", description=await fns.text_replacer(text['item'], ['{item}', item.displayname], ['{xp}', xp], ['{amount}', somethin['amount']]), color=place.color)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            await fns.add_xp(user, xp)
            await item.add_item(user, somethin['amount'])
            await fns.update_stat(user, 'search', 1)
            await fns.update_daily_task(user, "s", item.sid, somethin["amount"])

    @search.on_autocomplete("place")
    async def search_autocomplete(self, interaction, current: str):
        search_places = await fns.places()
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        data = {}
        i = 0
        if not current:
            for name in search_places:
                if await fns.check_location(interaction.user, name['name'], 'search'):
                    chk_it = fns.get_search_locations(name['name'], leng)
                    i += 1
                    data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))
        else:
            for name in search_places:
                if await fns.check_location(interaction.user, name['name'], 'search'):
                    chk_it = fns.get_search_locations(name['name'], leng)
                    if str(current.lower()) in chk_it.displayname.lower():
                        i += 1
                        data.update({chk_it.displayname: chk_it.name})
                if i == 24:
                    break
            await interaction.response.send_autocomplete(dict(sorted(data.items())))


def setup(client):
    client.add_cog(Searching(client))

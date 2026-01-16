import nextcord
from nextcord.ext import commands
import main
import buttons
from nextcord import Interaction, SlashOption
import functions as fns
from morex import MorexItem
import morex.logging as logging
from autocompletes import recipe_autocompletes


class Crafting(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cant_craft_item(self, interaction, cur_lan, text, recipe, amount, user_missing_items, edit=False):
        missing_items_text = []
        for missing_item in user_missing_items:
            missing_items_text.append(f"{missing_item['amount']} {missing_item['item']}")
        missing_items_text = "\n".join(missing_items_text)

        embed = nextcord.Embed(description=await fns.text_replacer(text['no_items'], ["{amount}", amount * recipe.amount], ["{item}", recipe.item], ["{text}", missing_items_text]), color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        if edit:
            await interaction.edit_original_message(embed=embed, view=None)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def can_craft_item(self, interaction, text, cur_lan, recipe, amount):
        user_missing_items = await recipe.get_missing_items(interaction.user, amount)
        if user_missing_items:
            await self.cant_craft_item(interaction, cur_lan, text, recipe, amount, user_missing_items)
            return False
        return True

    async def user_has_workbench(self, interaction, cur_lan, text):
        workbench: MorexItem = fns.get_item('i002', 'id', cur_lan)
        has_workbench = await workbench.get_amount(interaction.user, "1")
        if not has_workbench:
            errorembed = nextcord.Embed(description=text['no_workbench'], color=main.color_normal)
            errorembed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            errorembed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=errorembed, ephemeral=True)
            return False
        return True

    async def user_confirmed_crafting(self, interaction, cur_lan, text, recipe, amount):
        items_text = []
        for ingredient in recipe.ingredients:
            items_text.append(f"{ingredient['amount'] * amount} {ingredient['item']}")
        items_text = "\n".join(items_text)
        embea = nextcord.Embed(description=await fns.text_replacer(text['confirmation'], ["{amount}", amount * recipe.amount], ["{item}", recipe.item], ["{text}", items_text]), color=main.color_normal)
        embea.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embea.set_footer(text=main.version[cur_lan])

        confirmationui = buttons.ConfirmationButtons(60, interaction.user)
        await interaction.response.send_message(embed=embea, view=confirmationui)
        await confirmationui.wait()

        if confirmationui.value is None or confirmationui.value is False:
            await interaction.edit_original_message(view=None)
            return False
        return True

    @nextcord.slash_command(name="craft", description="Craft the items.", description_localizations={"pl": "Stwórz przedmioty."}, integration_types=main.integrations, contexts=main.contexts)
    async def craft(
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
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['craft']

        has_workbench = await self.user_has_workbench(interaction, cur_lan, text)
        if not has_workbench:
            return

        item = await fns.get_item_with_handling(itemp, "id", cur_lan, interaction)
        if not item:
            return

        recipe = fns.get_recipe(item.id, "id", cur_lan)
        if not recipe:
            await fns.missing_recipe(interaction, cur_lan)
            return
        if not recipe.available:
            await fns.unavailable_recipe(interaction, cur_lan)
            return

        amount = await fns.validate_amount_input(interaction, cur_lan, amount)
        if not amount:
            return

        if isinstance(amount, str):
            if amount == "all":
                amount = await recipe.get_all(user)

        can_craft = await self.can_craft_item(interaction, text, cur_lan, recipe, amount) 
        if not can_craft:
            return

        confirmed_crafting = await self.user_confirmed_crafting(interaction, cur_lan, text, recipe, amount)
        if not confirmed_crafting:
            return

        cant_craft = await recipe.craft(user, amount)
        if cant_craft:
            await self.cant_craft_item(interaction, cur_lan, text, recipe, amount, cant_craft, True)
            return

        if item.sid == "caveorb":
            await fns.update_quest(interaction.user, ["chapter1", "shopcraft"], 1, cur_lan)

        embed = nextcord.Embed(description=f"{text['crafted']} {amount * recipe.amount} {item.displayname}", color=main.color_normal)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.edit_original_message(embed=embed, view=None)

    @nextcord.slash_command(name="recipe", description="View recipes for certain items.", description_localizations={"pl": "Wyświetl receptury dla konkretnych przedmiotów."}, integration_types=main.integrations, contexts=main.contexts)
    async def recipe(
            self,
            interaction: Interaction,
            itemp: str = SlashOption(
                name="item",
                name_localizations={"pl": "przedmiot"},
                description="Choose the item.",
                description_localizations={"pl": "Wybierz przedmiot."},
                required=True,
            ),
    ):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['recipe']

        item = await fns.get_item_with_handling(itemp, "id", cur_lan, interaction)
        if not item:
            return

        recipe = fns.get_recipe(item.id, "id", cur_lan)
        if not recipe:
            await fns.missing_recipe(interaction, cur_lan)
            return
        if not recipe.available:
            await fns.unavailable_recipe(interaction, cur_lan)
            return

        recipe_text = []
        user_items = await recipe.get_items_amount_from_inv(user)
        for ingredient in recipe.ingredients:
            required_amount = ingredient['amount']
            ingredient_item = ingredient['item']
            user_amount = user_items[ingredient_item.id]

            icon = main.accept if user_amount >= required_amount else main.deny
            recipe_text.append(f"{icon} {user_amount} / {required_amount} {ingredient_item}")
        recipe_text = "\n".join(recipe_text)

        embed = nextcord.Embed(
            title=f"{text['recipe']} {item.disname}",
            description=recipe_text,
            color=main.color_normal
        )
        embed.set_thumbnail(url=item.image)
        embed.add_field(name=text['amount'], value=f"{recipe.amount} {item.displayname}", inline=False)
        has_user_enabled_debug_info = await fns.has_enabled(interaction.user, "debug_info")
        if has_user_enabled_debug_info:
            embed.add_field(name=text['dev'], value=f"**ID**: `{recipe.id}`", inline=False)
        embed.set_footer(text=main.version[cur_lan])
        await interaction.response.send_message(embed=embed)

    @craft.on_autocomplete("itemp")
    async def craft_autocomplete(self, interaction, current: str):
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        data = await recipe_autocompletes.all_recipes(leng, current)
        await interaction.response.send_autocomplete(data)

    @recipe.on_autocomplete("itemp")
    async def recipes_autocomplete(self, interaction, current: str):
        check_usr_acc = await fns.create_account(interaction.user, "youknowwhat")
        if check_usr_acc is False:
            leng = "en"
        else:
            leng = await fns.get_lang(interaction.user)

        data = await recipe_autocompletes.all_recipes(leng, current)
        await interaction.response.send_autocomplete(data)


def setup(client):
    client.add_cog(Crafting(client))

from nextcord.ext import commands


class PlugMan(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def plugin_load(self, ctx, plugin: str):
        try:
            self.client.load_extension(f"cogs.plugins.{plugin}")
            await ctx.send(f"**\"{plugin}\"** has been loaded!")
        except Exception as e:
            await ctx.send(f"It failed spectacularly...\n\n{e}")

    @commands.command()
    @commands.is_owner()
    async def plugin_reload(self, ctx, plugin: str):
        try:
            self.client.reload_extension(f"cogs.plugins.{plugin}")
            await ctx.send(f"**\"{plugin}\"** was reloaded for some reason..")
        except Exception as e:
            await ctx.send(f"It failed spectacularly...\n\n{e}")

    @commands.command()
    @commands.is_owner()
    async def plugin_unload(self, ctx, plugin: str):
        try:
            self.client.unload_extension(f"cogs.plugins.{plugin}")
            await ctx.send(f"**\"{plugin}\"** was unloaded. Yay I hated it.")
        except Exception as e:
            await ctx.send(f"It failed spectacularly...\n\n{e}")


def setup(client):
    client.add_cog(PlugMan(client))

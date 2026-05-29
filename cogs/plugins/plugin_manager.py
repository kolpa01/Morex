from nextcord.ext import commands


class PlugMan(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(PlugMan(client))

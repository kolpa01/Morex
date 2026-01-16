import nextcord
from nextcord.ext import commands
import complicated_relationship
import main
import buttons
from morex import CustomUser
from nextcord import Interaction, SlashOption
import modals
import functions as fns


class CustommobsUI(buttons.Pages):
    def __init__(self, timeout: float, lenght, embedz, user: nextcord.Member, aid, listy, chl, custom_footer, pager, leng, cur_lan) -> None:
        super().__init__(timeout, lenght, embedz, user, custom_footer, pager, leng)
        if lenght <= 1:
            for i, v in enumerate(self.children):
                v.disabled = True
                if i == 4:
                    break
        # self.lenght = int(lenght)
        # self.embedz = embedz
        # self.current = 0
        # self.user = user
        self.author_id = aid
        self.key = listy
        self.channel = chl
        self.leng = leng
        self.cur_lan = cur_lan

    @nextcord.ui.button(emoji='<:MX_Sword:1220425813132836904>', style=nextcord.ButtonStyle.gray, row=2)
    async def fajt(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        mob_id = self.key[self.current]

        cts = await fns.custommobs()
        user_id = cts[self.author_id]['id']
        await complicated_relationship.hunter(["custom", 1], interaction, (user_id, mob_id), main.color_normal)

        # sadly I won't be able to rewrite this Easter egg until it'll be more significant
        # if self.author_id == "826792866776219709" and mob_id == "c001":
        #     i = await fns.playerinfo()
        #
        #     errorembed = nextcord.Embed(description="Nie posiadasz broni.\nSpróbuj ją kupić lub wyposażyć.", color=main.color_normal)
        #     errorembed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.display_avatar)
        #     errorembed.set_footer(text=main.version)
        #     curweap = await fns.get_weapon(interaction.user)
        #     if curweap is False:
        #         await interaction.response.send_message(embed=errorembed, ephemeral=True)
        #         return
        #     cis = await fns.custommobs()
        #     for ajd in cis[str(self.author_id)]["mobs"]:
        #         if ajd["id"] == "c001":
        #             oponent = ajd['name']
        #             opponent = cis[str(self.author_id)]["mobs"]
        #             break
        #     else:
        #         return
        #
        #     for slum in opponent:
        #         if oponent == slum["name"]:
        #             ogm = slum
        #             disname = slum["displayname"]
        #             ejczpi = slum["hp"]
        #             image = slum["image"]
        #             hape = i[str(interaction.user.id)]["hp"]
        #             weapon = curweap
        #             break
        #     else:
        #         return
        #
        #     ico = await fns.player_icon(interaction.user)
        #     pbar = await fns.progress_bar(ejczpi, ejczpi)
        #     ebar = await fns.progress_bar(hape, hape)
        #     embed = nextcord.Embed(title=f"Walka", color=main.color_normal)
        #     embed.add_field(name=f"{ico} {interaction.user.name}", value=f"{pbar}\n{hape}/{hape} HP\n0 SH", inline=False)
        #     embed.add_field(name=f"{disname}", value=f"{ebar}\n{ejczpi}/{ejczpi} HP\n0 SH", inline=False)
        #     embed.add_field(name="Informacje", value="Trochę zmieniłam zasady. Teraz zamienimy się miejscami. Będę miała te same umiejętności co ty, a ty będziesz miał moje.", inline=False)
        #     embed.set_thumbnail(url=image)
        #     embed.set_footer(text=main.version)
        #
        #     view = buttons.reverseHuntButtons(360, ejczpi, hape, ejczpi, hape, image, weapon, 0, 3, True, ico, ogm, interaction.user)
        #     await interaction.response.edit_message(embed=embed, view=view)
        #
        # else:
            
    @nextcord.ui.button(emoji='<:MX_Pencil:1269702293591294063>', style=nextcord.ButtonStyle.gray, row=2)
    async def edit_mob(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if str(interaction.user.id) != self.author_id:
            return
        cis = await fns.custommobs()
        mob_id = self.key[self.current]

        mob = fns.get_morex_oponent((cis[str(self.author_id)]['id'], mob_id), "list", self.cur_lan)
        if not mob:
            return
        oponent = mob.sid
        disname = mob.disname
        emoji = mob.emoji
        image = mob.image
        hp = mob.hp
        atk = mob.attack
        if mob.has_default_meetup:
            meetup = ""
        else:
            meetup = mob.meetup
        
        await interaction.response.send_modal(modals.CustommobsEditModal(interaction.user, self.author_id, self.channel, oponent, disname, ','.join(str(v) for v in atk), str(hp), mob_id, emoji, image, self.cur_lan, self.leng, meetup))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("Bruh", ephemeral=True)
                return False
            return True


class Custommobs(commands.Cog):
    def __init__(self, client):
        self.client = client     

    @nextcord.slash_command(name="custommobs", integration_types=main.integrations, contexts=main.contexts)
    async def custommobs(self, interaction: Interaction):
        pass
    
    @custommobs.subcommand(name="create", description="Create your own custom mob.", description_localizations={"pl": "Stwórz swojego Własnego wroga."})
    async def custommobs_create(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)
        text = leng['commands']['custommobs_create']

        channel = await self.client.fetch_channel(1259559255787442228)
        
        cts = await fns.custommobs()
        lin = len(cts[str(user.id)]["mobs"])
        klas = main.custom_mobs_limits[cts[str(user.id)]["rank"]]
        
        if klas <= lin:
            embed = nextcord.Embed(description=f"{text['limit']} ({klas})", color=main.color_normal)
            embed.set_author(name=user.name, icon_url=str(user.display_avatar))
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.send_modal(modals.CustommobsCreationModal(user=user, channel=channel, cur_lan=cur_lan, leng=leng))
        
    @custommobs.subcommand(name="view", description="Show user's Custom mobs", description_localizations={"pl": "Wyświetl Własnych wrogów użytkownika."})
    async def viewermob(
            self,
            interaction: Interaction,
            member: nextcord.Member = SlashOption(
                name="member",
                name_localizations={"pl": "osoba"},
                description="Select a member.",
                description_localizations={"pl": "Wybierz osobę."},
                required=False
            )
    ):
        if member is None:
            user = await fns.firsttime(interaction.user)
            cur_lan = await fns.get_lang(user)
        else:
            cur_lan = await fns.get_lang(interaction.user)
            if member.id == 870358872769056859:
                interaction.user = await fns.firsttime(interaction.user)
                user = CustomUser(1, "Debug Account 1", "https://cdn.discordapp.com/attachments/1134067893840126012/1134067977839456276/Untitled_03-08-2023_10-39-45_11.png", False)
            else:
                aa = await fns.firsttime(interaction.user, member)

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
        text = leng['commands']['custommobs_view']
            
        cts = await fns.custommobs()
        
        if len(cts[str(user.id)]["mobs"]) == 0:
            embed = nextcord.Embed(title=f"{text['enemies']} {user.name}", description=text['no_enemies'], color=main.color_normal)
            embed.set_footer(text=main.version[cur_lan])
            await interaction.response.send_message(embed=embed)
            return
        else:
            embedz = []
            lenington = len(cts[str(user.id)]["mobs"])
            keys = []

            for i in cts[str(user.id)]["mobs"]:
                mob = fns.get_morex_oponent((cts[str(user.id)]['id'], i['id']), "list", cur_lan)
                embed = nextcord.Embed(title=mob.disname, description=f"```{mob.meetup}```\n**{text['name']}:** {mob.displayname}\n**{text['hp']}:** {mob.hp}\n**{text['attack']}:** {mob.attack[0]}/{mob.attack[1]}/{mob.attack[2]}\n**{text['author']}:** {user.name}", color=main.color_normal)
                embed.set_thumbnail(url=mob.image)
                reas = await fns.has_enabled(interaction.user, "debug_info")
                if reas is True:
                    embed.add_field(name=text['dev'], value=f"**ID**: `{mob.id}`\n**SID**: `{mob.sid}`", inline=False)
                keys.append(mob.id)
                embedz.append(embed)

            mbd = embedz[0]
            mbd.set_footer(text=f"{leng['other']['pages']['page']} 1/{lenington} | {main.version[cur_lan]}")
            chfg = self.client.get_channel(1269703558605967361)
            view = CustommobsUI(180, lenington, embedz, interaction.user, str(user.id), keys, chfg, main.version[cur_lan], leng['other']['pages']['page'], leng, cur_lan)
            if interaction.user.id != user.id:
                view.children.pop()
            await interaction.response.send_message(embed=mbd, view=view)
                

def setup(client):
    client.add_cog(Custommobs(client))

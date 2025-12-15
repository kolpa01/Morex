import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import dropdown
import functions as fns
import main
from morex import MorexQuest, MorexTask


class Quests(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    async def get_main_quests_embeds(user: nextcord.Member, cur_lan: str, leng: dict) -> list[nextcord.Embed]:
        text: dict = leng['commands']['quests']

        user_quests: dict = await fns.quests()
        embeds: list[nextcord.Embed] = []

        for quest in user_quests[str(user.id)]["mainquestline"]:
            current_quest: MorexQuest = fns.get_quest(quest['chapter'], quest['name'], cur_lan)
            rewards: str = await fns.list_rewards(current_quest.rewards, cur_lan)
            precent: int = int((quest["current"] / current_quest.etaps) * 100)
            bar: str = await fns.progress_bar(quest["current"], current_quest.etaps)

            embed: nextcord.Embed = nextcord.Embed(title=text['quests'], description=f"### {current_quest.chapter_title}", color=main.color_normal)
            embed.add_field(name=f"**{current_quest.disname} {current_quest.stage}**", value=f"{current_quest.description}\n{bar} {precent}% ({quest['current']}/{current_quest.etaps})", inline=False)
            embed.add_field(name=text['rewards'], value=rewards)

            embeds.append(embed)

        if len(embeds) == 0:
            embeds: list[nextcord.Embed] = [nextcord.Embed(title=text['quests'], description=text['no_quests'], color=main.color_normal)]

        return embeds

    @staticmethod
    async def get_daily_tasks_embeds(user, cur_lan, leng) -> list[nextcord.Embed]:
        text: dict = leng['commands']['quests']
        daily_tasks: dict = await fns.get_daily_tasks()

        daily_embed: nextcord.Embed = nextcord.Embed(title=text['daily'], color=main.color_normal)
        for user_task in daily_tasks[str(user.id)]["quests"]:
            task: MorexTask = fns.get_task(user_task, cur_lan)

            if task.type == "event":
                task_name: str = f"{main.accept if daily_tasks[str(user.id)]['quests'][user_task]['completed'] is True else main.deny} {task.displayname} :blue_heart:"
            else:
                task_name: str = f"{main.accept if daily_tasks[str(user.id)]['quests'][user_task]['completed'] is True else main.deny} {task.displayname}"

            bars: list[str] = []
            for requirement in task.quest:
                value_achieved_by_user: int = daily_tasks[str(user.id)]["quests"][user_task]['progress'][requirement]
                value_required: int = task.quest[requirement]
                bars.append(f'{await fns.progress_bar(value_achieved_by_user, value_required)} {int(value_achieved_by_user/value_required * 100)}% ({value_achieved_by_user}/{value_required})')

            rewards: str = await fns.list_rewards(task.rewards, cur_lan)
            daily_embed.add_field(name=task_name, value=f"{task.description}\n{'\n'.join(bars)}\n**{text['rewards']}:**\n{rewards}", inline=False)
        return [daily_embed]

    @staticmethod
    async def get_merchant_tasks_embeds(user, cur_lan, leng) -> list[nextcord.Embed]:
        text: dict = leng['commands']['quests']
        merchant_tasks = await fns.get_merchant_tasks()
        merbeds = []
        for merchant in merchant_tasks[str(user.id)]:
            for task in merchant_tasks[str(user.id)][merchant]['pr']['ongoing']:
                mer_task = fns.get_merchant_task(task, merchant, 'permanent', cur_lan)
                bars = []
                for v in mer_task.quest:
                    u_v = merchant_tasks[str(user.id)][merchant]['pr']['ongoing'][task]['progress'][v]
                    m_v = mer_task.quest[v]
                    bars.append(f'{await fns.progress_bar(u_v, m_v)} {int(u_v/m_v * 100)}% ({u_v}/{m_v})')

                rewarding = await fns.list_rewards(mer_task.rewards, cur_lan)

                merchant_body = fns.get_merchant(int(merchant), cur_lan)
                embed = nextcord.Embed(title=merchant_body.displayname, description=f"### {mer_task.disname}\n{mer_task.description}\n{'\n'.join(bars)}", color=main.color_normal)
                embed.add_field(name=f"**{text['rewards']}:**", value=f"{rewarding}")
                embed.set_thumbnail(url=merchant_body.icon)

                merbeds.append(embed)

            for task in merchant_tasks[str(user.id)][merchant]['rd']:
                mer_task = fns.get_merchant_task(task, merchant, 'random', cur_lan)
                bars = []
                for v in mer_task.quest:
                    u_v = merchant_tasks[str(user.id)][merchant]['rd'][task]['progress'][v]
                    m_v = mer_task.quest[v]
                    bars.append(f'{await fns.progress_bar(u_v, m_v)} {int(u_v/m_v * 100)}% ({u_v}/{m_v})')

                rewarding = await fns.list_rewards(mer_task.rewards, cur_lan)

                merchant_body = fns.get_merchant(int(merchant), cur_lan)
                embed = nextcord.Embed(title=merchant_body.displayname, description=f"### {mer_task.disname}\n{mer_task.description}\n{'\n'.join(bars)}", color=main.color_normal)
                embed.add_field(name=f"**{text['rewards']}:**", value=f"{rewarding}")
                embed.set_thumbnail(url=merchant_body.icon)

                merbeds.append(embed)

        if len(merbeds) == 0:
            merbeds: list[nextcord.Embed] = [nextcord.Embed(title=text['quests'], description=text['no_quests'], color=main.color_normal)]

        return merbeds

    @staticmethod
    async def get_event_quests_embeds(user, cur_lan, leng) -> list[nextcord.Embed]:
        text: dict = leng['commands']['quests']
        return [nextcord.Embed(title=text['quests'], description=text['no_quests'], color=main.color_normal)]

    @nextcord.slash_command(name="quests", description="Show your current quests.", description_localizations={"pl": "Wyświetl swoje obecne zadania."})
    async def quests(self, interaction: Interaction):
        user = await fns.firsttime(interaction.user)
        cur_lan = await fns.get_lang(interaction.user)
        leng = await fns.lang(cur_lan)

        main_quests_embeds: list[nextcord.Embed] = await self.get_main_quests_embeds(user, cur_lan, leng)
        daily_tasks_embeds: list[nextcord.Embed] = await self.get_daily_tasks_embeds(user, cur_lan, leng)
        merchant_tasks_embeds: list[nextcord.Embed] = await self.get_merchant_tasks_embeds(user, cur_lan, leng)
        event_quests_embeds: list[nextcord.Embed] = await self.get_event_quests_embeds(user, cur_lan, leng)

        displayed_embed: nextcord.Embed = main_quests_embeds[0]
        displayed_embed.set_footer(text=f"{leng['other']['pages']['page']} 1/{len(main_quests_embeds)} | {main.version[cur_lan]}")

        view = dropdown.QuestsMenu(180, len(main_quests_embeds), [main_quests_embeds, daily_tasks_embeds, event_quests_embeds, merchant_tasks_embeds], user, main.version[cur_lan], leng['other']['pages']['page'], leng, cur_lan)
        await interaction.response.send_message(embed=main_quests_embeds[0], view=view)


def setup(client):
    client.add_cog(Quests(client))

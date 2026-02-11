import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import morex.logging as logging
import checks
import asyncio

contexts = [nextcord.InteractionContextType.guild, nextcord.InteractionContextType.bot_dm]
integrations = [nextcord.IntegrationType.guild_install]

event = {}
mode = "mx"  # dev or mx
version_number = "2.4.0"
beta_version = "none"
version = {
    "pl": "Wersja 2.4.0 | Rolnictwo",
    "en": "Version 2.4.0 | Farming"
}

color_normal = 0xCE4DD5

coin = "<:MX_Coin:1146519037669548172>"
accept = "<:MX_Accept:1178757551060418600>"
deny = "<:MX_Cancel:1217191335048515634>"
one = "<:MX_One:1217191332993568910>"
two = "<:MX_Two:1217191324688711720>"
three = "<:MX_Three:1217191331529752576>"
four = "<:MX_Four:1217191326345596991>"
five = "<:MX_Five:1217191329981927627>"
six = "<:MX_Six:1217191328522440744>"
seven = "<:MX_Seven:1259099946590666842>"
eight = "<:MX_Eight:1259099948582965261>"
nine = "<:MX_Nine:1259099950252556318>"
left = "<:MX_ArrowLeft:1259099941297590283>"
right = "<:MX_ArrowRIght:1259099944938115123>"
farleft = "<:MX_EndLeft:1259099935815630951>"
farright = "<:MX_EndRight:1259099937225048107>"
magnifier = "<:MX_MagnifyingGlass:1259099943054872648>"
skillpoint = "<:MX_SkillPoint:1307462021188550686>"
empty = "<:MX_Empty:1306308101389029478>"

debug_account = False

custom_mobs_limits = {
    "d": 3,
    "c": 5,
    "b": 10,
    "a": 20,
    "s": 50,
    "ss": 1000
}

userdb = ["announcements", "battlesfrozenintime", "custommobs", "dailytasks", "farmlands", "inventories", "merchanttasks", "otherdatabase", "playerdata", "quests", "randomevent", "settings", "skills", "stats"]

if __name__ == "__main__":
    os.chdir("./")

    intents = nextcord.Intents.all()

    client = commands.Bot(command_prefix="m!", intents=intents)
    client.remove_command("help")

    logging.label("--------->     COG LOADER     <---------")
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            try:
                client.load_extension(f"cogs.{file[:-3]}")
                logging.success(f"Loaded {file}")
            except Exception as e:
                logging.critical(f"Failed to load {file}")
                logging.error(f"{e}")

    for file in os.listdir("./cogs/owner_tools/"):
        if file.endswith(".py"):
            try:
                client.load_extension(f"cogs.owner_tools.{file[:-3]}")
                logging.success(f"Loaded {file}")
            except Exception as e:
                logging.critical(f"Failed to load {file}")
                logging.error(f"{e}")

    logging.label("--------->  JSON FILES CHECK  <---------")
    have_any_files_loaded = False
    for file in userdb:
        if f"{file}.json" not in os.listdir("./userdb"):
            logging.warn(f"The {file}.json is missing.")
        else:
            have_any_files_loaded = True
            logging.success(f"The {file}.json exists.")

    if not have_any_files_loaded:
        logging.critical("All of the JSON files are missing. Aborting...")
        exit(1)
    if mode == "dev":
        asyncio.run(checks.check_item_names())
        asyncio.run(checks.check_item_descriptions())
    logging.label("--------->    MOREX OUTPUT    <---------")

    load_dotenv()
    
    if mode == "mx":
        client.run(os.environ["TOKEN_MOREX"])
    else:
        client.run(os.environ["TOKEN_TEST"])

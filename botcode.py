import discord
import asyncio
import os 
from discord import app_commands
from discord.ext import commands

# Initialize bot
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

# Define global variables to store stock and prices
stock_data = {
    "jailbreak": {},
    "pet simulator 99": {},
    "blox fruits": {}
}
price_data = {
    "jailbreak": {},
    "pet simulator 99": {},
    "blox fruits": {}
}

# Define a mapping for custom emojis
custom_emoji_mapping = {
    "torpedo": "<:torpedo:123456789012345678>",
    "arachnid": "<:arachnid:123456789012345678>",
    # Add the rest of your custom emojis here...
    "1b gems": "<:1bgems:123456789012345678>",
    "perm rocket": "<:rocket:1254652033991184444>",
    "perm spin": "<:spin:1254652474363478056>",
    "perm chop": "<:chop:1254652318574575658>",
    "perm spring": "<:spring:1254652155743178782>",
    "perm bomb": "<:bomb:1254652563748421744>",
    "perm smoke": "<:smoke:1254652851292999711>",
    "perm spike": "<:spike:1254652806670061582>",
    "perm flame": "<:flame:1254653167149514814>",
    "perm falcon": "<:falcon:1254653167149514814>",
    "perm ice": "<:ice:1254653295822241813>",
    "perm sand": "<:sand:1254653464156573706>",
    "perm dark": "<:dark:1254653552802926653>",
    "perm diamond": "<:diamond:1254653683325734912>",
    "perm light": "<:light:1254653804876664852>",
    "perm rubber": "<:rubber:1254653878260203571>",
    "perm barrier": "<:barrier:1254654005561266187>",
    "perm ghost": "<:ghost:1254654137874907191>",
    "perm magma": "<:magma:1254654396734767234>",
    "perm quake": "<:quake:1254654396734767234>",
    "perm buddha": "<:buddha:1254654539953340450>",
    "perm love": "<:love:1254654749224079451>",
    "perm spider": "<:spider:1254654887766003783>",
    "perm sound": "<:sound:1254654982611800185>",
    "perm phoenix": "<:phoenix:1254655082826432593>",
    "perm portal": "<:portal:1254655162832912497>",
    "perm rumble": "<:rumble:1254655333788287138>",
    "perm pain": "<:pain:1254655504614035558>",
    "perm blizzard": "<:blizzard:1254655655432683540>",
    "perm gravity": "<:gravity:1254657608351219743>",
    "perm mammoth": "<:mammoth:1254657758750576661>",
    "perm t-rex": "<:trex:1254658130655186956>",
    "perm dough": "<:dough:1254658240801935481>",
    "perm shadow": "<:shadow:1254658326134788128>",
    "perm venom": "<:venom:1254658416526233620>",
    "perm control": "<:control:1254659168044978177>",
    "perm spirit": "<:spirit:1254659269396140087>",
    "perm dragon": "<:dragon:1254659389500166244>",
    "perm leopard": "<:leopard:1254659480025825313>",
    "perm kitsune": "<a:kitsune:1254659587722711121>",
    "perm": "<:perm:1254662621215326238>"
}

# Helper function to format stock info
def format_stock_info(game):
    info = ""
    for item, quantity in stock_data[game].items():
        emoji = custom_emoji_mapping.get(item.lower(), "📦")  # Default to a box emoji if not found
        info += f"{emoji} - {item} - {quantity}x stock\n"
    return info or "No stock available."

# Helper function to format price info
def format_price_info(game):
    info = ""
    for item, price in price_data[game].items():
        emoji = custom_emoji_mapping.get(item.lower(), "💰")  # Default to a money bag emoji if not found
        if price:
            robux, money = price
            info += f"{emoji} - {item} - {robux} Robux | {money}$\n"
        else:
            info += f"{emoji} - {item} - Contact the Seller for price\n"
    return info or "No prices available."
# Event when the bot is ready
@bot.event
async def on_ready():
    print(f"Bot status - ONLINE\nLogged in as {bot.user.name}#{bot.user.discriminator}")

    # Set rich presence activity
    activity = discord.Activity(
        name="Managing Game Stocks",
        type=discord.ActivityType.playing,
        details="Checking stock and prices",
        state="Managing items"
    )
    await bot.change_presence(activity=activity)

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

# Slash command for /ping
@bot.tree.command(name="ping", description="shows pong")
async def help(interaction: discord.Interaction):
    op_text = """Pong"""
    await interaction.response.send_message(op_text)
    await asyncio.sleep(2)

    ko_text = "PongAgain"
    await interaction.edit_original_response(content=ko_text)
# Slash command for /help
@bot.tree.command(name="help", description="Displays available commands")
async def help(interaction: discord.Interaction):
    help_text = """**Commands**
    /stock {game}
    /price {game} {item}
    """
    await interaction.response.send_message(help_text)

# Split items into chunks of 25
def split_choices(choices, chunk_size=25):
    return [choices[i:i + chunk_size] for i in range(0, len(choices), chunk_size)]

# List of all items
jailbreak_items = ["torpedo", "arachnid", "jb8", "raptor", "beam hybrid", "crew capsule", "volt 4x4", "rattler", "banana car", "beignet", "icebreaker", "celsior", "jackrabbit", "macaron", "tiny toy", "bloxy", "goliath", "bandit", "proto-08", "shogun", "poseidon", "power-1", "longhorn", "frost crawler", "striker", "og monster truck", "brulee", "steed", "mighty", "megalodon", "suv", "posh", "classic", "airtail", "m12 molten", "agent", "torero", "nascar", "nascar free", "mcl36", "snake", "javelin", "parisian", "nascar 75", "aperture", "carbonara"]
bloxfruits_items = ["rocket", "spin", "chop", "spring", "bomb", "smoke", "spike", "flame", "falcon", "ice", "sand", "dark", "diamond", "light", "rubber", "barrier", "ghost", "magma", "quake", "buddha", "love", "spider", "sound", "phoenix", "portal", "rumble", "pain", "blizzard", "gravity", "mammoth", "t-rex", "dough", "shadow", "venom", "control", "spirit", "dragon", "leopard", "kitsune"]
bloxfruits_items_perm = [f"perm {item}" for item in bloxfruits_items]

# Chunked choices
jailbreak_chunks = split_choices(jailbreak_items)
bloxfruits_chunks = split_choices(bloxfruits_items_perm)

# Slash command for /stock
@bot.tree.command(name="stock", description="Displays the stock for a game")
@app_commands.describe(game="The game to check stock for")
@app_commands.choices(game=[
    app_commands.Choice(name="jailbreak", value="jailbreak"),
    app_commands.Choice(name="pet simulator 99", value="pet simulator 99"),
    app_commands.Choice(name="blox fruits", value="blox fruits")
])
async def stock(interaction: discord.Interaction, game: str):
    stock_info = format_stock_info(game)
    await interaction.response.send_message(f"**Stock for {game}**\n{stock_info}")

# Slash command for /price with chunked choices
for i, chunk in enumerate(jailbreak_chunks):
    @bot.tree.command(name=f"price_jailbreak_{i}", description="Displays the price for an item in Jailbreak")
    @app_commands.describe(item="The item to check price for")
    @app_commands.choices(item=[app_commands.Choice(name=item, value=item) for item in chunk])
    async def price(interaction: discord.Interaction, item: str):
        game = "jailbreak"
        emoji = custom_emoji_mapping.get(item, "💰")
        if item in price_data[game]:
            robux, money = price_data[game][item]
            if robux is not None and money is not None:
                await interaction.response.send_message(f"**Price for {item} in {game}**\n{emoji} - {item} - {robux} Robux | {money}$")
            else:
                await interaction.response.send_message(f"**Price for {item} in {game}**\n{emoji} - {item} - Contact the Seller for price")
        else:
            await interaction.response.send_message(f"No price available for {item} in {game}")

for i, chunk in enumerate(bloxfruits_chunks):
    @bot.tree.command(name=f"price_bloxfruits_{i}", description="Displays the price for an item in Blox Fruits")
    @app_commands.describe(item="The item to check price for")
    @app_commands.choices(item=[app_commands.Choice(name=item, value=item) for item in chunk])
    async def price(interaction: discord.Interaction, item: str):
        game = "blox fruits"
        emoji = custom_emoji_mapping.get(item, "💰")
        if item in price_data[game]:
            robux, money = price_data[game][item]
            if robux is not None and money is not None:
                await interaction.response.send_message(f"**Price for {item} in {game}**\n{emoji} - {item} - {robux} Robux | {money}$")
            else:
                await interaction.response.send_message(f"**Price for {item} in {game}**\n{emoji} - {item} - Contact the Seller for price")
        else:
            await interaction.response.send_message(f"No price available for {item} in {game}")

@bot.tree.command(name="price_pet_simulator_99", description="Displays the price for an item in Pet Simulator 99")
@app_commands.describe(item="The item to check price for")
@app_commands.choices(item=[app_commands.Choice(name="1b gems", value="1b gems")])
async def price(interaction: discord.Interaction, item: str):
    game = "pet simulator 99"
    emoji = custom_emoji_mapping.get(item, "💰")
    if item in price_data[game]:
        robux, money = price_data[game][item]
        if robux is not None and money is not None:
            await interaction.response.send_message(f"**Price for {item} in {game}**\n{emoji} - {item} - {robux} Robux | {money}$")
        else:
            await interaction.response.send_message(f"**Price for {item} in {game}**\n{emoji} - {item} - Contact the Seller for price")
    else:
        await interaction.response.send_message(f"No price available for {item} in {game}")

# Slash command for /stockupdate
for i, chunk in enumerate(jailbreak_chunks):
    @bot.tree.command(name=f"stockupdate_jailbreak_{i}", description="Update stock for an item in Jailbreak (Admin only)")
    @app_commands.describe(item="The item to update stock for", quantity="The quantity to update")
    @app_commands.choices(item=[app_commands.Choice(name=item.lower(), value=item.lower()) for item in chunk])
    @commands.has_permissions(administrator=True)
    async def stockupdate(interaction: discord.Interaction, item: str, quantity: int):
        game = "jailbreak"
        stock_data[game][item] = quantity
        await interaction.response.send_message(f"Updated stock for {item} in {game} to {quantity}x")

for i, chunk in enumerate(bloxfruits_chunks):
    @bot.tree.command(name=f"stockupdate_bloxfruits_{i}", description="Update stock for an item in Blox Fruits (Admin only)")
    @app_commands.describe(item="The item to update stock for", quantity="The quantity to update")
    @app_commands.choices(item=[app_commands.Choice(name=item, value=item) for item in chunk])
    @commands.has_permissions(administrator=True)
    async def stockupdate(interaction: discord.Interaction, item: str, quantity: int):
        game = "blox fruits"
        stock_data[game][item] = quantity
        await interaction.response.send_message(f"Updated stock for {item} in {game} to {quantity}x")

@bot.tree.command(name="stockupdate_pet_simulator_99", description="Update stock for an item in Pet Simulator 99 (Admin only)")
@app_commands.describe(item="The item to update stock for", quantity="The quantity to update")
@app_commands.choices(item=[app_commands.Choice(name="1b gems", value="1b gems")])
@commands.has_permissions(administrator=True)
async def stockupdate(interaction: discord.Interaction, item: str, quantity: int):
    game = "pet simulator 99"
    stock_data[game][item] = quantity
    await interaction.response.send_message(f"Updated stock for {item} in {game} to {quantity}x")

# Slash command for /updateprice
for i, chunk in enumerate(jailbreak_chunks):
    @bot.tree.command(name=f"updateprice_jailbreak_{i}", description="Update price for an item in Jailbreak (Admin only)")
    @app_commands.describe(item="The item to update price for", robux="The Robux price", money="The money price")
    @app_commands.choices(item=[app_commands.Choice(name=item.lower(), value=item.lower()) for item in chunk])
    @commands.has_permissions(administrator=True)
    async def updateprice(interaction: discord.Interaction, item: str, robux: int, money: float):
        game = "jailbreak"
        price_data[game][item] = (robux, money)
        await interaction.response.send_message(f"Updated price for {item} in {game} to {robux} Robux | {money}$")

for i, chunk in enumerate(bloxfruits_chunks):
    @bot.tree.command(name=f"updateprice_bloxfruits_{i}", description="Update price for an item in Blox Fruits (Admin only)")
    @app_commands.describe(item="The item to update price for", robux="The Robux price", money="The money price")
    @app_commands.choices(item=[app_commands.Choice(name=item, value=item) for item in chunk])
    @commands.has_permissions(administrator=True)
    async def updateprice(interaction: discord.Interaction, item: str, robux: int, money: float):
        game = "blox fruits"
        price_data[game][item] = (robux, money)
        await interaction.response.send_message(f"Updated price for {item} in {game} to {robux} Robux | {money}$")

@bot.tree.command(name="updateprice_pet_simulator_99", description="Update price for an item in Pet Simulator 99 (Admin only)")
@app_commands.describe(item="The item to update price for", robux="The Robux price", money="The money price")
@app_commands.choices(item=[app_commands.Choice(name="1b gems", value="1b gems")])
@commands.has_permissions(administrator=True)
async def updateprice(interaction: discord.Interaction, item: str, robux: int, money: float):
    game = "pet simulator 99"
    price_data[game][item] = (robux, money)
    await interaction.response.send_message(f"Updated price for {item} in {game} to {robux} Robux | {money}$")

# Run the bot with your token
bot.run(os.getenv("Token"))

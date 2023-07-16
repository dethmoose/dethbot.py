import discord
from discord import app_commands
import db
from dotenv import dotenv_values


description = "Dethbot, simple bot."
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

env = dotenv_values(".env")
DISCORD_BOT_SECRET = env.get("DISCORD_BOT_SECRET")

MY_GUILD = discord.Object(id=312691409096540180)
guilds = [
    MY_GUILD,
    discord.Object(id=983145793781366834)
]

@client.event
async def on_ready():
    print("Starting Bot...")
    await tree.sync(guild=discord.Object(id=983145793781366834))
    await tree.sync(guild=MY_GUILD)
    print("Ready!")

@tree.command(name="test_command", description="This is a test slash command", guilds=guilds)
async def test_command(interaction, arg: str ):
    print(arg)
    await interaction.response.send_message("Hello!")

@tree.command(name="blacklist", guilds=guilds)
@app_commands.choices(action=[
    app_commands.Choice(name="list", value="list"),
    app_commands.Choice(name="add", value="add"),
    app_commands.Choice(name="remove", value="remove")
])
# @app_commands.describe(action="list, add, or remove")
@app_commands.describe(name="Name of item to add/remove or user to list.")
async def blacklist(interaction: discord.Interaction, action: app_commands.Choice[str], name: str=None):
    user = interaction.user.name
    if action.value == "list":
        if name:
            items = db.get_items(name)
        else:
            items = db.get_items(user)

        list_string = "%s items:\n" % user
        for item in items:
            list_string += "* %s \n" % item

        await interaction.response.send_message(list_string)
        return
    elif action.value == "add" and name:
        db.add_item(user, name)
    elif action.value == "remove" and name:
        db.delete_item(user, name)
    else:
        await interaction.response.send_message("Nothing happened")
        return
    await interaction.response.send_message("Success")

@tree.command(name="poll", guilds=guilds)
@app_commands.describe(csv="Answers to the question in a comma separated string.")
async def poll(interaction: discord.Interaction, question: str, csv: str):
    numbers = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
    }
    answers = [n.strip() for n in csv.split(",")]
    answers_string = ""
    for i, answer in enumerate(answers, start=1):
        answers_string += f"""{numbers[i]} {answer}
        """
    embed = discord.Embed(title="Poll")
    embed.add_field(name=question, value=answers_string)
    await interaction.response.send_message(embed=embed)

    message_react: discord.Message
    async for message in interaction.channel.history():
        if not message.embeds:
            continue
        if message.embeds[0].title == embed.title:
            message_react = message
            break

    for i, _ in enumerate(answers, start=1):
        await message_react.add_reaction(numbers[i])

client.run(DISCORD_BOT_SECRET)

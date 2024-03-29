import discord
import os
from discord import app_commands, Intents, Client
from dotenv import load_dotenv

load_dotenv()
TOKEN: str = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready() -> None:
    print("Bot is Up and Ready!")
    try:
        synced = await tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

@tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hey {interaction.user.mention}!', ephemeral=True)

@tree.command(name="say")
@app_commands.describe(arg = "What should I say?")
async def say(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f'{interaction.user.name} said `{arg}`')

# MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
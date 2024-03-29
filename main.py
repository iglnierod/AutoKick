import discord
import os
from discord import app_commands, Intents, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

# LOAD DISCORD_TOKEN FROM ENV
load_dotenv()
TOKEN: str = os.getenv('DISCORD_TOKEN')

# CLIENT SET UP
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

# SLASH COMMANDS
@tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    log(interaction, "Hello")
    await interaction.response.send_message(f'Hey {interaction.user.mention}!', ephemeral=True)

@tree.command(name="say")
@app_commands.describe(message = "What should I say?")
async def say(interaction: discord.Interaction, message: str):
    log(interaction, f'Say({message})')
    await interaction.response.send_message(f'{interaction.user.name} said `{message}`')

@tree.command(name = "ping", description = "Test application")
async def ping(interaction: discord.Interaction):
    log(interaction, "Ping")
    await interaction.response.send_message("pong! 🏓")

@tree.command(name = "vckick", description="Auto kick from active voice chat")
async def vckick(interaction: discord.Interaction):
    log(interaction, "VcKick")
    await interaction.user.move_to(None)
    await interaction.response.send_message(f"Se te ha expulsado del canal de voz",ephemeral=True)


# LOG PRINTS
def log(interaction: discord.Interaction, command_name: str):
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f'({current_time}) [{interaction.guild}/{interaction.channel}] - {interaction.user.name}: {command_name}')

# MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
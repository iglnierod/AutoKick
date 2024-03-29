import discord
import os
import threading
import time
from discord import app_commands, Intents, Client, AppCommandOptionType
from datetime import datetime, timedelta
from keep_alive import keep_alive

TOKEN: str = os.environ.get("DISCORD_TOKEN")

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

@tree.command(name="vckick", description="Auto kick from active voice chat")
@app_commands.describe(time="Optional time in minutes to perform kick (e.g., 120 for 2 hours)")
async def vckick(interaction: discord.Interaction, time: int = None):
    log(interaction, f"VcKick (time: {time} minutes)")
    
    if time is not None:
        if time <= 0:
            await interaction.response.send_message("The specified time should be greater than 0.", ephemeral=True)
            return
        
        kick_time = datetime.now() + timedelta(minutes=time)
        
        threading.Thread(target=schedule_kick, args=(interaction, kick_time)).start()
        
        await interaction.response.send_message(f"Kick scheduled for {kick_time.strftime('%H:%M:%S')}.", ephemeral=True)
    else:
        await interaction.user.move_to(None)
        await interaction.response.send_message("You have been kicked from the voice channel.", ephemeral=True)

def schedule_kick(interaction: discord.Interaction, kick_time):
    delay_seconds = (kick_time - datetime.now()).total_seconds()
    time.sleep(delay_seconds)
    client.loop.create_task(kick_user(interaction.user))

async def kick_user(user):
    await user.move_to(None)

# LOG PRINTS
def log(interaction: discord.Interaction, command_name: str):
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f'({current_time}) [{interaction.guild}/{interaction.channel}] - {interaction.user.name}: {command_name}')

# MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)
    keep_alive()

if __name__ == '__main__':
    main()

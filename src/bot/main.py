import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# bot set up
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')

    # sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# slash command: /link
@bot.tree.command(name='link', description="Link you GitHub username to your Discord account")
async def link_command(interaction: discord.Interaction, github_username: str):
    # testing by echoing back what is entered
    await interaction.response.send_message(
        f"Linking GitHub Username: **{github_username}** to <@{interaction.user.id}>",
        ephemeral=True    
    )

# slash command: /setup
@bot.tree.command(name="setuprepo", description="Set up a repository for annnouncements")
async def setup_command(interaction: discord.Interaction, repo_owner: str, repo_name: str, channel: str):
    # check if the user has permission
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message(
            "You need **Manage Server** permissions to use this command.",
            ephemeral=True
        )
        return
    
    # testing by echoing back what is entered
    await interaction.response.send_message(
        f" Setting up repository: **{repo_owner}/{repo_name}**\n"
        f" announcements will be send to: {channel}",
        ephemeral=True
    )
       

# Run the bot
if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_TOKEN'))


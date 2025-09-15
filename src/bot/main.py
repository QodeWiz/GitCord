import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.database.models import Database

# load environment variables
load_dotenv()

# databse
db = Database()

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
    # save to database
    db.link_user(str(interaction.user.id), github_username)

    # get linked username to confirm
    linked_username = db.get_linked_github(str(interaction.user.id))

    await interaction.response.send_message(
        f"🔗 **Successfully linked!**\n"
        f"GitHub: **{linked_username}**\n"
        f"Discord: <@{interaction.user.id}>",
        ephemeral=True    
    )

# slash command: /setup
@bot.tree.command(name="setuprepo", description="Set up a repository for annnouncements")
async def setup_command(interaction: discord.Interaction, repo_owner: str, repo_name: str, channel: str):
    # check if the user has permission
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message(
            "❌ You need **Manage Server** permissions to use this command.",
            ephemeral=True
        )
        return
    
    # generate a random webhook secret
    import secrets
    webhook_secret = secrets.token_hex(16)

    # save to database
    db.save_repo(str(interaction.guild.id), repo_owner, repo_name, webhook_secret, channel)

    await interaction.response.send_message(
        f"⚙️ **Repository configured!**\n"
        f"📁 **{repo_owner}/{repo_name}**\n"
        f"�� **Channel:** {channel}\n"
        f"�� **Webhook Secret:** `{webhook_secret}`\n\n"
        f"**Next step:** Add this webhook to your GitHub repository!",
        ephemeral=True
    )
       

def main():
    """Main function to run the bot"""
    bot.run(os.getenv('DISCORD_TOKEN'))

# Run the bot
if __name__ == "__main__":
    main()


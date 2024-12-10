import discord

from Include import init
from modules import functions

from discord.ext import commands
from discord.ext import slash

#init.logger()

conf = init.config('discord')
token = conf.get_token()
domain = conf.get_pterodactyl_domain()
apikey = conf.get_pterodactyl_apikey()

bot = slash.SlashBot(command_prefix='!', help_command=None)

@bot.event
async def on_ready():
    print('Bot started succesfully')
    return

@bot.slash_cmd(aliases=["hilfe"])
async def help(ctx:slash.Context):
    "Hilfe für alle verwendbaren Befehle" #Help for all usable commands
    await functions.cmdhelp(ctx)

@bot.slash_cmd(aliases=["minecraft", "link"])
async def mc(ctx:slash.Context, name:slash.Option(description="Dein Minecraftname", required=True)): #Your Minecraft name
    "Registriere deinen Minecraft Namen" #Register your Minecraft name
    await functions.cmdmc(ctx, name.strip(), bot)

@bot.slash_cmd()
async def mcname(ctx:slash.Context):
    "Gibt deinen aktuellen Minecraft Namen an" #Outputs your linked Minecraft account
    await functions.cmdmcname(ctx)

@bot.slash_cmd()
async def shutdown(ctx:slash.Context):
    "Will shutdown the bot if you are mighty enough."
    if await functions.isAdmin(ctx, bot):
        await functions.cmdshutdown(ctx, bot)

@bot.slash_cmd()
async def verify(ctx:slash.Context):
    "Verify that you are an official student at HPI"
    await functions.cmdverify(ctx)

bot.run(token)
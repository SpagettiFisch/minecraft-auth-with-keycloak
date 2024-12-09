import discord
import json
import requests
import urllib
import random
import asyncio

from os import path
from shutil import copyfile
from discord.ext import slash

from modules import init

con, cur = init.getdb()
# mod_roles = init.config().get_mod_roles()
# admin_roles = init.config().get_admin_roles()

async def cmdhelp(ctx:slash.Context): #TODO change to actual commands
    embed = discord.Embed(title="Hilfe",
                          color=discord.Colour(0x15f00a))
    embed.add_field(name="/mc [Name]",
                    value="Registriere deinen Minecraft-Account")
    embed.add_field(name="/mcname",
                    value="Gibt deinen aktuellen Minecraft-Account wieder")
    await ctx.respond(embed=embed, ephemeral=True)
    return

async def cmdmc(ctx:slash.Context, name:str, client):
    mcsite = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{name}')
    mcinfo = mcsite.json()

    if not 'error' in mcinfo:
        mcinfo = mcsite.json() #TODO why again?
        uuid = mcinfo['id']
        uuid = f'{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:32]}'

        result = cur.execute(f"SELECT * FROM user WHERE id = '{ctx.author.id}'")
        result = cur.fetchone()
        if result:
            cur.execute(f"UPDATE user SET mcname = '{mcinfo['name']}', uuid = '{uuid}' WHERE id = {ctx.author.id}")
            await ctx.respond(f'Dein Minecraftname **{name}** wurde erfolgreich aktualisiert.')
        else:
            cur.execute(f"INSERT INTO user VALUES ({ctx.author.id}, '{ctx.author.nick}', '{ctx.author.avatar_url}', '{mcinfo['name']}', '{uuid}', {False})")
            await ctx.respond(f'Dein Minecraftname **{name}** wurde erfolgreich hinzugefügt.')
        con.commit()
        await syncWhitelist()
    else:
        await ctx.respond(f'Der Minecraftname **{name}** existiert nicht.', ephemeral=True)

async def cmdmcname(ctx:slash.Context): #TODO add skin view maybe
    result = cur.execute(f"SELECT * FROM user WHERE id = '{ctx.author.id}'")
    result = cur.fetchone()
    if result:
        if result[5]:
            color = '#859a22'
        else:
            color = '#b30f40'
        embed = discord.Embed(title=ctx.author,
                              color=discord.Colour(color))
        embed.add_field(name="Minecraftname:",
                        value=result[3])
        embed.set_image(url=result[2])
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        await ctx.respond('Du hast deinen Minecraftnamen noch nicht hinzugefügt. Nutze `/mc [name]` um ihn hinzuzufügen.', ephemeral=True)

async def cmdshutdown(ctx:slash.Context, bot):
    if str(ctx.channel.id) == str(init.config().get_guild_admin_id()):
        await ctx.respond('Logging out and initiating shutdown', ephemeral=True)
        print('Start logging out')
        await bot.logout()
        bot.clear()
        asyncio.run(bot.close())
        print('Log Out succesful\nExiting')
        exit()
    else:
        await ctx.respond('You are not as mighty as you may think you are.')

async def cmdverify(ctx:slash.Context):
    pass
    #TODO verify somehow

async def syncWhitelist():
    results = cur.execute("SELECT mcname, uuid, iswhitelisted FROM user")
    results = cur.fetchall()
    whitelist = []

    for result in results:
        if result[2]:
            whitelist.append({
                'uuid': result[1],
                'name': result[0]
            })
    with open('whitelist/whitelist.json', 'w') as outfile:
        json.dump(whitelist, outfile, indent=2)
    
    await syncWhitelistFiles()
    await syncWhitelistPterodactyl(whitelist)

async def syncWhitelistFiles():
    paths = open('whitelist/paths.txt', 'r')
    for line in paths:
        copyfile('whitelist/whitelist.json', f'{str(line.rstrip())}whitelist.json')
    paths.close()

async def syncWhitelistPterodactyl(whitelist):
    paths = open("whitelist/pterodactyl.txt", "r")
    for line in paths:
        parts = line.split(" ")
        serverid = parts[0]
        whitelistpath = parts[1]

        await pterodactylWriteFile(serverid, whitelistpath, json.dumps(whitelist), init.config().get_pterodactyl_apikey())
    paths.close()

async def pterodactylWriteFile(serverid, path, data, apikey):
    url = f'{init.config().get_pterodactyl_domain()}api/client/servers/{serverid}/files/write?file={urllib.parse.quote(path)}'
    requests.post(url, data=data, headers={"Accept": "application/json", "Authorization": f"Bearer {apikey}"})

# async def isMod(ctx:slash.Context, bot):
#     allowed = False
#     for id in mod_roles:
#         guild = bot.get_guild(ctx.guild.id)
#         role = guild.get_role(id)
#         member = await guild.fetch_member(ctx.author.id)
#         if role in member.roles:
#             allowed = True
#             break

#     if allowed:
#         return True
#     else:
#         await ctx.respond("Du hast nicht die nötigen Rechte um diesen Befehl auszuführen.", ephemeral=True) #You are not allowed to perform this command
#         return 
    
# async def isAdmin(ctx:slash.Context, bot):
#     allowed = False
#     for id in admin_roles:
#         guild = bot.get_guild(ctx.guild.id)
#         role = guild.get_role(id)
#         member = await guild.fetch_member(ctx.author.id)
#         if role in member.roles:
#             allowed = True
#             break

#     if allowed:
#         return True
#     else:
#         await ctx.respond("You are not mighty enough to perform this operation.", ephemeral=True)
#         return 
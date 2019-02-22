#!/usr/bin/env python3

import discord
from discord.ext import commands
import asyncio
import logging, json
from datetime import datetime

logging.basicConfig(level=logging.INFO)

description = '''A bot for the RPI discord server'''
pfx = '?'

green = 0x2dc614
red = 0xc91628
blue = 0x2044f7

bot = commands.Bot(command_prefix=pfx, description=description, pm_help=True,
        case_insensitive=True)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='with the Tute Screw'))

@bot.command(aliases=['about'])
async def info(ctx):
    '''Shows info about the bot.'''
    embed = discord.Embed(title='About ComputerMan', description=bot.description, colour=blue)
    embed = embed.add_field(name='Contributing', value='Check out the source on GitHub: https://github.com/galengold/rpibot-discord', inline=False)
    embed = embed.add_field(name='License', value='ComputerMan is released under the GNU General Public License, version 3.0', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f'**Pong!** Current ping is {bot.latency*1000:.1f} ms')

@bot.command(aliases=['h'])
async def help(ctx):
    '''Show this message.'''
    embed = discord.Embed(title='Commands', description=bot.description, colour=green)
    cmds = sorted(list(bot.commands), key=lambda x:x.name)
    for cmd in cmds:
        v = cmd.help
        if len(cmd.aliases) > 0:
            v += '\n*Aliases:* ?' +\
                f', {pfx}'.join(cmd.aliases).rstrip(f', {pfx}')
        embed = embed.add_field(name=pfx+cmd.name, value=v, inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['nuke'])
async def nukeme(ctx):
    '''Deletes your messages in #support. Does not work in any other channel.'''
    with ctx.typing():
        if ctx.channel.id in secrets['nuke_channels']:
            print('################################ channel matches')
            history = ctx.channel.history(limit=None).flatten()
            filtered = [x for x in history if x.author.id == ctx.author.id]
            ctx.channel.delete_messages(filtered)
            try:
                await ctx.message.add_reaction("✅")
            except:
                return
        else:
            try:
                await ctx.message.add_reaction("❌")
            except:
                return


# Special Commands

@bot.command()
async def restart(ctx):
    if any([str(x.id) in secrets['exit_role'] for x in ctx.author.roles]):
        await ctx.channel.send("Restarting...")
        await bot.logout()
    else:
        try:
            await ctx.message.add_reaction("❌")
        except:
            return

@bot.command()
async def shutdown(ctx):
    if any([str(x.id) in secrets['exit_role'] for x in ctx.author.roles]):
        await ctx.channel.send("Shutting down...")
        os._exit(42)
    else:
        try:
            await ctx.message.add_reaction("❌")
        except:
            return

#########################

with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

bot.run(secrets['token'])

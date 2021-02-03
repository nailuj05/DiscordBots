import discord
from discord.ext import commands, tasks
from itertools import cycle
import numpy as np

bot = commands.Bot(command_prefix='/')
status = cycle(["Patentamt", "Recht und Ordnung", "/newPatent", "/Patente"])

patente = np.array([])

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(''))
    change_status.start()
    print('Bot online')

# change_status
@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.command(pass_context = True)
async def newPatent(ctx):
    global patente
    msg = 'Nutzer {0.author.mention} hat ein Patent angemeldet: '.format(ctx.message)
    patent = ctx.message.content
    patent = patent.replace("/newPatent", "")
    msg = msg + patent
    patente = np.append(patente, patent)
    await ctx.send(msg)

@bot.command(pass_context = True)
async def newpatent(ctx):
    global patente
    msg = 'Nutzer {0.author.mention} hat ein Patent angemeldet: '.format(ctx.message)
    patent = ctx.message.content
    patent = patent.replace("/newpatent", "")
    msg = msg + patent
    patente = np.append(patente, patent)
    await ctx.send(msg)

@bot.command(pass_context = True)
async def Patente(ctx):
    global patente

    for i in range(0, len(patente)):
        await ctx.send(format(i + 1) + ". Patent: " + patente[i])



bot.run("")

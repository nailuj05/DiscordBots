import discord
from discord.ext import commands, tasks
from itertools import cycle
import numpy as np

bot = commands.Bot(command_prefix='/')
status = cycle(["Patentamt", "Recht und Ordnung", "/newPatent", "/Patente"])

patente = np.array([])

csvData = np.array([])

try:
    csvData = np.load('patente.npy')
except:
    print("failed to load")
    np.save("patente.npy", np.array(["Patente: "]))

patente = csvData

def in_channel():
    def predicate(ctx):
        print(ctx.message.channel.id)
        return ctx.message.channel.id == 806547139685253160
    return commands.check(predicate)

@bot.event
async def on_ready():
    global patente
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(''))
    change_status.start()


    print(patente)
    print('Bot online')

# change_status
@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.command(pass_context = True)
@in_channel()
async def newPatent(ctx):
    global patente
    msg = 'Nutzer {0.author.mention} hat ein Patent angemeldet: '.format(ctx.message)
    patent = ctx.message.content
    patent = patent.replace("/newPatent", "")
    msg = msg + patent
    patente = np.append(patente, patent + " von: " + format(ctx.message.author.name))

    np.save("patente", patente)

    await ctx.send(msg)

@bot.command(pass_context = True)
@in_channel()
async def newpatent(ctx):
    global patente
    msg = 'Nutzer {0.author.mention} hat ein Patent angemeldet: '.format(ctx.message)
    patent = ctx.message.content
    patent = patent.replace("/newpatent", "")
    patent = patent.replace("@", "")
    msg = msg + patent
    print(patente)
    patente = np.append(patente, patent + " von: " + format(ctx.message.author.name))

    print(patente)
    np.save("patente", patente)

    await ctx.send(msg)

@bot.command(pass_context = True)
@in_channel()
async def Patente(ctx):
    global patente

    res = "Patente: \n"

    print(patente)

    for i in range(0, len(patente)):
        res += format(i + 1) + ". Patent: " + patente[i] + "\n"
        print(patente[i])

    await ctx.send(res)



bot.run("")

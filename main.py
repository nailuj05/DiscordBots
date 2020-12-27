import discord
from discord.ext import commands
import numpy as np

bot = commands.Bot(command_prefix='/')

board = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
isPlayerO = False
gameWon = False

@bot.command(name = "newGame", help="Creates a new game")
async def newGame(ctx):
    global board
    global gameWon
    global isPlayerO
    board = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    boardString = Plot(board)

    embed = discord.Embed(title="TicTacToe", colour=ctx.author.colour, timestamp=ctx.message.created_at)
    embed.add_field(name="New game created", value=boardString, inline=True)

    gameWon = False
    isPlayerO = False

    await ctx.send(embed = embed)

@bot.command(name = "play", help="Make a move with /play [row] [collumn}")
async def play(ctx, row: int, collumn: int):
    index = (((row - 1) * 3) + collumn) - 1

    global gameWon
    global board
    global isPlayerO

    embed = discord.Embed(title="TicTacToe", colour=ctx.author.colour, timestamp=ctx.message.created_at)

    if(gameWon != True):
        if(board[index] == 0):

            if(isPlayerO):
                board[index] = -1
                nameField = "O played"
            else:
                board[index] = 1
                nameField = "X played"

            isPlayerO = not isPlayerO

            embed.add_field(name=nameField, value=Plot(board), inline=True)

            await ctx.send(embed = embed)
        else:
            embed.add_field(name="Diskrepanz!", value=(Plot(board) + "Das Feld ist schon voll"), inline=True)
            await ctx.send(embed = embed)
    else:
        embed.add_field(name="Diskrepanz!", value=(Plot(board) + "Das Spiel ist bereits gespielt, erstelle ein neues Spiel mit /newGame"), inline=True)
        await ctx.send(embed=embed)

    if (WinCheckBoard(board) == 'X'):
        embed.add_field(name="Game Over!", value="Spieler X gewinnt", inline=True)
        gameWon = True
        await ctx.send(embed = embed)
    elif(WinCheckBoard(board) == 'O'):
        embed.add_field(name="Game Over!", value="Spieler O gewinnt", inline=True)
        gameWon = True
        await ctx.send(embed = embed)
    elif(WinCheckBoard(board) == 'Q'):
        embed.add_field(name="Game Over!", value="Unentschieden, niemand gewinnt!", inline=True)
        gameWon = True
        await ctx.send(embed = embed)


def Plot(board):
    returnstring = ""
    for i in range(9):
        if(board[i] == 0):
            returnstring += " - "
        elif(board[i] == 1):
            returnstring += " X "
        elif(board[i] == -1):
            returnstring += " O "
        if(i == 2 or i == 5):
            returnstring += "\n"
        if(i == 8):
            returnstring += "\n"

    return returnstring

def WinCheckBoard(board):
    tmpsum = board[0]+board[1]+board[2]
    if tmpsum == 3:
        return 'X'
    elif tmpsum == -3:
        return 'O'
    tmpsum = board[3]+board[4]+board[5]
    if tmpsum == 3:
        return 'X'
    elif tmpsum == -3:
        return 'O'
    tmpsum = board[6]+board[7]+board[8]
    if tmpsum == 3:
        return 'X'
    elif tmpsum == -3:
        return 'O'
    tmpsum = board[0]+board[3]+board[6]
    if tmpsum == 3:
        return 'X'
    elif tmpsum == -3:
        return 'O'
    tmpsum = board[1]+board[4]+board[7]
    if tmpsum == 3:
        return 'X'
    elif tmpsum == -3:
        return 'O'
    tmpsum = board[2]+board[5]+board[8]
    if tmpsum == 3:
        return 'X'
    elif tmpsum == -3:
        return 'O'
    tmpsum = board[0]+board[4]+board[8]
    if tmpsum == 3:
        return 'X'
    elif tmpsum == -3:
        return 'O'
    tmpsum = board[2]+board[4]+board[6]
    if tmpsum == 3:
        return 'X'
    elif tmpsum == -3:
        return 'O'
    if(all(board!=0)):
        return 'Q'
    return 'N'

bot.run('TOKEN')

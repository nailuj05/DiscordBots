import discord
from discord import Member
from discord.ext import commands, tasks
from itertools import cycle
import time

bot = commands.Bot(command_prefix='/')
status = cycle(['Moderation bot', 'Hello World!'])


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(''))
    change_status.start()
    print('Bot online')


# change_status
@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


# command ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


# command_clear
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'{amount} messages have been cleared!')
    time.sleep(1)
    await ctx.channel.purge(limit=1)


# command_kick
@bot.command(name="kick", help="kick a member")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')


# command_ban
@bot.command(name="ban", help="ban a member")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


# command_unban
@bot.command(name="unban", help="unban a member")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.descriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


# command_userinfo
@bot.command(name='userinfo', help='userinfo')
async def userinfo(ctx, member: discord.Member):
    roles = [role for role in member.roles]
    embed = discord.Embed(title=f'Userinfo for {member.display_name}', color=member.color,
                          timestamp=ctx.message.created_at)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
    embed.add_field(name='Joined server:', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                    inline=True)
    embed.add_field(name='Joined Discord:', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                    inline=True),
    embed.add_field(name=f'Roles ({len(roles)})', value=' '.join([role.mention for role in roles]), inline=True)
    embed.add_field(name='Bot?', value=member.bot, inline=True)
    await ctx.send(embed=embed)


# error
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please set an amount of messages to delete!')
        time.sleep(1)
        ctx.channel.purge(limit=1)


# error_listener
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.purge(limit=1)
        await ctx.send('invalid command')
        time.sleep(1)
        await ctx.channel.purge(limit=1)


# @bot.event (not working) WIP
# async def on_message(message):
#    if "discord.gg" in message.content:
#        await message.channel.purge(limit=1)
#        await message.channel.send(f'Invites are not allowed')
#        time.sleep(1)
#        await message.channel.purge(limit=1)


bot.run('TOKEN')

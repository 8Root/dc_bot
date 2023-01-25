import discord
import os
import asyncio
import datetime
import keep_alive
from discord.ext import commands, tasks
from discord import permissions
import time

token = os.getenv("bot_token")
bot_name = "Frok"
cmd_prefix = "$"
mod_role = "Frokky"

intents = discord.Intents().all()
client = commands.Bot(command_prefix=cmd_prefix, intents=intents)
client.remove_command('help')


@client.command()
@commands.is_owner()
async def shutdown(ctx):
  await ctx.send("Logging out.")
  await client.logout()


@shutdown.error
async def shutdown_error(ctx, error):
  if isinstance(error, commands.NotOwner):
    await ctx.send("You are not the owner of the bot.")


@client.event
async def on_message(message):
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  with open("log.txt", "a") as text_file:
    print(f"<{st}> <{message.author}> <{message.id}>  {message.content}",
          file=text_file)
  await client.process_commands(message)


@client.command()
async def say(ctx, *, text):
  await ctx.send(f"{text}")
  await ctx.message.delete()


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name=f""))



print ("bot online")

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Streaming(
    name='balls hahahahahahahahahahahaha', url='https://www.youtube.com/watch?v=OR4N5OhcY9s'))

  print('Connected to bot: {}'.format(client.user.name))
  print('Bot ID: {}'.format(client.user.id))


@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, time, reason=None):
  desctime = time
  guild = ctx.guild
  mutedRole = discord.utils.get(guild.roles, name="Muted")
  time_convert = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
    "w": 604800,
    "mo": 18144000,
    "y": 31536000
  }
  tempmute = int(time[-1]) * time_convert[time[-1]]
  if not mutedRole:
    mutedRole = await guild.create_role(name="Muted")
    for channel in guild.channels:
      await channel.set_permissions(mutedRole,
                                    speak=False,
                                    send_messages=False,
                                    read_message_history=True,
                                    read_messages=False)
  embed = discord.Embed(
    title="muted",
    description=f"{member.mention} was muted   for {desctime} ",
    colour=discord.Colour.light_gray())
  embed.add_field(name="reason:", value=reason, inline=True)
  await ctx.send(embed=embed)
  await member.add_roles(mutedRole, reason=reason)
  await asyncio.sleep(tempmute)
  await member.send(f" you have been muted from: {guild.name} reason: {reason}"
                    )
  await member.remove_roles(mutedRole)


@client.command()
async def help(ctx):
  embed = discord.Embed(title='Help',
                        description="Try out these commmands below",
                        colour=discord.Colour.orange())

  embed.set_footer(text="Bot by @Rootqit.")
  embed.set_author(name=bot_name)
  embed.add_field(name=f"{cmd_prefix}ping", value="Check Ping", inline=False)
  embed.add_field(
    name=f"{cmd_prefix}shutdown",
    value="Shut down the bot. Will not go offline instantly, takes some time.",
    inline=False)
  embed.add_field(
    name=f"{cmd_prefix}log",
    value=
    "Create a full log of all messages/activities, can only be viewed by the owner.",
    inline=False)
  embed.add_field(name=f"{cmd_prefix}say",
                  value="Make the bot say something!",
                  inline=False)
  await ctx.send(embed=embed)


@client.command()
async def update(ctx):
  embed = discord.Embed(title='Update! v1.1',
                        description="New update!",
                        colour=discord.Colour.orange())
  embed.set_footer(text="Bot by @Rootqit.")
  embed.set_author(name=bot_name)
  embed.add_field(name=f"New command!",
                  value="$log got added! only for the owner tho.",
                  inline=True)
  await ctx.send(embed=embed)


@client.command()
@commands.has_role(mod_role)
async def clear(ctx, amount=10):
  await ctx.message.delete()
  await ctx.channel.clear(limit=amount)


@client.command()
@commands.has_role(mod_role)
async def give_role(ctx,
                    member: discord.Member,
                    role: discord.Role,
                    *,
                    reason=None):
  member.add_roles(role, reason=reason)


keep_alive.keep_alive()
client.run(token)

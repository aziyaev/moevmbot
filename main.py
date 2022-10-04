import asyncio
import disnake
from disnake.ext import commands

import config

bot = commands.Bot(command_prefix="?", help_command=None, intents=disnake.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.dnd, activity=disnake.Game("help"))

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(config.CHANNEL_ID)
    role = disnake.utils.get(member.guild.roles, id=config.ROLE_ID)

    await member.add_roles(role)

@bot.event
async def on_raw_reaction_add(payload):
    messageid = payload.message_id
    if str(messageid) == config.MESSAGE_ID:
        member = payload.member
        guild = bot.get_channel(config.CHANNEL_ID)
        for role in member.roles:
            if role.id in config.ROLES.values():
                await bot.http.remove_reaction(payload.channel_id, payload.message_id,
                                               payload.emoji.name, payload.user_id)
                return
        for emoji in config.ROLES:
            if payload.emoji.name == emoji:
                role = disnake.utils.get(member.guild.roles, id=int(config.ROLES[emoji]))
                await member.add_roles(role)

@bot.command(name="kick", brief="Выгнать пользователя с сервера")
@commands.has_permissions(administrator=True, kick_members=True)
async def delete(ctx, role: disnake.Role, *, reason=None):
    await ctx.message.delete()

    for member in ctx.guild.members:
        for _role in member.roles:
            if _role.id == role.id:
                await ctx.send(f"Участник {member.mention}, был выгнан с сервера!")
                await member.kick(reason=reason)

bot.run(config.TOKEN)


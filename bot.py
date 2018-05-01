import discord
from discord.ext import commands
import logging
import asyncio
import random
import time
import os

client = commands.Bot(command_prefix="Mike ")
footer_text = "Open Mic"

@client.event
async def on_ready():
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    print("---------------")
    await client.change_presence(game=discord.Game(name='wit Huskie'))

# }tempmute <user> <time> [reason]
@client.command(pass_context=True)
async def tempmute(ctx, userName: discord.Member = None, time: int = None, *, args = None):
    member_role = discord.utils.get(ctx.message.server.roles, name ='Listener')
    punished_role = discord.utils.get(ctx.message.server.roles, name='Muted')
    helper_role = discord.utils.get(ctx.message.server.roles, name='Helper')
    mod_role = discord.utils.get(ctx.message.server.roles, name='Mods')
    admin_role = discord.utils.get(ctx.message.server.roles, name='Co-Owner')
    manager_role = discord.utils.get(ctx.message.server.roles, name='Owners')
    owner_role = discord.utils.get(ctx.message.server.roles, name='Real Toothless')
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if helper_role in author.roles or mod_role in author.roles or admin_role in author.roles or manager_role in author.roles or owner_role in author.roles:
        if userName == None or time == None:
            msg.add_field(name=":warning: ", value="`Mike tempmute (user) (time) (reason)`")
            await client.say(embed=msg)
        elif helper_role in userName.roles or mod_role in userName.roles or admin_role in userName.roles or manager_role in userName.roles or owner_role in userName.roles:
            msg.add_field(name=":warning: ", value="`You can't punish other staff!`")
            await client.say(embed=msg)
        elif punished_role in userName.roles:
            msg.add_field(name=":warning: ", value="`That user is already muted!`")
            await client.say(embed=msg)
        else:
            time2 = time * 60
            if args == None:
                await client.add_roles(userName, punished_role)
                await client.remove_roles(userName, member_role)
                msg.add_field(name=":speak_no_evil: ", value="`{} has been temp muted by {}! for {} minute(s)!`\n`Reason: ?`".format(userName.display_name, author.display_name, time))
                await client.say(embed=msg)
                await asyncio.sleep(float(time2))
                await client.remove_roles(userName, punished_role)
                await client.say("```diff\n- Removed {}'s mute! ({} minute(s) are up.)\n```".format(userName.display_name, time))
            else:
                await client.add_roles(userName, punished_role)
                msg.add_field(name=":speak_no_evil: ", value="`{} has been temp muted by {} for {} minute(s)!`\n`Reason: {}`".format(userName.display_name, author.display_name, time, args))
                await client.say(embed=msg)
                await asyncio.sleep(float(time2))
                await client.remove_roles(userName, punished_role)
                await client.say("```diff\n- Removed {}'s mute! ({} minute(s) are up.)\n```".format(userName.display_name, time))
    else:
        msg.add_field(name=":warning: ", value="`This command can only be used by staff!`")
        await client.say(embed=msg)
        
# <say <text>
@client.command(pass_context=True)
async def say(ctx, *, args=None): 
    staff_role = discord.utils.get(ctx.message.server.roles, name='Staff')
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if staff_role in author.roles or staff_role in author.roles:
        if args == None:
            msg.add_field(name=":warning: ", value="Mike say <text>")
            await client.say(embed=msg)
        else:
            await client.say("{}".format(args))
            await client.delete_message(ctx.message)
    else:
        msg.add_field(name=":warning: ", value="`This command can only be used by Staff!`")
        await client.say(embed=msg)
        
# EVENT - JOIN / LEAVE
@client.async_event
async def on_member_join(userName: discord.User):
    joins = ["Hey {}, welcome this legend".format(userName)]
    await client.send_message(client.get_channel("421935231600427008"), "{}".format(random.choice(joins)))
    print("============================================================")
    print("JOIN EVENT")
    print("{} ### {}".format(userName, userName.id))
    print("============================================================")
    
# <kick <user> [reason]
@client.command(pass_context=True)
async def kick(ctx, userName: discord.Member = None, *, args = None):
    helper_role = discord.utils.get(ctx.message.server.roles, name='Helpers')
    mod_role = discord.utils.get(ctx.message.server.roles, name='Mods')
    admin_role = discord.utils.get(ctx.message.server.roles, name='Co-Owner')
    manager_role = discord.utils.get(ctx.message.server.roles, name='Owners')
    owner_role = discord.utils.get(ctx.message.server.roles, name='Real Toothless')
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if mod_role in author.roles or admin_role in author.roles or manager_role in author.roles or owner_role in author.roles:
        if userName == None:
            msg.add_field(name=":warning: ", value="`Mike kick (user) (reason)`")
        elif helper_role in userName.roles or mod_role in userName.roles or admin_role in userName.roles or manager_role in userName.roles or owner_role in userName.roles:
            msg.add_field(name=":warning: ", value="`You can't kick other staff!`")
        elif args == None:
            msg.add_field(name=":boot: Kicker", value="`{} kicked {}!`\n`Reason: ?`".format(author.display_name, userName.display_name))
            await client.kick(userName)
        else:
            msg.add_field(name=":boot: Kicker", value="`{} kicked {}!`\n`Reason: {}`".format(author.display_name, userName.display_name, args))
            await client.kick(userName)
    else:
        msg.add_field(name=":warning: ", value="`This command can only be used by Moderators, Co Owners and Owners!`")
    await client.say(embed=msg)
    
# <matchmake <user1> <user2>
@client.command(pass_context=True)
async def ship(ctx, userName1: discord.Member = None, userName2: discord.Member = None):
    percent = random.randint(0, 101)
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName1 == None or userName2 == None:
        msg.add_field(name=":warning: ",value="`Mike ship (user1) (user2)`")
    else:
        if percent >= 1 and percent <= 10:
            msg.add_field(name=":heartpulse: Matchmaking... :heartpulse: ", value=":small_red_triangle_down: **{}**\n:small_red_triangle: **{}**\n```fix\n{}% - No point\n```\n:sob: ".format(userName1.display_name, userName2.display_name, percent))
        elif percent >= 11 and percent <= 20:
            msg.add_field(name=":heartpulse: Matchmaking... :heartpulse: ", value=":small_red_triangle_down: **{}**\n:small_red_triangle: **{}**\n```fix\n{}% - Trash\n```\n:cry: ".format(userName1.display_name, userName2.display_name, percent))
        elif percent >= 21 and percent <= 30:
            msg.add_field(name=":heartpulse: Matchmaking... :heartpulse: ", value=":small_red_triangle_down: **{}**\n:small_red_triangle: **{}**\n```fix\n{}% - Just don't\n```\n:frowning2: ".format(userName1.display_name, userName2.display_name, percent))
        elif percent >= 31 and percent <= 40:
            msg.add_field(name=":heartpulse: Matchmaking... :heartpulse: ", value=":small_red_triangle_down: **{}**\n:small_red_triangle: **{}**\n```fix\n{}% - The opposite to good\n```\n:slight_frown: ".format(userName1.display_name, userName2.display_name, percent))
        elif percent >= 41 and percent <= 50:
            msg.add_field(name=":heartpulse: Matchmaking... :heartpulse: ", value=":small_red_triangle_down: **{}**\n:small_red_triangle: **{}**\n```fix\n{}% - 50/50 ish\n```\n:neutral_face: ".format(userName1.display_name, userName2.display_name, percent))
        elif percent >= 51 and percent <= 60:
            msg.add_field(name=":heartpulse: Matchmaking... :heartpulse: ", value=":small_red_triangle_down: **{}**\n:small_red_triangle: **{}**\n```fix\n{}% - Good\n```\n:slight_smile: ".format(userName1.display_name, userName2.display_name, percent))
        elif percent >= 61 and percent <= 70:
            msg.add_field(name=":heartpulse: Matchmaking... :heartpulse: ", value=":small_red_triangle_down: **{}**\n:small_red_triangle: **{}**\n```fix\n{}% - Very Good\n```\n:smiley: ".format(userName1.display_name, userName2.display_name, percent))
        elif percent >= 71 and percent <= 80:
            msg.add_field(name=":heartpulse: Matchmaking... :heartpulse: ", value=":small_red_triangle_down: **{}**\n:small_red_triangle: **{}**\n```fix\n{}% - Fantastic\n```\n:blush: ".format(userName1.display_name, userName2.display_name, percent))
        elif percent >= 81 and percent <= 90:
            msg.add_field(name=":heartpulse: Matchmaking... :heartpulse: ", value=":small_red_triangle_down: **{}**\n:small_red_triangle: **{}**\n```fix\n{}% - Amazing\n```\n:heart_eyes: ".format(userName1.display_name, userName2.display_name, percent))
        else:
            msg.add_field(name=":heartpulse: Matchmaking... :heartpulse: ", value=":small_red_triangle_down: **{}**\n:small_red_triangle: **{}**\n```fix\n{}% - Get a room you two\n```\n:revolving_hearts: ".format(userName1.display_name, userName2.display_name, percent))
    await client.say(embed=msg)
    
# <cuddle <user>
@client.command(pass_context=True)
async def cuddle(ctx, userName: discord.Member = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None:
        msg.add_field(name=":warning: ", value="`Mike cuddle (user)`")
    else:
        msg.set_image(url="{}".format(random.choice(cuddlelinks)))
        msg.add_field(name=":tongue: Emotes :tongue:", value="`{}, you got a cuddle from {}!`".format(userName.display_name, author.display_name), inline=True)
    await client.say(embed=msg)
    print("============================================================")
    print("}cuddle <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")

cuddlelinks = ["https://i.imgur.com/GWNWcLH.gif",
               "https://i.imgur.com/i3Eqqgz.gif",
               "https://i.imgur.com/GpFk6fE.gif",
               "https://i.imgur.com/mc3Z7wf.gif",
               "https://i.imgur.com/N5JYB5r.gif",
               "https://i.imgur.com/PGp8JYq.gif"]

# <pat <user>
@client.command(pass_context=True)
async def pat(ctx, userName: discord.Member = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None:
        msg.add_field(name=":warning: ", value="`Mike pat (user)`")
    else:
        msg.set_image(url="{}".format(random.choice(patlinks)))
        msg.add_field(name=":tongue: Emotes :tongue:", value="`{}, you got a pat from {}!`".format(userName.display_name, author.display_name), inline=True)
    await client.say(embed=msg)
    print("============================================================")
    print("}pat <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")

patlinks = ["https://i.imgur.com/8eApUKG.gif",
            "https://i.imgur.com/qVcP9Pt.gif",
            "https://i.imgur.com/X9hKO2p.gif",
            "https://i.imgur.com/v8cRPH9.gif",
            "https://i.imgur.com/N6C7C30.gif",
            "https://i.imgur.com/M9QPcY6.gif",
            "https://i.imgur.com/oUSdjX6.gif",
            "https://i.imgur.com/mFFr4e0.gif",
            "https://i.imgur.com/3F7kmCd.gif",
            "https://i.imgur.com/7yFvJ6m.gif",
            "https://i.imgur.com/y3La9yP.gif"]

# <kiss <user>
@client.command(pass_context=True)
async def kiss(ctx, userName: discord.Member = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None:
        msg.add_field(name=":warning: ", value="`Mike kiss (user)`")
    else:
        msg.set_image(url="{}".format(random.choice(kisslinks)))
        msg.add_field(name=":tongue: Emotes :tongue:", value="`{}, you got kissed by {}!`".format(userName.display_name, author.display_name), inline=True)
    await client.say(embed=msg)
    print("============================================================")
    print("}kiss <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")

kisslinks = ["https://i.imgur.com/0Ri9sfq.gif",
             "https://i.imgur.com/EMdpmXW.gif",
             "https://i.imgur.com/Y9iLoiv.gif",
             "https://i.imgur.com/ZlqZy8S.gif",
             "https://i.imgur.com/ySav1IQ.gif",
             "https://i.imgur.com/ZGfrn2d.gif",
             "https://i.imgur.com/glwWeUl.gif",
             "https://i.imgur.com/j5hDl7V.gif",
             "https://i.imgur.com/w7mVYty.gif",
             "https://i.imgur.com/FJ5bckO.gif",
             "https://i.imgur.com/KqVmVU7.gif",
             "https://i.imgur.com/EM1C9a6.gif",
             "https://i.imgur.com/TACVpH9.gif",
             "https://i.imgur.com/opiHLtc.gif",
             "https://i.imgur.com/LylJAea.gif"]

# <poke <user>
@client.command(pass_context=True)
async def poke(ctx, userName: discord.Member = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None:
        msg.add_field(name=":warning: ", value="`Mike poke (user)`")
    else:
        msg.set_image(url="{}".format(random.choice(pokelinks)))
        msg.add_field(name=":tongue: Emotes :tongue:", value="`{}, you got poked by {}!`".format(userName.display_name, author.display_name), inline=True)
    await client.say(embed=msg)
    print("============================================================")
    print("}poke <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")

pokelinks = ["https://i.imgur.com/HAAktbl.gif",
             "https://i.imgur.com/Fmd0Rsu.gif",
             "https://i.imgur.com/1rObSM3.gif",
             "https://i.imgur.com/Wo2fc94.gif",
             "https://i.imgur.com/rtTucBW.gif",
             "https://i.imgur.com/4c2mC5d.gif",
             "https://i.imgur.com/1DVD84G.gif"]

# <spank <user>
@client.command(pass_context=True)
async def spank(ctx, userName: discord.Member = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None:
        msg.add_field(name=":warning: ", value="`Mike spank (user)`")
    else:
        msg.set_image(url="{}".format(random.choice(spanklinks)))
        msg.add_field(name=":tongue: Emotes :tongue:", value="`{} spanked {}!`".format(author.display_name, userName.display_name), inline=True)
    await client.say(embed=msg)
    print("============================================================")
    print("}spank <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")

spanklinks = ["https://i.imgur.com/dt1TTQu.gif",
              "https://i.imgur.com/ZsTbDvh.gif",
              "https://i.imgur.com/4LHwG60.gif",
              "https://i.imgur.com/xLOoHKP.gif",
              "https://i.imgur.com/UShywVv.gif",
              "https://i.imgur.com/RE3mnrA.gif"]

# <hug <user>
@client.command(pass_context=True)
async def hug(ctx, userName: discord.Member = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None:
        msg.add_field(name=":warning: ", value="`Mike hug (user)`")
    else:
        msg.set_image(url="{}".format(random.choice(huglinks)))
        msg.add_field(name=":tongue: Emotes:tongue:", value="`{}, you got a hug from {}!`".format(userName.display_name, author.display_name), inline=True)
    await client.say(embed=msg)
    print("============================================================")
    print("}hug <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")

huglinks = ["https://i.imgur.com/yE2RnXK.gif",
            "https://i.imgur.com/R9sYxk8.gif",
            "https://i.imgur.com/iLBEoKv.gif",
            "https://i.imgur.com/cc554e8.gif",
            "https://i.imgur.com/1dqkjHe.gif",
            "https://i.imgur.com/Ph8GTqg.gif",
            "https://i.imgur.com/G6EnOxd.gif",
            "https://i.imgur.com/ZxwHn5Y.gif",
            "https://i.imgur.com/movPIsP.gif",
            "https://i.imgur.com/tKlfSgo.gif",
            "https://i.imgur.com/ICg9nCr.gif",
            "https://i.imgur.com/yC95DC2.gif",
            "https://i.imgur.com/hRYXNKX.gif",
            "https://i.imgur.com/br3bGQc.gif",
            "https://i.imgur.com/IcNGAQD.gif"]

# <lick <user>
@client.command(pass_context=True)
async def lick(ctx, userName: discord.Member = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None:
        msg.add_field(name=":warning: ", value="`Mike lick <user>`")
    else:
        msg.set_image(url="{}".format(random.choice(licklinks)))
        msg.add_field(name=":tongue: Emotes :tongue:", value="`{} licked {}!`".format(author.display_name, userName.display_name), inline=True)
    await client.say(embed=msg)
    print("============================================================")
    print("}lick <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")

licklinks = ["https://i.imgur.com/QkRz1GJ.gif",
             "https://i.imgur.com/ObCPKYV.gif",
             "https://i.imgur.com/7fWrYqd.gif",
             "https://i.imgur.com/O8CNVUL.gif",
             "https://i.imgur.com/4QIlJtC.gif",
             "https://i.imgur.com/LptJIi1.gif",
             "https://i.imgur.com/THGgRJz.gif"]
client.run(os.environ['BOT_TOKEN'])

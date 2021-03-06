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
    await client.change_presence(game=discord.Game(name='on Open Mic™'))

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
    
# }userinfo <user>
@client.command(pass_context=True)
async def userinfo(ctx, userName: discord.Member = None):
    member_role = discord.utils.get(ctx.message.server.roles, name='Listener')
    staff_role = discord.utils.get(ctx.message.server.roles, name='Staff')
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if member_role in author.roles or staff_role in author.roles:
        if userName == None:
            msg.title = ""
            msg.add_field(name="       :warning: ", value="`Mike userinfo (user)`")
        else:
            imageurl = userName.avatar_url
            msg.title = ":closed_book: USER INFORMATION"
            msg.set_thumbnail(url=imageurl)
            msg.add_field(name="NAME:", value=(userName), inline=True)
            msg.add_field(name="ID:", value=(userName.id), inline=True)
            msg.add_field(name="CREATED AT:", value=(userName.created_at), inline=True)
            msg.add_field(name="JOINED AT:", value=(userName.joined_at), inline=True)
            msg.add_field(name="STATUS:", value=(userName.status), inline=True)
            msg.add_field(name="IS BOT:", value=(userName.bot), inline=True)
            msg.add_field(name="GAME:", value="Playing {}".format(userName.game), inline=True)
            msg.add_field(name="NICKNAME:", value=(userName.nick), inline=True)
            msg.add_field(name="TOP ROLE:", value=(userName.top_role), inline=True)
            msg.add_field(name="VOICE CHANNEL:", value=(userName.voice_channel), inline=True)
    await client.say(embed=msg)
    print("============================================================")
    print("<userinfo <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# }punch <user>
@client.command(pass_context=True)
async def punch(ctx, userName: discord.Member = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None:
        msg.add_field(name=":warning: ", value="`Mike punch (user)`")
    else:
        msg.set_image(url="{}".format(random.choice(punchlinks)))
        msg.add_field(name=":tongue: Emotes :tongue:", value="`{}, you got punched by {}! :3`".format(userName.display_name, author.display_name), inline=True)
    await client.say(embed=msg)
    print("============================================================")
    print("}punched <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
punchlinks = ["https://i.imgur.com/T2HdIv8.gif",
              "https://i.imgur.com/LZz65rg.gif",
              "https://i.imgur.com/FqPBIf3.gif",
              "https://i.imgur.com/KmqPDQG.gif",
              "https://i.imgur.com/yEx4aKu.gif"]

# }highfive <user>
@client.command(pass_context=True)
async def highfive(ctx, userName: discord.Member = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None:
        msg.add_field(name=":warning: ", value="`Mike highfive (user)`")
    else:
        msg.set_image(url="{}".format(random.choice(highfivelinks)))
        msg.add_field(name=":tongue: Emotes :tongue:", value="`{} highfived {}! :3`".format(author.display_name, userName.display_name), inline=True)
    await client.say(embed=msg)
    print("============================================================")
    print("}highfive <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
highfivelinks = ["https://i.imgur.com/hjoQeOt.gif",
                 "https://i.imgur.com/9nhheqT.gif",
                 "https://i.imgur.com/yw3xMOu.gif",
                 "https://i.imgur.com/Y4g5fsT.gif",
                 "https://i.imgur.com/p6Hvx5r.gif",
                 "https://i.imgur.com/33nuO9D.gif",
                 "https://i.imgur.com/uFQnmYa.gif",
                 "https://i.imgur.com/9KG3k2n.gif",
                 "https://i.imgur.com/nHCC1ps.gif",
                 "https://i.imgur.com/aKvaNba.gif",
                 "http://i.imgur.com/hnHR29x.gif"]

# }serverinfo
@client.command(pass_context=True)
async def serverinfo(ctx):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ":page_with_curl: SERVER INFORMATION"
    msg.set_footer(text=footer_text)
    msg.add_field(name="MEMBERS", value=(len(ctx.message.server.members)), inline=True)
    msg.add_field(name="CHANNELS", value=(len(ctx.message.server.channels)), inline=True)
    msg.add_field(name="EMOJIS", value=(len(ctx.message.server.emojis)), inline=True)
    msg.add_field(name="ID", value=(ctx.message.server.id), inline=True)
    msg.add_field(name="REGION", value=(ctx.message.server.region), inline=True)
    msg.add_field(name="ROLES", value=(len(ctx.message.server.roles)), inline=True)
    msg.add_field(name="OWNER", value=(ctx.message.server.owner), inline=True)
    msg.add_field(name="CREATED AT", value=(ctx.message.server.created_at), inline=True)
    msg.add_field(name="RELEASE DATE:", value="5th of January 2018", inline=True)
    await client.say(embed=msg)
    print("============================================================")
    print("}serverinfo")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# }kill <user>
@client.command(pass_context=True)
async def kill(ctx, userName: discord.Member = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None:
        msg.add_field(name=":warning: ", value="`Mike kill (user)`")
    else:
        msg.add_field(name=":newspaper: NEWS", value="`{} killed {} by {}`".format(author.display_name, userName.display_name, random.choice(killmsgs)))
    await client.say(embed=msg)
    print("============================================================")
    print("}kill <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
killmsgs = ["beating them with a baseball bat covered with barbed wire!",
            "breaking all their bones with chains!",
            "shooting them with a shotgun!",
            "drowning them in a glass of water!",
            "throwing them into a pool with sharks!",
            "roasting the shit out of them!",
            "throwing them out of a plane!",
            "pushing them off a mountain!",
            "farting at their face!",
            "pushing them into a volcano!",
            "spamming their DMs!",
            "stealing their memes!",
            "stealing their chocolate!",
            "stealing their diamonds on their minecraft server!",
            "throwing a bomb at them!",
            "nuking them!",
            "breaking their toilet!",
            "hacking their toaster!",
            "trapping them in a cage with hungry lions!",
            "hacking their car while they were driving!",
            "hitting their private spot!",
            "poisoning their food!",
            "playing earrape too loud!",
            "putting them in the hunger games!",
            "putting them in the maze!",
            "making them watch furry porn!",
            "making them use internet explorer!",
            "driving over them with a tank!",
            "shooting them with a tank!",
            "trapping them in their mind!",
            "sending them to the realm of darkness!",
            "cutting them to death!",
            "torturing them til they died!",
            "sending them to hell!",
            "selling their soul to the devil!",
            "leaking their browsing history!",
            "setting them on fire!"]

# }giverole <user> <role name>
@client.command(pass_context=True)
async def giverole(ctx, userName: discord.Member = None, *, args = None):
    admin_role = discord.utils.get(ctx.message.server.roles, name='Admins')
    manager_role = discord.utils.get(ctx.message.server.roles, name='Co-Owner')
    owner_role = discord.utils.get(ctx.message.server.roles, name='Owners')
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    serverroles = [ctx.message.server.roles]
    if admin_role in author.roles or manager_role in author.roles or owner_role in author.roles:
        if userName == None or args == None:
            msg.add_field(name=":warning: ", value="`Mike giverole (user) (role name)`")
        else:
            rolename2 = discord.utils.get(ctx.message.server.roles, name='{}'.format(args))
            if rolename2 == None:
                msg.add_field(name=":octagonal_sign: ", value="`The specified role has not been found! Caps Sensitive`")
            elif author.top_role == rolename2 or author.top_role < rolename2:
                msg.add_field(name=":octagonal_sign: ", value="`You cannot give a role that is the same or higher than your top role!`")
            else:
                await client.add_roles(userName, rolename2)
                msg.add_field(name=":inbox_tray: ", value="`{} gave {} to {}!`".format(author.display_name, args, userName.display_name))
    else:
        msg.add_field(name=":octagonal_sign: ", value="`This command can only be used by Admins, Co-Owners and Owners!`")
    await client.say(embed=msg)
    print("============================================================")
    print("}giverole <user> <role name>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# }takerole <user> <role name>
@client.command(pass_context=True)
async def takerole(ctx, userName: discord.Member = None, *, args = None):
    admin_role = discord.utils.get(ctx.message.server.roles, name='Admins')
    manager_role = discord.utils.get(ctx.message.server.roles, name='Co-Owners')
    owner_role = discord.utils.get(ctx.message.server.roles, name='Owners')
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    serverroles = [ctx.message.server.roles]
    if admin_role in author.roles or manager_role in author.roles or owner_role in author.roles:
        if userName == None or args == None:
            msg.add_field(name=":warning: ", value="`Mike takerole (user) (role name)`")
        else:
            rolename2 = discord.utils.get(ctx.message.server.roles, name='{}'.format(args))
            if rolename2 == None:
                msg.add_field(name=":octagonal_sign: ", value="`The specified role has not been found! Caps Sensitive`")
            elif author.top_role == rolename2 or author.top_role < rolename2:
                msg.add_field(name=":octagonal_sign: ", value="`You cannot remove a role that is the same or higher than your top role!`")
            else:
                await client.remove_roles(userName, rolename2)
                msg.add_field(name=":outbox_tray: ", value="`{} removed {} from {}!`".format(author.display_name, args, userName.display_name))
    else:
        msg.add_field(name=":octagonal_sign: ", value="`This command can only be used by Admins, Co-Owners and Owners!`")
    await client.say(embed=msg)
    print("============================================================")
    print("}takerole <user> <role name>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# }purge <number>
@client.command(pass_context=True)
async def purge(ctx, number: int = None):
    helper_role = discord.utils.get(ctx.message.server.roles, name='Mods')
    mod_role = discord.utils.get(ctx.message.server.roles, name='Mods')
    admin_role = discord.utils.get(ctx.message.server.roles, name='Admins')
    manager_role = discord.utils.get(ctx.message.server.roles, name='Co-Owner')
    owner_role = discord.utils.get(ctx.message.server.roles, name='Owners')
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if helper_role in author.roles or mod_role in author.roles or admin_role in author.roles or manager_role in author.roles or owner_role in author.roles:
        if number == None:
            msg.add_field(name=":octagonal_sign: ", value="`Mike purge (number)`")
        else:
            deleted = await client.purge_from(ctx.message.channel, limit=number)
            if len(deleted) < number:
                msg.add_field(name=":wastebasket: ", value="`{} tried to delete {} messages!`\n`Deleted {} message(s)!`".format(author.display_name, number, len(deleted)))
            else:
                msg.add_field(name=":wastebasket: ", value="`{} deleted {} message(s)!`".format(author.display_name, len(deleted)))
    else:
        msg.add_field(name=":octagonal_sign: ", value="`This command can only be used by staff!`")
    await client.say(embed=msg)
    print("============================================================")
    print("}purge <number>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# }mute <user>
@client.command(pass_context=True)
async def mute(ctx, userName: discord.Member = None):
    partner_role = discord.utils.get(ctx.message.server.roles, name='Muted')
    mod_role = discord.utils.get(ctx.message.server.roles, name='Mods')
    admin_role = discord.utils.get(ctx.message.server.roles, name='Admins')
    manager_role = discord.utils.get(ctx.message.server.roles, name='Co-Owner')
    owner_role = discord.utils.get(ctx.message.server.roles, name='Owners')
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if mod_role in author.roles or admin_role in author.roles or manager_role in author.roles or owner_role in author.roles:
        if userName == None:
            msg.add_field(name=":warning: ", value="`Mike mute (user)`")
        else:
            if partner_role in userName.roles:
                await client.remove_roles(userName, partner_role)
                msg.add_field(name=":speak_no_evil: ", value="`{} removed {}'s mute!`".format(author.display_name, userName.display_name))
            else:
                await client.add_roles(userName, partner_role)
                msg.add_field(name=":speak_no_evil: ", value="`{} muted {}!`".format(author.display_name, userName.display_name))
    else:
        msg.add_field(name=":octagonal_sign: ", value="`This command can only be used by Moderators, Administrators, Managers and Owners!`")
    await client.say(embed=msg)
    print("============================================================")
    print("}partner <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")

# }tempban <user> <time> [reason]
@client.command(pass_context=True)
async def tempban(ctx, userName: discord.Member = None, time: int = None, *, args = None):
    helper_role = discord.utils.get(ctx.message.server.roles, name='Mods')
    mod_role = discord.utils.get(ctx.message.server.roles, name='Mods')
    admin_role = discord.utils.get(ctx.message.server.roles, name='Admins')
    manager_role = discord.utils.get(ctx.message.server.roles, name='Co-Owners')
    owner_role = discord.utils.get(ctx.message.server.roles, name='Owners')
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if mod_role in author.roles or admin_role in author.roles or manager_role in author.roles or owner_role in author.roles:
        if userName == None or time == None:
            msg.add_field(name=":warning:`Mike tempban (user) (time) (reason)`")
            await client.say(embed=msg)
        else:
            if helper_role in userName.roles or mod_role in userName.roles or admin_role in userName.roles or manager_role in userName.roles or owner_role in userName.roles:
                msg.add_field(name=":warning: ", value="`You can't ban other staff!`")
                await client.say(embed=msg)
            else:
                time2 = time * 60
                user_id = userName.id
                if args == None:
                    msg.add_field(name=":hammer: Ban Hammer", value="`{} banned {} for {} minute(s)!`\n`Reason: ?`".format(author.display_name, userName.display_name, time))
                    await client.say(embed=msg)
                    await client.ban(userName)
                    await asyncio.sleep(float(time2))
                    banned_users = await client.get_bans(ctx.message.server)
                    user = discord.utils.get(banned_users,id=user_id)
                    await client.unban(ctx.message.server, user)
                    await client.say("```diff\n- The user with the following ID has been unbanned: {} ({} minute(s) are up!)\n```".format(user_id, time))
                else:
                    msg.add_field(name=":hammer: Ban Hammer", value="`{} banned {} for {} minute(s)!`\n`Reason: {}`".format(author.display_name, userName.display_name, time, args))
                    await client.say(embed=msg)
                    await client.ban(userName)
                    await asyncio.sleep(float(time2))
                    banned_users = await client.get_bans(ctx.message.server)
                    user = discord.utils.get(banned_users,id=user_id)
                    await client.unban(ctx.message.server, user)
                    await client.say("```diff\n- The user with the following ID has been unbanned: {} ({} minute(s) are up!)\n```".format(user_id, time))
    else:
        msg.add_field(name=":warning: ", value="`This command can only be used by Moderators, Admins, Co-Owners Owners!`")
        await client.say(embed=msg)
    print("============================================================")
    print("}tempban <user> <time> [reason]")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# }ban <user> [reason]
@client.command(pass_context=True)
async def ban(ctx, userName: discord.Member = None, *, args = None):
    helper_role = discord.utils.get(ctx.message.server.roles, name='Mods')
    mod_role = discord.utils.get(ctx.message.server.roles, name='Mods')
    admin_role = discord.utils.get(ctx.message.server.roles, name='Admins')
    manager_role = discord.utils.get(ctx.message.server.roles, name='Co-Owner')
    owner_role = discord.utils.get(ctx.message.server.roles, name='Owners')
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if mod_role in author.roles or admin_role in author.roles or manager_role in author.roles or owner_role in author.roles:
        if userName == None:
            msg.add_field(name=":warning: ", value="`Mike ban (user) (reason)`")
        elif helper_role in userName.roles or mod_role in userName.roles or admin_role in userName.roles or manager_role in userName.roles or owner_role in userName.roles:
            msg.add_field(name=":warning: ", value="`You can't ban other staff!`")
        elif args == None:
            msg.add_field(name=":hammer: Ban Hammer", value="`{} banned {}!`\n`Reason: ?`".format(author.display_name, userName.display_name))
            await client.ban(userName)
        else:
            msg.add_field(name=":hammer: Ban Hammer", value="`{} banned {}!`\n`Reason: {}`".format(author.display_name, userName.display_name, args))
            await client.ban(userName)
    else:
        msg.add_field(name=":warning: ", value="`This command can only be used by Moderators, Administrators, Co-Owners and Owners!`")
    await client.say(embed=msg)
    print("============================================================")
    print("}ban <user> [reason]")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# }unban <user id>
@client.command(pass_context=True)
async def unban(ctx, userID = None):
    mod_role = discord.utils.get(ctx.message.server.roles, name='Mods')
    admin_role = discord.utils.get(ctx.message.server.roles, name='Admins')
    manager_role = discord.utils.get(ctx.message.server.roles, name='Co-Owner')
    owner_role = discord.utils.get(ctx.message.server.roles, name='Owners')
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if mod_role in author.roles or admin_role in author.roles or manager_role in author.roles or owner_role in author.roles:
        if userID == None:
            msg.add_field(name=":warning: ", value="`Mike unban (user id)`")
        else:
            banned_users = await client.get_bans(ctx.message.server)
            user = discord.utils.get(banned_users,id=userID)
            if user is not None:
                await client.unban(ctx.message.server, user)
                msg.add_field(name=":tools: ", value="`{} unbanned the user with the following ID: {}!`".format(author.display_name, userID))
            else:
                msg.add_field(name=":warning: ", value="`The ID you specified is not banned! ID: {}`".format(userID))
    else:
        msg.add_field(name=":warning: ", value="`This command can only be used by Moderators, Administrators, Co-Owners and Owners!`")
    await client.say(embed=msg)
    print("============================================================")
    print("}unban <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# }idban <user id> [reason]
@client.command(pass_context=True)
async def idban(ctx, userID: int = None, *, args = None):
    manager_role = discord.utils.get(ctx.message.server.roles, name='Mods')
    owner_role = discord.utils.get(ctx.message.server.roles, name='Admins')
    author = ctx.message.author
    guild = ctx.message.server
    user = guild.get_member(userID)
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if manager_role in author.roles or owner_role in author.roles:
        if userID == None:
            msg.add_field(name=":warning: ", value="`Mike idban (user id) (reason)`")
        elif user == None and args is not None:
            msg.add_field(name=":tools: ", value="`{} ID-Banned the following ID: {}!`\n`Reason: {}`".format(author.display_name, userID, args))
            await client.http.ban(userID, guild.id, 0)
        elif user == None and args == None:
            msg.add_field(name=":tools: ", value="`{} ID-Banned the following ID: {}!`\n`Reason: ?`".format(author.display_name, userID))
            await client.http.ban(userID, guild.id, 0)
        else:
            msg.add_field(name=":warning: ", value="`Unknown error!`")
    else:
        msg.add_field(name=":warning: ", value="`This command can only be used by Mods and Admins!`")
    await client.say(embed=msg)
    print("============================================================")
    print("}idban <user id> [reason]")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# }help
client.remove_command('help')
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.add_field(name=":incoming_envelope: ", value="`You can see all commands in the #mike-commands channel!`")
    msg.set_footer(text=footer_text)
    await client.say(embed=msg)
    print("============================================================")
    print("}help")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# }ping
@client.command(pass_context=True)
async def ping(ctx):
    channel = ctx.message.channel
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.set_footer(text=footer_text)
    msg.title = ""
    t1 = time.perf_counter()
    await client.send_typing(channel)
    t2 = time.perf_counter()
    msg.add_field(name=":satellite: ", value="`Yes, I am here. No need to ping me.`\n`Ping: {}ms`".format(round((t2-t1)*1000)))
    await client.say(embed=msg)
    print("============================================================")
    print("}ping")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# %cookie <user> <number>
@client.command(pass_context=True)
async def cookie(ctx, userName: discord.Member = None, number: int = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None or number == None:
        msg.add_field(name=":warning: ", value="`Mike cookie (user) (number)`")
    else:
        if number > 100:
            msg.add_field(name=":warning: ", value="`You can't give over 100 cookies to someone! Save some for yourself!`")
        else:
            msg.add_field(name=":smiley: ", value="`{} gave {}` :cookie: `to {}!`\n`Be like {}!`".format(author.display_name, number, userName.display_name, author.display_name))
    await client.say(embed=msg)
    print("============================================================")
    print("}cookie <user> <number>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# %cake <user> <number>
@client.command(pass_context=True)
async def cake(ctx, userName: discord.Member = None, number: int = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None or number == None:
        msg.add_field(name=":warning: ", value="`Mike cake (user) (number)`")
    else:
        if number > 8:
            msg.add_field(name=":warning: ", value="`There are usually 8 slices in one cake, you trying to give them diabetes?!`")
        else:
            msg.add_field(name=":smiley: ", value="`{} gave {}` :cake: `to {}!`\n`Praise {}!`".format(author.display_name, number, userName.display_name, author.display_name))
    await client.say(embed=msg)
    print("============================================================")
    print("}cookie <user> <number>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
# %annoy <user> [text]
@client.command(pass_context=True)
async def annoy(ctx, userName: discord.Member = None, *, args = None):
    author = ctx.message.author
    msg = discord.Embed(colour=0xdb5000, description= "")
    msg.title = ""
    msg.set_footer(text=footer_text)
    if userName == None:
        msg.add_field(name=":warning: ", value="`Mike annoy (user) (text)`")
        await client.say(embed=msg)
    else:
        if args == None:
            msg.add_field(name=":drooling_face: ", value="`Sending a beautiful video to {}...`".format(userName.display_name))
            await client.say(embed=msg)
            await client.send_message(userName, "{}".format(random.choice(rickrolls)))
        else:
            msg.add_field(name=":drooling_face: ", value="`Sliding in {}'s DMs...`".format(userName.display_name))
            await client.say(embed=msg)
            await client.send_message(userName, "{}".format(args))
    print("============================================================")
    print("}rickroll <user>")
    print("{} ### {}".format(author, author.id))
    print("============================================================")
    
rickrolls = ["https://www.youtube.com/watch?v=V-_O7nl0Ii0",
             "https://www.youtube.com/watch?v=ID_L0aGI9bg",
             "https://www.youtube.com/watch?v=yBLdQ1a4-JI",
             "https://www.youtube.com/watch?v=6-HUgzYPm9g",
             "https://www.youtube.com/watch?v=Gc2u6AFImn8",
             "https://www.youtube.com/watch?v=4n7_Il1dft0",
             "https://www.youtube.com/watch?v=OL7B2z56ziQ",
             "https://www.youtube.com/watch?v=li7qFeHI5KM",
             "https://www.youtube.com/watch?v=wvWX-jWhLBI",
             "https://youtu.be/ByC8sRdL-Ro",
             "https://www.youtube.com/watch?v=HoWcnTsc5s8",
             "hi lol",
             "https://www.youtube.com/watch?v=E9DlT_DS0wA",
             "https://youtu.be/rp8hvyjZWHs",
             "https://www.youtube.com/watch?v=3HfnLwopb58"]
client.run(os.environ['BOT_TOKEN'])

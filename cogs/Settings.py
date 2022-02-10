import discord
from discord.ext import commands
import json
from utils import Paginator

async def enabled_cogs(ctx):
    with open("./database/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == ctx.guild.id:
            plugins = i['settings']['plugins']
    em = discord.Embed(title="Plugins:",description="These are all the plugins that have been enabled on your server", color=ctx.author.color)
    for key, value in plugins.items():
        if value == True:
            emoji = "Enabled ✅"
        else:
            emoji = "Disabled ❌"
        em.add_field(name=key, value=emoji)
    em.set_footer(text=f"Use {ctx.prefix}plugins to toggle plugins")
    return em

async def get_channels(self, ctx):
    with open("./database/db.json") as f:
        data = json.load(f)
    em = discord.Embed(title="Channels", color=ctx.author.color)
    em.set_footer(text="Use /set to set these")
    for i in data:
        if i['guild_id'] == ctx.guild.id:
            if i['counting_channel'] == None:
                counting="Not Set"
            else:
                channel = await self.client.fetch_channel(i['counting_channel'])
                counting = channel
            if i['welcome_channel'] == None:
                welcome="Not Set"
            else:
                channel = await self.client.fetch_channel(i['welcome_channel'])
                welcome = channel
            if i['log_channel'] == None:
                log="Not Set"
            else:
                channel = await self.client.fetch_channel(i['log_channel'])
                log = channel
            em.add_field(name="Counting:", value=counting)
            em.add_field(name="Welcome:", value=welcome)
            em.add_field(name="Log:", value=log)
    return em
        
async def autorole(self, ctx):
    with open("./database/db.json") as f:
        data = json.load(f)
    em = discord.Embed(title="Autorole", color=ctx.author.color)
    em.set_footer(text="Use ?autorole [@role] [all/bot] to set the autorole")
    for i in data:
        if i['guild_id'] == ctx.guild.id:
            autorole = i['autorole']
    if autorole['all'] == None:
        em.add_field(name="All", value="Not set")
    else:
        role = ctx.guild.get_role(autorole['all'])
        em.add_field(name="All", value=role.mention)
    if autorole['bot'] == None:
        em.add_field(name="Bot", value="Not set")
    else:
        role = ctx.guild.get_role(autorole['bot'])
        em.add_field(name="Bot", value=role.mention)
    return em

async def welcome_text(ctx):
    with open("./database/db.json") as f:
        data = json.load(f)
    em = discord.Embed(title="Welcome Text", color=ctx.author.color)
    em.set_footer(text="Use ?setwelcometext [text] to set the text")
    for i in data:
        if i['guild_id'] == ctx.guild.id:
            wt = i['welcome']['text_footer']
    em.add_field(name="Text:", value=wt)
    return em

async def autocalc(ctx):
  with open("./database/db.json") as f:
    data = json.load(f)
  for i in data:
    if i['guild_id'] == ctx.guild.id:
      autocalc = i['settings']['autocalc']
  if autocalc == True:
    status = "Enabled ✅"
  if autocalc == False:
    status = "Disabled ❌"
    
  em = discord.Embed(title='Auto Calculator', description=status, color=ctx.author.color)

  return em
  
class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="This command is used to show the settings for you discord server. You can use this command to quickly check all the current settings to know if you want to change it", extras={"category":"Settings"}, usage="settings", description="Shows the servers Why Bot settings")
    async def settings(self,ctx):
        plugins = await enabled_cogs(ctx)

        em = discord.Embed(title="Settings", description="Use the arrows to look throught the settings", color=ctx.author.color)
        
        prefix = discord.Embed(title = "Prefix", description=f"The prefix is `{ctx.prefix}`", color=ctx.author.color)
        prefix.set_footer(text=f"You can use {ctx.prefix}setprefix [prefix] to set the prefix")

        channels = await get_channels(self, ctx)
        autoroles = await autorole(self, ctx)
        welcometext = await welcome_text(ctx)
        auto_calc  = await autocalc(ctx)

        ems = [em, plugins, prefix, channels, autoroles, auto_calc, welcometext]
        view = Paginator(ctx=ctx, ems=ems)

        message = await ctx.send(embed=em, view=view)
        res = await view.wait()
        if res:
            for i in view.children:
                i.disabled = True
        return await message.edit(view=view)
    
    @commands.group(help="This command is used to enable/disable plugins for your server. You can stop certain categories from working on this server\nThe plugin name is case sensitive", extras={"category":"Settings"}, usage="plugins [enable/disable] [plugin name]", description="Enable/Disable Plugins for Why bot")
    async def plugins(self, ctx):
        if ctx.invoked_subcommand is None:
          em = discord.Embed(title="Plugins", description=f"Use `{ctx.prefix}plugins [enable/disable] [plugin name]`", color=ctx.author.color)
          em.add_field(name="Plugin List:", value="Counting\nModeration\nEconomy\nTextConvert\nSearch\nWelcome\nLeveling\nMusic\nOnping\nTicket\nMinecraft\nUtilities")
          em.set_footer(text="This command is case sensitive so please use capital letters")
          await ctx.send(embed=em)
    
    @plugins.group()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx, plugin:str):
        plist = ["Counting","Moderation","Economy","TextConvert","Search","Welcome","Leveling","Music","Onping","Ticket","Minecraft","Utilities", "Fun"]
        if plugin not in plist:
            return await ctx.send(f"Plugin not found, use `{ctx.prefix}plugins` for a list of them")
        with open('./database/db.json') as f:
            data = json.load(f)
        for i in data:
            if i['guild_id'] == ctx.guild.id:
                i['settings']['plugins'][plugin] = True

        with open("./database/db.json", 'w') as f:
            json.dump(data, f, indent=4)
        
        await ctx.send(f"{plugin} has been enabled")


    @plugins.group()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx, plugin:str):
        plist = ["Counting","Moderation","Economy","TextConvert","Search","Welcome","Leveling","Music","Onping","Ticket","Minecraft","Utilities"]
        if plugin not in plist:
            return await ctx.send(f"Plugin not found, use `{ctx.prefix}plugins` for a list of them")
        with open('./database/db.json') as f:
            data = json.load(f)
        for i in data:
            if i['guild_id'] == ctx.guild.id:
                i['settings']['plugins'][plugin] = False

        with open("./database/db.json", 'w') as f:
            json.dump(data, f, indent=4)
        
        await ctx.send(f"{plugin} has been disabled")


    @commands.command(help="This command is used to set the prefix for the server. Default prefix is ?", extras={"category":"Settings"}, usage="setprefix [prefix]", description="Sets the server prefix")
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, pref: str):
        with open(f'./database/db.json') as f:
            data = json.load(f)
        for i in data:
            if i["guild_id"] == ctx.guild.id:
                i["prefix"] = pref
        with open(f'./database/db.json', 'w') as f:
            json.dump(data, f)
        await ctx.send(embed=discord.Embed(title=f"Prefix has been set to `{pref}`", color=ctx.author.color))

    @commands.command(help="This command turns on autocalc for the server.\nAuto calc basicaly autocalculates any thing you type. For example in chat you type\n1 + 1\nin chat, The bot will reply 2", extras={"category":"Settings"}, usage="autocalc [True/false]", description="Toggles autocalc for this server")
    @commands.has_permissions(administrator=True)
    async def autocalc(self, ctx, ena):
        with open(f'./database/db.json') as f:
            data = json.load(f)
        for i in data:
            if i["guild_id"] == ctx.guild.id:
                if ena.lower() == "true":
                  status = "Enabled ✅"
                  i["settings"]['autocalc'] = True
                elif ena.lower() == "false":
                  i["settings"]['autocalc'] = False
                  status = "Disabled ❌"
                else:
                  await ctx.send("Invalid option. Only `true` or `false`")
        with open(f'./database/db.json', 'w') as f:
            json.dump(data, f)
        await ctx.send(embed=discord.Embed(title=f"Autocalc is {status}", color=ctx.author.color))
    
def setup(client):
    client.add_cog(Settings(client))
import datetime
import random
import os
import praw
import discord
from discord.ext import commands
from commands.functions import log, get_author, get_prefix_string, get_botc, get_colour, get_memec, redditnsfwcheck\
    , get_memes, get_checkedmemes, writejson, readjson


class fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def würfel(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        value = random.randint(1, 6)
        if name == botchannel or botchannel == "None":
            embed = discord.Embed(title='**Würfel**', colour=get_colour(ctx.message))
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/645276319311200286/803550939112931378/wurfelv2.png')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎', value='Du hast eine ```' + str(value) + '``` gewürfelt!', inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(user) + ' hat eine ' + str(value) + ' gewürfelt.'
                , id= ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                get_prefix_string(ctx.message) + 'würfel im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx, redditname=None):
        if redditname is None:
            redditname = get_memes(ctx.guild.id)
        global submission
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        memechannel = get_memec(ctx.message)
        path = os.path.join('data', 'verifiedmemes', 'memes.json')
        if name == memechannel or memechannel == "None":
            try:
                reddit = praw.Reddit(client_id='JiHoJGCPBC9vlg',
                                     client_secret='egXFBVdIx7ucn9_6tji18kyLClWCIA',
                                     user_agent='Test Meme Bot',
                                     check_for_async=False)
                memes_submissions = reddit.subreddit(redditname).hot()
                post_to_pick = random.randint(1, 100)
                if redditname != get_memes(ctx.guild.id) and get_checkedmemes(redditname) is False:
                    if redditname in readjson("failed", path) or redditnsfwcheck(redditname):
                        embed = discord.Embed(title="**Fehler**",
                                          description=f"Der angegebene Reddit **{redditname}** enthält nicht "
                                                      "zulässigen Inhalt.",
                                          color=get_colour(ctx.message))
                        embed.set_thumbnail(
                        url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                            '.png?width=676&height=676')
                        embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                        get_prefix_string(message=ctx.message)),
                                     icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                              '/803322491480178739/winging-easy.png?width=676&height=676')
                        await ctx.send(embed=embed)
                        log(f"{time}: Der Spieler {user} hat beim Befehl"
                        f"'{get_prefix_string(ctx.message)}meme ein ungültiges Argument eingegeben.", ctx.guild.id)
                        return
                    else:
                        with open(path, "r+") as f:
                            data = json.load(f)
                        data["verified"].append(redditname)
                        json.dump(data, f, indent=4)
                for i in range(0, post_to_pick):
                    submission = next(x for x in memes_submissions if not x.stickied)
                embed = discord.Embed(title=f"**{submission.title}**", colour=get_colour(ctx.message))
                embed.set_image(url=submission.url)
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' +
                                get_prefix_string(message=ctx.message), icon_url='https://media.discordapp.net/'
                                'attachments/645276319311200286'
                                '/803322491480178739/winging-easy.png?width=676&height=676')
                await ctx.send(embed=embed)
                log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +get_prefix_string(ctx.message) +
                    'meme benutzt!', id=ctx.guild.id)
                return
            except Exception:
                embed = discord.Embed(title="**Fehler**",
                                      description=f"Beim Reddit **{redditname}** ist wohl etwas schiefgelaufen. "
                                      "Das könnte z.B. bedeuten das der Reddit nicht existiert oder das der Reddit "
                                      "aufgrund von zu vielen Anfragen nicht automatisch auf NSFW Content überprüft "
                                      "wurde. Sollte letzteres zutreffen, warte ein paar Minuten!",
                                      color=get_colour(ctx.message))
                embed.set_thumbnail(
                    url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                        '.png?width=676&height=676')
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                    get_prefix_string(message=ctx.message)),
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                          '/803322491480178739/winging-easy.png?width=676&height=676')
                await ctx.send(embed=embed)
                log(f"{time}: Der Spieler {user} hat beim Befehl"
                    f"'{get_prefix_string(ctx.message)}meme ein ungültiges Argument eingegeben.", ctx.guild.id)
                raise Exception

        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                get_prefix_string(ctx.message) + 'meme im Channel #' + str(memechannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(memechannel),
                           delete_after=3)
            await msg2.delete()

    @meme.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="**Cooldown**", description=f"Versuch es nochmal in {error.retry_after:.2f}s.",
                               color=get_colour(ctx.message))
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                    '.png?width=676&height=676')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                get_prefix_string(message=ctx.message)),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                      '/803322491480178739/winging-easy.png?width=676&height=676')
            await ctx.send(embed=embed)
            log(f"{time}: Der Spieler {user} hat trotz eines Cooldowns versucht den Befehl'"
                f"'{get_prefix_string(ctx.message)}meme im Kanal #{ctx.channel.name} zu nutzen.", ctx.guild.id)

    @commands.command()
    async def ssp(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        if name == botchannel or botchannel == "None":
            embed = discord.Embed(title='**Schere Stein Papier**', description='Lass uns "Schere Stein Papier" spielen!'
                                  'Nutze dazu die Commands:', colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name=
                get_prefix_string(ctx.message) + 'schere', value='Spiele die Schere aus!', inline=False)
            embed.add_field(name=get_prefix_string(ctx.message) + 'stein', value='Spiele den Stein aus!', inline=False)
            embed.add_field(name=get_prefix_string(ctx.message) + 'papier', value='Spiele das Papier aus!'
                            , inline=False)
            await ctx.send(embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                get_prefix_string(ctx.message) + 'ssp benutzt!', id=ctx.guild.id)

        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                get_prefix_string(ctx.message) + 'ssp im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @commands.command()
    async def schere(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        if name == botchannel or botchannel == "None":
            schere = ['Ich hatte auch die Schere, Unentschieden!',
                      'Du hast gewonnen, ich hatte mich für das Papier entschieden!',
                      'Guter Versuch, aber ich habe aber mit dem Stein gewonnen!']
            schererandom = random.choice(schere)
            embed = discord.Embed(title='**Schere Stein Papier**', colour=get_colour(ctx.message))
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/645276319311200286/803373963316953158/stp.png')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎', value=str(schererandom), inline=False)
            await ctx.send(embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                get_prefix_string(ctx.message) + 'schere benutzt!', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                get_prefix_string(ctx.message) + 'schere im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @commands.command()
    async def stein(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        if name == botchannel or botchannel == "None":
            stein = ['Ich hatte auch den Stein, Unentschieden!',
                     'Du hast gewonnen, ich hatte mich für die Schere entschieden!',
                     'Guter Versuch, aber ich habe aber mit dem Papier gewonnen!']
            steinrandom = random.choice(stein)
            embed = discord.Embed(title='**Schere Stein Papier**', colour=get_colour(ctx.message))
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/645276319311200286/803373963316953158/stp.png')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎', value=str(steinrandom), inline=False)
            await ctx.send(embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                get_prefix_string(ctx.message) + 'stein benutzt!', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                get_prefix_string(ctx.message) + 'stein im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @commands.command()
    async def papier(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        if name == botchannel or botchannel == "None":
            papier = ['Ich hatte auch das Papier, Unentschieden!',
                      'Du hast gewonnen, ich hatte mich für den Stein entschieden!',
                      'Guter Versuch, aber ich habe aber mit der Schere gewonnen! Papier ist leider nur so dünn...']
            papierrandom = random.choice(papier)
            embed = discord.Embed(title='**Schere Stein Papier**', colour=get_colour(ctx.message))
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/645276319311200286/803373963316953158/stp.png')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎', value=str(papierrandom), inline=False)
            await ctx.send(embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                get_prefix_string(ctx.message) + 'papier benutzt!', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                get_prefix_string(ctx.message) + 'papier im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()


########################################################################################################################


def setup(bot):
    bot.add_cog(fun(bot))
# bot.py
from abc import abstractmethod
from easybetsregister import *
from registercentral import *
import random
import datetime


class SportsBetting():
    """
    Interface for slots machines
    """

    @abstractmethod
    def __init__(self, bot):
        self.bot = bot
        pass

    @abstractmethod
    def bought_confirmation_embed(self, arr_of_rows, money_won, balance):
        """ Creates the embed that the bot will print """
        pass

    @abstractmethod
    def won_embed(self, moneywon, gamename, original, new):
        """ Creates the embed that the bot will print """
        pass

    @abstractmethod
    def pay_for_bet(self, ctx, *args):
        """ Takes payment from the player for the spin """
        pass

    @abstractmethod
    def create_sports_bet(self, arr_of_rows, money_won, balance):
        """ Creates the embed that the bot will print """
        pass

    @abstractmethod
    def activate_payout(self, payout_rules):
        """ Pays the player if they won """
        pass

    @abstractmethod
    def pick_winners(self, ctx, *args):
        """ Runs one spin """
        pass


class SportsBot(commands.Cog, SportsBetting):

    def __init__(self, bot, predictions, winner_channel_id, minimum_bet, maximum_bet):
        self.bot = bot
        self.predictions = predictions
        self.winner_channel_id = winner_channel_id
        self.minimum_bet = minimum_bet
        self.maximum_bet = maximum_bet
        pass

    def sports_game_statuses_sub(self, embed, gamelist):
        """ Creates the embed that the bot will print """
        for sports in gamelist:
            matchname = sports[0]
            teamone = sports[1]
            teamtwo = sports[2]
            firsthalf = "{}: T1: {} vs T2: {}".format(matchname, teamone, teamtwo)
            teamoneodds = sports[6]
            teamtwoodds = sports[7]
            drawodds = sports[9]
            secondhalf = "T1 Odds: {} T2 Odds: {} Draw Odds: {}".format(teamoneodds, teamtwoodds, drawodds)
            embed.add_field(name=firsthalf, value=secondhalf, inline=True)
        return embed

    def sports_game_statuses(self):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="Sports Games Betting Sessions")
        gameslist = grab_sports_games()
        embed = self.sports_game_statuses_sub(embed, gameslist)
        return embed

    def win_channel_embed(self, moneywon, gamename):
        embed = discord.Embed(title=":partying_face: Easy Payday!!! :partying_face:",
                              description="Somebody has won {} from betting in {}!".format(moneywon, gamename),
                              color=0xf2e12c)
        return embed


    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_users_role_sportsgames(self, ctx, role_name, channel_id, server_id):
        try:
            channel = self.bot.get_channel(channel_id)
            role = discord.utils.get(channel.guild.roles, name=role_name)
            guild = self.bot.get_guild(server_id)
            member = await guild.fetch_member(ctx.author.id)
            if role in member.roles:
                return True
            else:
                return False
        except Exception as e:
            await ctx.send(e)

    def sportsgame_created_notif(self, game):
        matchname = game[0]
        teamone = game[1]
        teamtwo = game[2]
        firsthalf = "{}: T1: {} vs T2: {}".format(matchname, teamone, teamtwo)
        teamoneodds = game[6]
        teamtwoodds = game[7]
        drawodds = game[9]
        secondhalf = "T1 Odds: {} T2 Odds: {} Draw Odds: {}".format(teamoneodds, teamtwoodds, drawodds)
        embed = discord.Embed(title="Sports Betting", description="", color=0xd5c144)
        embed.add_field(name=firsthalf, value=secondhalf, inline=True)
        return embed

    def bought_confirmation_embed(self, cost, original, new):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="Bet Cost", description="", color=0xd5c144)
        embed.add_field(name="Cost $", value=cost, inline=True)
        embed.add_field(name="Original Balance", value=original, inline=True)
        embed.add_field(name="New Balance", value=new, inline=False)
        return embed

    def won_embed(self, moneywon, gamename, original, new):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="Winner! Winner!",
                              description="You won {} from betting in {}!".format(moneywon, gamename),
                              color=0xf2e12c)
        embed.add_field(name="Original Balance", value=original, inline=True)
        embed.add_field(name="New Balance", value=new, inline=False)
        return embed
        pass

    @commands.command(name='ssg')
    async def display_current_sportsgames(self, ctx):
        embed = self.sports_game_statuses()
        await ctx.send(embed=embed)

    @commands.command(name='msb')
    async def pay_for_bet(self, ctx, *args):
        try:
            if await self.check_users_role_sportsgames(ctx, 'Baller', 979584371461877834, 979584371013079090) == True:
                charname = check_my_active_player(ctx.author.id)
                if charname:
                    if check_charexists(charname):
                        if len(args) == 3:
                            matchgame = args[0]
                            prediction = args[1]
                            if prediction in self.predictions:
                                amount = int(args[2])
                                discordid = ctx.author.id
                                print(type(self.maximum_bet), type(self.minimum_bet))
                                if self.minimum_bet <= amount and amount <= self.maximum_bet:
                                    if check_enough_balance(charname, 'characteraccs', 'balance',
                                                            amount):
                                        if check_sportsgame_exists(matchgame):
                                            if check_sportsgameoutcome_status(matchgame, prediction) and check_sportsgame_status(matchgame):
                                                change_balance(charname, amount, False)
                                                add_sportsgame_bet(discordid, charname, matchgame, prediction, amount)
                                                current_balance = grab_char_balance(charname)
                                                embed = self.bought_confirmation_embed(amount, int(current_balance) +
                                                                        int(amount), int(current_balance))
                                                await ctx.send(embed=embed)
                                            else:
                                                await ctx.send("Betting on {} for session {} has been disabled!".format(prediction, matchgame))
                                        else:
                                            await ctx.send("Match does not exist.")
                                    else:
                                        await ctx.send("You don't have enough money!")
                                else:
                                    await ctx.send("Bet must be between ${} and ${}!".format(self.minimum_bet, self.maximum_bet))
                            else:
                                await ctx.send("Prediction has to be either: t1, t2, or draw!")
                        else:
                            await ctx.send("Missing arguments $mb matchgame prediction amount")
                    else:
                        await ctx.send("Character doesn't exist!")
                else:
                    await ctx.send("You have not set an active character! $sc firstname lastname")
            else:
                await ctx.send("You are not a verified member, register first!")
        except Exception as e:
            print(e)
            pass

    @commands.command(name='csg')
    @commands.has_any_role('EasyBet', 'Admin')
    async def cancel_match(self, ctx, *args):
        try:
            if len(args) == 1:
                matchname = args[0]
                if check_sportsgame_exists(matchname):
                    players = grab_sportsgame_players(matchname)
                    for player in players:
                        print("PLAYER: ", player)
                        player_name = player[0]
                        player_stake = player[1]
                        change_balance(player_name, player_stake, True)
                        embed = discord.Embed(title="SPORTS BET REFUNDED",
                                              description="You got refunded {} from betting in {}!".format(player_stake, matchname),
                                              color=0xf2e12c)
                        await ctx.send(embed=embed)
                    clear_sportsgames_bets(matchname)
                else:
                    await ctx.send("Match doesn't exist!")
            else:
                await ctx.send("Missing arguments $pw matchname outcome")
        except Exception as e:
            print(e)

    @commands.command(name='psgw')
    @commands.has_any_role('EasyBet', 'Admin')
    async def pick_winners(self, ctx, *args):
        try:
            if len(args) == 2:
                matchname = args[0]
                outcome = args[1]
                winners = grab_sportsgame_winners(matchname, outcome)
                odd_multi = grab_sportsgame_outcomeodd(matchname, outcome)
                for winner in winners:
                    winner_name = winner[0]
                    winner_stake = winner[1]
                    won_money = winner_stake * float(odd_multi)
                    won_money = int(won_money)
                    change_balance(winner_name, won_money, True)
                    current_balance = grab_char_balance(winner_name)
                    embed = self.won_embed(won_money, matchname, current_balance - won_money, current_balance)
                    user = await self.bot.fetch_user(grab_discordid_from_sportsgame(winner_name, matchname)[0][0])
                    await user.send(embed=embed)
                    channelembed = self.win_channel_embed(won_money, matchname)
                    channel = self.bot.get_channel(self.winner_channel_id)
                    await channel.send(embed=channelembed)
                clear_sportsgames_bets(matchname)
            else:
                await ctx.send("Missing arguments $pw matchname outcome")
        except Exception as e:
            print(e)

    @commands.command(name='csb')
    @commands.has_any_role('EasyBet', 'Admin')
    async def create_sports_bet(self, ctx, *args):
        try:
            if len(args) == 9:
                matchname = args[0]
                t1_name = args[1]
                t1_odd = float(args[2])
                t2_name = args[3]
                t2_odd = float(args[4])
                t1_status = args[5]
                t2_status = args[6]
                draw_status = args[7]
                draw_odd = float(args[8])
                if not check_sportsgame_exists(matchname):
                    add_into_sportsgames(matchname, t1_name, t1_odd, t2_name, t2_odd, t1_status, t2_status, draw_status,
                                         draw_odd)
                    channelembed = self.sportsgame_created_notif([matchname, t1_name, t2_name, 1, t1_status, t2_status, t1_odd, t2_odd, draw_status, draw_odd])
                    channel = self.bot.get_channel(983826023898546176)
                    await channel.send(embed=channelembed)
                else:
                    await ctx.send("Game already exists!")
            else:
                await ctx.send(
                    "Missing arguments $csb matchname, t1_name, t1_odd, t2_name, t2_odd, t1_status, t2_status, draw_status, draw_odd")
        except Exception as e:
            await ctx.send(e)

    @commands.command(name='csbm')
    @commands.has_any_role('EasyBet', 'Admin')
    async def count_sportsbet_money(self, ctx, *args):
        try:
            if len(args) == 2:
                matchname = args[0]
                outcome = args[1]
                sum = count_sportsgamesbet(matchname, outcome)
                if sum is not None:
                    await ctx.send("{} has been placed on {} for game {}".format(sum, outcome, matchname))
                else:
                    await ctx.send("No bets placed for {} in game {}!".format(outcome, matchname))
            else:
                await ctx.send(
                    "Missing arguments $csbm matchname outcome")
        except Exception as e:
            await ctx.send(e)

    @commands.command(name='dsg')
    @commands.has_any_role('EasyBet', 'Admin')
    async def disable_sports_game(self, ctx, *args):
        try:
            if len(args) == 1:
                matchname = args[0]
                update_sportsgames_status(matchname, 0)
                await ctx.send("{} has been disabled, no more bets!".format(matchname))
            else:
                await ctx.send(
                    "Missing arguments $edsg matchname")
        except Exception as e:
            ctx.send(e)

    @commands.command(name='esg')
    @commands.has_any_role('EasyBet', 'Admin')
    async def enable_sports_game(self, ctx, *args):
        try:
            if len(args) == 1:
                matchname = args[0]
                update_sportsgames_status(matchname, 1)
                await ctx.send("{} has been enabled!".format(matchname))
            else:
                await ctx.send(
                    "Missing arguments $edsg matchname")
        except Exception as e:
            ctx.send(e)

    @commands.command(name='dsg2')
    @commands.has_any_role('EasyBet', 'Admin')
    async def disable_sports_game_outcome(self, ctx, *args):
        try:
            if len(args) == 2:
                matchname = args[0]
                outcome = args[1]
                update_sportsgames_outcomestatus(matchname, outcome, 0)
                await ctx.send("{}'s {} has been disabled, no more bets!".format(matchname, outcome))
            else:
                await ctx.send(
                    "Missing arguments $edsg2 matchname outcome")
        except Exception as e:
            await ctx.send(e)

    @commands.command(name='esg2')
    @commands.has_any_role('EasyBet', 'Admin')
    async def enable_sports_game_outcome(self, ctx, *args):
        try:
            if len(args) == 2:
                matchname = args[0]
                outcome = args[1]
                update_sportsgames_outcomestatus(matchname, outcome, 1)
                await ctx.send("{}'s {} has been enabled, no more bets!".format(matchname, outcome))
            else:
                await ctx.send(
                    "Missing arguments $edsg2 matchname outcome")
        except Exception as e:
            await ctx.send(e)

async def setup(bot):
    print("Adding Sports Bot!")
    predictions = ["t1", "t2", "draw"]
    winner_channel = 982103854025945118
    await bot.add_cog(SportsBot(bot, predictions, winner_channel, 100, 200))
    print("Added Sports Bot!")

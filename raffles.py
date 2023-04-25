# bot.py
from abc import abstractmethod
from easybetsregister import *
from registercentral import *
import random
import datetime


class Raffles():
    """ Interface for slots machines """

    @abstractmethod
    def __init__(self, bot):
        pass

    @abstractmethod
    def bought_confirmation_embed(self, arr_of_rows, money_won, balance):
        """ Creates the embed that the bot will print """
        pass

    @abstractmethod
    def won_embed(self, arr_of_rows, money_won, balance):
        """ Creates the embed that the bot will print """
        pass

    @abstractmethod
    def win_channel_embed(self, arr_of_rows, money_won, balance):
        """ Creates the embed that the bot will print """
        pass

    @abstractmethod
    def pay_for_ticket(self):
        """ Takes payment from the player for the spin """
        pass

    @abstractmethod
    def create_big_raffle(self, arr_of_rows, money_won, balance):
        """ Creates the embed that the bot will print """
        pass

    @abstractmethod
    def activate_payout(self, payout_rules):
        """ Pays the player if they won """
        pass

    @abstractmethod
    def pick_winner(self, ctx, *args):
        """ Runs one spin """
        pass

class RafflesRobot(commands.Cog, Raffles):

    def __init__(self, bot, games, winner_channel_id):
        self.bot = bot
        self.raffle_games = games
        self.winner_channel_id = winner_channel_id
        pass

    def bought_confirmation_embed(self, cost, original, new):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="Ticket Cost", description="", color=0xd5c144)
        embed.add_field(name="Cost $", value=cost, inline=True)
        embed.add_field(name="Original Balance", value=original, inline=True)
        embed.add_field(name="New Balance", value=new, inline=False)
        return embed

    def raffle_game_statuses_sub(self, embed, gamelist):
        """ Creates the embed that the bot will print """
        for raffle in gamelist:
            rafflegame = raffle[0]
            maxtickets = raffle[1]
            ticketprice = raffle[2]
            counttickets = count_rafflegame_tickets(rafflegame)
            if counttickets is not None:
                ticketsleft = maxtickets - count_rafflegame_tickets(rafflegame)
            else:
                ticketsleft = maxtickets
            embed.add_field(name=rafflegame, value="{} tickets left ${} each".format(ticketsleft, ticketprice), inline=True)
        return embed

    def raffle_game_statuses(self):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="Raffle Royale Game Statuses")
        gameslist = grab_raffle_games()
        embed = self.raffle_game_statuses_sub(embed, gameslist)
        return embed

    @commands.command(name='rgs')
    async def display_raffle_games(self, ctx):
        gameslist = grab_raffle_games()
        embed = self.raffle_game_statuses()
        await ctx.send(embed=embed)

    def won_embed(self, moneywon, gamename, original, new, servicefee):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="Only one man was left standing...",
                              description="You won {} from {}!".format(moneywon, gamename),
                              color=0xf2e12c)
        embed.add_field(name="Service Fee", value=servicefee, inline=False)
        embed.add_field(name="Original Balance", value=original, inline=True)
        embed.add_field(name="New Balance", value=new, inline=False)
        return embed

    def lost_embed(self, gamename):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="Only one man was left standing...",
                              description="You unfortunately lost in {}, better luck next time!".format(gamename),
                              color=0xf2e12c)
        return embed

    def win_channel_embed(self, moneywon, gamename):
        embed = discord.Embed(title=":partying_face: Easy Payday!!! :partying_face:",
                              description="Somebody has won {} from {}!".format(moneywon, gamename),
                              color=0xf2e12c)
        return embed

    def take_payment(self, charname, amount_to_withdraw):
        """ Takes payment from the player for the roll """
        change_balance(charname, amount_to_withdraw, False)

    def activate_payout(self, charname, money_won):
        """ Pays the player if they won """
        # print("MONEY WON: ", money_won)
        change_balance(charname, money_won, True)

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def pick_winner(self, ctx, rafflegame):
        results = pick_raffle_winner(rafflegame)
        return random.choice(results)[0]
        pass

    @commands.command(name='cgt')
    async def clear_game_ticks(self, ctx, *args):
        clear_game_tickets(args[0])

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_users_role_raffles(self, ctx, role_name, channel_id, server_id):
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

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def send_winner_message(self, players, winner, rafflegame, untaxed, taxedprofit, fee):
        for player in players:
            if winner == player[0]:
                current_balance = grab_char_balance(player[0])
                user = await self.bot.fetch_user(player[1])
                wonmsg = self.won_embed(untaxed, rafflegame, current_balance, current_balance + taxedprofit, fee)
                await user.send(embed=wonmsg)

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def send_losers_message(self, players, winner, rafflegame):
        for player in players:
            if winner != player[0]:
                user = await self.bot.fetch_user(player[1])
                lostmsg = self.lost_embed(rafflegame)
                await user.send(embed=lostmsg)

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def buy_tickets_sub(self, ctx, rafflegame, ticketamount, charname, taxedprofit, fee, max_tickets):
        ticket_price = check_ticket_price(rafflegame)
        amount_to_withdraw = ticketamount * ticket_price
        # print("WITHDRAW: ", amount_to_withdraw)
        self.take_payment(charname, amount_to_withdraw)
        add_ticket_purchase(ctx.author.id, charname, ticketamount, rafflegame)
        current_balance = grab_char_balance(charname)
        buyconfirm = self.bought_confirmation_embed(amount_to_withdraw, int(current_balance) +
                                                    int(amount_to_withdraw), int(current_balance))
        await ctx.send(embed=buyconfirm)
        if check_raffle_status(rafflegame) == True:
            winner = await self.pick_winner(ctx, rafflegame)
            # print("THE WINNER SHOULD BE!!! {}".format(winner))
            players = grab_players_from_game(rafflegame)
            # print("THE TICKET PRICE IS!!! {}".format(ticket_price))
            untaxed = ticket_price * max_tickets
            if winner == charname:
                wonmsg = self.won_embed(untaxed, rafflegame, current_balance, (current_balance + taxedprofit),
                                        fee * max_tickets)
                await ctx.send(embed=wonmsg)
                await self.send_losers_message(players, winner, rafflegame)
            else:
                await self.send_winner_message(players, winner, rafflegame, untaxed, taxedprofit, fee * max_tickets)
                await self.send_losers_message(players, winner, rafflegame)
            self.activate_payout(winner, taxedprofit)
            channelmsg = self.win_channel_embed(ticket_price * max_tickets, rafflegame)
            channel = self.bot.get_channel(self.winner_channel_id)
            await channel.send(embed=channelmsg)
            date = datetime.datetime.now()
            add_into_profitlogs(winner, ticket_price * 0.10, rafflegame, date)
            clear_game_tickets(rafflegame)

    @commands.command(name='brt')
    async def buy_tickets(self, ctx, *args):
        try:
            if await self.check_users_role_raffles(ctx, 'Baller', 979584371461877834, 979584371013079090) == True:
                if check_game_state('Raffles'):
                    if len(args) == 1:
                        rafflegame = args[0]
                        game_status = check_raffle_status(rafflegame)
                        # tickets_left = check_tickets_left(rafflegame)
                        if not game_status:
                            # print("GAME STATUS IS: ", game_status)
                            if rafflegame in self.raffle_games:
                                    charname = check_my_active_player(ctx.author.id)
                                    if charname:
                                        if not check_asset_transfer(ctx.author.id, rafflegame):
                                            if check_charexists(charname):
                                                ticket_price = check_ticket_price(rafflegame)
                                                amount_to_withdraw = ticket_price
                                                if check_enough_balance(charname, 'characteraccs', 'balance',
                                                                                        amount_to_withdraw):
                                                    max_tickets = grab_max_tickets_from_game(rafflegame)
                                                    fee = ticket_price * 0.10
                                                    money_won = (ticket_price - fee) * max_tickets
                                                    await self.buy_tickets_sub(ctx, rafflegame, 1, charname,
                                                                                   money_won, fee, max_tickets)
                                                else:
                                                    await ctx.send("You don't have enough money!")
                                            else:
                                                await ctx.send("Character doesn't exist!")
                                        else:
                                            await ctx.send("You already have another character invested in this game! "
                                                               "No asset transfering!!!")
                                    else:
                                        await ctx.send("You have not set an active character! $sc firstname lastname")
                            else:
                                await ctx.send("Raffle game not recognized!")
                        else:
                            await ctx.send("No more available tickets!")
                    else:
                        await ctx.send("Missing arguments $brt rafflegame")
                else:
                    await ctx.send("Game has been disabled!")
            else:
                await ctx.send("You are not a verified member, register first!")
        except Exception as e:
            print(e)

    def create_big_raffle(self, arr_of_rows, money_won, balance):
        pass

async def setup(bot):
    raffle_games = ["duel1", "duel2", "duel3", "br1", "br2", "br3"]
    print("Adding raffle bot!")
    await bot.add_cog(RafflesRobot(bot, raffle_games, 982103854025945118))
    print("Added raffle bot!")

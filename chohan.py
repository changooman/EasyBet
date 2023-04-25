# bot.py
from abc import ABC, abstractmethod
from random import randrange

from discord import app_commands

from easybetsregister import *
from registercentral import *
import datetime

class DiceGame():
    """ Interface for slots machines """

    @abstractmethod
    def __init__(self, bot, description, emoji_theme, payout_rules, num_of_rows, slots_each_row, lowest_roll, highest_roll,
                 stake_tiers, prediction_choices, max_spins):
        self.bot = bot
        self.description = description
        self.emoji_theme = emoji_theme
        self.payout_rules = payout_rules
        self.num_of_rows = num_of_rows
        self.slots_each_row = slots_each_row
        self.lowest_roll = lowest_roll
        self.highest_roll = highest_roll
        self.stake_tiers = stake_tiers
        self.max_spins = max_spins
        self.prediction_choices = prediction_choices
        pass

    @abstractmethod
    def num_to_emojis(self, num_row, emoji_theme):
        """ Takes an array of numbers and converts them to emoji code """
        pass

    @abstractmethod
    def assemble_all_emoji_row(self, arr_of_rows, embed):
        """ Runs through the given list of rows and turns them into their respective emoji version"""
        pass

    @abstractmethod
    def create_embed(self, arr_of_rows, money_won, balance):
        """ Creates the embed that the bot will print """
        pass

    @abstractmethod
    def check_win(self, all_rows):
        """ Checks if the player won their spin """
        pass

    @abstractmethod
    def pay_for_roll(self):
        """ Takes payment from the player for the spin """
        pass

    @abstractmethod
    def activate_payout(self, payout_rules):
        """ Pays the player if they won """
        pass

    @abstractmethod
    def format_stake_tier(self, stake_tiers):
        """ Formats the stake tiers into a neat string for printing """
        pass

    @abstractmethod
    def sub_roll(self, ctx, stake_amount, charname):
        pass

    @abstractmethod
    def roll_die(self, ctx, *args):
        """ Runs one spin """
        pass

class ChoHan(commands.Cog, DiceGame):

    def __init__(self, bot, description, emoji_theme, payout_rules, num_of_rows, slots_each_row, lowest_roll,
                 highest_roll,
                 stake_tiers, prediction_choices, max_spins):
        self.bot = bot
        self.description = description
        self.emoji_theme = emoji_theme
        self.payout_rules = payout_rules
        self.num_of_rows = num_of_rows
        self.slots_each_row = slots_each_row
        self.lowest_roll = lowest_roll
        self.highest_roll = highest_roll
        self.stake_tiers = stake_tiers
        self.max_spins = max_spins
        self.winner_channel = 982103854025945118
        self.prediction_choices = prediction_choices

    def num_to_emojis(self, num_row, emoji_theme):
        """ Takes an array of numbers and converts them to emoji code """
        emoji_string = ''
        for num in num_row:
            emoji_result = emoji_theme[num]
            emoji_string += emoji_result
        return emoji_string

    def assemble_all_emoji_row(self, arr_of_rows, embed):
        """ Runs through the given list of rows and turns them into their respective emoji version """
        for arr in arr_of_rows:
            emoji_set = self.num_to_emojis(arr, self.emoji_theme)
            embed.add_field(name="Row", value=emoji_set, inline=False)
        return embed

    def spin_embed(self, cost, original, new):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="Roll Cost", description="", color=0xd5c144)
        embed.add_field(name="Cost $", value=cost, inline=True)
        embed.add_field(name="Original Balance", value=original, inline=True)
        embed.add_field(name="New Balance", value=new, inline=False)
        return embed

    def create_embed(self, arr_of_rows, money_won, balance):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="CHO HAN", description="", color=0xd5c144)
        embed.set_author(name="Lucky Buddha", icon_url="https://i.imgur.com/YYBursK.png")
        new_embed = self.assemble_all_emoji_row(arr_of_rows, embed)
        new_embed.add_field(name="Won", value=money_won, inline=True)
        new_embed.add_field(name="Balance", value=balance, inline=False)
        return embed

    def check_win(self, all_rows, prediction):
        """ Checks if the player won their spin """
        for row in all_rows:
            # if 6 in row:
            #     return 6
            # if 1 in row:
            #     return 1
            roll_total = sum(row)
            if prediction == "double":
                return (len(set(row)) == 1)
            elif prediction == "lucky8":
                return (roll_total==8)
            elif prediction == "even":
                return (roll_total%2==0)
            elif prediction == "odd":
                return (roll_total%2!=0)
            else:
                return False
        return False

    def pay_for_roll(self, charname, amount_to_withdraw):
        """ Takes payment from the player for the spin """
        change_balance(charname, amount_to_withdraw, False)
        pass

    def activate_payout(self, payout_rules, spin_result, stake_amount, charname):
        """ Pays the player if they won """
        win_multiplier = payout_rules[spin_result]
        money_won = win_multiplier * stake_amount
        change_balance(charname, money_won, True)
        return money_won

    def format_stake_tier(self, stake_tiers):
        """ Formats the stake tiers into a neat string for printing """
        stake_format = "{}, {}, {}".format(stake_tiers[0], stake_tiers[1], stake_tiers[2])
        return stake_format

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def post_in_winners_cho(self, channel, moneywon, themachine, jackpot):
        """ Posts a win message if the player won their spin """
        if jackpot:
            embed = discord.Embed(title=":champagne:  :rotating_light: JACKPOT ALERT!!! :rotating_light:  :champagne_glass: ",
                                  description="Somebody has won {} from {}!".format(moneywon, themachine), color=0xf2e12c)
        else:
            embed = discord.Embed(title=":partying_face: Easy Payday!!! :partying_face:",
                                  description="Somebody has won {} from {}!".format(moneywon, themachine),
                                  color=0xf2e12c)
        await channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def sub_roll(self, ctx, stake_amount, charname, prediction):
        all_rows = []
        total_row_count = 0
        while total_row_count != self.num_of_rows:
            slot_count = 0
            row_to_add = []
            while slot_count != self.slots_each_row:
                row_to_add.append(randrange(self.lowest_roll, self.highest_roll + 1))
                slot_count += 1
            all_rows.append(row_to_add)
            total_row_count += 1
        spin_result = self.check_win(all_rows, prediction)

        date = datetime.datetime.now()
        if not spin_result:
            add_into_profitlogs(charname, stake_amount, "Cho Han", date)
            embed_to_print = self.create_embed(all_rows, 0, grab_char_balance(charname))
            await ctx.send(embed=embed_to_print)
        else:
            money_won = self.activate_payout(self.payout_rules, prediction, stake_amount, charname)
            add_into_winner(charname, money_won, "Cho Han", date)
            await self.post_in_winners_cho(self.bot.get_channel(self.winner_channel), money_won, "Cho Han", False)
            embed_to_print = self.create_embed(all_rows, money_won, grab_char_balance(charname))
            await ctx.send(embed=embed_to_print)

    @commands.command(name='chd')
    async def slot_desc_cho(self, ctx):
        await ctx.send(embed=self.description)

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_users_role_cho(self, ctx, role_name, channel_id, server_id):
        try:
            channel = self.bot.get_channel(channel_id)
            role = discord.utils.get(channel.guild.roles, name=role_name)
            guild = self.bot.get_guild(server_id)
            member = await guild.fetch_member(ctx.author.id)
            if role in member.roles:
                return True
            else:
                return False
            return False
        except Exception as e:
            await ctx.send(e)

    @commands.hybrid_command(name="ch")
    @app_commands.describe(prediction='Please pick a valid  prediction: odd, even, double, or lucky8!')
    @app_commands.describe(stake_amount='Invalid stake amount. Please choose either: 50, 100, 200')
    @app_commands.describe(num_of_spins='Invalid number of spins. Must be between 1 and 3.')
    async def roll_die(self, ctx: commands.Context, prediction: str, stake_amount: int, num_of_spins: int):
        """ Runs x spins based on cawk """
        try:
            if await self.check_users_role_cho(ctx, 'Baller', 979584371461877834, 979584371013079090) == True:
                if check_game_state('Cho Han'):
                    if prediction:
                        spin_count = 0
                        if num_of_spins <= self.max_spins and num_of_spins >= 1:
                            if stake_amount in self.stake_tiers:
                                if prediction in self.prediction_choices:
                                    charname = check_my_active_player(ctx.author.id)
                                    if charname:
                                        if check_charexists(charname):
                                            #Withdraw num of spins * stake from player account
                                            amount_to_withdraw = stake_amount * num_of_spins
                                            if check_enough_balance(charname, 'characteraccs', 'balance', amount_to_withdraw):
                                                self.pay_for_roll(charname, amount_to_withdraw)
                                                current_balance = grab_char_balance(charname)
                                                cost_embed = self.spin_embed(amount_to_withdraw, int(current_balance) +
                                                                             int(amount_to_withdraw), current_balance)
                                                await ctx.send(embed=cost_embed)
                                                while spin_count != num_of_spins:
                                                    await self.sub_roll(ctx, stake_amount, charname, prediction)
                                                    spin_count += 1
                                            else:
                                                await ctx.send("You don't have enough money!")
                                        else:
                                            await ctx.send("Character doesn't exist!")
                                    else:
                                        await ctx.send("You have not set an active character! $sc firstname lastname")
                                else:
                                    await ctx.send("Please pick a valid  prediction: odd, even, double, or lucky8")
                            else:
                                await ctx.send("Invalid stake amount. Please choose either: {}".
                                               format(self.format_stake_tier(self.stake_tiers)))
                        else:
                            await ctx.send("Invalid number of spins. Must be between 1 and {}.".format(self.max_spins))
                    else:
                        await ctx.send("Missing arguments $ch prediction stakeamount numofspins")
                else:
                    await ctx.send("Game has been disabled!")
            else:
                await ctx.send("You are not a verified member, register first!")
        except Exception as e:
            print(e)


async def setup(bot):
    emoji_theme = {1: '<:diceone:982342727381426176>', 2: '<:dicetwo:982344216715886672>',
                   3: '<:dicethree:982344216669724702>', 4: '<:dicefour:982344216808157184>',
                   5: '<:dicefive:982344216707465276>', 6: '<:dicesix:982344217022046278>'}
    payout_rules = {'odd': 2, 'even': 2, 'double': 4, 'lucky8': 7}
    prediction_choices = ['odd', 'even', 'double', 'lucky8']
    stake_tiers = [50, 100, 200]
    chohan = discord.Embed(title="CHO HAN", description="Predict the outcome of the dice to win!")
    chohan.add_field(name="Odd", value=":two: :zero: :regional_indicator_x: ", inline=True)
    chohan.add_field(name="Even", value=" :two: :regional_indicator_x:", inline=True)
    chohan.add_field(name="Double", value=" :six: :regional_indicator_x:", inline=True)
    chohan.add_field(name="Lucky Eight", value=":eight: :regional_indicator_x: ", inline=True)
    print("Loading Cho Han!")
    await bot.add_cog(ChoHan(bot, chohan, emoji_theme, payout_rules, 1, 2, 1, 6, stake_tiers, prediction_choices, 3))
    print("Loaded Cho Han!")

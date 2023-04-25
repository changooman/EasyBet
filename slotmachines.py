# bot.py
from abc import ABC, abstractmethod
from random import randrange
from easybetsregister import *
from registercentral import *
import datetime

class Slots():
    """ Interface for slots machines """

    @abstractmethod
    def __init__(self, bot, description, emoji_theme, payout_rules, num_of_rows, slots_each_row, lowest_roll, highest_roll,
                 stake_tiers, max_spins):
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
        """ Creates the embed that the bot will print"""
        pass

    @abstractmethod
    def check_win(self, all_rows):
        """ Checks if the player won their spin"""
        pass

    @abstractmethod
    def pay_for_spin(self):
        """ Takes payment from the player for the spin"""
        pass

    @abstractmethod
    def activate_payout(self, payout_rules):
        """ Pays the player if they won"""
        pass

    @abstractmethod
    def format_stake_tier(self, stake_tiers):
        """ Formats the stake tiers into a neat string for printing"""
        pass

    @abstractmethod
    def sub_spin(self):
        pass

    @abstractmethod
    def spin(self):
        """ Runs one spin"""
        pass


class FruitPalooza(commands.Cog, Slots):

    def __init__(self, bot, description, emoji_theme, payout_rules, num_of_rows, slots_each_row, lowest_roll,
                 highest_roll,
                 stake_tiers, max_spins):
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

    def num_to_emojis(self, num_row, emoji_theme):
        """ Takes an array of numbers and converts them to emoji code """
        emoji_string = ''
        for num in num_row:
            emoji_result = emoji_theme[num]
            emoji_string += emoji_result
        return emoji_string

    def assemble_all_emoji_row(self, arr_of_rows, embed):
        """ Runs through the given list of rows and turns them into their respective emoji version"""
        for arr in arr_of_rows:
            emoji_set = self.num_to_emojis(arr, self.emoji_theme)
            embed.add_field(name="Row", value=emoji_set, inline=False)
        return embed

    def spin_embed(self, cost, original, new):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="Spin Cost", description="", color=0xd5c144)
        embed.add_field(name="Cost $", value=cost, inline=True)
        embed.add_field(name="Original Balance", value=original, inline=True)
        embed.add_field(name="New Balance", value=new, inline=False)
        return embed

    def create_embed(self, arr_of_rows, money_won, balance):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="FRUIT PALOOZA", description="", color=0xd5c144)
        embed.set_author(name="Lucky Buddha", icon_url="https://i.imgur.com/YYBursK.png")
        new_embed = self.assemble_all_emoji_row(arr_of_rows, embed)
        new_embed.add_field(name="Won", value=money_won, inline=True)
        new_embed.add_field(name="Balance", value=balance, inline=False)
        return embed

    def check_win(self, all_rows):
        """ Checks if the player won their spin """
        for row in all_rows:
            # if 6 in row:
            #     return 6
            # if 1 in row:
            #     return 1
            if len(set(row)) == 1:
                return row[0]
        return False

    def pay_for_spin(self, charname, amount_to_withdraw):
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
    async def post_in_winners_fruit(self, channel, moneywon, themachine, jackpot):
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
    async def sub_spin_fruit(self, ctx, stake_amount, charname):
        all_rows = []
        total_row_count = 0
        # print("asdasdasd")
        while total_row_count != self.num_of_rows:
            slot_count = 0
            row_to_add = []
            while slot_count != self.slots_each_row:
                row_to_add.append(randrange(self.lowest_roll, self.highest_roll + 1))
                slot_count += 1
            all_rows.append(row_to_add)
            total_row_count += 1
        spin_result = self.check_win(all_rows)
        date = datetime.datetime.now()
        if not spin_result:
            add_into_profitlogs(charname, stake_amount, "Fruit Palooza", date)
            embed_to_print = self.create_embed(all_rows, 0, grab_char_balance(charname))
            await ctx.send(embed=embed_to_print)
        else:
            money_won = self.activate_payout(self.payout_rules, spin_result, stake_amount, charname)
            add_into_winner(charname, money_won, "Fruit Palooza", date)
            if spin_result == 6:
                await self.post_in_winners_fruit(self.bot.get_channel(self.winner_channel), money_won, "Fruit Palooza", True)
            else:
                await self.post_in_winners_fruit(self.bot.get_channel(self.winner_channel), money_won, "Fruit Palooza", False)
            embed_to_print = self.create_embed(all_rows, money_won, grab_char_balance(charname))
            await ctx.send(embed=embed_to_print)

    @commands.command(name='sdf')
    async def slot_desc_fruit(self, ctx):
        await ctx.send(embed=self.description)

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_users_role_fruit(self, ctx, role_name, channel_id, server_id):
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

    @commands.command(name='sf')
    async def spin_fruit(self, ctx, *args):
        """ Runs x spins """
        # print("check")
        try:
            if await self.check_users_role_fruit(ctx, 'Baller', 979584371461877834, 979584371013079090) == True:
                if check_game_state('Fruit Machine'):
                    if len(args) == 2:
                        spin_count = 0
                        stake_amount = int(args[0])
                        num_of_spins = int(args[1])
                        if num_of_spins <= self.max_spins and num_of_spins >= 1:
                            if stake_amount in self.stake_tiers:
                                charname = check_my_active_player(ctx.author.id)
                                if charname:
                                    if check_charexists(charname):
                                        #Withdraw num of spins * stake from player account
                                        amount_to_withdraw = stake_amount * num_of_spins
                                        if check_enough_balance(charname, 'characteraccs', 'balance', amount_to_withdraw):
                                            self.pay_for_spin(charname, amount_to_withdraw)
                                            current_balance = grab_char_balance(charname)
                                            cost_embed = self.spin_embed(amount_to_withdraw, int(current_balance) +
                                                                         int(amount_to_withdraw), current_balance)
                                            await ctx.send(embed=cost_embed)
                                            while spin_count != num_of_spins:
                                                await self.sub_spin_fruit(ctx, stake_amount, charname)
                                                spin_count += 1
                                        else:
                                            await ctx.send("You don't have enough money!")
                                    else:
                                        await ctx.send("Character doesn't exist!")
                                else:
                                    await ctx.send("You have not set an active character! $sc firstname lastname")
                            else:
                                await ctx.send("Invalid stake amount. Please choose either: {}".
                                               format(self.format_stake_tier(self.stake_tiers)))
                        else:
                            await ctx.send("Invalid number of spins. Must be between 1 and {}.".format(self.max_spins))
                    else:
                        await ctx.send("Missing arguments $sf stakeamount numofspins")
                else:
                    await ctx.send("Game has been disabled!")
            else:
                await ctx.send("You are not a verified member, register first!")
        except Exception as e:
            print(e)

class GreatGem(commands.Cog, Slots):

    def __init__(self, bot, description, emoji_theme, payout_rules, num_of_rows, slots_each_row, lowest_roll,
                 highest_roll,
                 stake_tiers, max_spins):
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

    def num_to_emojis(self, num_row, emoji_theme):
        """ Takes an array of numbers and converts them to emoji code """
        emoji_string = ''
        for num in num_row:
            emoji_result = emoji_theme[num]
            emoji_string += emoji_result
        return emoji_string

    def assemble_all_emoji_row(self, arr_of_rows, embed):
        """ Runs through the given list of rows and turns them into their respective emoji version"""
        for arr in arr_of_rows:
            emoji_set = self.num_to_emojis(arr, self.emoji_theme)
            embed.add_field(name="Row", value=emoji_set, inline=False)
        return embed

    def spin_embed(self, cost, original, new):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="Spin Cost", description="", color=0xd5c144)
        embed.add_field(name="Cost $", value=cost, inline=True)
        embed.add_field(name="Original Balance", value=original, inline=True)
        embed.add_field(name="New Balance", value=new, inline=False)
        return embed

    def create_embed(self, arr_of_rows, money_won, balance):
        """ Creates the embed that the bot will print """
        embed = discord.Embed(title="GREAT CAVERNS", description="", color=0xd5c144)
        embed.set_author(name="Lucky Buddha", icon_url="https://i.imgur.com/YYBursK.png")
        new_embed = self.assemble_all_emoji_row(arr_of_rows, embed)
        new_embed.add_field(name="Won", value=money_won, inline=True)
        new_embed.add_field(name="Balance", value=balance, inline=False)
        return embed

    def check_win(self, all_rows):
        """ Checks if the player won their spin """
        for row in all_rows:
            # if 6 in row:
            #     return 6
            # if 1 in row:
            #     return 1
            if len(set(row)) == 1:
                return row[0]
        return False

    def pay_for_spin(self, charname, amount_to_withdraw):
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
    async def post_in_winners_gem(self, channel, moneywon, themachine, jackpot):
        """Posts a win message if the player won their spin"""
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
    async def sub_spin_gem(self, ctx, stake_amount, charname):
        all_rows = []
        total_row_count = 0
        # print("asdasdasd")
        while total_row_count != self.num_of_rows:
            slot_count = 0
            row_to_add = []
            while slot_count != self.slots_each_row:
                row_to_add.append(randrange(self.lowest_roll, self.highest_roll + 1))
                slot_count += 1
            all_rows.append(row_to_add)
            total_row_count += 1
        spin_result = self.check_win(all_rows)
        date = datetime.datetime.now()
        if not spin_result:
            add_into_profitlogs(charname, stake_amount, "Great Caverns", date)
            embed_to_print = self.create_embed(all_rows, 0, grab_char_balance(charname))
            await ctx.send(embed=embed_to_print)
        else:
            money_won = self.activate_payout(self.payout_rules, spin_result, stake_amount, charname)
            add_into_winner(charname, money_won, "Great Caverns", date)
            if spin_result == 6:
                await self.post_in_winners_gem(self.bot.get_channel(self.winner_channel), money_won, "Great Caverns", True)
            else:
                await self.post_in_winners_gem(self.bot.get_channel(self.winner_channel), money_won, "Great Caverns", False)
            embed_to_print = self.create_embed(all_rows, money_won, grab_char_balance(charname))
            await ctx.send(embed=embed_to_print)

    @commands.command(name='sdg')
    async def slot_desc_gem(self, ctx):
        await ctx.send(embed=self.description)

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_users_role_gem(self, ctx, role_name, channel_id, server_id):
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

    @commands.command(name='sg')
    async def spin_gem(self, ctx, *args):
        """ Runs x spins """
        # print("check")
        try:
            if await self.check_users_role_gem(ctx, 'Baller', 979584371461877834, 979584371013079090) == True:
                if check_game_state('Great Caverns'):
                    if len(args) == 2:
                        spin_count = 0
                        stake_amount = int(args[0])
                        num_of_spins = int(args[1])
                        if num_of_spins <= self.max_spins and num_of_spins >= 1:
                            if stake_amount in self.stake_tiers:
                                charname = check_my_active_player(ctx.author.id)
                                if charname:
                                    if check_charexists(charname):
                                        #Withdraw num of spins * stake from player account
                                        amount_to_withdraw = stake_amount * num_of_spins
                                        if check_enough_balance(charname, 'characteraccs', 'balance', amount_to_withdraw):
                                            self.pay_for_spin(charname, amount_to_withdraw)
                                            current_balance = grab_char_balance(charname)
                                            cost_embed = self.spin_embed(amount_to_withdraw, int(current_balance) +
                                                                         int(amount_to_withdraw), current_balance)
                                            await ctx.send(embed=cost_embed)
                                            while spin_count != num_of_spins:
                                                await self.sub_spin_gem(ctx, stake_amount, charname)
                                                spin_count += 1
                                        else:
                                            await ctx.send("You don't have enough money!")
                                    else:
                                        await ctx.send("Character doesn't exist!")
                                else:
                                    await ctx.send("You have not set an active character! $sc firstname lastname")
                            else:
                                await ctx.send("Invalid stake amount. Please choose either: {}".
                                               format(self.format_stake_tier(self.stake_tiers)))
                        else:
                            await ctx.send("Invalid number of spins. Must be between 1 and {}.".format(self.max_spins))
                    else:
                        await ctx.send("Missing arguments $sg stakeamount numofspins")
                else:
                    await ctx.send("This game has been disabled!")
            else:
                await ctx.send("You are not a verified member, register first!")
        except Exception as e:
            print(e)


async def setup(bot):
    emoji_theme = {1: ':lemon:', 2: ':grapes:', 3: ':banana:', 4: ':pineapple:', 5: ':tangerine:', 6: ':mango:'}
    payout_rules = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 60}
    stake_tiers = [10, 20, 50]
    fruit = discord.Embed(title="FRUIT PALOOZA", description="Match three fruit in a row to win!")
    fruit.add_field(name=":mango:", value=":six: :zero: :regional_indicator_x: ", inline=True)
    fruit.add_field(name=":tangerine:", value=" :five: :regional_indicator_x:", inline=True)
    fruit.add_field(name=":pineapple:", value=" :four: :regional_indicator_x:", inline=True)
    fruit.add_field(name=":banana:", value=":three: :regional_indicator_x: ", inline=True)
    fruit.add_field(name=":grapes:", value=" :two: :regional_indicator_x:", inline=True)
    fruit.add_field(name=":lemon:", value=":one: :regional_indicator_x:", inline=True)
    emoji_theme_two = {1: '<:sapphire:982322964475293716>', 2: '<:emerald:982322765799505990>',
                       3: '<:ruby:982322765765939240>', 4: '<:silver:982322765740802108>',
                       5: '<:topaz:982322765732405299>', 6: '<:purplegem:982322765614940201>'}
    payout_rules_two = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 60}
    stake_tiers_two = [100, 200, 300]
    gem = discord.Embed(title="THE GREAT CAVERNS", description="Match three gems in a row to win!")
    gem.add_field(name="<:sapphire:982322964475293716>", value=":six: :zero: :regional_indicator_x: ", inline=True)
    gem.add_field(name="<:emerald:982322765799505990>", value=" :five: :regional_indicator_x:", inline=True)
    gem.add_field(name="<:ruby:982322765765939240>", value=" :four: :regional_indicator_x:", inline=True)
    gem.add_field(name="<:silver:982322765740802108>", value=":three: :regional_indicator_x: ", inline=True)
    gem.add_field(name="<:topaz:982322765732405299>", value=" :two: :regional_indicator_x:", inline=True)
    gem.add_field(name="<:purplegem:982322765614940201>", value=":one: :regional_indicator_x:", inline=True)
    # fruit.spin()
    print("Loading Slots!")
    await bot.add_cog(FruitPalooza(bot, fruit, emoji_theme, payout_rules, 1, 3, 1, 6, stake_tiers, 3))
    await bot.add_cog(GreatGem(bot, gem, emoji_theme_two, payout_rules_two, 1, 3, 1, 6, stake_tiers_two, 3))
    print("Loaded Slots!")

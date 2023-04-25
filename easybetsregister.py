# bot.py

import mysql.connector

import discord
from discord import activity
from discord.ext import commands
from registercentral import *

import math

class EasyBetsRegister(commands.Cog):

    def __init__(self, bot):
        self.intents = discord.Intents.default()
        self.mydb = mysql.connector.connect(
            host="",
            port='',
            user="",
            password="",
            database=""
        )
        self.mycursor = self.mydb.cursor()
        self.bot = bot
        self.severid = 979584371013079090
        self.general = 979584371461877834
        self.register_requests = 980961137401139280
        self.add_requests = 981032921110544424
        self.withdraw_requests = 981035318964789259
        self.staff_lounge = 981646064895537252
        self.extension_list = ['slotmachines', 'easybetsregister', 'chohan', 'raffles', 'sportsbetting']

    @commands.command(name='ra')
    @commands.has_any_role('EasyBet', 'Admin')
    async def reload_db(self, ctx):
        print("RELOADING!!!")
        for ext in self.extension_list:
            self.bot.unload_extension(ext)
            self.bot.load_extension(ext)

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_user_role(self, ctx, role_name, channel_id, server_id):
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


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            error_message = 'This command is on cooldown, you can use it in {0} seconds.'.format(round(error.retry_after, 2))
            await ctx.send(error_message)

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_ucpownership(self, ctx, check_ucp_name):
        id_string = ctx.message.author.id
        sql_query = "SELECT ucpname FROM masteraccs where discordid = {} LIMIT 1".format(id_string)
        self.mycursor.execute(sql_query)
        result = self.mycursor.fetchone()
        if self.mycursor.rowcount != 0:
            if result[0] == check_ucp_name:
                return True
            else:
                return False
        else:
            return False
        return self.mycursor

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_ucp_exists(self, ctx, check_ucp_name):
        check_ucp_name = '"' + check_ucp_name + '"'
        sql_query = "SELECT discordid FROM masteraccs where ucpname = {}".format(check_ucp_name)
        self.mycursor.execute(sql_query)
        result = self.mycursor.fetchone()
        if self.mycursor.rowcount == 0:
            return False
        else:
            return True

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_discord_exists(self, ctx, discordid):
        sql_query = "SELECT ucpname FROM masteraccs where discordid = {}".format(discordid)
        self.mycursor.execute(sql_query)
        result = self.mycursor.fetchone()
        if self.mycursor.rowcount == 0:
            return False
        else:
            return True

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def set_role_member(self, ctx):
        channel = self.bot.get_channel(self.general)
        guild = self.bot.get_guild(self.severid)
        role = discord.utils.get(channel.guild.roles, name='Baller')
        member = await guild.fetch_member(ctx.author.id)
        await member.add_roles(role)

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def reclaim_role_confirm(self, ctx):
        embed = discord.Embed(title="You've been reassigned your role, welcome back!")
        return embed

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def registration_accept_embed(self, ctx):
        embed = discord.Embed(title="You've been reassigned your role, welcome back!")
        return embed

    @commands.command(name='rec')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def reclaim_role(self, ctx):
        if await self.check_user_role(ctx, 'Baller', 979584371461877834, 979584371013079090) == False:
            exists = await self.check_discord_exists(ctx, ctx.author.id)
            if exists:
                await self.set_role_member(ctx)
                embed = await self.reclaim_role_confirm(ctx)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Your discord account is not recognized!")
        else:
            await ctx.send("You already have the role!")

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def return_ucp_from_discord(self, discordid):
        # print("Made it here!")
        sql_query = "SELECT ucpname FROM masteraccs where discordid = {}".format(discordid)
        self.mycursor.execute(sql_query)
        # print("Made it here!")
        result = self.mycursor.fetchone()
        if self.mycursor.rowcount == 0:
            # print("nope!")
            return False
        else:
            # print(result[0])
            return result[0]

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_ucpcharowner(self, charname, ucpname):
        fullname = '"' + charname + '"'
        try:
            sql_query = "SELECT ucpname FROM characteraccs where charname = {} LIMIT 1".format(fullname)
            self.mycursor.execute(sql_query)
            result = self.mycursor.fetchone()
            if result[0] == ucpname:
                return True
            else:
                return False
        except Exception as e:
            print("Something went wrong!")
            pass

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_char_balance(self, charname):
        fullname = '"' + charname + '"'
        try:
            sql_query = "SELECT balance FROM characteraccs where charname = {} LIMIT 1".format(fullname)
            self.mycursor.execute(sql_query)
            result = self.mycursor.fetchone()
            # print(result[0])
            return result[0]
        except Exception as e:
            print("Something went wrong!")
            pass

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_charexists(self, charname):
        fullname = '"' + charname + '"'
        try:
            sql_query = "SELECT EXISTS(SELECT add_amount FROM characteraccs where charname = {})".format(fullname)
            self.mycursor.execute(sql_query)
            result = self.mycursor.fetchone()
            if result[0] == 0:
                return False
            else:
                return True
        except Exception as e:
            print("Something went wrong!")
            pass

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_change_balance(self, charname, request_type):
        fullname = '"' + charname + '"'
        if request_type == 'Add':
            sql_query = "SELECT add_amount FROM characteraccs where charname = {}".format(fullname)
        else:
            sql_query = "SELECT take_amount FROM characteraccs where charname = {}".format(fullname)
        try:
            self.mycursor.execute(sql_query)
            result = self.mycursor.fetchone()
            if result[0] == 0:
                return False
            else:
                return True
        except Exception as e:
            print("Something went wrong!")
            pass

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def register(self, ucpname, authorid, user, check_channel, server_id):
        sql_query = "INSERT INTO masteraccs (discordid, ucpname) values (%s, %s)"
        values = (authorid, ucpname)
        try:
            self.mycursor.execute(sql_query, values)
        except Exception as e:
            await user.send("Either your ucp or discord account have already been registered.")
        else:
            self.mydb.commit()
            await user.send("Your registration request for UCP {} has been accepted!".format(ucpname))
            channel = self.bot.get_channel(check_channel)
            guild = self.bot.get_guild(server_id)
            role = discord.utils.get(channel.guild.roles, name='Baller')
            member = await guild.fetch_member(user.id)
            await member.add_roles(role)
            return self.mycursor

    @commands.command(name='rr')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def register_request(self, ctx, *args):
        if len(args) != 2:
            await ctx.send("Missing arguments! $rr ucpname ownershipimgurlink")
        else:
            ucpname = args[0]
            proof = args[1]
            if not await self.check_ucp_exists(ctx, ucpname):
                if not await self.check_discord_exists(ctx, ctx.author.id):
                    embed = discord.Embed(title="Register Request", description="{}".format(ucpname))
                    emoji_string = ''
                    emoji_string += ':white_check_mark:'
                    embed.add_field(name="React with to confirm:", value=':white_check_mark:', inline=True)
                    embed.add_field(name="Proof:", value="\u200b", inline=False)
                    embed.set_image(url=proof)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("This Discord account has already been registered.")
            else:
                await ctx.send("This UCP account has already been registered.")

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def add_char_embed(self, charname, ucpname):
        embed = discord.Embed(title="Character Request", description="{}".format(charname))
        embed.add_field(name="UCP Name", value=ucpname, inline=False)
        embed.add_field(name="React with to confirm character registration:", value=':white_check_mark:', inline=False)
        return embed

    @commands.command(name='addchar')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def add_character_request(self, ctx, *args):
        # print("asdasda")
        if len(args) != 2:
            await ctx.send("Missing arguments! $addchar firstname lastname")
        else:
            firstname = args[0]
            lastname = args[1]
            if await self.check_user_role(ctx, 'Baller', 979584371461877834, 979584371013079090) == True:
                # print("asdasda")
                ucpname = await self.return_ucp_from_discord(ctx.author.id)
                # print("asdasd22")
                discord_owner = await self.check_ucpownership(ctx, ucpname)
                user = await self.bot.fetch_user(ctx.author.id)
                charname = firstname + ' ' + lastname
                if discord_owner:
                    if not await self.check_charexists(charname):
                        embed = await self.add_char_embed(charname, ucpname)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("Character already exists!")
                else:
                    await ctx.send("That UCP does not belong to you.")
            else:
                await ctx.send("You are not a verified member. Please register and try again.")

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def add_character_confirm_embed(self, charname):
        embed=discord.Embed(title="Your character, {}, has been registered!".format(charname))
        return embed

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def add_character(self, charname, ucpname, userid):
        sql_query = "INSERT INTO characteraccs (charname, ucpname, balance) values (%s, %s, 0)"
        values = (charname, ucpname)
        user = await self.bot.fetch_user(userid)
        try:
            self.mycursor.execute(sql_query, values)
        except Exception as e:
            await user.send("Your character has already been claimed.")
        else:
            embed = await self.add_character_confirm_embed(charname)
            await user.send(embed=embed)
            self.mydb.commit()
            return self.mycursor

    @commands.has_any_role('EasyBet', 'Admin')
    async def grab_discord_from_embed(self, the_message):
        for field in the_message.fields:
            if field.name == 'Discord ID':
                return field.value

    @commands.has_any_role('EasyBet', 'Admin')
    async def grab_amount_from_embed(self, the_message):
        for field in the_message.fields:
            if field.name == 'Amount':
                return field.value

    @commands.has_any_role('EasyBet', 'Admin')
    async def grab_ucpname_from_embed(self, the_message):
        for field in the_message.fields:
            if field.name == 'UCP Name':
                return field.value

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def list_characters_embed(self, result):
        embed = discord.Embed(title="Your Characters")
        character_title = 'Character/Balance'
        for character in result:
            display = '{}/{}'.format(character[0], character[1])
            embed.add_field(name=character_title, value=display, inline=False)
        return embed

    @commands.command(name='lc')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def list_characters(self, ctx, *args):
        if await self.check_user_role(ctx, 'Baller', 979584371461877834, 979584371013079090) == True:
            ucpname = await self.return_ucp_from_discord(ctx.author.id)
            ucpname = '"' + ucpname + '"'
            sql_query = "SELECT charname, balance from characteraccs where ucpname = {}".format(ucpname)
            self.mycursor.execute(sql_query)
            result = self.mycursor.fetchall()
            if len(result) != 0:
                embed = await self.list_characters_embed(result)
                await ctx.send(embed = embed)
            else:
                ctx.send("You have no characters! Do $addchar firstname lastname to register a character")
            return
        else:
            await ctx.send("You are not a verified member. Please register and try again.")

    @commands.has_any_role('EasyBet', 'Admin')
    async def organize_private_msg(self, payload, message, channelid):
        approved_channel_id = [self.add_requests, self.withdraw_requests, self.register_requests]
        if channelid in approved_channel_id:
            if payload.emoji.name == '✅':
                user = await self.bot.fetch_user(payload.user_id)
                if channelid == self.register_requests:
                    try:
                        the_message = message.embeds[0]
                    except Exception as e:
                        # print("Didn't react to an embed.")
                        pass
                    else:
                        if the_message.title == 'Register Request':
                            discord_id = await self.grab_discord_from_embed(the_message)
                            ucpname = the_message.description
                            user = await self.bot.fetch_user(discord_id)
                            await self.register(ucpname, discord_id, user, 979584371461877834, 979584371013079090)
                else:
                    try:
                        the_message = message.embeds[0]
                    except Exception as e:
                        # print("Didn't react to an embed.")
                        pass
                    else:
                        discord_id = await self.grab_discord_from_embed(the_message)
                        user = await self.bot.fetch_user(discord_id)
                        if the_message.title == 'Add Request':
                            if await self.check_change_balance(the_message.description, 'Add') == 1:
                                await self.setup_change_balance(the_message.description, 'addbalance', 'add_amount',
                                                                    self.add_requests, True, user)
                            else:
                                post_in = self.bot.get_channel(self.staff_lounge)
                                await post_in.send("There is no existing add balance request for {}.".format(the_message.description))
                        elif the_message.title == 'Withdraw Request':
                            await self.setup_change_balance(the_message.description, 'takebalance', 'take_amount',
                                                                    self.withdraw_requests, False, user)

    @commands.Cog.listener()
    @commands.has_any_role('EasyBet', 'Admin')
    async def on_raw_reaction_add(self, payload):
        register_requests_channel_id = 980961137401139280
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if not isinstance(channel, discord.DMChannel):
            await self.organize_private_msg(payload, message, payload.channel_id)
        else:
            try:
                the_message = message.embeds[0]
            except Exception as e:
                # print("Didn't react to an embed.")
                pass
            else:
                if the_message.title == 'Register Request':
                    ucp_name = the_message.description
                    embed = discord.Embed(title="Register Request", description="{}".format(ucp_name))
                    embed.add_field(name="Discord ID", value=payload.user_id, inline=True)
                    embed.add_field(name="React with to confirm their registration:", value=':white_check_mark:', inline=False)
                    embed.add_field(name="Proof:", value="\u200b", inline=False)
                    embed.set_image(url=the_message.image.url)
                    register_requests_channel = self.bot.get_channel(register_requests_channel_id)
                    await register_requests_channel.send(embed=embed)
                if the_message.title == 'Character Request':
                    ucp_name = await self.grab_ucpname_from_embed(the_message)
                    await self.add_character(the_message.description, ucp_name, payload.user_id)
                if the_message.title == 'Add Request':
                    charname = the_message.description
                    ucpname = await self.return_ucp_from_discord(payload.user_id)
                    proof = the_message.image.url
                    amount = await self.grab_amount_from_embed(the_message)
                    await self.change_balance_request(payload.user_id, charname, ucpname, amount, proof, 'addbalance', 'add_amount',
                                                      self.add_requests, 'Add')
                if the_message.title == 'Withdraw Request':
                    charname = the_message.description
                    ucpname = await self.return_ucp_from_discord(payload.user_id)
                    proof = the_message.image.url
                    amount = await self.grab_amount_from_embed(the_message)
                    fullname = '"' + charname + '"'
                    sql_query2 = "SELECT balance from characteraccs where charname = {}".format(fullname)
                    self.mycursor.execute(sql_query2)
                    result = self.mycursor.fetchone()
                    amount2 = result[0] - int(amount)
                    sql_query3 = "UPDATE characteraccs SET balance = {} where charname = {}".format(amount2, fullname)
                    self.mycursor.execute(sql_query3)
                    await self.change_balance_request(payload.user_id, charname, ucpname, amount, proof, 'takebalance', 'take_amount',
                                                      self.withdraw_requests, 'Withdraw')

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def change_balance_embed(self, charname, proof, amount, req_type, user_id):
        embed = discord.Embed(title="{} Request".format(req_type), description="{}".format(charname))
        embed.add_field(name="Discord ID", value=user_id, inline=True)
        embed.add_field(name="Amount", value=amount, inline=True)
        embed.add_field(name="React with to confirm their request:", value=':white_check_mark:',
                        inline=False)
        if req_type == 'Add':
            embed.add_field(name="Proof:", value="\u200b", inline=False)
            embed.set_image(url=proof)
        return embed

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def balance_request_confirm_embed(self, request_type):
        embed=discord.Embed(title="Your {} request has been received and is pending!".format(request_type))
        return embed

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def cancel_add_balance_embed(self, charname):
        embed = discord.Embed(title="Add balance request canceled for {}.".format(charname))
        return embed

    @commands.command(name='cab')
    @commands.has_any_role('EasyBet', 'Admin')
    async def cancel_add_balance(self, ctx, *args):
        firstname = args[0]
        lastname = args[1]
        charname = firstname + ' ' + lastname
        fullname = '"' + charname + '"'
        if len(args) != 2:
            await ctx.send("Missing arguments! $cab firstname lastname")
        else:
            if await self.check_charexists(charname) == 0:
                await ctx.send("This character, {}, does not exist.".format(charname))
            elif await self.check_change_balance(charname, 'Add') == 0:
                await ctx.send("There is no existing balance request for {0}.".format(charname, 'Add'))
            else:
                sql_query4 = "UPDATE characteraccs SET {} = {} where charname = {}".format('add_amount', 0, fullname)
                sql_query5 = "DELETE FROM {} WHERE charname = {}".format('addbalance', fullname)
                try:
                    self.mycursor.execute(sql_query4)
                    self.mycursor.execute(sql_query5)
                except Exception as e:
                    print(e)
                    pass
                else:
                    embed = await self.cancel_add_balance_embed(charname)
                    await ctx.send(embed=embed)
                    self.mydb.commit()
                    return self.mycursor

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def change_balance_request(self, user_id, charname, ucpname, amount, proof, target_tb, target_col,
                                     target_channel, request_type):
        channel = self.bot.get_channel(target_channel)
        user = await self.bot.fetch_user(user_id)
        if await self.check_charexists(charname) == 0:
            await user.send("This character, {}, does not exist.".format(charname))
        elif not await self.check_ucpcharowner(charname, ucpname):
            await user.send("You don't own that character.")
        elif await self.check_change_balance(charname, request_type) == 1:
            await user.send("You already have an existing {1} balance request for {0}.".format(charname, request_type))
        # elif not await self.check_ucpownership(ctx, ucpname):
        #     await user.send("You don't own that UCP.")
        else:
            sql_query = "INSERT INTO {} (charname, ucpname, amount) values (%s, %s, %s)".format(target_tb)
            values = (charname, ucpname, amount)
            try:
                self.mycursor.execute(sql_query, values)
                embed = await self.change_balance_embed(charname, proof, amount, request_type, user_id)
                await channel.send(embed=embed)
                fullname = '"' + charname + '"'
                sql_query2 = "UPDATE characteraccs SET {} = {} where charname = {}".format(target_col, 1, fullname)
                embed2 = await self.balance_request_confirm_embed(request_type)
                await user.send(embed=embed2)
                self.mycursor.execute(sql_query2)
            except NameError as e:
                print(e)
                pass
            except Exception as e:
                if e.errno == 1062:
                    await user.send("You already have a pending {} balance request for {0}.".format(charname, request_type))
                else:
                    print(e)
                    pass
            else:
                self.mydb.commit()
                return self.mycursor

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def change_balancereq_confirm_embed(self, ctx, charname, proof, amount, req_type):
        embed = discord.Embed(title="{} Request".format(req_type), description="{}".format(charname))
        embed.add_field(name="Discord ID", value=ctx.author.id, inline=True)
        embed.add_field(name="Amount", value=amount, inline=True)
        embed.add_field(name="React with to confirm your request:", value=':white_check_mark:',
                        inline=False)
        if req_type == 'Add':
            embed.add_field(name="Proof:", value="\u200b", inline=False)
            embed.set_image(url=proof)
        return embed

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_balance_embed(self, charname, balance):
        embed = discord.Embed(title="{}, your balance is {}.".format(charname, balance))
        return embed

    @commands.command(name='cb')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def check_balance(self, ctx, *args):
        if len(args) != 2:
            await ctx.send("Missing arguments! $abr firstname lastname")
        else:
            firstname = args[0]
            lastname = args[1]
            ucpname = await self.return_ucp_from_discord(ctx.author.id)
            if await self.check_user_role(ctx, 'Baller', 979584371461877834, 979584371013079090) == True:
                charname = firstname + ' ' + lastname
                if await self.check_charexists(charname):
                    if await self.check_ucpcharowner(charname, ucpname):
                        balance = await self.check_char_balance(charname)
                        embed = await self.check_balance_embed(charname, balance)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("You don't own the UCP that the character belongs to.")
                else:
                    await ctx.send("That character doesn't exist!")
            else:
                await ctx.send("You are not a verified member. Please register and try again.")

    @commands.command(name='abr')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def add_balance_request(self, ctx, *args):
        minimum_amount = 500
        if len(args) != 4:
            await ctx.send("Missing arguments! $abr firstname lastname amount proofofpayment")
        else:
            firstname = args[0]
            lastname = args[1]
            amount = args[2]
            proof = args[3]
            if int(amount) >= minimum_amount:
                if await self.check_user_role(ctx, 'Baller', 979584371461877834, 979584371013079090) == True:
                    charname = firstname + ' ' + lastname
                    embed = await self.change_balancereq_confirm_embed(ctx, charname, proof, amount, 'Add')
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("You are not a verified member. Please register and try again.")
            else:
                await ctx.send("You need to add at least {}!".format(minimum_amount))

    @commands.command(name='awr')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def add_withdraw_request(self, ctx, *args):
        minimum_amount = 500
        if len(args) != 3:
            await ctx.send("Missing arguments! $awr firstname lastname amount")
        else:
            firstname = args[0]
            lastname = args[1]
            amount = args[2]
            if int(amount) >= minimum_amount:
                if await self.check_user_role(ctx, 'Baller', 979584371461877834, 979584371013079090) == True:
                    if await self.check_enough_balance(ctx, firstname, lastname, "characteraccs", "balance", amount) == True:
                        charname = firstname + ' ' + lastname
                        embed = await self.change_balancereq_confirm_embed(ctx, charname, "", amount, 'Withdraw')
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("Not enough money in your balance!")
                else:
                    await ctx.send("You are not a verified member. Please register and try again.")
            else:
                await ctx.send("You need to withdraw at least {}!".format(minimum_amount))

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def balance_accept_confirm_embed(self, request_type, amount):
        embed = discord.Embed(title="Your {} request has been accepted! Your new balance is: ${}".format(request_type, amount))
        return embed

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def change_balance(self, fullname, sql_query, sql_query4, sql_query5, channel, stay_pos, user):
        try:
            self.mycursor.execute(sql_query)
            result = self.mycursor.fetchone()
            amount = result[0]
            sql_query2 = "SELECT balance from characteraccs where charname = {}".format(fullname)
            self.mycursor.execute(sql_query2)
            result = self.mycursor.fetchone()
            amount2 = result[0]
            if stay_pos:
                amount2 = amount2 + amount
                embed = await self.balance_accept_confirm_embed('add', amount2)
                await user.send(embed=embed)
                sql_query3 = "UPDATE characteraccs SET balance = {} where charname = {}".format(amount2, fullname)
                self.mycursor.execute(sql_query3)
            else:
                embed = await self.balance_accept_confirm_embed('withdraw', amount2)
                await user.send(embed=embed)
            self.mycursor.execute(sql_query4)
            self.mycursor.execute(sql_query5)
        except Exception as e:
            await channel.send(e)
        else:
            self.mydb.commit()
            return self.mycursor

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def setup_change_balance(self, charname, target_tb, target_col, target_channel, stay_pos, user):
        fullname = '"' + charname + '"'
        channel = self.bot.get_channel(target_channel)
        sql_query = "SELECT amount FROM {} WHERE charname = {}".format(target_tb, fullname)
        sql_query5 = "DELETE FROM {} WHERE charname = {}".format(target_tb, fullname)
        sql_query4 = "UPDATE characteraccs SET {} = {} where charname = {}".format(target_col, 0, fullname)
        await self.change_balance(fullname, sql_query, sql_query4, sql_query5, channel, stay_pos, user)

    @commands.command()
    @commands.has_any_role('EasyBet', 'Admin')
    async def check_enough_balance(self, ctx, firstname, lastname, target_tb, target_col, amount):
        charname = firstname + ' ' + lastname
        fullname = '"' + charname + '"'
        user = await self.bot.fetch_user(ctx.author.id)
        if await self.check_charexists(charname) == 0:
            await user.send("This character, {}, does not exist.".format(charname))
        else:
            try:
                sql_query = "SELECT {} FROM {} WHERE charname = {}".format(target_col, target_tb, fullname)
                self.mycursor.execute(sql_query)
                result = self.mycursor.fetchone()
            except Exception as e:
                print("Something went wrong!")
                pass
            else:
                if result[0] < int(amount):
                    return False
                else:
                    return True

    @commands.command(name='sc')
    async def set_character(self, ctx, *args):
        if len(args) != 2:
            await ctx.send("Missing arguments! $sc firstname lastname")
        else:
            firstname = args[0]
            lastname = args[1]
            ucpname = await self.return_ucp_from_discord(ctx.author.id)
            if await self.check_user_role(ctx, 'Baller', 979584371461877834, 979584371013079090) == True:
                charname = firstname + ' ' + lastname
                if await self.check_charexists(charname):
                    if await self.check_ucpcharowner(charname, ucpname):
                        set_active_player(ctx.author.id, charname)
                        embed = discord.Embed(title="Character switched to {}.".format(charname))
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("You don't own the UCP that the character belongs to.")
                else:
                    await ctx.send("That character doesn't exist!")
            else:
                await ctx.send("You are not a verified member. Please register and try again.")

    @commands.command(name='sgs')
    @commands.has_any_role('EasyBet', 'Admin')
    async def set_game_state(self, ctx, *args):
        if len(args) != 2:
            await ctx.send("Missing arguments! $sgs onoroff 'game'")
        else:
            onoroff = args[0]
            game = args[1]
            if onoroff == "on":
                set_game_state(1, game)
                await ctx.send("{} has been set to on!".format(game))
            elif onoroff == "off":
                set_game_state(0, game)
                await ctx.send("{} has been set to off!".format(game))
            else:
                await ctx.send("Please pick either 'on' or 'off'!")

    @commands.command(name='psw')
    @commands.has_any_role('EasyBet', 'Admin')
    async def profit_since_when(self, ctx, *args):
        if len(args) == 1:
            date = args[0]
            print("Asdasdasd")
            revenue = money_since_when('profitlogs', date)
            loss = money_since_when('winnerlogs', date)
            await ctx.send('Profit since start of {} is ${}!'.format(date, revenue - loss))
        else:
            await ctx.send("$psw date")
async def setup(bot):
    await bot.add_cog(EasyBetsRegister(bot))
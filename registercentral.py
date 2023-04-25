import mysql.connector

mydb = mysql.connector.connect(
    host="",
    port='',
    user="",
    password="",
    database="",
    autocommit=True
)
mycursor = mydb.cursor()

active_players = {}


# SPORTSGAMES

def grab_sports_games():
    sql_query = "SELECT * FROM sportsgames"
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchall()
        return result
    except Exception as e:
        print(e)


def add_into_sportsgames(matchname, t1_name, t1_odd, t2_name, t2_odd, t1_status, t2_status, draw_status, draw_odd):
    matchname = '"' + matchname + '"'
    t1_name = '"' + t1_name + '"'
    t2_name = '"' + t2_name + '"'
    t1_odd = float(t1_odd)
    t2_odd = float(t2_odd)
    sql_query = "INSERT INTO sportsgames (matchname, t1, t2, betstatus, t1_status, t2_status, t1_odd, t2_odd, draw_status, draw_odd) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
        matchname, t1_name, t2_name, 1, t1_status, t2_status, t1_odd, t2_odd, draw_status, draw_odd)
    try:
        mycursor.execute(sql_query)
    except Exception as e:
        print(e)
    else:
        mydb.commit()
        return mycursor
    pass


def update_sportsgames_status(matchname, status):
    matchname = '"' + matchname + '"'
    sql_query = "UPDATE sportsgames SET betstatus = {} where matchname = {}".format(status, matchname)
    try:
        mycursor.execute(sql_query)
    except Exception as e:
        print(e)
    else:
        mydb.commit()
        return mycursor


def update_sportsgames_outcomestatus(matchname, outcomestatus, status):
    matchname = '"' + matchname + '"'
    if outcomestatus == "t1":
        sql_query = "UPDATE sportsgames SET t1_status = {} where matchname = {}".format(status, matchname)
    elif outcomestatus == "t2":
        sql_query = "UPDATE sportsgames SET t2_status = {} where matchname = {}".format(status, matchname)
    elif outcomestatus == "draw":
        sql_query = "UPDATE sportsgames SET draw_status = {} where matchname = {}".format(status, matchname)
    else:
        pass
    try:
        mycursor.execute(sql_query)
    except Exception as e:
        print(e)
    else:
        mydb.commit()
        return mycursor


def add_sportsgame_bet(discordid, charname, matchname, outcome, amount):
    charname = '"' + charname + '"'
    matchname = '"' + matchname + '"'
    outcome = '"' + outcome + '"'
    sql_query = "INSERT INTO sportsbet (discordid, charname, matchname, outcome, amount) VALUES ({}, {}, {}, {}, {})".format(discordid, charname,
                                                                                                              matchname,
                                                                                                              outcome,
                                                                                                              amount)
    try:
        mycursor.execute(sql_query)
    except Exception as e:
        print(e)
    else:
        mydb.commit()
        return mycursor


def clear_sportsgames_bets(matchname):
    matchname = '"' + matchname + '"'
    sql_query = "DELETE FROM sportsgames WHERE matchname = {}".format(matchname)
    sql_query2 = "DELETE FROM sportsbet WHERE matchname = {}".format(matchname)
    try:
        mycursor.execute(sql_query)
        mycursor.execute(sql_query2)
    except Exception as e:
        print(e)
    else:
        mydb.commit()
        return mycursor


def count_sportsgamesbet(matchname, outcome):
    matchname = '"' + matchname + '"'
    outcome = '"' + outcome + '"'
    sql_query = "SELECT SUM(amount) FROM sportsbet WHERE matchname = {} and outcome = {}".format(matchname, outcome)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        return result[0]
    except Exception as e:
        print(e)


def grab_sportsgame_outcomeodd(matchname, outcome):
    matchname = '"' + matchname + '"'
    outcome = '"' + outcome + '"'
    if "t1" in outcome:
        sql_query = "SELECT t1_odd FROM sportsgames WHERE matchname = {}".format(matchname)
    if "t2" in outcome:
        sql_query = "SELECT t2_odd FROM sportsgames WHERE matchname = {}".format(matchname)
    if "draw" in outcome:
        sql_query = "SELECT draw_odd FROM sportsgames WHERE matchname = {}".format(matchname)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        return result[0]
    except Exception as e:
        print(e)


def check_sportsgame_status(matchname):
    matchname = '"' + matchname + '"'
    sql_query = "SELECT betstatus FROM sportsgames WHERE matchname = {}".format(matchname)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        if result[0] == 0:
            return False
        else:
            return True
    except Exception as e:
        print(e)


def check_sportsgameoutcome_status(matchname, outcome):
    matchname = '"' + matchname + '"'
    outcome = '"' + outcome + '"'
    print("Matchname is: {}".format(matchname))
    if "t1" in outcome:
        sql_query = "SELECT t1_status FROM sportsgames WHERE matchname = {}".format(matchname)
    if "t2" in outcome:
        sql_query = "SELECT t2_status FROM sportsgames WHERE matchname = {}".format(matchname)
    if "draw" in outcome:
        sql_query = "SELECT draw_status FROM sportsgames WHERE matchname = {}".format(matchname)
    try:
        print("Matchname is")
        mycursor.execute(sql_query)
        print("Matchname is")
        result = mycursor.fetchone()
        if result[0] == 0:
            return False
        else:
            return True
    except Exception as e:
        print(e)



def grab_sportsgame_winners(matchname, outcome):
    matchname = '"' + matchname + '"'
    outcome = '"' + outcome + '"'
    sql_query = "SELECT charname, amount FROM sportsbet WHERE matchname = {} and outcome = {}".format(matchname,
                                                                                                      outcome)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchall()
        return result
    except Exception as e:
        print(e)

def grab_sportsgame_players(matchname):
    matchname = '"' + matchname + '"'
    sql_query = "SELECT charname, amount FROM sportsbet WHERE matchname = {}".format(matchname)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchall()
        return result
    except Exception as e:
        print(e)


def check_sportsgame_exists(matchname):
    matchname = '"' + matchname + '"'
    print("match name: ", matchname)
    try:
        sql_query = "SELECT EXISTS(SELECT * FROM sportsgames where matchname = {})".format(matchname)
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        print("Result is! ", result)
        if result[0] == 0:
            return False
        else:
            return True
    except Exception as e:
        print("Something went wrong!")
        return mycursor
        pass


def grab_discordid_from_sportsgame(charname, matchname):
    charname = '"' + charname + '"'
    matchname = '"' + matchname + '"'
    sql_query = "SELECT discordid FROM sportsbet where charname = {} and matchname = {}".format(charname, matchname)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchall()
        return result
    except Exception as e:
        print(e)

##END OF SPORTS GAMES


def check_my_active_player(discordid):
    if discordid in active_players:
        return active_players[discordid]
    else:
        return False


def set_active_player(discordid, charname):
    active_players[discordid] = charname


def check_charexists(charname):
    fullname = '"' + charname + '"'
    try:
        sql_query = "SELECT EXISTS(SELECT add_amount FROM characteraccs where charname = {})".format(fullname)
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        if result[0] == 0:
            return False
        else:
            return True
    except Exception as e:
        print("Something went wrong!")
        return mycursor
        pass


def grab_players_from_game(rafflegame):
    game = '"' + rafflegame + '"'
    sql_query = "SELECT charname, discordid FROM raffleticketbuyins where rafflename = {}".format(game)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchall()
        return result
    except Exception as e:
        print(e)


def grab_max_tickets_from_game(rafflegame):
    game = '"' + rafflegame + '"'
    sql_query = "SELECT max_tickets FROM rafflegamelist where rafflename = {}".format(game)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        return result[0]
    except Exception as e:
        print(e)


def grab_raffle_games():
    sql_query = "SELECT * FROM rafflegamelist"
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchall()
        return result
    except Exception as e:
        print(e)


def pick_raffle_winner(rafflegame):
    game = '"' + rafflegame + '"'
    sql_query = "SELECT charname FROM raffleticketbuyins where rafflename = {}".format(game)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchall()
        return result
    except Exception as e:
        print(e)


def count_rafflegame_tickets(rafflegame):
    game = '"' + rafflegame + '"'
    sql_query = "SELECT COUNT(*) FROM raffleticketbuyins where rafflename = {}".format(game)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchall()
        return result[0][0]
    except Exception as e:
        print(e)


def grab_char_balance(charname):
    fullname = '"' + charname + '"'
    try:
        sql_query = "SELECT balance FROM characteraccs where charname = {} LIMIT 1".format(fullname)
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        return result[0]
    except Exception as e:
        print("Something went wrong!")
        pass


def add_into_winner(charname, amount, game, date):
    game = '"' + game + '"'
    fullname = '"' + charname + '"'
    date = '"' + str(date) + '"'
    sql_query = "INSERT INTO winnerlogs (charname, amount, game, date) VALUES ({}, {}, {}, {})".format(fullname, amount,
                                                                                                       game, date)
    try:
        mycursor.execute(sql_query)
    except Exception as e:
        print(e)
    else:
        mydb.commit()
        return mycursor


def add_into_profitlogs(charname, amount, game, date):
    game = '"' + game + '"'
    fullname = '"' + charname + '"'
    date = '"' + str(date) + '"'
    sql_query = "INSERT INTO profitlogs (charname, amount, game, date) VALUES ({}, {}, {}, {})".format(fullname, amount,
                                                                                                       game, date)
    try:
        mycursor.execute(sql_query)
    except Exception as e:
        print(e)
    else:
        mydb.commit()
        return mycursor


def add_ticket_purchase(discordid, charname, amount, game):
    game = '"' + game + '"'
    fullname = '"' + charname + '"'
    sql_query = "INSERT INTO raffleticketbuyins (discordid, charname, rafflename, num_tickets) VALUES ({}, {}, {}, {})".format(
        discordid, fullname, game,
        amount)
    try:
        mycursor.execute(sql_query)
    except Exception as e:
        print(e)
    else:
        mydb.commit()
        return mycursor


def check_asset_transfer(discordid, rafflename):
    game = '"' + rafflename + '"'
    sql_query = "SELECT EXISTS(SELECT * FROM raffleticketbuyins where discordid = {} AND rafflename = {})".format(
        discordid, game)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        if result[0] == 0:
            return False
        else:
            return True
    except Exception as e:
        print(e)


def clear_game_tickets(game):
    game = '"' + game + '"'
    sql_query = "DELETE FROM raffleticketbuyins WHERE rafflename = {}".format(game)
    try:
        mycursor.execute(sql_query)
    except Exception as e:
        print(e)
    else:
        mydb.commit()
        return mycursor


def check_tickets_left(rafflename):
    game = '"' + rafflename + '"'
    sql_query = "SELECT max_tickets FROM rafflegamelist where rafflename = {}".format(game)
    sql_query2 = "SELECT SUM(num_tickets) FROM raffleticketbuyins where rafflename = {}".format(game)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        ticket_reqs = result[0]
        mycursor.execute(sql_query2)
        result = mycursor.fetchone()
        tickets_current = result[0]
        if tickets_current is not None:
            tickets_left = ticket_reqs - tickets_current
            return tickets_left
        else:
            return ticket_reqs
    except Exception as e:
        print(e)


def check_raffle_status(rafflename):
    game = '"' + rafflename + '"'
    sql_query = "SELECT max_tickets FROM rafflegamelist where rafflename = {}".format(game)
    sql_query2 = "SELECT SUM(num_tickets) FROM raffleticketbuyins where rafflename = {}".format(game)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        ticket_reqs = result[0]
        mycursor.execute(sql_query2)
        result = mycursor.fetchone()
        tickets_current = result[0]
        if ticket_reqs == tickets_current:
            return True
        else:
            return False
    except Exception as e:
        print(e)


def check_game_state(game):
    game = '"' + game + '"'
    sql_query = "SELECT enabled FROM gamestates where game = {}".format(game)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        return result[0]
    except Exception as e:
        print(e)


def check_ticket_price(game):
    game = '"' + game + '"'
    sql_query = "SELECT ticket_price FROM rafflegamelist where rafflename = {}".format(game)
    try:
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        print(result[0])
        return result[0]
    except Exception as e:
        print(e)


def set_game_state(state, game):
    game = '"' + game + '"'
    state = state
    sql_query = "UPDATE gamestates SET enabled = {} where game = {}".format(state, game)
    try:
        mycursor.execute(sql_query)
    except Exception as e:
        print(e)
    else:
        return mycursor


def check_enough_balance(charname, target_tb, target_col, amount):
    fullname = '"' + charname + '"'
    if not check_charexists(charname):
        return False
    else:
        try:
            sql_query = "SELECT {} FROM {} WHERE charname = {}".format(target_col, target_tb, fullname)
            mycursor.execute(sql_query)
            result = mycursor.fetchone()
        except Exception as e:
            print("Something went wrong!")
            return mycursor
            pass
        else:
            if result[0] < int(amount):
                return False
            else:
                return True


def change_balance(charname, amount, stay_pos):
    fullname = '"' + charname + '"'
    try:
        if stay_pos:
            sql_query2 = "UPDATE characteraccs SET balance = balance + {} where charname = {}".format(int(amount),
                                                                                                      fullname)
        else:
            sql_query2 = "UPDATE characteraccs SET balance = balance - {} where charname = {}".format(int(amount),
                                                                                                      fullname)
        mycursor.execute(sql_query2)
    except Exception as e:
        print("Uh oh!")
    else:
        mydb.commit()
        return mycursor


def money_since_when(table, dates):
    dates = '"' + dates + '"'
    try:
        print("Asdasdasd")
        sql_query = "SELECT SUM(amount) FROM {} where {} > {}".format(table, 'date', dates)
        mycursor.execute(sql_query)
        result = mycursor.fetchone()
        print("Adasda: ", result[0])
        return result[0]
    except Exception as e:
        print(e)

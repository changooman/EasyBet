import mysql.connector

mydb = mysql.connector.connect(
    host="",
    port='',
    user="",
    password="",
    database=""
)
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS masteraccs (discordid VARCHAR(100) PRIMARY KEY, ucpname VARCHAR(100), UNIQUE(ucpname))")
mycursor.execute("CREATE TABLE IF NOT EXISTS characteraccs (charname VARCHAR(100) PRIMARY KEY, ucpname VARCHAR(100), balance INT NOT NULL, add_amount BOOLEAN NOT NULL DEFAULT FALSE, take_amount BOOLEAN NOT NULL DEFAULT FALSE)")
mycursor.execute("CREATE TABLE IF NOT EXISTS addbalance (charname VARCHAR(100) PRIMARY KEY, ucpname VARCHAR(100), amount INT NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS takebalance (charname VARCHAR(100) PRIMARY KEY, ucpname VARCHAR(100), amount INT NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS winnerlogs (charname VARCHAR(100), amount INT NOT NULL, game VARCHAR(100), date DATETIME)")
mycursor.execute("CREATE TABLE IF NOT EXISTS profitlogs (charname VARCHAR(100), amount INT NOT NULL, game VARCHAR(100), date DATETIME)")
mycursor.execute("CREATE TABLE IF NOT EXISTS gamestates (game VARCHAR(100) PRIMARY KEY, enabled BOOLEAN NOT NULL DEFAULT FALSE)")
mycursor.execute("INSERT IGNORE INTO gamestates (game, enabled) VALUES ('Fruit Machine', TRUE)")
mycursor.execute("INSERT IGNORE INTO gamestates (game, enabled) VALUES ('Great Caverns', TRUE)")
mycursor.execute("INSERT IGNORE INTO gamestates (game, enabled) VALUES ('Cho Han', TRUE)")
mycursor.execute("INSERT IGNORE INTO gamestates (game, enabled) VALUES ('Raffles', TRUE)")
mycursor.execute("CREATE TABLE IF NOT EXISTS rafflegamelist (rafflename VARCHAR(100) PRIMARY KEY, max_tickets INT NOT NULL, ticket_price INT NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS raffleticketbuyins (discordid VARCHAR(100), charname VARCHAR(100), rafflename VARCHAR(100), num_tickets INT NOT NULL)")
mycursor.execute("INSERT IGNORE INTO rafflegamelist (rafflename, max_tickets, ticket_price) VALUES ('duel1', 2, 100)")
mycursor.execute("INSERT IGNORE INTO rafflegamelist (rafflename, max_tickets, ticket_price) VALUES ('duel2', 2, 100)")
mycursor.execute("INSERT IGNORE INTO rafflegamelist (rafflename, max_tickets, ticket_price) VALUES ('duel3', 2, 100)")
mycursor.execute("INSERT IGNORE INTO rafflegamelist (rafflename, max_tickets, ticket_price) VALUES ('br1', 5, 100)")
mycursor.execute("INSERT IGNORE INTO rafflegamelist (rafflename, max_tickets, ticket_price) VALUES ('br2', 5, 100)")
mycursor.execute("INSERT IGNORE INTO rafflegamelist (rafflename, max_tickets, ticket_price) VALUES ('br3', 5, 100)")
mycursor.execute("CREATE TABLE IF NOT EXISTS sportsgames (matchname VARCHAR(100) PRIMARY KEY, t1 VARCHAR(100), t2 VARCHAR(100), betstatus BOOLEAN NOT NULL DEFAULT FALSE, t1_status BOOLEAN NOT NULL DEFAULT FALSE, t2_status BOOLEAN NOT NULL DEFAULT FALSE, t1_odd FLOAT, t2_odd FLOAT, draw_status BOOLEAN NOT NULL DEFAULT FALSE, draw_odd FLOAT)")
mycursor.execute("CREATE TABLE IF NOT EXISTS sportsbet (discordid VARCHAR(100), charname VARCHAR(100), matchname VARCHAR(100), outcome VARCHAR(100), amount INT NOT NULL)")

mydb.commit()
mycursor.close()


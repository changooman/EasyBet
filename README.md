# **_EasyBet_**

A discord bot centered around gambling with pretend money. The registration system is designed to allow players to sign up using their discord account and then choose from a variety of games to play such as: Slots, Cho Han, Sports Betting, and Raffles

Information regarding player registration, player balances and logs for when a player wins or makes a stake is all kept in a MySQL database of the owner’s choosing. 

## Slot Machines

![image](https://user-images.githubusercontent.com/22184390/234155361-8d842a76-6f7c-4c2a-9eea-d6b00d2c0786.png) ![image](https://user-images.githubusercontent.com/22184390/234155274-d7e38ab1-c161-42db-a77a-1f4b90fed638.png)


**Ability to configure:**
* The description of the individual slot machine
* Emoji representation for each possible result
* Payout rules
* Define slot dimensions
* How much the player can stake
* Max # spins if player chooses the autospin 



## Cho Han (Dice Game Machine)

![image](https://user-images.githubusercontent.com/22184390/234155651-2e3b5662-2554-45a1-aaa8-2d779843020f.png)

**Ability to configure:**
* The description of the individual slot machine
* Emoji representation for each possible result
* Payout rules
* Define slot dimensions
* How much the player can stake
* Max # rolls if player chooses the autospin 
* Predictions the player can stake on 

## Raffles

![image](https://user-images.githubusercontent.com/22184390/234156414-2b0d7f55-97b1-4fcb-b709-3472f8fbcfe3.png)


Raffle games are preconfigured when the DB is launched but new ones can be added with calls to the DB 

**Ability to configure:**
* Available set of raffle games
* Raffle name
* Max number of tickets
* Price of each ticket

### Summary 
When the max number of tickets is reached for a game, a random winner is selected. A small percentage is taxed by the house and the rest is passed added onto the winner’s balance

## Sports Bets

**Ability to configure:**
* Predictions the player can stake on
* Minimum bet the player must stake
* Maximum bet the player can stake

## Support System:
* Add balance

![image](https://user-images.githubusercontent.com/22184390/234156543-70c386c2-b843-4f41-9587-81756d40e429.png)


* Withdraw balance

![image](https://user-images.githubusercontent.com/22184390/234156026-dcfa4d4b-fc18-4a9f-a537-6810ce8c7d2b.png)

* Register user (Requires user with admin role to verify)

* Player stakes in the discord bot’s direct messages for privacy 
* Emergency toggle to disable a game 

## Community:

![image](https://user-images.githubusercontent.com/22184390/234156243-235f8f15-349f-47ce-b2c7-d57ccbf22743.png)

![image](https://user-images.githubusercontent.com/22184390/234156207-92405a52-8d60-4a61-9822-e62a0d5aa196.png)

* Winnings Announcement channel when somebody wins big


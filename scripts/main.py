from locations import locations as baseLocations
from mobs import generateMobs
from ascii_art import showAscii
from combat import combat, useItem, chooseItem, roleStats, raceStats
from mobs import mobs
from scores import recordScore, showLeaderboard
from save_load import saveGame, saveExists, loadGame, deleteSave

from copy import deepcopy
#creates a copy of the locations data to not affect the original

#sets up the class to store character information
class character:

    #stores all character infor entered by user
    def __init__(self, name, age, gender, race, role):
        self.name = name
        self.age = age
        self.gender = gender
        self.race = race
        self.role = role

        #sets up the starting parameters
        self.inventory = []
        self.location = "Field"
        self.money = 0

        #sets your stats to the base
        classStats = roleStats[self.role.lower()]
        self.baseAtk = classStats["attack"]
        self.baseDef = classStats["defense"]
        self.baseSpeed = classStats["speed"]

        #applying race stat modifiers
        rStats = raceStats[self.race.lower()]
        self.baseAtk += rStats.get("attack", 0)
        self.baseDef += rStats.get("defense", 0)
        self.baseSpeed += rStats.get("speed", 0)

        self.baseMaxHP = 125
        self.maxHP = self.baseMaxHP
        self.health = self.maxHP

        #flag to see if tutorial is done
        self.tutorialDone = False

    #displays all the characters information
    def showInfo(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Gender: {self.gender}")
        print(f"Race: {self.race}")
        print(f"Role: {self.role}")

#declaring lists with all races and roles so they can be referred to throughout
#the code
races = ["Human", "Elf", "Orc", "Dwarf"]
roles = ["Knight", "Mage", "Archer", "Rogue"]
bossName = "Crazed Warlock"

#this sets the stats for the items you can get throughout
itemStats = {
    "Rusty Helmet": {
        "defense": 2
    },
    "Sturdy Chestplate": {
        "defense": 4
    },
    "Rune of Vigor": {
        "maxHP": 25
    },
    "Rune of Enhancement": {
        "attack": 5
    }
}

#method that hold all the save data
def playerFromSave(playerData):
    #hold the information provided by the player at the beginning
    p = character (
        playerData["name"],
        playerData["age"],
        playerData["gender"],
        playerData["race"],
        playerData["role"],
    )

    #holds values like money, the inventory and location data
    p.location = playerData.get("location", "Field")
    p.money = playerData.get("money", 0)
    p.inventory = playerData.get("inventory", [])
    p.tutorialDone = playerData.get("tutorialDone", False)

    #holds the players health and their maximum health points
    p.baseMaxHP = playerData.get("baseMaxHP", p.baseMaxHP)
    p.maxHP = playerData.get("maxHP", p.maxHP)
    p.health = playerData.get("health", p.health)

    p.bonusAtk = 0
    p.bonusDef = 0
    p.bonusHP = 0

    #after your items change it will recalculate your current stats
    recalcStats(p)

    #if the players health exceeds the max or is lower than 0 it will set the health to what it should be in these edge cases
    if p.health > p.maxHP:
        p.health = p.maxHP
    if p.health < 0:
        p.health = 0

    return p

#a simple function to clear the console
def clearScreen():
    print("\n" * 50)

#pauses the game until the player is ready to move on
def pause():
    input("\nPress enter to continue...")

#this is a brief tutorial that is shown to the player to inform how to play
def showTutorial(player):
    clearScreen()
    print("=== Tutorial: Combat Basics ===\n")
    print("Combat starts automatically when you enter a room with enemies.\n")

    print("1) Attacking")
    print("- Your damage is based on your class, race and the luck of the dice.")
    print("- Each attack rolls random numbers, then your class attack stat is added.\n")

    print("2) Defending")
    print("- Enemies also roll for damage.")
    print("- Your defense stat reduces the damage you take (also roll-based).\n")

    print("3) Actions")
    print("- On your turn you can: attack, use an item, or attempt to flee.")
    print("- Using an item may still allow an attack if your Speed is high enough.\n")

    print("4) Fleeing")
    print("- Flee chance depends on your Speed compared to the enemy.")
    print("- If you flee successfully, you return to the room you came from.\n")

    print(f"Your class: {player.role.capitalize()}")
    print("Good luck!\n")

    input("Press Enter to begin the tutorial fight...")

#the function to recalculate the players stats
def recalcStats(player):
    #sets the bonus' to 0
    player.bonusAtk = 0
    player.bonusDef = 0
    player.bonusHP = 0

    #runs through the items in the inventory and grants their effects if applicable
    for item in player.inventory:
        effects = itemStats.get(item)
        if not effects:
            continue

        #adds the correct bonus to the base stats
        player.bonusAtk += effects.get("attack", 0)
        player.bonusDef += effects.get("defense", 0)
        player.bonusHP += effects.get("maxHP", 0)

    #inceases the maxhp by the amount of bonus you have and the base hp
    player.maxHP = player.baseMaxHP + player.bonusHP

    #if the player health then exceeds the max it will set it to the maximum value
    if player.health > player.maxHP:
        player.health = player.maxHP

#the function to give the player an item
def awardItemsOnce(player, room):
    #checks if the room has an item, if not ends the function
    items = room.get("items", [])
    if not items:
        return

    #shows a message telling you the item you got and appends it to the inventory
    print("\nYou have found:")
    for item in items:
        item = item.strip()
        player.inventory.append(item)
        print(f"- {item}")

    #removes the item from the room and recalculates the players stats while pausing the game
    room["items"] = []
    recalcStats(player)
    pause()

#runs at the beginning to create the character
def createCharacter():
    while True:

        #prints the introductory messages
        print("Welcome to the game!")
        print("Character Creation:")
        print("===================")

        #asks the user for a name and checks that its valid
        while True:
            name = input("\nEnter character name: ")
            if name.isalpha():
                name = name.capitalize()
                break
            else:
                print("Please enter a valid name (letters only)")

        #asks user for an age and checks it is valid
        while True:
            age = input("\nEnter character age: ")

            if not age.isnumeric():
                print("Please enter a valid age (numbers only) (20 - 65)")
                continue

            age = int(age)  # convert to integer

            #makes sure the age is between 20 and 65
            if age > 65:
                print("You are too old for this adventure!")
                print("Please enter a valid age (20 - 65)")
            elif age < 20:
                print("You are too young for this adventure!")
                print("Please enter a valid age (20 - 65)")
            else:
                break

        while True:
            print("\nPlease choose a race:")

            #loops through the races displaying them
            for r in races:
                print(f"- {r}")
            #sets the race to the players input
            race = input().strip().capitalize()

            #if what is entered it asks for another, otherwise the program continues
            if race not in races:
                print("Please enter a valid race.")
            else:
                break

        #asks the user for their gender and checks its valid
        while True:
            gender = input('\nEnter characters gender (Male or Female): ')
            if gender.lower() == 'male' or gender.lower() =='female':
                break
            else:
                print('Please enter male or female')

        #asks the user for the class they wish to play (or role) and checks its valid
        while True:
            print("\nPlease choose a class:")

            #displays all roles in a user-friendly way
            for c in roles:
                print(f"- {c}")

            #strips and capitalises the input so it can be compared to the list
            role = input().strip().capitalize()

            #if what is entered is not valid it asks the user to enter another class
            if role not in roles:
                print("Please enter a valid class.")
            else:
                break

        break

    #returns this to the character class
    return character(name, age, gender, race, role)

#the fucntion to build a new location
def buildNewLocations():
    #creates a copy of the locations data to not interfere with the hard copy
    locations = deepcopy(baseLocations)

    #loops through the locations and generates the correct mobs using a function if they should be
    for locationData in locations.values():
        if "spawn" in locationData:
            locationData["mobs"] = generateMobs(locationData["spawn"])
        else:
            #otherwise it clears the mobs
            locationData["mobs"] = []

    return locations

#the function that starts the game
def startGame():
    #checks if a save exists if so it lets the player load a save
    if saveExists():
        choice = input("\nA saved game was found, would you like to continue? (y/n): ").strip().lower()
        while choice not in ["y", "n"]:
            choice = input("\nPlease choose a choice (y/n): ").strip().lower()

        if choice == "y":
            #if the player chooses the load the save it sets that to the current load
            loaded = loadGame()
            if loaded is not None:
                #if there is saved data it sets all relevant variables to that save
                playerData, savedLocations = loaded
                player = playerFromSave(playerData)

                locations = savedLocations

                playGame(player, locations)
                return
        #then removes the save
        deleteSave()

    #runs the create character methods, builds the locations and runs play game
    player = createCharacter()
    locations = buildNewLocations()
    playGame(player, locations)

#main gameplay loop
def playGame(player, locations):
    turns = 0

    #message to start the adventure
    print(f"\nWelcome, {player.name}! You begin in the {player.location}...\n")
    print("Loading...")
    pause()

    #sets the last visited and previous locations visited
    lastLocation = None
    previousLocation = None

    #sets the avaliable commands
    commands = ["north", "south", "east", "west", "inventory", "use", "help", "quit"]

    while True:

        #gets the players location
        current = locations[player.location]
        enteredNewLocation = (player.location != lastLocation)

        #when you enter a new location it clears the console and shows the art while setting your previous location for fleeing
        if enteredNewLocation:
            clearScreen()
            showAscii(player.location)
            lastLocation = player.location

            #if the player is in the starting location and the tutorial is not done it shows it and sets it to complete
            if player.location == "Field" and not getattr(player, "tutorialDone", False):
                showTutorial(player)
                player.tutorialDone = True

        #prints the current location and the description given with it
        print(f"\n== {player.location} ==")
        print(current["description"])

        print("\nExits:")

        #checks to see if the current location has exits
        hasExits = False
        for direction in ["north", "south", "east", "west"]:
            if direction in current:
                exit_data = current[direction]

                #if the exit is stored as a dict it means it's locked or otherwise different
                if isinstance(exit_data, dict):
                    dest = exit_data.get("destination", "Unknown")
                    if exit_data.get("locked"):
                        print(f"- {direction.capitalize()}: {dest} (Locked)")
                    else:
                        print(f"- {direction.capitalize()}: {dest}")
                else:
                    print(f"- {direction.capitalize()}: {exit_data}")

                hasExits = True

        #displays all mobs in an area
        if current.get("mobs"):
            mobCounts = {}

            for mob in current["mobs"]:
                if mob in mobCounts:
                    mobCounts[mob] += 1
                else:
                    mobCounts[mob] = 1
                #counts the amount of enemies in the area

            totalEnemies = sum(mobCounts.values())
            #tallies this into total enemies

            if totalEnemies == 1:
                print("\nEnemy present:")
            else:
                print("\nEnemies present:")
                #prints an appropriate message informing the player of the enemies in the area

            for mob, count in mobCounts.items():
                if count == 1:
                    print(f"- {mob.capitalize()}")
                else:
                    print(f"- {mob.capitalize()} x{count}")
                    #prints out all the enemies in the area in a list through a for loop

        #starts combat only on room entry
        if enteredNewLocation and current.get("mobs") and len(current["mobs"]) > 0:
            fled = False
            # fight one enemy at a time until clear, flee, or death
            while current.get("mobs") and len(current["mobs"]) > 0:
                enemyName = current["mobs"][0]
                outcome = combat(player, enemyName, mobs)  # returns dict

                if outcome["result"] == "won":
                    defeated = current["mobs"][0]
                    # remove defeated enemy
                    current["mobs"].pop(0)

                    # add money for killed enemy
                    player.money += outcome["money"]
                    print(f"You gained {outcome['money']} coins")
                    print(f"Total coins: {player.money}")

                    #if the boss is defeated it displays the victory message
                    if defeated == bossName:
                        print("\n=== VICTORY ===")
                        print("The Crazed Warlock falls... The castle goes silent at long last.")
                        showAscii("win")
                        pause()

                        #gets the players score and shows the leaderboard
                        recordScore(player, outcome="win", turns=turns)
                        showLeaderboard(10)
                        return

                    # room clear reward
                    if len(current["mobs"]) == 0:
                        awardItemsOnce(player, current)

                    continue

                #if you flee combat it takes you back to the previous location if there is one
                if outcome["result"] == "fled":
                    if previousLocation is not None:
                        print(f"You flee back to {previousLocation}!")
                        player.location = previousLocation

                        #then clears the last location
                        lastLocation = None
                        fled = True
                        #if there is nowhere to flee it shows a message
                    else:
                        print("You have nowhere to flee to!")
                    break

                #if combat results in a death it shows a game over and the scoreboard
                if outcome["result"] == "dead":
                    print("Game Over!")
                    recordScore(player, outcome="dead", turns=turns)
                    showLeaderboard(10)
                    return

            if fled:
                continue

        #if you enter a new location and there's no mobs it awards the items for the area
        if enteredNewLocation:
            noMobs = (not current.get("mobs")) or (len(current.get("mobs", [])) == 0)
            if noMobs:
                awardItemsOnce(player, current)
        #asks the user for a command and then compares it with the list of commands to make sure its valid
        cmd = input("\nEnter command: (North, South, East, West, Inventory, Use, Quit): ").strip().lower()
        while cmd not in commands:
            cmd = input("Please enter a valid command: ").strip().lower()

        turns += 1

        #handles all non-movement commands
        if cmd == "inventory":
            print(f"Coins: {player.money}")
            print(f"HP: {player.health}/{player.maxHP}")
            print(f"Defense: {player.baseDef + player.bonusDef}")
            if player.inventory:
                print("You are carrying:")
                for item in player.inventory:
                    print(f"- {item}")
            else:
                print("Your inventory is empty")
            continue

        #if use is entered it lets the player select and item to use
        if cmd == "use":
            itemName = chooseItem(player)
            if itemName:
                useItem(player, itemName)
            continue

        #if you quit it saves your game and records your score before showing the leaderboard and displaying appropriate messages
        if cmd == "quit":
            print("Thanks for playing!")
            print("Saving game...")

            saveGame(player, locations, turns=turns)

            recordScore(player, outcome="quit", turns=turns)
            showLeaderboard(10)

            break

        #handles movement commands
        if cmd not in current:
            print("You can't go that way!")
            continue

        #stores where the player wants to go next
        exitData = current[cmd]
        oldLocation = player.location

        #tracks if movement happened for combat

        if isinstance(exitData, dict):
            if exitData.get("locked"):
                #checks if the exit is locked
                if exitData.get("key") in player.inventory:
                    #if so it checks the players inventory for a key
                    needed_key = exitData.get("key")
                    print(f"\nYou unlock the path using the {needed_key}")
                    exitData["locked"] = False
                    player.location = exitData["destination"]
                    previousLocation = oldLocation
                    #if so the way is unlocked and a message is printed before taking you to the next location
                else:
                    print("The way is locked. You need a key")
                    #otherwise it tells you a key is needed (staying put)
            else:
                player.location = exitData["destination"]
                previousLocation = oldLocation
                #if it is not locked sends the player to the desired destination
        else:
            player.location = exitData
            previousLocation = oldLocation
            #normal exits are just destination strings

startGame()
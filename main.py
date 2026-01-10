import os
from locations import locations as baseLocations
from mobs import generateMobs
from scripts.ascii_art import showAscii

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
        self.health = 100
        self.location = "Field"
        self.money = 0

    #displays all the characters information
    def showInfo(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Gender: {self.gender}")
        print(f"Race: {self.race}")
        print(f"Role: {self.role}")

#declaring lists with all races and roles so they can be referred to throughout
#the code
races = ["Human", "Elf", "Orc", "Dwarf", "Goblin"]
roles = ["Knight", "Mage", "Archer", "Cleric", "Rogue"]

roleStats = {
    #establishes the different statistics of the roles you can choose between
    "knight": {"attack": 5, "defense": 5, "heal": 0, "speed": 2}, #block? + higher health pool
    "mage": {"attack": 9, "defense": 2, "heal": 1, "speed": 3}, #casts shield that tanks one hit + option to charge up an attack one turn and do a big hit the next
    "archer": {"attack": 7, "defense": 3, "heal": 0, "speed": 5}, #dodge chance 30% + extra turn at beginning (close the distance)
    "cleric": {"attack": 2, "defense": 4, "heal": 6, "speed": 3}, #self-heal on turn
    "rogue": {"attack": 6, "defense": 4, "heal": 0, "speed": 5}, #two actions per turn (50% chance)
}

#a simple function to clear the console
def clearScreen():
    print("\n" * 50)

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

        #asks the user for their race and checks its valid
        while True:
            print("\nPlease choose a race:")

            for r in races:
                print(f"- {r}")

            race = input().strip().capitalize()

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

            if role not in roles:
                print("Please enter a valid class.")
            else:
                break

        break

    #returns this to the character class
    return character(name, age, gender, race, role)


#main gameplay loop
def playGame(player, locations):

    #message to start the adventure
    print(f"\nWelcome, {player.name}! You begin in the {player.location}...\n")

    lastLocation = None

    commands = ["north", "south", "east", "west", "inventory", "help", "quit"]

    while True:

        #gets the players location
        current = locations[player.location]

        if player.location != lastLocation:
            clearScreen()
            showAscii(player.location)
            lastLocation = player.location

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

        #asks the user for a command and then compares it with the list of commands to make sure its valid
        cmd = input("\nEnter command: (North, South, East, West, Inventory, Help, Quit): ").strip().lower()
        while cmd not in commands:
            cmd = input("Please enter a valid command: ").strip().lower()

        #handles all non-movement commands
        if cmd == "inventory":
            if player.inventory:
                print("You are carrying:")
                for item in player.inventory:
                    print(f"- {item}")
            else:
                print("Your inventory is empty")
            continue

        if cmd == "help":
            print("Commands: North, South, East, West, Inventory, Help, Quit")
            continue

        if cmd == "quit":
            print("Thanks for playing!")
            #save shit to file here
            #update_scores()
            break

        #handles movement commands
        if cmd not in current:
            print("You can't go that way!")
            continue

        #stores where the player wants to go next
        exitData = current[cmd]

        if isinstance(exitData, dict):
            if exitData.get("locked"):
                #checks if the exit is locked
                if exitData.get("key") in player.inventory:
                    #if so it checks the players inventory for a key
                    needed_key = exitData.get("key")
                    print(f"\nYou unlock the path using the {needed_key}")
                    exitData["locked"] = False
                    player.location = exitData["destination"]
                    #if so the way is unlocked and a message is printed before taking you to the next location
                else:
                    print("The way is locked. You need a key")
                    #otherwise it tells you a key is needed (stay put)
            else:
                player.location = exitData["destination"]
                #if it is not locked sends the player to the desired destination
        else:
            player.location = exitData
            #normal exits are just destination strings

#creates the player character
player = createCharacter()

#creates a copy of all the locations so the original doesn't change in runtime
locations = deepcopy(baseLocations)
for locationData in locations.values():
    #checking to see if there is any attached enemy data
    if "spawn" in locationData:
        #generating enemies for the location
        locationData["mobs"] = generateMobs(locationData["spawn"])
    else:
        locationData["mobs"] = []

playGame(player, locations)
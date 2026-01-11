from locations import locations as baseLocations
from mobs import generateMobs
from scripts.ascii_art import showAscii
from combat import combat
from mobs import mobs

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
races = ["Human", "Elf", "Orc", "Dwarf", "Goblin"]
roles = ["Knight", "Mage", "Archer", "Cleric", "Rogue"]

#a simple function to clear the console
def clearScreen():
    print("\n" * 50)

def pause():
    input("\nPress enter to continue...")

def showTutorial(player):
    clearScreen()
    print("=== Tutorial: Combat Basics ===\n")
    print("Combat starts automatically when you enter a room with enemies.\n")

    print("1) Attacking")
    print("- Your damage is based on your class and the luck of the dice.")
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
    print("Loading...")
    pause()

    lastLocation = None
    previousLocation = None

    commands = ["north", "south", "east", "west", "inventory", "help", "quit"]

    while True:

        #gets the players location
        current = locations[player.location]
        enteredNewLocation = (player.location != lastLocation)


        if enteredNewLocation:
            clearScreen()
            showAscii(player.location)
            lastLocation = player.location

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
            # fight one enemy at a time until clear, flee, or death
            while current.get("mobs") and len(current["mobs"]) > 0:
                enemyName = current["mobs"][0]
                outcome = combat(player, enemyName, mobs)  # returns dict

                if outcome["result"] == "won":
                    # remove defeated enemy
                    current["mobs"].pop(0)

                    # add money for killed enemy
                    player.money += outcome["money"]
                    print(f"You gained {outcome['money']} coins")
                    print(f"Total coins: {player.money}")

                    # room clear reward
                    if len(current["mobs"]) == 0:
                        roomItem = current.get("item", "")
                        if roomItem:
                            player.inventory.append(roomItem)
                            print(f"You found: {roomItem}")
                            current["item"] = ""

                        pause()  # pause so player can read rewards

                    continue

                if outcome["result"] == "fled":
                    if previousLocation is not None:
                        print(f"You flee back to {previousLocation}!")
                        player.location = previousLocation
                    else:
                        print("You have nowhere to flee to!")
                    break

                if outcome["result"] == "dead":
                    print("Game Over!")
                    return

        #asks the user for a command and then compares it with the list of commands to make sure its valid
        cmd = input("\nEnter command: (North, South, East, West, Inventory, Help, Quit): ").strip().lower()
        while cmd not in commands:
            cmd = input("Please enter a valid command: ").strip().lower()

        #handles all non-movement commands
        if cmd == "inventory":
            print(f"Coins: {player.money}")
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
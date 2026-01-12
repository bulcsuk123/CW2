import json
import os

#sets the save data as a json
savePath = os.path.join("../data", "savegame.json")

#makes sure the save json was created
def ensureDataFolder():
    os.makedirs(os.path.dirname(savePath), exist_ok=True)

#returns the save path as bool
def saveExists() -> bool:
    return os.path.exists(savePath)

#function to save the game
def saveGame(player, locations, turns: int = 0) -> None:
    ensureDataFolder()

    #saves all relevant data in this format
    data = {
        "player": {
            "name": player.name,
            "age": player.age,
            "gender": player.gender,
            "race": player.race,
            "role": player.role,

            "location": player.location,
            "health": player.health,
            "maxHP": player.maxHP,
            "baseMaxHP": player.baseMaxHP,

            "money": player.money,
            "inventory": list(player.inventory),

            "tutorialDone": getattr(player, "tutorialDone", False),

            # Save stat fields too (safe and helps debugging)
            "baseAtk": getattr(player, "baseAtk", 0),
            "baseDef": getattr(player, "baseDef", 0),
            "bonusAtk": getattr(player, "bonusAtk", 0),
            "bonusDef": getattr(player, "bonusDef", 0),
            "bonusHP": getattr(player, "bonusHP", 0),

            "turns": turns,
        },
        "locations": locations,
    }

    #open the save file
    with open(savePath, "w", encoding="utf-8") as f:
        #converts game state to json with indentation
        json.dump(data, f, indent=2)


def loadGame():
    #checks if a save exists
    if not saveExists():
        return None

    #opens the save file in read mode and reads/loads contents
    with open(savePath, "r", encoding="utf-8") as f:
        data = json.load(f)

    #returns the save data
    return data.get("player"), data.get("locations")

#removes the save path
def deleteSave():
    if saveExists():
        os.remove(savePath)
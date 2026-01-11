import json
import os

savePath = os.path.join("data", "savegame.json")

def ensureDataFolder():
    os.makedirs(os.path.dirname(savePath), exist_ok=True)


def saveExists() -> bool:
    return os.path.exists(savePath)


def saveGame(player, locations, turns: int = 0) -> None:
    ensureDataFolder()

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

    with open(savePath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def loadGame():
    if not saveExists():
        return None

    with open(savePath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("player"), data.get("locations")


def deleteSave():
    if saveExists():
        os.remove(savePath)
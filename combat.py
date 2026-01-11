import random
from scripts.ascii_art import showAscii
import time

roleStats = {
    #establishes the different statistics of the roles you can choose between
    "knight": {"attack": 6, "defense": 6,"speed": 2},
    "mage": {"attack": 9, "defense": 2, "speed": 3},
    "archer": {"attack": 7, "defense": 3,  "speed": 4},
    "rogue": {"attack": 6, "defense": 4, "speed": 4},
}

raceStats = {
    "human": {"attack": 2, "defense": 0, "speed": 2},
    "elf": {"attack": 2,"defense": 0,"speed": 2},
    "orc": {"attack": 1,"defense": 3,"speed": 0},
    "dwarf": {"attack": 3,"defense": 1,"speed": 0},
}

maxHp = 125

itemEffects = {
    "Health Potion": {"type": "heal", "min": 20, "max": 45}
    #add more eg better health potions
}

def clamp(n , lo, hi):
    return lo if n < lo else hi if n > hi else n

def rollAttack(baseAttack : int) -> int:
    return random.randint(1, 6) + random.randint(1, 6) + baseAttack

def rollDefense(baseDefense : int) -> int:
    return random.randint(1, 6) + baseDefense

def resolveDmg(attRoll : int, defRoll : int) -> int:
    dmg = attRoll - (defRoll // 2)
    return max(1, dmg)

def doubleAction(speed: int) -> bool:
    if speed >= 5:
        return True
    if speed >= 3:
        return random.random() < 0.25
    return random.random() < 0.10

def fleeSuccess(playerSpeed : int, mobSpeed : int) -> tuple[bool, int]:
    #base flee chance of 30% which is then modified by speed difference of mob and player
    chance = 0.3 + 0.1 * (playerSpeed - mobSpeed)
    chance = clamp(chance, 0.05, 0.85)
    return (random.random() < chance), int(chance * 100)

def usableItem(itemName : str) -> bool:
    return itemName in itemEffects

def chooseItem(player):
    usable = [item for item in player.inventory if usableItem(item)]

    if not usable:
        print("You have no usable items (like potions)")
        return None

    print("\nUsable items:")
    for i, item in enumerate(usable, start=1):
        print(f"{i}. {item}")

    choice = input("Choose and item (number or 'back'): ").strip().lower()
    if choice == "back":
        return None
    if not choice.isdigit():
        print("Invalid choice")
        return None

    idx = int(choice) - 1
    if idx < 0 or idx >= len(usable):
        print("Invalid choice")
        return None

    return usable[idx]

def useItem(player, itemName : str) -> bool:
    effect = itemEffects.get(itemName)
    if not effect:
        print(f"{itemName} cannot be used right now!")
        return False

    if effect["type"] == "heal":
        healAmount = random.randint(effect["min"], effect["max"])
        oldHealth = player.health
        player.health = min(maxHp, player.health + healAmount)
        player.inventory.remove(itemName)
        print(f"You have used {itemName}! And healed {player.health - oldHealth} HP. (HP: {player.health}/{maxHp})")
        return True

    return False

def combat(player, mobName: str, mobsDb: dict) -> dict:

    if not hasattr(player, "bonusAtk"):
        player.bonusAtk = 0
    if not hasattr(player, "bonusDef"):
        player.bonusDef = 0
    if not hasattr(player, "bonusHP"):
        player.bonusHP = 0

    template = mobsDb[mobName]
    enemy = {
        "name": mobName,
        "hp": template["health"],
        "atk": template["attack"],
        "def": template["defense"],
        "money": template.get("money", 0),
        "desc": template.get("description", ""),
        "speed": template.get("speed", 3)
    }

    print("\nCombat Begins!")
    if enemy["desc"]:
        print(enemy["desc"])

    #final boss monologue
    if mobName == "Crazed Warlock":
        print(f"A {player.race} huh? To think after all those years it was one of you who bested my right hand...")
        print("-")
        time.sleep(3)
        print(f"You know I think I've heard the name {player.name} before. You're quite famous you know that?...")
        print("The true heir to the throne some say, come to reclaim your birthright?...")
        print("Well I guess it's only natural for you to want revenge given how I've puppeteered your ancestors corpses for years now...")
        print("-")
        time.sleep(3)
        print("I wish you the best of luck in our battle but I will warn you that seeing as I no longer have guard for the castle")
        print("I think your skills would do nicely to fill the role")

    if mobName == "The Groundskeeper":
        print(f"I haven't seen you in years {player.name}, I'm sorry that I failed to guard your history . . .")
        time.sleep(2)
        print("but the wheels of fate have turned too far towards the dark . . .")
        time.sleep(2)
        print("I'm sorry, but my will is not my own... I urge you to flee.")
        time.sleep(2)

    while enemy["hp"] > 0 and player.health > 0:
        print(f"\nYour HP: {player.health}/{player.maxHP}")
        print(f"{enemy['name']} HP: {enemy['hp']}")

        action = input("Choose an action: (attack/item/flee) ").strip().lower()
        while action not in ["attack", "item", "flee"]:
            action = input("Choose an action: (attack/item/flee) ").strip().lower()

        # player's turn
        if action == "attack":
            att = rollAttack(player.baseAtk + player.bonusAtk)
            dfn = rollDefense(enemy["def"])
            dmg = resolveDmg(att, dfn)
            enemy["hp"] -= dmg
            print(f"You hit {enemy['name']} for {dmg} damage!")

        elif action == "item":
            itemName = chooseItem(player)
            if itemName:
                used = useItem(player, itemName)
                if used and enemy["hp"] > 0:
                    # use TOTAL player speed (class + race)
                    if doubleAction(player.baseSpeed):
                        print("You are quick enough to attack after using the item!")
                        att = rollAttack(player.baseAtk + player.bonusAtk)
                        dfn = rollDefense(enemy["def"])
                        dmg = resolveDmg(att, dfn)
                        enemy["hp"] -= dmg
                        print(f"You hit {enemy['name']} for {dmg} damage!")
                    else:
                        print("You don't have enough time to attack after using the item!")

        elif action == "flee":
            if mobName == "Crazed Warlock":
                print(f"\n{enemy['name']} raises a hand and the doors slam shut...")
                print("A crushing pressure grips your chest—you cannot flee!")
                continue

            # use TOTAL player speed (class + race)
            success, pct = fleeSuccess(player.baseSpeed, enemy["speed"])
            if success:
                print(f"You escaped! (Chance was ~{pct}%)")
                return {"result": "fled", "money": 0}
            else:
                print(f"You failed to escape! (Chance was ~{pct}%)")

        if enemy["hp"] <= 0:
            print(f"\nYou defeated {enemy['name']}!")
            return {"result": "won", "money": enemy["money"]}

        # mob turn
        mAtt = rollAttack(enemy["atk"])
        pDef = rollDefense(player.baseDef + player.bonusDef)
        dmgTaken = resolveDmg(mAtt, pDef)
        player.health -= dmgTaken
        print(f"{enemy['name']} hit you for {dmgTaken} damage! (HP: {player.health}/{player.maxHP})")

    showAscii("Game Over")
    print("\nYou have been killed...")
    return {"result": "dead", "money": 0}
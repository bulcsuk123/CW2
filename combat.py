import random

roleStats = {
    #establishes the different statistics of the roles you can choose between
    "knight": {"attack": 5, "defense": 5, "heal": 0, "speed": 2}, #block? + higher health pool
    "mage": {"attack": 9, "defense": 2, "heal": 1, "speed": 3}, #casts shield that tanks one hit + option to charge up an attack one turn and do a big hit the next
    "archer": {"attack": 7, "defense": 3, "heal": 0, "speed": 5}, #dodge chance 30% + extra turn at beginning (close the distance)
    "cleric": {"attack": 2, "defense": 4, "heal": 6, "speed": 3}, #self-heal on turn
    "rogue": {"attack": 6, "defense": 4, "heal": 0, "speed": 5}, #two actions per turn (50% chance)
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

def doubleAction(speed : int) -> int:
    if speed >= 5:
        return True
    if speed >= 3:
        return random.random() < 0.25

    return random.random() < 0.25

def fleeSuccess(playerSpeed : int, mobSpeed : int) -> tuple[bool, int]:
    #base flee chance of 30% which is then modified by speed difference of mob and player
    chance = 0.3 + 0.1 * (playerSpeed - mobSpeed)
    chance = clamp(chance, 0.05, 0.85)
    return (random.random() < chance), int(chance * 100)

def chooseItem(player):
    if not player.inventory:
        print("You have no items to use!")
        return None

    print("\nInventory:")
    for i, item in enumerate(player.inventory, start = 1):
        print(f"{i}. {item}")

    choice = input("Choose an item: (number or 'back')").strip().lower()
    if choice == "back":
        return None
    if not choice.isdigit():
        print("You have to choose a number!")
        return None

    idx = int(choice) - 1
    if idx < 0 or idx >= len(player.inventory):
        print("Invalid choice!")
        return None

    return player.inventory[idx]

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

def combat(player, mobName : str, mobsDb : dict) -> dict:

    role = player.role.lower()
    pstats = roleStats[role]

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

    while enemy["hp"] > 0 and player.health > 0:
        print(f"\nYour HP: {player.health}/{maxHp}")
        print(f"\n{enemy['name']} HP: {enemy['hp']}")

        action = input("Choose an action: (attack/item/flee)").strip().lower()
        while action not in ["attack", "item", "flee"]:
            action = input("Choose an action: (attack/item/flee)").strip().lower()

        #player's turn
        if action == "attack":
            att = rollAttack(pstats["attack"])
            dfn = rollDefense(enemy["def"])
            dmg = resolveDmg(att, dfn)
            enemy["hp"] -= dmg
            print(f"You hit {enemy['name']} for {dmg} damage!")

        elif action == "item":
            itemName = chooseItem(player)
            if itemName:
                used = useItem(player, itemName)
                if used and enemy["hp"] > 0:
                    if doubleAction(pstats["speed"]):
                        print("You are quick enough to attack after using the item!")
                        att = rollAttack(pstats["attack"])
                        dfn = rollDefense(enemy["def"])
                        dmg = resolveDmg(att, dfn)
                        enemy["hp"] -= dmg
                        print(f"You hit {enemy['name']} for {dmg} damage!")
                    else:
                        print("You don't have enough time to attack after using the item!")

        elif action == "flee":
            success, pct = fleeSuccess(pstats["speed"], enemy["speed"])
            if success:
                print(f"You escaped! (Chance was ~{pct})%")
                return {"result": "fled", "money": 0}
            else:
                print(f"You failed to escape! (Chance was ~{pct}%)")

        if enemy["hp"] <= 0:
            print(f"\nYou defeated {enemy['name']}!")
            return {"result": "won", "money": enemy["money"]}

        #mob turn
        mAtt = rollAttack(enemy["atk"])
        pDef = rollDefense(pstats["defense"])
        dmgTaken = resolveDmg(mAtt, pDef)
        player.health -= dmgTaken
        print(f"{enemy['name']} hit you for {dmgTaken} damage! (HP: {player.health}/{maxHp})")

    print("\nYou have been killed...")
    return {"result": "dead", "money": 0}
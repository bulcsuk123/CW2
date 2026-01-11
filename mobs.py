import random

mobs = {
    #cave
    "Armoured Skeleton": {
        "description": "A rattling skeleton in dented plate armour drags a rusted blade across the stone, its empty gaze fixed on you . . .",
        "health": 10,
        "attack": 5,
        "defense": 4,
        "speed": 2,
        "money": 5,
    },

    #cave
    "Giant Cave Spider": {
        "description": "An eight legged horror with coarse black hair and a monstrous form, towering over children . . .",
        "health": 7,
        "attack": 4,
        "defense": 4,
        "speed": 5,
        "money": 5,
    },

    #beach
    "Siren": {
        "description": "A siren stands by the surf, her song twisting the air into something sweet and dangerous . . .",
        "health": 15,
        "attack": 7,
        "defense": 4,
        "speed": 4,
        "money": 20,
    },

    #beach
    "Sand Crab": {
        "description": "A small creature with a thick exoskeleton that burrows under sand waiting for the perfect moment to strike . . .",
        "health": 10,
        "attack": 4,
        "defense": 2,
        "speed": 4,
        "money": 5,
    },

    #forest
    "Treant": {
        "description": "A towering treant shifts from the trees themselves, bark creaking as it raises branch-like arms to strike . . .",
        "health": 30,
        "attack": 5,
        "defense": 5,
        "speed": 2,
        "money": 15,
    },

    #forest
    "Hobgoblin": {
        "description": "A scarred hobgoblin steps into your path with a cruel grin, gripping a chipped weapon tightly . . .",
        "health": 20,
        "attack": 6,
        "defense": 4,
        "speed": 4,
        "money": 20,
    },

    #field
    "Ghoul": {
        "description": "A hunched ghoul crawls through the grass, sniffing the air before lunging toward you with feral hunger . . .",
        "health": 2,
        "attack": 2,
        "defense": 2,
        "speed": 2,
        "money": 2,
    },

    #castle entrance
    "Undead Warrior": {
        "description": "An undead warrior blocks the gateway, its armour cracked and blackened, yet it moves with grim purpose . . .",
        "health": 25,
        "attack": 5,
        "defense": 5,
        "speed": 2,
        "money": 10,
    },

    #castle entrance
    "Undead Archer": {
        "description": "An undead Archer standing distant at the entrance to the castle, bows withered yet still drawn as it prepares to defend its castle one last time . . .",
        "health": 20,
        "attack": 7,
        "defense": 3,
        "speed": 4,
        "money": 5,
    },

    #castle grounds (medium bad)()
    "The Groundskeeper": {
        "description": "The castle's groundskeeper shuffles forward with broadsword in hand, eyes hollow and movements unnervingly calm . . .",
        "health": 50,
        "attack": 8,
        "defense": 7,
        "speed": 15,
        "money": 40,
    },

    #castle, ground floor
    "Possessed Armour": {
        "description": "A suit of armour snaps to life with a metallic shriek, moving without a body inside as it advances on you . . .",
        "health": 18,
        "attack": 4,
        "defense": 6,
        "speed": 3,
        "money": 10,
    },

    #castle, ground floor
    "Royal Mage": {
        "description": "A Mage of the old times, casting spells to deter any adventures from approaching its master's chamber . . .",
        "health": 15,
        "attack": 8,
        "defense": 3,
        "speed": 6,
        "money": 10,
    },

    #castle treasury (3 chests in the room, one some coins, one a good wep upgrade and 3rd a mimic)
    "Mimic": {
        "description": "A treasure chest trembles... then sprouts teeth. The mimic snaps open with a wet, hungry click . . .",
        "health": 25,
        "attack": 6,
        "defense": 4,
        "speed": 1,
        "money": 30,
    },

    #castle, first floor (biggest bad)(1)
    "Crazed Warlock": {
        "description": "A tall figure waits in the shadows above, crowned in dust and silence. Its presence feels heavy—like the room itself is holding its breath . . .",
        "health": 100,
        "attack": 20,
        "defense": 15,
        "speed": 50,
        "money": 100,
    },

}

def generateMobs(spawnRules):

    #the function to create the games enemies
    cap = spawnRules["cap"]
    #sets the amount of enemies that can spawn in any given area
    types = spawnRules["types"]
    #sets the types of enemies that can spawn in a given area

    total = random.randint(1, cap)
    #sets the amount of enemies that will spawn between 1 and the given cap

    mobs = []
    for i in range(total):
        mobs.append(random.choice(types))

    return mobs
locations = {
    "Village":  {
        "description": "A quaint settlement made up of a few houses, surrounded by a dark forest",
        "north": "Forest",
        "east": "Cave",
        "west": "Field",
        "item": "Health Potion",
    },

    "Field": {
        "description": "An open grassy field stretches out before you, the wind rustling softly through tall grass",
        "east": "Village",
        "item": "Health Potion",
        "spawn": {
            "cap": 1,
            "types": ["Ghoul"]
        }
    },

    "Forest": {
        "description": "A gloomy and perilous woodland, be careful of those who lurk here",
        "north": "Castle Entrance",
        "south": "Village",
        "item": "Health Potion",
        "spawn": {
            "cap": 3,
            "types": ["Treant", "Hobgoblin"]
        }
    },

    "Castle Entrance": {
        "description": "A towering stone gateway looms ahead, its heavy doors scarred by age and guarded by silence",
        "north": {
            "destination": "Castle, Ground Floor",
            "locked": True,
            "key": "Castle Key"
        },
        "south": "Forest",
        "west": "Castle Grounds",
        "item": "Health Potion",
        "spawn": {
            "cap": 4,
            "types": ["Undead Warrior", "Undead Archer"],
        }
    },

    "Castle Grounds": {
        "description" : "A beautiful yet unkept garden, surrounded by crumbling walls",
        "east": "Castle Entrance",
        "item": "Castle Key",
        "spawn": {
            "cap": 1,
            "types": ["The Groundskeeper"],
        }
    },

    "Castle, First Floor": {
        "description" : "",
        "south": "Castle, Ground Floor",
        "item": "",
        "spawn": {
            "cap": 1,
            "types": ["Crazed Warlock"]
        }
    },

    "Castle, Ground Floor" : {
        "description" : "A vast stone hall filled with dust and broken banners, echoing with the weight of forgotten history",
        "south": "Castle Entrance",
        "north": "Castle, First Floor",
        "east": "Castle Treasury",
        "item": "Tattered Note",
        "spawn": {
            "cap": 5,
            "types": ["Possessed Armour", "Royal Mage"]
        }
    },

    "Castle Treasury": {
        "description": "A stone chamber reinforced with iron bars and heavy doors. Several chests remain sealed, their contents unknown, and the air hums with the promise of untouched treasure",
        "west": "Castle, Ground Floor",
        "item": "Bejewelled sword/staff/bow/daggers",
        "spawn": {
            "cap": 1,
            "types": ["Mimic"]
        }
    },

    "Beach": {
        "description": "A sparkly sandy beach with the ocean expanding towards the horizon",
        "west": "Cave",
        "item": "Rune of Vigor",
        "spawn": {
            "cap": 3,
            "types": ["Siren","Sand Crab"]
        }
    },

    "Cave": {
        "description": "A dark, echoing cave carved by time, where shadows cling to cold stone.",
        "east": "Beach",
        "west": "Village",
        "item": "Sturdy Chestplate",
        "spawn": {
            "cap": 4,
            "types": ["Armoured Skeleton","Giant Cave Spider"]
        }
    }
}
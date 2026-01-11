locations = {
    "Village":  {
        "description": "A quaint settlement made up of a few houses, surrounded by a dark forest",
        "north": "Forest",
        "east": "Cave",
        "west": "Field",
        "items": [
            "Health Potion",
        ]
    },

    "Field": {
        "description": "An open grassy field stretches out before you, the wind rustling softly through tall grass",
        "east": "Village",
        "items": [
            "Health Potion",
        ],
        "spawn": {
            "cap": 1,
            "types": ["Ghoul"]
        }
    },

    "Forest": {
        "description": "A gloomy and perilous woodland, be careful of those who lurk here",
        "north": "Castle Entrance",
        "south": "Village",
        "items": [
            "Health Potion",
            "Rusty Helmet",
        ],
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
        "items": [
            "Health Potion",
        ],
        "spawn": {
            "cap": 4,
            "types": ["Undead Warrior", "Undead Archer"],
        }
    },

    "Castle Grounds": {
        "description" : "A beautiful yet unkept garden, surrounded by crumbling walls",
        "east": "Castle Entrance",
        "items": [
            "Castle Key",
        ],
        "spawn": {
            "cap": 1,
            "types": ["The Groundskeeper"],
        }
    },

    "Castle, First Floor": {
        "description" : "The room stand before you, a wide expanse of cracked stone bricks with vines and wear showing through, the air is filled with a still dust and the only light in the room comes from a series of cracked stained glass windows illuminating the throne in the middle and the figure that sits upon it . . .",
        "south": "Castle, Ground Floor",
        "items": [
            "Trophy",
        ],
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
        "items": [
            "Health Potion",
            "Tattered Note",
        ],
        "spawn": {
            "cap": 5,
            "types": ["Possessed Armour", "Royal Mage"]
        }
    },

    "Castle Treasury": {
        "description": "A stone chamber reinforced with iron bars and heavy doors. Several chests remain sealed, their contents unknown, and the air hums with the promise of untouched treasure",
        "west": "Castle, Ground Floor",
        "items": [
            "Rune of Enhancement",
        ],
        "spawn": {
            "cap": 1,
            "types": ["Mimic"]
        }
    },

    "Beach": {
        "description": "A sparkly sandy beach with the ocean expanding towards the horizon",
        "west": "Cave",
        "items": [
            "Rune of Vigor", #raise max hp by 25
        ],
        "spawn": {
            "cap": 3,
            "types": ["Siren","Sand Crab"]
        }
    },

    "Cave": {
        "description": "A dark, echoing cave carved by time, where shadows cling to cold stone.",
        "east": "Beach",
        "west": "Village",
        "items": [
            "Health Potion",
            "Sturdy Chestplate"
        ],
        "spawn": {
            "cap": 4,
            "types": ["Armoured Skeleton","Giant Cave Spider"]
        }
    }
}
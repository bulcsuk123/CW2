import os

asciiFolder = os.path.join("resources", "ascii")

asciiMap = {
    "Field" : "field.txt",
    "Village" : "village.txt",
    "Forest" : "forest.txt",
    "Cave" : "cave.txt",
    "Beach" : "beach.txt",
    "Castle Entrance" : "castle_entrance.txt",
    "Castle Grounds" : "castle_grounds.txt",
    "Castle, Ground Floor" : "castle_ground_floor.txt",
    "Castle Treasury" : "castle_treasury.txt",
    "Castle, First Floor" : "castle_first_floor.txt",
    "Game Over" : "game_over.txt",
}

def showAscii(locationName: str) -> None:
    filename = asciiMap.get(locationName)
    if not filename:
        return

    path = os.path.join(asciiFolder, filename)

    try:
        with open(path, "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        #if the file is missing it doesn't crash and instead returns an error message
        return
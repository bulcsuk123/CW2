import os

#gets the folder for the ascii
baseDir = os.path.dirname(os.path.dirname(__file__))
asciiFolder = os.path.join(baseDir, "resources", "ascii")

#applies each ascii image to each location
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
    "Win" : "win.txt",
}

#shows the corresponding ascii, otherwise does nothing
def showAscii(locationName: str) -> None:
    filename = asciiMap.get(locationName)
    if not filename:
        return

    #sets the file path
    path = os.path.join(asciiFolder, filename)

    #trys to open the file, if not returns to the program
    try:
        with open(path, "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        #if the file is missing it doesn't crash and instead returns an error message
        return
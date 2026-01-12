import json
import os
from datetime import datetime

#defines the path to the leaderboard.json
scoresPath = os.path.join("../data", "leaderboard.json")

#ensures that the "data" folder exists
def ensureDataFolder():
    os.makedirs(os.path.dirname(scoresPath), exist_ok = True)

#a function to return the data essentially loading the scores as a list
def loadScores():
    ensureDataFolder()
    #if the path doesn't exist it returns an empty list
    if not os.path.exists(scoresPath):
        return []

    #try-except catch to stop program from crashing
    try:
        #open the json file
        with open(scoresPath, "r", encoding="utf-8") as f:
            #asign the json file contents to data variable
            data = json.load(f)
            #return the data variable if it contains data, else return an empty list
            return data if isinstance(data, list) else []
    #throw an exception if there was a json error and the return an empty list
    except (json.JSONDecodeError, OSError):
        return []

#function to save score of the player
def saveScores(scores: list[dict]) -> None:
    #checks if the data folder exists
    ensureDataFolder()
    #opens the json file in write mode and writes the "scores" list variable to it with indents
    with open(scoresPath, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)

#records the score of the player using different variables such as outcome and turns
def recordScore(player, outcome: str, turns: int) -> None:
    scores = loadScores()

    #formats data into readable layout
    entry = {
        "name": player.name,
        "role": getattr(player, "role", ""),
        "race": getattr(player, "race", ""),
        "coins": getattr(player, "money", 0),
        "turns": turns,
        "outcome": outcome,
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }

    #adds the formatted version to the scores variable
    scores.append(entry)
    #scores variable written to json file
    saveScores(scores)

#function to display top 10 leaderboard info
def showLeaderboard(topN: int = 10) -> None:
    scores = loadScores()

    #if scores variable is empty prints appropriate message
    if not scores:
        print("\n=== Leaderboard ===")
        print("No scores yet. Be the first to play!\n")
        return

    #sorts the scores in order of coins, resorts to turns if there is a tie
    scoresSorted = sorted(scores, key=lambda s: (-s.get("coins", 0), s.get("turns", 99999999)))

    #formatting for the leaderboard page
    print("\n=== Leaderboard (Top {}) ===".format(topN))
    print("{:<4} {:<14} {:<8} {:<6} {:<7} {:<8} {}".format("#", "Name", "Role", "Coins", "Turns", "Outcome", "When"))
    print("-" * 70)

    #prints all of the leaderboard info into console
    for i, s in enumerate(scoresSorted[:topN], start=1):
        #nicely formatting leaderboard entries
        print("{:<4} {:<14} {:<8} {:<6} {:<7} {:<8} {}".format(
            i,
            str(s.get("name", ""))[:14],
            str(s.get("role", ""))[:8],
            s.get("coins", 0),
            s.get("turns", 0),
            str(s.get("outcome", ""))[:8],
            str(s.get("timestamp", ""))[:19],
        ))

    print()
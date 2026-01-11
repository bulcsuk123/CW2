import json
import os
from datetime import datetime

scoresPath = os.path.join("data", "leaderboard.json")

def ensureDataFolder():
    os.makedirs(os.path.dirname(scoresPath), exist_ok = True)

def loadScores():
    ensureDataFolder()
    if not os.path.exists(scoresPath):
        return []

    try:
        with open(scoresPath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def saveScores(scores: list[dict]) -> None:
    ensureDataFolder()
    with open(scoresPath, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)

def recordScore(player, outcome: str, turns: int) -> None:
    scores = loadScores()

    entry = {
        "name": player.name,
        "role": getattr(player, "role", ""),
        "race": getattr(player, "race", ""),
        "coins": getattr(player, "money", 0),
        "turns": turns,
        "outcome": outcome,
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }

    scores.append(entry)
    saveScores(scores)

def showLeaderboard(topN: int = 10) -> None:
    scores = loadScores()

    if not scores:
        print("\n=== Leaderboard ===")
        print("No scores yet. Be the first to play!\n")
        return

    scoresSorted = sorted(scores, key=lambda s: (-s.get("coins", 0), s.get("turns", 99999999)))

    print("\n=== Leaderboard (Top {}) ===".format(topN))
    print("{:<4} {:<14} {:<8} {:<6} {:<7} {:<8} {}".format("#", "Name", "Role", "Coins", "Turns", "Outcome", "When"))
    print("-" * 70)

    for i, s in enumerate(scoresSorted[:topN], start=1):
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
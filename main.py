"""Simple CLI app to track deaths by game/chapter/boss.

Usage: run `python main.py` and follow the interactive prompts.
Data is persisted to `deaths.json` in the project folder.
"""

import json
import os
from pathlib import Path

DATA_FILE = Path("deaths.json")


def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"games": {}}


def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))


def ensure_game(data, game_name):
    games = data.setdefault("games", {})
    return games.setdefault(game_name, {"chapters": {}})


def ensure_chapter(game, chapter_name):
    chapters = game.setdefault("chapters", {})
    return chapters.setdefault(chapter_name, {"bosses": {}})


def ensure_boss(chapter, boss_name):
    bosses = chapter.setdefault("bosses", {})
    return bosses.setdefault(boss_name, {"deaths": 0})


def add_game(data):
    name = input("Game name: ").strip()
    if not name:
        print("Cancelled")
        return
    ensure_game(data, name)
    save_data(data)
    print(f"Added game: {name}")


def add_chapter(data):
    game_name = input("Game name: ").strip()
    if not game_name or game_name not in data.get("games", {}):
        print("Game not found. Use Add Game first.")
        return
    chapter = input("Chapter/Area name: ").strip()
    if not chapter:
        print("Cancelled")
        return
    ensure_chapter(data["games"][game_name], chapter)
    save_data(data)
    print(f"Added chapter '{chapter}' to game '{game_name}'")


def add_boss(data):
    game_name = input("Game name: ").strip()
    if game_name not in data.get("games", {}):
        print("Game not found.")
        return
    chapter_name = input("Chapter/Area name: ").strip()
    chapters = data["games"][game_name].get("chapters", {})
    if chapter_name not in chapters:
        print("Chapter not found. Add it first.")
        return
    boss = input("Boss name: ").strip()
    if not boss:
        print("Cancelled")
        return
    ensure_boss(chapters[chapter_name], boss)
    save_data(data)
    print(f"Added boss '{boss}' in '{chapter_name}' of '{game_name}'")


def increment_death(data):
    game_name = input("Game name: ").strip()
    if game_name not in data.get("games", {}):
        print("Game not found.")
        return
    chapter_name = input("Chapter/Area name (leave blank to increment game total): ").strip()
    if not chapter_name:
        # increment a generic game-wide counter
        game = data["games"][game_name]
        game.setdefault("deaths", 0)
        game["deaths"] += 1
        save_data(data)
        print(f"Incremented death for game '{game_name}' (total now {game['deaths']})")
        return
    chapters = data["games"][game_name].get("chapters", {})
    if chapter_name not in chapters:
        print("Chapter not found.")
        return
    boss_name = input("Boss name (leave blank to increment chapter total): ").strip()
    chapter = chapters[chapter_name]
    if not boss_name:
        chapter.setdefault("deaths", 0)
        chapter["deaths"] += 1
        save_data(data)
        print(f"Incremented death for chapter '{chapter_name}' (total now {chapter['deaths']})")
        return
    bosses = chapter.setdefault("bosses", {})
    if boss_name not in bosses:
        print("Boss not found. Add it first.")
        return
    bosses[boss_name].setdefault("deaths", 0)
    bosses[boss_name]["deaths"] += 1
    save_data(data)
    print(f"Incremented death for boss '{boss_name}' (total now {bosses[boss_name]['deaths']})")


def show_stats(data):
    games = data.get("games", {})
    if not games:
        print("No games tracked yet.")
        return
    for gname, gdat in games.items():
        g_deaths = gdat.get("deaths", 0)
        print(f"Game: {gname}  (deaths: {g_deaths})")
        for cname, cdat in gdat.get("chapters", {}).items():
            c_deaths = cdat.get("deaths", 0)
            print(f"  Chapter: {cname}  (deaths: {c_deaths})")
            for bname, bdat in cdat.get("bosses", {}).items():
                print(f"    Boss: {bname}  (deaths: {bdat.get('deaths',0)})")


def list_games(data):
    for name in data.get("games", {}):
        print(name)


def export_data(data):
    path = input("Export file path (default: deaths-export.json): ").strip() or "deaths-export.json"
    Path(path).write_text(json.dumps(data, indent=2))
    print(f"Exported to {path}")


def import_data(data):
    path = input("Import file path: ").strip()
    if not path or not Path(path).exists():
        print("File not found")
        return
    incoming = json.loads(Path(path).read_text())
    # naive merge: replace
    save_data(incoming)
    print(f"Imported data from {path}")


def reset_all(data):
    confirm = input("Type YES to reset and delete all tracked deaths: ")
    if confirm == "YES":
        data.clear()
        data["games"] = {}
        save_data(data)
        print("Reset complete")
    else:
        print("Aborted")


def help_text():
    print("Commands:")
    print("  add-game    - Add a new game")
    print("  add-chapter - Add chapter/area to a game")
    print("  add-boss    - Add boss to a chapter")
    print("  kill        - Increment death (game/chapter/boss)")
    print("  show        - Show all stats")
    print("  list        - List games")
    print("  export      - Export JSON")
    print("  import      - Import JSON (replaces current data)")
    print("  reset       - Reset all data")
    print("  help        - Show this help")
    print("  quit        - Exit")


def main():
    data = load_data()
    print("Death Counter CLI — simple tracker for game deaths")
    help_text()
    while True:
        cmd = input("cmd> ").strip().lower()
        if cmd in ("q", "quit", "exit"):
            break
        if cmd == "add-game":
            add_game(data)
        elif cmd == "add-chapter":
            add_chapter(data)
        elif cmd == "add-boss":
            add_boss(data)
        elif cmd == "kill":
            increment_death(data)
        elif cmd == "show":
            show_stats(data)
        elif cmd == "list":
            list_games(data)
        elif cmd == "export":
            export_data(data)
        elif cmd == "import":
            import_data(data)
            data = load_data()
        elif cmd == "reset":
            reset_all(data)
        elif cmd == "help":
            help_text()
        else:
            print("Unknown command. Type 'help'.")


if __name__ == "__main__":
    main()

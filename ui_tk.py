import json
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

DATA_FILE = Path("deaths.json")


def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"games": {}}


def save_data(data):
    # recompute aggregates before saving
    recompute_all(data)
    DATA_FILE.write_text(json.dumps(data, indent=2))


def recompute_chapter(data, game_name, chapter_name):
    chapter = data["games"][game_name]["chapters"][chapter_name]
    bosses = chapter.get("bosses", {})
    boss_sum = sum(b.get("deaths", 0) for b in bosses.values())
    manual = chapter.get("deaths_manual", 0)
    chapter["deaths"] = boss_sum + manual
    return chapter["deaths"]


def recompute_game(data, game_name):
    game = data["games"][game_name]
    chapters = game.get("chapters", {})
    total = sum(c.get("deaths", 0) for c in chapters.values())
    manual = game.get("deaths_manual", 0)
    game["deaths"] = total + manual
    return game["deaths"]


def recompute_all(data):
    for gname, gdat in data.get("games", {}).items():
        for cname in gdat.get("chapters", {}):
            recompute_chapter(data, gname, cname)
        recompute_game(data, gname)


class DeathsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Death Counter")
        self.geometry("640x240")
        self.data = load_data()

        frm = ttk.Frame(self, padding=8)
        frm.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(frm)
        top.pack(fill=tk.X, pady=4)

        self.game_cb = ttk.Combobox(top, state="readonly", width=24)
        self.game_cb.pack(side=tk.LEFT, padx=4)
        self.game_cb.bind("<<ComboboxSelected>>", lambda e: self.update_chapters())

        self.chapter_cb = ttk.Combobox(top, state="readonly", width=24)
        self.chapter_cb.pack(side=tk.LEFT, padx=4)
        self.chapter_cb.bind("<<ComboboxSelected>>", lambda e: self.update_bosses())

        self.boss_cb = ttk.Combobox(top, state="readonly", width=24)
        self.boss_cb.pack(side=tk.LEFT, padx=4)

        row = ttk.Frame(frm)
        row.pack(fill=tk.X, pady=6)
        ttk.Button(row, text="Add Game", command=self.add_game).pack(side=tk.LEFT, padx=4)
        ttk.Button(row, text="Add Chapter", command=self.add_chapter).pack(side=tk.LEFT, padx=4)
        ttk.Button(row, text="Add Boss", command=self.add_boss).pack(side=tk.LEFT, padx=4)

        row2 = ttk.Frame(frm)
        row2.pack(fill=tk.X, pady=6)
        ttk.Button(row2, text="+ Death", command=self.increment_death).pack(side=tk.LEFT, padx=4)
        ttk.Button(row2, text="Show Stats", command=self.show_stats).pack(side=tk.LEFT, padx=4)
        ttk.Button(row2, text="Export", command=self.export_data).pack(side=tk.LEFT, padx=4)

        self.status = ttk.Label(frm, text="Ready")
        self.status.pack(fill=tk.X, pady=6)

        self.refresh()

    def refresh(self):
        games = list(self.data.get("games", {}).keys())
        self.game_cb["values"] = games
        if games:
            self.game_cb.set(games[0])
        else:
            self.game_cb.set("")
        self.update_chapters()

    def update_chapters(self):
        g = self.game_cb.get()
        chapters = []
        if g in self.data.get("games", {}):
            chapters = list(self.data["games"][g].get("chapters", {}).keys())
        self.chapter_cb["values"] = chapters
        if chapters:
            self.chapter_cb.set(chapters[0])
        else:
            self.chapter_cb.set("")
        self.update_bosses()

    def update_bosses(self):
        g = self.game_cb.get()
        c = self.chapter_cb.get()
        bosses = []
        if g in self.data.get("games", {}) and c in self.data["games"][g].get("chapters", {}):
            bosses = list(self.data["games"][g]["chapters"][c].get("bosses", {}).keys())
        self.boss_cb["values"] = bosses
        if bosses:
            self.boss_cb.set(bosses[0])
        else:
            self.boss_cb.set("")

    def add_game(self):
        name = simpledialog.askstring("Add Game", "Game name:", parent=self)
        if not name:
            return
        self.data.setdefault("games", {}).setdefault(name, {"chapters": {}})
        save_data(self.data)
        self.status["text"] = f"Added game: {name}"
        self.refresh()

    def add_chapter(self):
        g = self.game_cb.get()
        if not g:
            messagebox.showwarning("No game", "Select a game first", parent=self)
            return
        name = simpledialog.askstring("Add Chapter", "Chapter/Area name:", parent=self)
        if not name:
            return
        self.data.setdefault("games", {}).setdefault(g, {}).setdefault("chapters", {}).setdefault(name, {"bosses": {}})
        self.data["games"][g]["chapters"][name].setdefault("deaths_manual", 0)
        save_data(self.data)
        self.status["text"] = f"Added chapter: {name}"
        self.refresh()

    def add_boss(self):
        g = self.game_cb.get()
        c = self.chapter_cb.get()
        if not g or not c:
            messagebox.showwarning("Missing", "Select a game and chapter first", parent=self)
            return
        name = simpledialog.askstring("Add Boss", "Boss name:", parent=self)
        if not name:
            return
        self.data.setdefault("games", {}).setdefault(g, {}).setdefault("chapters", {}).setdefault(c, {}).setdefault("bosses", {}).setdefault(name, {"deaths": 0})
        self.data["games"][g]["chapters"][c].setdefault("deaths_manual", 0)
        recompute_chapter(self.data, g, c)
        recompute_game(self.data, g)
        save_data(self.data)
        self.status["text"] = f"Added boss: {name}"
        self.refresh()

    def increment_death(self):
        g = self.game_cb.get()
        c = self.chapter_cb.get()
        b = self.boss_cb.get()
        if not g:
            messagebox.showwarning("No game", "Select a game first", parent=self)
            return
        if b:
            self.data["games"][g]["chapters"][c]["bosses"][b].setdefault("deaths", 0)
            self.data["games"][g]["chapters"][c]["bosses"][b]["deaths"] += 1
            recompute_chapter(self.data, g, c)
            recompute_game(self.data, g)
            save_data(self.data)
            self.status["text"] = f"+1 death for boss {b}"
            return
        if c:
            self.data["games"][g]["chapters"][c].setdefault("deaths_manual", 0)
            self.data["games"][g]["chapters"][c]["deaths_manual"] += 1
            recompute_chapter(self.data, g, c)
            recompute_game(self.data, g)
            save_data(self.data)
            self.status["text"] = f"+1 death for chapter {c}"
            return
        self.data["games"][g].setdefault("deaths_manual", 0)
        self.data["games"][g]["deaths_manual"] += 1
        recompute_game(self.data, g)
        save_data(self.data)
        self.status["text"] = f"+1 death for game {g}"

    def show_stats(self):
        lines = []
        for g, gdat in self.data.get("games", {}).items():
            lines.append(f"Game: {g}  deaths: {gdat.get('deaths',0)}")
            for c, cdat in gdat.get("chapters", {}).items():
                lines.append(f"  Chapter: {c}  deaths: {cdat.get('deaths',0)}")
                for b, bdat in cdat.get("bosses", {}).items():
                    lines.append(f"    Boss: {b}  deaths: {bdat.get('deaths',0)}")
        if not lines:
            lines = ["No data"]
        messagebox.showinfo("Stats", "\n".join(lines), parent=self)

    def export_data(self):
        path = Path("deaths-export.json")
        path.write_text(json.dumps(self.data, indent=2))
        self.status["text"] = f"Exported to {path}"


def run_tk():
    app = DeathsApp()
    app.mainloop()


if __name__ == "__main__":
    run_tk()

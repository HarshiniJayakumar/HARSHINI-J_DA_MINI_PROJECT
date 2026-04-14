import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("ball_by_ball_ipl_data.csv")
df.columns = df.columns.str.strip()

# -----------------------------
# PLAYER ANALYSIS
# -----------------------------
player_runs = df.groupby("batter_name")["batsman_run"].sum()
player_balls = df.groupby("batter_name")["id"].count()

player_stats = pd.DataFrame({
    "runs": player_runs,
    "balls": player_balls
})

player_stats["strike_rate"] = (player_stats["runs"] / player_stats["balls"]) * 100

top_players = player_stats.sort_values(by="runs", ascending=False).head(10)

# -----------------------------
# TEAM ANALYSIS
# -----------------------------
team_runs = df.groupby("batting_team")["total_run"].sum()

# -----------------------------
# BOWLER ANALYSIS  
# -----------------------------
bowler_wickets = df[df["batsman_run"] == 0].groupby("bowler_name")["id"].count()
top_bowlers = bowler_wickets.sort_values(ascending=False).head(10)

# -----------------------------
# FUNCTIONS
# -----------------------------

def show_statistics():
    result_text.delete(1.0, tk.END)

    runs = player_stats["runs"]

    result_text.insert(tk.END, "📊 STATISTICAL ANALYSIS\n\n")
    result_text.insert(tk.END, f"Mean Runs: {round(np.mean(runs),2)}\n")
    result_text.insert(tk.END, f"Median Runs: {round(np.median(runs),2)}\n")
    result_text.insert(tk.END, f"Std Deviation: {round(np.std(runs),2)}\n")


def show_players():
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "🏏 TOP BATSMEN\n\n")

    for p, r in top_players.iterrows():
        result_text.insert(tk.END, f"{p} | Runs: {r['runs']} | SR: {round(r['strike_rate'],2)}\n")


def show_teams():
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "🏆 TEAM RUNS\n\n")

    for t, r in team_runs.sort_values(ascending=False).items():
        result_text.insert(tk.END, f"{t}: {r}\n")


def show_bowlers():
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "🎯 TOP BOWLERS (Dot Ball Wickets Proxy)\n\n")

    for b, w in top_bowlers.items():
        result_text.insert(tk.END, f"{b}: {w}\n")


def show_insights():
    best_player = top_players.index[0]
    best_team = team_runs.idxmax()
    best_bowler = top_bowlers.idxmax()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "📌 SMART INSIGHTS SUMMARY\n\n")

    result_text.insert(tk.END, f"🏏 Best Batsman: {best_player}\n")
    result_text.insert(tk.END, f"🏆 Best Team: {best_team}\n")
    result_text.insert(tk.END, f"🎯 Best Bowler: {best_bowler}\n\n")

    if player_stats["strike_rate"].mean() > 120:
        result_text.insert(tk.END, "🔥 Overall batting is aggressive\n")
    else:
        result_text.insert(tk.END, "⚖ Overall batting is balanced\n")

    result_text.insert(tk.END, "\n✔ System successfully analyzes batting, bowling and team performance.")


# -----------------------------
# GRAPHS
# -----------------------------

def show_player_graph():
    plt.figure()
    plt.bar(top_players.index, top_players["runs"])
    plt.xticks(rotation=45)
    plt.title("Top Batsmen")
    plt.show()


def show_team_graph():
    plt.figure()
    team_runs.sort_values(ascending=False).head(10).plot(kind='bar')
    plt.title("Team Runs")
    plt.xticks(rotation=45)
    plt.show()


def show_bowler_graph():
    plt.figure()
    top_bowlers.head(10).plot(kind='bar')
    plt.title("Top Bowlers")
    plt.xticks(rotation=45)
    plt.show()


# -----------------------------
# GUI DESIGN 
# -----------------------------
root = tk.Tk()
root.title("Smart Cricket Analytics System")
root.geometry("1000x650")
root.configure(bg="#0f172a")

title = tk.Label(
    root,
    text="🏏 SMART CRICKET PERFORMANCE ANALYTICS SYSTEM",
    font=("Arial", 18, "bold"),
    bg="#0f172a",
    fg="white"
)
title.pack(pady=10)

subtitle = tk.Label(
    root,
    text="Batting • Bowling • Team Analysis using Ball-by-Ball Data",
    font=("Arial", 11),
    bg="#0f172a",
    fg="#38bdf8"
)
subtitle.pack()

frame = tk.Frame(root, bg="#0f172a")
frame.pack(pady=10)

# Buttons
tk.Button(frame, text="Statistics", width=18, command=show_statistics, bg="#f97316").grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame, text="Top Batters", width=18, command=show_players, bg="#22c55e").grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame, text="Teams", width=18, command=show_teams, bg="#3b82f6").grid(row=0, column=2, padx=5, pady=5)

tk.Button(frame, text="Bowlers", width=18, command=show_bowlers, bg="#a855f7").grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame, text="Player Graph", width=18, command=show_player_graph, bg="#ec4899").grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame, text="Team Graph", width=18, command=show_team_graph, bg="#14b8a6").grid(row=1, column=2, padx=5, pady=5)

tk.Button(frame, text="Bowler Graph", width=18, command=show_bowler_graph, bg="#f43f5e").grid(row=2, column=1, padx=5, pady=5)

tk.Button(frame, text="Insights", width=18, command=show_insights, bg="#eab308").grid(row=3, column=1, padx=5, pady=10)

# Output Box
result_text = tk.Text(root, height=18, width=110, bg="#111827", fg="white")
result_text.pack(pady=15)

root.mainloop()
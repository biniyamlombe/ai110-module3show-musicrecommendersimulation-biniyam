"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender by defining 
several simulated user taste profiles (like High-Energy Pop, Chill Lofi, 
and an Adversarial Edge Case) and evaluating them against the songs catalog.

It relies on functions and OOP classes from `recommender.py` to calculate
vibe matches and generate the final recommendations.
"""

import os
import csv
from datetime import datetime

from src.recommender import load_songs, recommend_songs

def _truncate(text: str, width: int = 60) -> str:
    if text is None:
        return ""
    return (text[: width - 3] + "...") if len(text) > width else text

def print_recommendations_table(recs, title: str = "Recommendations"):
    """
    Print recommendations as a table including reasons.
    Tries to use `tabulate` if installed, otherwise falls back to ASCII formatting.
    """
    rows = []
    for i, (song, score, explanation) in enumerate(recs, start=1):
        rows.append([i, song.get("title", ""), song.get("artist", ""), f"{score:.2f}", _truncate(explanation, 80)])

    headers = ["#", "Title", "Artist", "Score", "Reasons"]
    try:
        from tabulate import tabulate  # optional dependency
        print(f"\n--- {title} ---")
        print(tabulate(rows, headers=headers, tablefmt="github"))
    except Exception:
        col_widths = [3, 30, 18, 7, 80]
        fmt = "{:<3}  {:<30}  {:<18}  {:>7}  {:<80}"
        print(f"\n--- {title} ---")
        print(fmt.format(*headers))
        print("-" * (sum(col_widths) + 10))
        for r in rows:
            print(fmt.format(r[0], r[1][:30], r[2][:18], r[3], r[4][:80]))

def interactive_mode(songs):
    print("\n" + "="*50)
    print("Welcome to VibeFinder Interactive Mode!")
    print("Let's build your custom taste profile.")
    print("="*50)
    
    name = input("What's your name? ").strip() or "Guest"
    genre = input("What genre are you feeling? (e.g., pop, lofi, metal, rock): ").strip().lower()
    mood = input("What mood are you in? (e.g., happy, chill, sad, energetic): ").strip().lower()
    
    try:
        energy_input = float(input("How much energy do you want? (1-10): "))
        energy = min(max(energy_input / 10.0, 0.0), 1.0)
    except ValueError:
        energy = 0.5
        
    try:
        valence_input = float(input("How happy/positive should it be? (1-10): "))
        valence = min(max(valence_input / 10.0, 0.0), 1.0)
    except ValueError:
        valence = 0.5
        
    priority = input("What do you care about most? (1) Exact Genre, or (2) Exact Energy?: ").strip()
    weight_genre = 1.0
    weight_energy = 2.0
    if priority == "1":
        weight_genre = 5.0
        weight_energy = 0.5
    elif priority == "2":
        weight_genre = 0.0
        weight_energy = 5.0

    user_profile = {
        "name": name,
        "genre": genre,
        "mood": mood,
        "energy": energy,
        "valence": valence,
        "weight_genre": weight_genre,
        "weight_energy": weight_energy
    }
    
    print(f"\nAwesome, {name}! Generating recommendations...")
    recommendations = recommend_songs(user_profile, songs, k=5)
    print_recommendations_table(recommendations, title=f"Top for {name}")

    if recommendations:
        top_song = recommendations[0][0]
        like = input(f"\nDid you like the #1 song '{top_song.get('title')}'? (y/n): ").strip().lower()
        if like == 'y':
            print("\nAwesome! Learning from your feedback... tweaking your profile.")
            # Shift the user's energy and valence closer to the song's properties (blend 50/50)
            user_profile["energy"] = (user_profile["energy"] + float(top_song.get("energy", user_profile["energy"]))) / 2.0
            if "valence" in top_song:
                user_profile["valence"] = (user_profile["valence"] + float(top_song["valence"])) / 2.0
            
            # Re-generate recommendations with adjusted math
            new_recommendations = recommend_songs(user_profile, songs, k=5)
            print_recommendations_table(new_recommendations, title=f"Updated Top for {name} (Learned from feedback!)")
            recommendations = new_recommendations

    save = input("\nWould you like to save this playlist to a CSV? (y/n): ").strip().lower()
    if save == 'y':
        os.makedirs("outputs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/playlist_{name.replace(' ', '_')}_{timestamp}.csv"
        
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Rank", "Title", "Artist", "Score", "Reasons"])
            for i, (song, score, explanation) in enumerate(recommendations, start=1):
                writer.writerow([i, song.get('title', ''), song.get('artist', ''), f"{score:.2f}", explanation])
        
        print(f"Playlist successfully saved to {filename}!")


def main() -> None:
    songs = load_songs("data/songs.csv") 

    print("\n--- VibeFinder Simulation ---")
    choice = input("Would you like to try Interactive Mode? (y/n): ").strip().lower()
    if choice == 'y':
        interactive_mode(songs)
        return


    # 1. High-Energy Pop (Standard Profile)
    profile_1 = {"name": "High-Energy Pop", "genre": "pop", "mood": "happy", "energy": 0.85, "valence": 0.8, 
                 "detailed_mood": "euphoric", "release_decade": 2010, "target_popularity": 80, "vocal_presence": 0.8, "instrumentalness": 0.1}
    
    # 2. Chill Lofi (Standard Profile)
    profile_2 = {"name": "Chill Lofi", "genre": "lofi", "mood": "chill", "energy": 0.3, "valence": 0.5,
                 "detailed_mood": "serene", "release_decade": 2020, "target_popularity": 45, "vocal_presence": 0.1, "instrumentalness": 0.9}
    
    # 3. Adversarial / Edge Case (Conflicting: intense but acoustic/low tempo)
    # Testing what happens when a user asks for heavy metal, but with extremely low energy and high valence.
    profile_3 = {"name": "Adversarial Metal", "genre": "metal", "mood": "happy", "energy": 0.1, "valence": 0.9,
                 "detailed_mood": "euphoric", "release_decade": 1980, "target_popularity": 90, "vocal_presence": 0.9, "instrumentalness": 0.2}

    profiles = [profile_1, profile_2, profile_3]

    for p in profiles:
        print(f"\n========== Top recommendations for: {p['name']} ==========")
        recommendations = recommend_songs(p, songs, k=5, mode=p.get("mode", "base"))
        print_recommendations_table(recommendations, title=f"Top for {p['name']}")
        print("==================================================================")


if __name__ == "__main__":
    main()

"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender by defining 
several simulated user taste profiles (like High-Energy Pop, Chill Lofi, 
and an Adversarial Edge Case) and evaluating them against the songs catalog.

It relies on functions and OOP classes from `recommender.py` to calculate
vibe matches and generate the final recommendations.
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

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
        recommendations = recommend_songs(p, songs, k=5)
        for rec in recommendations:
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
        print("==================================================================")


if __name__ == "__main__":
    main()

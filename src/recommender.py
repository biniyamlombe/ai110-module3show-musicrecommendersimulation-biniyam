import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            row['popularity'] = int(row['popularity'])
            row['release_decade'] = int(row['release_decade'])
            row['vocal_presence'] = float(row['vocal_presence'])
            row['instrumentalness'] = float(row['instrumentalness'])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user profile using our Algorithm Recipe.
    Returns a tuple of (total_score, list_of_reasons).
    """
    score = 0.0
    reasons = []

    if 'genre' in user_prefs and song['genre'] == user_prefs['genre']:
        score += 1.0  # EXP: Halved from 2.0
        reasons.append("genre match (+1.0)")
    
    if 'mood' in user_prefs and song['mood'] == user_prefs['mood']:
        score += 1.0
        reasons.append("mood match (+1.0)")
        
    if 'detailed_mood' in user_prefs and song['detailed_mood'] == user_prefs['detailed_mood']:
        score += 1.5
        reasons.append("detailed mood match (+1.5)")

    if 'release_decade' in user_prefs and song['release_decade'] == user_prefs['release_decade']:
        score += 1.0
        reasons.append(f"{song['release_decade']}s era match (+1.0)")

    if 'target_popularity' in user_prefs:
        pop_diff = abs(user_prefs['target_popularity'] - song['popularity']) / 100.0
        pop_score = max(0.0, 1.0 - pop_diff)
        score += pop_score
        reasons.append(f"popularity match (+{pop_score:.2f})")

    if 'vocal_presence' in user_prefs:
        vocal_score = max(0.0, 1.0 - abs(user_prefs['vocal_presence'] - song['vocal_presence']))
        score += vocal_score
        reasons.append(f"vocal match (+{vocal_score:.2f})")

    if 'instrumentalness' in user_prefs:
        inst_score = max(0.0, 1.0 - abs(user_prefs['instrumentalness'] - song['instrumentalness']))
        score += inst_score
        reasons.append(f"instrumentalness match (+{inst_score:.2f})")

    if 'energy' in user_prefs:
        energy_score = 2.0 * max(0.0, 1.0 - abs(user_prefs['energy'] - song['energy'])) # EXP: Doubled weight
        score += energy_score
        reasons.append(f"energy match (+{energy_score:.2f})")

    if 'valence' in user_prefs and 'valence' in song:
        valence_score = max(0.0, 1.0 - abs(user_prefs['valence'] - song['valence']))
        score += valence_score
        reasons.append(f"valence match (+{valence_score:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = []
    
    # Loop over every song in the catalog
    for song in songs:
        # 1. Use the judge to calculate score
        score, reasons = score_song(user_prefs, song)
        
        # 2. Format the reasons list into a single readable string
        explanation = ", ".join(reasons) if reasons else "No matching vibe found."
        
        # 3. Store the result
        scored_songs.append((song, score, explanation))
        
    # Pythonic sorting: list.sort() sorts the list in-place.
    # We use a lambda function to tell it to sort by index [1] (which is the score).
    # `reverse=True` puts the highest scores at the top.
    scored_songs.sort(key=lambda item: item[1], reverse=True)
    
    # Return the top k elements slice
    return scored_songs[:k]

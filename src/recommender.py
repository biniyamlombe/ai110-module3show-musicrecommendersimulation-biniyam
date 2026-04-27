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
# Strategy pattern (single feature addition)
class ScoringStrategy:
    """Minimal strategy interface: score returns (score, reasons)."""
    def score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        raise NotImplementedError

    def explain(self, user: UserProfile, song: Song) -> str:
        sc, reasons = self.score(user, song)
        return ", ".join(reasons) if reasons else "No matching vibe found."

class BaseStrategy(ScoringStrategy):
    """Wrap existing score_song by converting dataclasses to dicts."""
    def score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        # convert UserProfile -> user_prefs dict expected by score_song
        prefs: Dict = {}
        if getattr(user, "favorite_genre", None):
            prefs["genre"] = user.favorite_genre
        if getattr(user, "favorite_mood", None):
            prefs["mood"] = user.favorite_mood
        prefs["energy"] = getattr(user, "target_energy", 0.5)
        # likes_acoustic is kept for future strategies (not used by score_song currently)
        prefs["likes_acoustic"] = getattr(user, "likes_acoustic", False)

        # convert Song dataclass to dict in the same shape as load_songs rows
        song_dict: Dict = song.__dict__.copy()
        return score_song(prefs, song_dict)

class GenreFirstStrategy(BaseStrategy):
    """Boost songs that match genre by an additional small bonus."""
    def __init__(self, bonus: float = 1.5):
        self.bonus = bonus

    def score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        base_score, reasons = super().score(user, song)
        if user.favorite_genre and song.genre and song.genre.lower() == user.favorite_genre.lower():
            base_score += self.bonus
            reasons = reasons + [f"genre first bonus (+{self.bonus:.2f})"]
        return base_score, reasons
    
class MoodFirstStrategy(BaseStrategy):
    """Boost songs that match mood by an additional small bonus."""
    def __init__(self, bonus: float = 1.5):
        self.bonus = bonus

    def score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        base_score, reasons = super().score(user, song)
        if user.favorite_mood and song.mood and song.mood.lower() == user.favorite_mood.lower():
            base_score += self.bonus
            reasons = reasons + [f"mood first bonus (+{self.bonus:.2f})"]
        return base_score, reasons
    
class EnergyFocusedStrategy(BaseStrategy):
    """Boost songs whose energy is close to the user's target by an additional proportional bonus."""
    def __init__(self, bonus_multiplier: float = 1.5):
        self.bonus_multiplier = bonus_multiplier

    def score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        base_score, reasons = super().score(user, song)
        # energy similarity in [0,1]
        energy_sim = max(0.0, 1.0 - abs(getattr(user, "target_energy", 0.5) - getattr(song, "energy", 0.5)))
        if energy_sim > 0.0:
            bonus = energy_sim * self.bonus_multiplier
            base_score += bonus
            reasons = reasons + [f"energy focus bonus (+{bonus:.2f})"]
        return base_score, reasons
    
class Recommender:
    """
    OOP implementation of the recommendation logic.
    Supports injecting different ScoringStrategy implementations (like GenreFirst, 
    MoodFirst, EnergyFocused) via the `mode` parameter to dynamically alter 
    scoring and ranking behavior.
    """
    def __init__(self, songs: List[Song], mode: str = "base"):
        self.songs = songs
        # select strategy
        if mode == "genre_first":
            self.strategy: ScoringStrategy = GenreFirstStrategy()
        elif mode == "mood_first":
            self.strategy = MoodFirstStrategy()
        elif mode == "energy_focused":
            self.strategy = EnergyFocusedStrategy()
        else:
            self.strategy = BaseStrategy()

    def recommend(self, user: UserProfile, k: int = 5,
                  artist_penalty: float = 0.7, genre_penalty: float = 0.8,
                  max_per_artist: Optional[int] = None, max_per_genre: Optional[int] = None) -> List[Song]:
        # compute base scores using strategy
        scored: List[Tuple[float, Song]] = []
        for song in self.songs:
            base_score, _ = self.strategy.score(user, song)
            scored.append((float(base_score), song))
        scored.sort(key=lambda t: (-t[0], t[1].id))

        # greedy selection with diversity penalties
        selected: List[Song] = []
        artist_counts: Dict[str, int] = {}
        genre_counts: Dict[str, int] = {}

        for base_score, song in scored:
            if len(selected) >= k:
                break
            artist = (song.artist or "").strip().lower()
            genre = (song.genre or "").strip().lower()
            a_count = artist_counts.get(artist, 0)
            g_count = genre_counts.get(genre, 0)

            if max_per_artist is not None and a_count >= max_per_artist:
                continue
            if max_per_genre is not None and g_count >= max_per_genre:
                continue

            adj_score = base_score * (artist_penalty ** a_count) * (genre_penalty ** g_count)

            selected.append(song)
            artist_counts[artist] = a_count + 1
            genre_counts[genre] = g_count + 1

        return selected

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return self.strategy.explain(user, song)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file, casting numerical strings into floats and ints.
    Provides the data source for our Content-Based recommender.
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

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "base") -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Scores the entire catalog against user preferences, applies dynamic bonus scoring 
    based on the selected `mode` (genre_first, mood_first, energy_focused), 
    and sorts the results to return the top `k` recommendations along with explanations.
    """
    scored_songs = []
    
# Loop over every song in the catalog
    for song in songs:
        # 1. Use the judge to calculate base score
        score, reasons = score_song(user_prefs, song)
        
        # 2. Apply mode-specific bonus and annotate reasons
        if mode == "genre_first":
            if 'genre' in user_prefs and user_prefs.get('genre') and song.get('genre') and song['genre'].lower() == user_prefs['genre'].lower():
                bonus = 1.5
                score += bonus
                reasons.append(f"genre-first bonus (+{bonus:.2f})")
        elif mode == "mood_first":
            if 'mood' in user_prefs and user_prefs.get('mood') and song.get('mood') and song['mood'].lower() == user_prefs['mood'].lower():
                bonus = 1.5
                score += bonus
                reasons.append(f"mood-first bonus (+{bonus:.2f})")
        elif mode == "energy_focused":
            user_energy = float(user_prefs.get('energy', 0.5))
            song_energy = float(song.get('energy', 0.5))
            energy_sim = max(0.0, 1.0 - abs(user_energy - song_energy))
            if energy_sim > 0.0:
                bonus = 1.5 * energy_sim
                score += bonus
                reasons.append(f"energy-focus bonus (+{bonus:.2f})")
        
        # 3. Format the reasons list into a single readable string
        explanation = ", ".join(reasons) if reasons else "No matching vibe found."
        
        # 4. Store the result
        scored_songs.append((song, float(score), explanation))
        
    # Sort by score descending, deterministic tie-breaker by id
    scored_songs.sort(key=lambda item: (-item[1], int(item[0].get("id", 0))))
    
    # Return the top k elements slice
    return scored_songs[:k]

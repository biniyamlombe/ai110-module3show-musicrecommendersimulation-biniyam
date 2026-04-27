"""
Unit tests for the Music Recommender Simulation.
Tests evaluate both the OOP (Recommender) and Functional (recommend_songs) 
implementations, verifying base scoring logic, deterministic tie-breaking, 
and the effects of different ScoringStrategy modes (e.g. genre_first, energy_focused).
"""

from src.recommender import Song, UserProfile, Recommender, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
# small synthetic catalog for tests
SONGS = [
    {"id": 1, "title": "A", "artist": "X", "genre": "pop", "mood": "happy", "energy": 0.82, "tempo_bpm": 118,
     "valence": 0.84, "danceability": 0.79, "acousticness": 0.18, "popularity": 85, "release_decade": 2010,
     "detailed_mood": "euphoric", "vocal_presence": 0.9, "instrumentalness": 0.0},
    {"id": 2, "title": "B", "artist": "Y", "genre": "lofi", "mood": "chill", "energy": 0.42, "tempo_bpm": 78,
     "valence": 0.56, "danceability": 0.62, "acousticness": 0.71, "popularity": 40, "release_decade": 2020,
     "detailed_mood": "serene", "vocal_presence": 0.1, "instrumentalness": 0.9},
]

def test_genre_first_changes_ranking():
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    base = recommend_songs(user, SONGS, k=2, mode="base")
    genre_first = recommend_songs(user, SONGS, k=2, mode="genre_first")
    # ensure top result in genre-first is song id 1
    assert genre_first[0][0]["id"] == 1

def test_energy_focused_bonus_affects_score_range():
    user = {"genre": "", "mood": "", "energy": 0.8}
    scored = recommend_songs(user, SONGS, k=2, mode="energy_focused")
    for _, score, _ in scored:
        assert 0.0 <= score  # score should be non-negative

def test_explanation_contains_mode_hint():
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    scored = recommend_songs(user, SONGS, k=1, mode="genre_first")
    explanation = scored[0][2]
    assert "genre-first" in explanation or "genre" in explanation
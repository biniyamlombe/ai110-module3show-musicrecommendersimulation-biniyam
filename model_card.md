# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**  

---

## 2. Intended Use  

This recommender is designed to generate customized music playlist suggestions based on a user's specific "taste profile". It assumes the user knows exactly what overarching genre and mood they want, and what "energy" level they are looking for. This simulation is intended for classroom exploration and conceptual testing only, not for a production commercial application.

---

## 3. How the Model Works  

The algorithm uses a "Content-Based Filtering" methodology. Rather than looking at what other users listen to, it calculates a numerical score for every single song in our catalog by comparing the user's requested features directly against the song's features. 
- A song earns a massive bonus score (+1.0 point) if it hits the exact requested genre or mood string.
- **Advanced String matching:** A song earns +1.5 points for matching a highly specific `detailed_mood` string and +1.0 for matching the explicit `release_decade`.
- **Numerical traits** like "energy", "valence", "vocal_presence", "instrumentalness", and "popularity" use a math-based distance calculation. If a user asks for an energy of 0.8 and the song is 0.8, it earns the maximum points. The further away the song's data is from the user's preference, the fewer points it earns.
- **Recommendation Modes (Strategy Pattern):** The algorithm now supports dynamic scoring strategies. Users can select modes like `GenreFirst`, `MoodFirst`, or `EnergyFocused` to wrap the base score and apply targeted bonus multipliers.
- **Diversity Penalties:** To prevent "filter bubbling" where a single artist dominates the results, the system employs a greedy selection phase that applies multiplicative penalties (`artist_penalty`, `genre_penalty`) to repeating artists and genres, optionally enforcing hard caps.
Finally, the system ranks all the songs based on their adjusted score and returns the top 5!

---

## 4. Data  

Our dataset (`data/songs.csv`) contains a curated catalog of exactly 18 songs. I expanded the original dataset to include wilder outliers like "Heavy Metal" and "Cyberpunk" across diverse tempos and valences. 
I also completed **Challenge 1**, upgrading the table by adding 5 advanced columns of data per song: `popularity`, `release_decade`, `detailed_mood`, `vocal_presence`, and `instrumentalness`.
A major limitation of this data is its size—with only 18 tracks representing the entirety of world music, the algorithm is forced to recommend wildly mismatched songs to users simply because there aren't enough exact matches in the catalog.

---

## 5. Strengths  

This system works exceptionally well for users who want standard, high-tempo pop or strictly defined low-tempo chill acoustic music. Because genre matching earns flat points while energy uses distance vectors, the system brilliantly separates fast, aggressive music from relaxing music when interpreting basic user profiles. 

---

## 6. Limitations and Bias 

One major weakness is "Filter Bubbling" caused by feature weight imbalances. When I tested an "Adversarial" user who requested happy music with extremely low energy but demanded the Metal genre, the system completely ignored the only Metal song in the catalog. Because our algorithm heavily weights numerical features (Energy/Valence), the model prioritized mathematically perfect but culturally irrelevant tracks (like Reggae!) over imperfect songs in the requested genre. This creates a bias where the system automatically filters out genres that don't inherently fit strict numerical expectations.

---

## 7. Evaluation  

I systematically tested the recommender using three diverse profiles: "High-Energy Pop", "Chill Lofi", and an adversarial rule-breaking "Adversarial Metal" profile.
When comparing the Pop profile vs the Lofi profile, the outputs behaved exactly as human intuition would expect. However, what surprised me was the result from the adversarial test. The system ranked a Reggae song as the best Heavy Metal recommendation strictly because the underlying numbers matched our math formula closely enough to override the genre tag. This proved that purely math-based systems can fail the intuition test!

---

## 8. Future Work  

If I were to continue developing this:
1. I would add a "Strict Filter" override, so a user could say "ONLY show me Rock music", turning genre into a binary pass/fail rather than just a weighted point bonus.
2. I would dramatically increase the dataset size so that users aren't recommended irrelevant music simply because the catalog ran out of options.
3. I would add social "Collaborative Filtering" elements so the system could recommend a song simply because a friend liked it, overriding the strict audio math entirely.

---

## 9. Personal Reflection  

My biggest learning moment during this project was realizing that recommenders don't actually "know" what music is—they are completely blind systems mathematically grouping floating-point numbers together based on weights! 
Using AI tools helped me rapidly build out the Python sorting structures, but I had to double-check the AI whenever we shifted the weighted points (like halving genre vs doubling energy) to ensure the math actually resulted in human-readable music recommendations. 
It was incredibly surprising how "smart" a simple addition/subtraction algorithm can feel when you apply it to strings like "Happy Pop". 
If I extended this project, I would love to connect it to the actual Spotify API to let this algorithm judge and score millions of real tracks based on these tiny math rules!

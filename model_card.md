# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

One major weakness I discovered during my experiments is "Filter Bubbling" caused by feature weight imbalances. When I tested an "Adversarial" user who requested happy music with extremely low energy but demanded the Metal genre, the system completely ignored the only Metal song in the catalog. Because I had experimentally doubled the weight of the Numerical features (Energy/Valence), the model prioritized mathematically perfect but culturally irrelevant tracks (like Reggae!) over imperfect songs in the requested genre. This creates a bias where the system heavily discriminates against genres that don't conform to strict mathematical boundaries.

---

## 7. Evaluation  

I systematically tested the recommender using three diverse profiles: "High-Energy Pop", "Chill Lofi", and an adversarial rule-breaking "Adversarial Metal" profile (requesting intense metal but with extremely low energy/high valence parameters).

When comparing the Pop profile vs the Lofi profile, the outputs behaved perfectly—the system easily separated high-energy vibrant tracks from low-energy relaxing ones. However, what surprised me was the result from the adversarial test. The system ranked a Reggae song as the best Heavy Metal recommendation strictly because the underlying numbers matched our math formula. This proved that purely math-based systems can sometimes fail the "human intuition" test if weights are not properly balanced!

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

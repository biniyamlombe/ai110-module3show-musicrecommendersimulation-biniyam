# 🪞 System Reflection

## Profile Comparisons

**1. High-Energy Pop vs. Chill Lofi Profiles**
When comparing the High-Energy Pop profile against the Chill Lofi profile, the recommended list was entirely different. The Pop profile grabbed fast, intense tracks like "Sunrise City" and "Gym Hero," while the Lofi profile completely abandoned those in favor of acoustic, slow tracks like "Library Rain" and "Acoustic Sunset." This makes perfect sense! Our scoring algorithm uses distance math for energy restrictions. The Lofi profile prefers low energy (0.3), meaning that whenever it evaluated a high-energy pop track, the track lost massive similarity points and fell to the bottom of the rankings. 

**2. Explaining "Gym Hero" (Pop vs Adversarial Metal)**
To explain this simply: "Gym Hero" keeps showing up at the top of the list for Happy Pop fans because our recipe gives out massive points for matching the correct genre tag and high energy levels. However, during our "Adversarial Metal" test, the user specifically asked for Heavy Metal music, but assigned themselves extremely low energy and high happiness requirements! Because of this, actual Heavy Metal tracks failed the math test, and the system literally recommended a "Reggae" track as the winner. This shows a limitation of our code: the math rules are so strict that our simulation will ignore a user's stated genre if the raw energy numbers align better elsewhere.

## Challenge 1: Advanced Song Features
I extended the baseline dataset by adding 5 advanced complex attributes: `popularity`, `release_decade`, `detailed_mood`, `vocal_presence`, and `instrumentalness`. By programming custom weighting matrices for these (such as assigning a flat +1.5 bonus for a perfect `detailed_mood` match rather than a basic mood match), the algorithm became dramatically more precise. I learned that adding granular tracking data allows the math to create highly robust recommendations that begin to mirror the complexity of a fully commercial application.


## Challenge 2: Multiple Scoring Modes

I implemented a simple Strategy pattern and three ranking modes: genre first, mood-first, and energy focused. Each mode wraps the base score and applies a small bonus that emphasizes one primary signal. This allowed quick experiments showing how weighting changes reorder recommendations and exposed tie breaker behavior. Unit tests were added to verify mode specific effects (ordering, score validity, and explanation contents).

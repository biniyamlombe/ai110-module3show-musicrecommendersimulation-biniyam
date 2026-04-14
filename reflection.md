# 🪞 System Reflection

## Profile Comparisons

**1. High-Energy Pop vs. Chill Lofi Profiles**
When comparing the High-Energy Pop profile against the Chill Lofi profile, the recommended list was entirely different. The Pop profile grabbed fast, intense tracks like "Sunrise City" and "Gym Hero," while the Lofi profile completely abandoned those in favor of acoustic, slow tracks like "Library Rain" and "Acoustic Sunset." This makes perfect sense! Our scoring algorithm uses distance math for energy restrictions. The Lofi profile prefers low energy (0.3), meaning that whenever it evaluated a high-energy pop track, the track lost massive similarity points and fell to the bottom of the rankings. 

**2. Explaining "Gym Hero" (Pop vs Adversarial Metal)**
To explain this simply: "Gym Hero" keeps showing up at the top of the list for Happy Pop fans because our recipe gives out massive points for matching the correct genre tag and high energy levels. However, during our "Adversarial Metal" test, the user specifically asked for Heavy Metal music, but assigned themselves extremely low energy and high happiness requirements! Because of this, actual Heavy Metal tracks failed the math test, and the system literally recommended a "Reggae" track as the winner. This shows a limitation of our code: the math rules are so strict that our simulation will ignore a user's stated genre if the raw energy numbers align better elsewhere.

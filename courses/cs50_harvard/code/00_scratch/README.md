# 🎮 The Gravity-Switcher

**CS50 Week 0 Project** | Physics-Based Platformer Game  
**Course:** Harvard CS50x Introduction to Computer Science  
**Developer:** Manuel Reyes | [LinkedIn](https://linkedin.com/in/mr410) | [Portfolio](https://manuel-reyes-ml.github.io/learning_journey/)

[![Play on Scratch](https://img.shields.io/badge/Play-Scratch-orange?logo=scratch)](https://scratch.mit.edu/projects/YOUR_PROJECT_ID/)
[![View Code](https://img.shields.io/badge/View-GitHub-blue?logo=github)](https://github.com/manuel-reyes-ml/learning_journey/tree/main/cs50_harvard/scratch)

---

## 🎯 Project Overview

An **infinite runner platformer** where instead of jumping, you flip gravity to run on the ceiling. Built to demonstrate fundamental computer science concepts including physics simulation, coordinate geometry, and memory management.

**🎮 [Play the game →](https://scratch.mit.edu/projects/YOUR_ID/)**

### Key Features

- **Dynamic Physics Engine:** Real acceleration/deceleration using velocity variables
- **Procedural Generation:** Infinite obstacles spawned using cloning & randomization  
- **Coordinate-Based Collision:** Mathematical boundary detection (stable & bug-free)
- **State Management:** Clean variable architecture for game state tracking

---

## 🚀 Quick Start

### Play Online
1. Visit [scratch.mit.edu/projects/YOUR_ID](https://scratch.mit.edu/projects/YOUR_ID/)
2. Click the green flag to start
3. Press **SPACE** to flip gravity
4. Dodge the lightning bolts!

### Run Locally
1. Download `gravity-switcher.sb3` from this repository
2. Go to [scratch.mit.edu](https://scratch.mit.edu)
3. Click "File" → "Load from your computer"
4. Select the downloaded `.sb3` file

---

## 🎓 CS50 Requirements Met

✅ **2+ Sprites:** Player (Cyber-Square) + Hazard (Lightning)  
✅ **3+ Scripts:** Player movement, hazard spawner, hazard mover  
✅ **Conditional:** Collision detection, input handling  
✅ **Loop:** Forever game loop, obstacle movement  
✅ **Variable:** y_velocity, gravity_direction, score  
✅ **Custom Block:** *(Add if you created one, otherwise create one)*

---

## 🧠 Technical Deep Dive

### Architecture Decisions

#### **1. Physics Simulation**
**Challenge:** Make movement feel natural with acceleration/deceleration  
**Solution:** Implemented velocity-based physics system
```
Physics Loop (Forever):
  velocity = velocity + (gravity_direction * acceleration)
  y_position = y_position + velocity
  
  If y_position < -150:
    y_position = -150
    velocity = 0
```

**Why this works:** Real objects accelerate under gravity. Using velocity creates smooth, realistic movement vs. fixed-step jumping.

---

#### **2. Coordinate Math vs. Color Sensing**
**Initial Approach:** Used "touching color" for collision  
**Problem:** Caused vibration bugs & sprite sticking

**Final Approach:** Mathematical boundaries
```
If y_position < -150 then set y to -150
If y_position > 150 then set y to 150
```

**Result:** Eliminated collision bugs entirely. More reliable than color sensing.

---

#### **3. Memory Management (Cloning)**
**Challenge:** Need infinite obstacles without creating 50 separate sprites  
**Solution:** Clone spawner pattern
```
Spawner (Forever):
  Wait random(1-3) seconds
  Create clone of [Lightning]

Clone Worker:
  Go to x: 240
  Forever:
    Move -10 steps
    If x < -230: delete this clone
```

**Why this matters:** Prevents memory overflow (Scratch limit = 300 clones). Shows understanding of resource constraints.

---

## 📊 Skills Demonstrated

| CS50 Concept | Implementation | Real-World Application |
|--------------|----------------|------------------------|
| **Algorithms** | Gravity algorithm (velocity += acceleration) | Game engines, physics simulations |
| **Abstraction** | Clone pattern vs. individual sprites | Object-oriented programming |
| **Decomposition** | Separate physics/spawning/collision logic | Modular code architecture |
| **Data Structures** | Variables for state management | Database design, state machines |
| **Concurrency** | Multiple sprites running simultaneously | Multi-threaded applications |

---

## 🐛 Debugging Journey

### Major Bug Fixed: "Sticky Collision"

**Symptom:** Player would vibrate when touching floor/ceiling  
**Root Cause:** Using "touching color" created feedback loop
```
Bad Logic:
If touching [pink floor]:
  move up 5 steps  ← Player moves up
  (Still touching floor, moves again → vibration)
```

**Solution:** Switched to coordinate boundaries
- Forcibly set y_position to exact boundary value
- Prevents feedback loop entirely
- Demonstrates understanding of numerical stability

**Lesson Learned:** Mathematical comparisons > visual detection for physics

---

## 📈 Future Enhancements

If I rebuild this in Python/JavaScript:
- [ ] Add score system with difficulty progression
- [ ] Multiple obstacle types with different speeds
- [ ] Power-ups (shield, slow motion)
- [ ] Parallax scrolling backgrounds
- [ ] Leaderboard (local storage)
- [ ] Mobile touch controls

---

## 💡 What I Learned

### Computer Science Concepts
1. **Variables model real-world physics:** velocity, acceleration, position
2. **Coordinate geometry is powerful:** Math > visual detection
3. **Resource management matters:** Delete unused clones
4. **Iteration is key:** Started with color sensing, evolved to coordinates

### Transferable Skills
- Breaking complex problems into smaller functions
- Debugging systematically (isolate, test, fix)
- Choosing right algorithm for the job
- Documentation explains *why*, not just *what*

---

## 🔗 Related Projects

**Learning Journey:** [github.com/manuel-reyes-ml/learning_journey](https://github.com/manuel-reyes-ml/learning_journey)  
**37-Month Roadmap:** [manuel-reyes-ml.github.io/learning_journey/roadmap.html](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)

---

## 📜 License

MIT License - Feel free to learn from this code!

---

## 🙏 Acknowledgments

- **CS50 Staff:** Prof. David J. Malan and team for incredible course
- **MIT Media Lab:** Scratch development team
- **CS50 Community:** Fellow students for inspiration

---

## 📫 Connect

I'm on a 37-month journey from **Financial Services Professional → Senior LLM Engineer**.  
Currently in Stage 1 (Data Analyst), actively seeking opportunities!

**LinkedIn:** [linkedin.com/in/mr410](https://linkedin.com/in/mr410)  
**Email:** manuelreyesv410@gmail.com  
**Portfolio:** [manuel-reyes-ml.github.io](https://manuel-reyes-ml.github.io/learning_journey/)

**Open to:** Data Analyst roles, mentorship, trading + tech collaborations

---

*"From Scratch blocks to production systems - every expert was once a beginner."*
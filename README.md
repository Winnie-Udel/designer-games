## Contributors

---
| Name                  | UD Email               |
|:----------------------|:-----------------------|
| Winnie Li             | winnie@udel.edu        |
| Samita Bomasamudram   | samiboma@udel.edu      |

## Pitch

---
In *Shark Invasion*, the player plays as a small, vulnerable fish amidst the deep 
blue ocean. The goal is simple: survive and grow! To do so, avoid the 
predators and consume the food before the timer runs out! Beware, predators 
exist above and beneath the ocean.

## Game Plan

---
### Phase 1
- [X] Fish Exists: *There is a fish on the screen.*
- [X] Fish Moves: *The fish moves left, right, up, and down when the arrow keys
are pressed.*
- [X] Screen Limits: *The fish cannot be moved offscreen, instead it wraps to the 
other side.*
- [X] Spawning Shrimp: *Shrimp randomly spawns within the given boundaries.*

[Video: Phase 1 Progress](https://youtu.be/xGT1E1P8qBs)

### Phase 2
- [X] Grow: *If fish collide with shrimp, the fish grows bigger.*
- [X] Spawning Sharks: *Sharks randomly spawn within the given boundaries.*
- [X] Shark Move: *Sharks move from side to side.*
- [X] Fish Hurt: *If fish collide with a shark, the player loses a life.* 
- [X] Fish Last Life: *If player has one life left, fish starts flickering.*

[Video: Phase 2 Progress](https://youtu.be/jQUauZPf3S8)

### Phase 3
- [X] Display Stats: *A section of the screen that displays the timer, current 
score, and number of lives.*
- [ ] Game Over: *Displays the player's final score when the player runs 
out of lives/timer runs out.*
- [X] Bonus Points: *If player has remaining lives left after the timer runs out, each lives count as 
an extra 15 points.*
- [X] Play Button: *A cover screen with a play button.*
- [X] More Sharks: *As the game progresses, more shark is spawned. The difficulty grows 
as the shark also grows in speed.*
- [ ] Marine Snow: *Marine snow will descend from above, and if collides with fish, the
fish shrinks.*
- [X] Add Time: *Time-power ups would descend from above, and if collides with fish,
15 more seconds is added to the timer.*
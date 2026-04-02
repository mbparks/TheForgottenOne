# The Forgotten One

**A text adventure of memory, loss, and truth.**

You wake in an old house. You don't know your name. You don't know how you got here. But the rooms feel familiar — not like a stranger's home, but like your own after a long trip away.

Somewhere in the dust and silence, there are objects that hold pieces of who you used to be. A locket with a photograph. A journal in your handwriting. A pocket watch that stopped ticking a long time ago. Each one unlocks a fragment of a life you've forgotten — a mother, a career, a marriage, a child.

But you are not alone. Something else moves through the house. **The Darkness** — a creeping, formless presence that erases everything it touches. If it finds you, your memories unspool and vanish, and you wake again in a house you no longer recognize. It has rearranged itself around the hole where you used to be.

Find the artifacts. Recover the memories. Piece together the life of the person who lived here. And when the final truth reveals itself — the one the house has been keeping from you all along — decide whether you're ready to hear it.

---

## Features

- **Procedurally generated layouts** — the house rebuilds itself every playthrough. Room selection, connections, and item placement are randomized from a pool of 17 rooms, 5 memory artifacts, and 18 flavor objects. No two games are the same.

- **A layered narrative** — five memory artifacts tell a complete life story across a mother's lullaby, a career in botany, a wedding, a child, and a letter that means more than it first appears. The story rewards attention and recontextualizes details you noticed but dismissed.

- **The Darkness** — a roaming threat that occupies a room for several turns before relocating. Adjacent rooms carry warning signs. Entering The Darkness triggers a 3-turn countdown: escape, or lose everything. Recovery of a specific memory unlocks a way to fight back.

- **Flavor objects** — not every item triggers a memory. Briar pipes, chess pieces, pressed orchids, recipe cards, and medicine bottles fill out the world without advancing the plot. They make real discoveries feel earned rather than inevitable, and some carry quiet significance that only lands after the ending.

- **Persistent consequences** — if The Darkness consumes you, the game resets with a new layout and empty inventory, but your death count carries forward. The finale acknowledges how many times you were lost and incorporates it into the story's resolution.

---

## Requirements

- Python 3.6+
- A terminal that supports Unicode characters (most modern terminals)
- No external dependencies

## Installation

```bash
git clone https://github.com/yourusername/the-forgotten-one.git
cd the-forgotten-one
```

## Running the Game

```bash
python ghost_adventure.py
```

On some systems you may need `python3` instead of `python`.

---

## How to Play

### Commands

| Command | Aliases | Description |
|---|---|---|
| `go <direction>` | `n`, `s`, `e`, `w` | Move to an adjacent room |
| `look` | `l` | Re-examine your current surroundings |
| `take <item>` | `get`, `grab`, `pick` | Pick up an item in the room |
| `examine <item>` | `x`, `inspect`, `read` | Study a held item closely |
| `hum` | `sing`, `lullaby` | Hum whatever melody you can remember |
| `inventory` | `inv`, `i` | List what you're carrying |
| `memories` | `memory`, `remember` | Review recovered memory fragments |
| `map` | `m` | See rooms you've visited and uncollected items |
| `help` | `?` | Show the command list in-game |
| `quit` | `exit`, `q` | Attempt to leave the house |

### Movement

Type a direction to move: `north`, `south`, `east`, `west`, or their single-letter abbreviations `n`, `s`, `e`, `w`. You can also type `go north` or just `north`. Room descriptions list all available exits and where they lead. Exits marked with `↑stairs` or `↓stairs` move between floors.

### Items

The house contains two kinds of items:

- **Memory artifacts** unlock a recovered memory when examined. These are marked with a `✦` in your inventory after examination. There are five in every game, and finding all five triggers the ending.

- **Flavor objects** can be picked up and examined but don't trigger memories. They flesh out the world and the life of the person who lived here. Some contain details that resonate differently after the ending.

Items appear in room descriptions when you enter or `look`. Pick them up with `take`, then `examine` them from your inventory. You don't need to be in the same room to examine something you've already picked up. Partial names work — `take locket` and `take silver` both work for the Tarnished Silver Locket.

### The Darkness

A presence roams the house. It occupies one room at a time, staying for several turns before relocating.

**Warning signs.** When The Darkness is in an adjacent room, you'll notice unsettling details — a chill, a pull toward a certain exit, shadows that feel too heavy. These are your signal to move the other direction.

**Encounter.** If you enter a room where The Darkness is waiting, the atmosphere changes dramatically. You have **3 turns** to act before it consumes you.

**Escape.** Move to any adjacent room. Leaving the room immediately ends the encounter.

**The Lullaby.** After recovering a specific memory, you learn a melody you can hum. Typing `hum` while in The Darkness's room banishes it entirely for 8–14 turns. You can also hum from an adjacent room to push it further away.

**Consumption.** If you neither leave nor hum within 3 turns, The Darkness takes you. Your memories unravel. The game restarts with a completely new house layout, new item placement, and an empty inventory. Your reset count persists and is acknowledged in the story.

**Strategy.** The Darkness never appears in the foyer. Pay attention to ambient descriptions when revisiting rooms — nearby warnings appear as subtle flavor text. If you have the lullaby, you can hum preemptively in any room to check whether The Darkness is close and push it away without confronting it directly.

### Winning

Find and examine all five memory artifacts. The order doesn't matter. Once the fifth memory is recovered, the ending plays automatically. There is no way to lose the ending once it begins — even The Darkness cannot interrupt it.

### The Map

Type `map` to see a list of every room you've visited, which floor it's on, and whether uncollected items remain. Your current location is marked with `◄`. Rooms you haven't entered yet don't appear on the map.

---

## Tips for First-Time Players

- **Explore thoroughly.** Not every item is a memory artifact. Some rooms have multiple objects. The map command helps track what you've missed.

- **Listen to the house.** Ambient descriptions change on repeat visits and can hint at nearby danger or narrative details that matter later.

- **Find the lullaby early.** One of the five artifacts gives you the ability to hum. Without it, your only option against The Darkness is to run. With it, you control the encounter.

- **Read everything twice.** Flavor objects, room descriptions, and ambient text contain details that land differently once you know the ending. The game rewards a second playthrough.

- **Don't rush the ending.** The finale is paced deliberately. Let it breathe.

---

## Architecture

The game is a single Python file with no dependencies. Key systems:

- **Procedural generation** selects 8–10 rooms from a pool of 17, builds a connected graph with randomized exits per floor, links floors via stairs, and distributes items randomly.

- **The Darkness** operates on a turn-based roaming timer (5–8 turns per room) with a 3-turn encounter countdown. Banishment disables it for 8–14 turns before it reforms in a new room.

- **Narrative milestones** fire at memory counts 3 and 4, contextualizing discoveries. The finale adjusts its text based on whether the player was ever consumed.

---

## License

 GPL-3.0 license

---

*Thank you for helping Elias remember. Thank you for helping him go home.*

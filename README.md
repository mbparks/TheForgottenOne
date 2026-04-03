# The Forgotten One

**A text adventure of memory, loss, and truth.**

Play here:  https://mbparks.com/loss

You wake in an old house. You don't know your name. You don't know how you got here. But the rooms feel familiar — not like a stranger's home, but like your own after a long trip away.

Somewhere in the dust and silence, there are objects that hold pieces of who you used to be. A locket with a photograph. A journal in your handwriting. A pocket watch that stopped ticking a long time ago. Each one unlocks a fragment of a life you've forgotten — a mother, a career, a marriage, a child.

But not every memory is warm. Somewhere in this house, behind a rusted iron lock, there is something you hid from yourself on purpose. Something that hurt too much to look at. You'll need to decide whether to open it.

And you are not alone. **The Darkness** — a creeping, formless presence that erases everything it touches. If it finds you, your memories unspool and vanish, and you wake again in a house you no longer recognize.

Find the artifacts. Recover the memories. Piece together the life of the person who lived here. And when the final truth reveals itself — the one the house has been keeping from you all along — decide whether you're ready to hear it.

---

## Features

- **Procedurally generated layouts** — the house rebuilds itself every playthrough. Room selection, connections, and item placement are randomized from a pool of 17 rooms, 6 memory artifacts, and 19 other objects. No two games are the same.

- **A locked safe** — one memory is hidden behind an iron strongbox that requires a key found elsewhere in the house. What's inside is something Elias locked away on purpose. You don't have to open it. But if you don't, you'll carry that weight with you.

- **Two endings** — the game can be completed with 5 of 6 memories for a bittersweet ending where Elias crosses over but leaves something unresolved. Finding and confronting the locked memory unlocks the full ending, with a reconciliation that only works because Elias chose to face it.

- **An interactive twist** — at the climax, the game stops and asks you a question. Your answer changes how the ending plays out.

- **The Darkness** — a roaming threat that hunts what you need, grows faster with each reset, and corrupts the game's own text as it closes in. Recovery of a specific memory unlocks a way to fight back.

- **Room decay** — rooms deteriorate the more you visit them. The portrait darkens. The armchair collapses. The nursery crib lays itself down. The house is dissolving because remembering is what lets it go.

- **Unreliable text** — when The Darkness is nearby, room descriptions start lying. Words swap: "four" becomes "five," "home" becomes "tomb." At close range, inventory names glitch and text dissolves into black bars. The narrator is failing.

- **Traces between runs** — when The Darkness consumes you and the house resets, remnants of your previous life survive as ambient messages: tally marks on a doorframe, a note in your handwriting saying "DON'T FORGET THE LULLABY," a scrap referencing your last recovered memory.

- **Real clock integration** — the game reads your device's local time. Late-night play gets different ambient text than morning play. And if you happen to be playing at exactly 11:47 PM — the moment Elias died — a special event triggers that most players will never see.

- **Procedural audio** (browser version) — all sound is synthesized live with the Web Audio API. A droning hum shifts between floors. The lullaby plays actual music-box notes. The Darkness rumbles below hearing. Memory recovery swells a warm chord. No audio files — everything is generated in real time.

- **Textual sound descriptions** (Python version) — bracketed atmospheric descriptions convey what the player would hear, from the lullaby's three crystalline notes to the Darkness's sub-audible rumble.

---

## Requirements

**Browser version:** Any modern browser. No installation, no server, no dependencies.

**Python version:** Python 3.6+. No external packages. A terminal with Unicode support.

## Installation

```bash
git clone https://github.com/yourusername/the-forgotten-one.git
cd the-forgotten-one
```

## Running the Game

**Browser (recommended):**
Open `the-forgotten-one/index.html` in any browser, or host it on any static server. For GitHub Pages, push the repo and enable Pages in Settings.

**Python terminal:**
```bash
python ghost_adventure.py
```

---

## How to Play

### Commands

| Command | Aliases | Description |
|---|---|---|
| `go <direction>` | `n`, `s`, `e`, `w` | Move to an adjacent room |
| `look` | `l` | Re-examine your current surroundings |
| `take <item>` | `get`, `grab`, `pick` | Pick up an item in the room |
| `examine <item>` | `x`, `inspect`, `read` | Study a held item closely |
| `open` | `unlock`, `use` | Open a locked container (when present) |
| `hum` | `sing`, `lullaby` | Hum whatever melody you can remember |
| `step` | `leave`, `through`, `cross` | Step through (when the way is open) |
| `inventory` | `inv`, `i` | List what you're carrying |
| `memories` | `memory`, `remember` | Review recovered memory fragments |
| `map` | `m` | See rooms you've visited and uncollected items |
| `help` | `?` | Show the command list in-game |
| `quit` | `exit`, `q` | Attempt to leave the house |

### Movement

Type a direction: `north`, `south`, `east`, `west`, or abbreviate to `n`, `s`, `e`, `w`. Room descriptions list all exits and where they lead. Exits marked with `↑stairs` or `↓stairs` connect floors.

### Items

The house contains three kinds of items:

- **Memory artifacts** unlock a recovered memory when examined. Marked with `✦` in your inventory. There are six total — five placed openly and one locked in a strongbox.

- **The iron key** is a mechanical item needed to open the strongbox. It doesn't trigger a memory, but finding it is essential for the full ending.

- **Flavor objects** can be picked up and examined but don't trigger memories. They flesh out the world. Some contain details that resonate differently after the ending.

Items appear in room descriptions when you enter or `look`. Pick them up with `take`, then `examine` them from your inventory. Partial names work — `take locket`, `take father`, `take iron` all work. The game prefers items in your current room when names are ambiguous.

### The Strongbox

One room contains a locked iron strongbox. When you find it, the description reads: *"An iron strongbox sits in the corner, its lock crusted with age but solid."*

To open it, you need the **Blackened Iron Key**, found in a different room. With the key in your inventory, type `open safe`, `open strongbox`, `unlock`, or `examine safe`. The strongbox opens and reveals its contents — a letter you can take and examine to unlock the sixth memory.

You don't have to open it. See "Two Endings" below.

### The Darkness

A presence roams the house, biased toward rooms containing uncollected memory artifacts. It gets faster after each reset.

**Warning signs.** Adjacent rooms show subtle cues — a chill, shadows too dark, a pull toward one exit.

**Encounter.** Entering its room triggers a countdown (3 turns on your first cycle, dropping to 2 after repeated resets). Text descriptions escalate with each turn.

**Unreliable text.** Near The Darkness, room descriptions corrupt. Words swap ("home" → "tomb"), inventory names glitch, and at close range text dissolves into black bars. Exit names are never corrupted so the game stays playable.

**Escape.** Move to any adjacent room. Leaving ends the encounter immediately.

**The Lullaby.** After recovering a specific memory, you unlock the `hum` command. Humming banishes The Darkness for 8–14 turns. You can also hum from an adjacent room to push it away preemptively.

**Consumption.** If the countdown reaches zero, your memories unravel one by one. The game resets with a new house layout and empty inventory. Your death count persists and is woven into the story.

### Two Endings

**The Lesser Ending (5 of 6 memories):** After collecting five memories without opening the strongbox, the study window begins to glow with golden light. The game tells you there's still something locked away in the house, but you could `step through` and leave. If you do, Elias crosses over to Margaret and Thomas — but feels a weight he can't name. *"Something locked in an iron box you never opened. Maybe some boxes stay closed. Or maybe you'll wonder. Forever."* The endgame screen reads: **"There is another ending."**

**The Full Ending (6 of 6 memories):** Find the iron key. Open the strongbox. Read the letter inside. Confront the memory it contains. The sixth memory triggers the complete finale automatically — including the interactive twist, the full life summary, and a figure standing at the edge of the light who wasn't there in the lesser ending. The strongbox is open. The letter is gone. Nothing is left behind.

### The Map

Type `map` to see every room you've visited, which floor it's on, and a count of uncollected items. Your location is marked with `◄`. Rooms you haven't entered don't appear.

---

## Tips for First-Time Players

- **Explore thoroughly.** The map command tracks uncollected items per room. Revisit rooms — the house changes as you do.

- **Find the lullaby early.** One of the six artifacts gives you the ability to hum. Without it, your only option against The Darkness is to run.

- **Pay attention to ambient text.** Room descriptions shift on repeat visits. Some hint at nearby danger. Some hint at the story. Some do both.

- **The strongbox is optional but significant.** You can finish the game without it. Whether you should is a different question.

- **Read everything twice.** Flavor objects, room descriptions, and the medicine bottle all contain details that only land after the ending.

- **Don't rush the ending.** Either one. They're paced deliberately. Let them breathe.

---

## Architecture

Both versions are synchronized — same rooms, items, mechanics, narrative, and endings.

**Browser (`the-forgotten-one/index.html`):**
A single self-contained HTML file. CSS, JS, and all game data are inlined. The only external request is a Google Font (IBM Plex Mono), with Courier New as fallback. Procedural audio via Web Audio API. CRT terminal aesthetic with scanlines, vignette, and screen effects for Darkness encounters and memory recovery. Works on mobile.

**Python (`ghost_adventure.py`):**
A single Python file with no dependencies. Typewriter text output, dramatic pauses, and bracketed sound descriptions for atmospheric moments. Runs in any terminal with Unicode support.

**Shared systems:**
- **Procedural generation** — 8–11 rooms selected from 17, connected via spanning tree + loop edges, floors linked by stairs, items distributed randomly with the strongbox and iron key guaranteed to be in separate rooms.
- **Smart Darkness** — turn-based roaming with 60% bias toward uncollected memory artifacts, escalating speed and shorter countdowns after resets.
- **Text corruption** — 25 word-swap pairs applied at 3 severity levels based on proximity to The Darkness.
- **Room decay** — 3-tier progressive descriptions triggered by visit count per room.
- **Traces** — 2 remnants per reset injected as ambient messages into the new layout.
- **Clock** — local time checked on revisits, with a special trigger at 23:47.
- **Priority matching** — item name resolution prefers the current room (for `take`) or inventory (for `examine`) to avoid ambiguity between similarly-named items.
- **Two finales** — lesser (5/6) and full (6/6) share structure but diverge in emotional resolution, with the full ending requiring the player to actively choose to confront a painful truth.

---

## File Structure

```
the-forgotten-one/
├── the-forgotten-one/
│   └── index.html        ← Browser version (single file, drop anywhere)
├── ghost_adventure.py     ← Python terminal version
└── README.md
```

---

## License

GPL-3.0 license

---

*Thank you for helping Elias remember.*
*Thank you for helping him go home.*

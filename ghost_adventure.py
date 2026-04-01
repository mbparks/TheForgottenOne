#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              T H E   F O R G O T T E N   O N E               ║
║         A Text Adventure of Memory and Discovery             ║
║                         M.B. Parks                           ║
╚══════════════════════════════════════════════════════════════╝

You wake in darkness. You don't know who you are.
You don't know where you are. You don't know *what* you are.
All you know is this house... and the feeling that something
important has been lost.

Collect the artifacts. Remember. Understand.
"""

import sys
import textwrap
import time
import os
import random

# ─────────────────────────── UTILITIES ───────────────────────────

TERM_WIDTH = 72

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.03, width=TERM_WIDTH):
    """Print text character-by-character for atmosphere."""
    wrapped = textwrap.fill(text, width=width)
    for ch in wrapped:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def dramatic_pause(seconds=1.0):
    time.sleep(seconds)

def print_separator(char="─", width=TERM_WIDTH):
    print(char * width)

def print_boxed(text, width=TERM_WIDTH):
    lines = textwrap.wrap(text, width=width - 6)
    print("╔" + "═" * (width - 2) + "╗")
    for line in lines:
        padding = width - 4 - len(line)
        print(f"║  {line}{' ' * padding}║")
    print("╚" + "═" * (width - 2) + "╝")

def prompt():
    print()
    return input("  > ").strip().lower()

# ────────────────────── MEMORY FRAGMENTS ─────────────────────────

MEMORY_FRAGMENTS = {
    "locket": {
        "name": "Tarnished Silver Locket",
        "room_desc": "A tarnished silver locket lies on the mantelpiece, its chain coiled like a sleeping snake.",
        "examine": "The locket is cold — impossibly cold. Your fingers pass through it twice before you focus hard enough to hold it. Inside is a faded photograph: a woman with kind eyes and a child on her lap. Something tugs inside you. You know that face. You KNOW it.",
        "memory": (
            "A flood of warmth. The scent of lavender and fresh bread. "
            "A voice — soft, melodic — singing a lullaby you can almost hum. "
            "\"Sleep now, my little one,\" she says. Mother. She was your MOTHER. "
            "You had a mother who loved you. The memory glows, then fades to "
            "a dull ache. You cannot remember her name."
        ),
        "memory_tag": "A mother's love — you were someone's child.",
        "order": 1,
    },
    "journal": {
        "name": "Water-Damaged Journal",
        "room_desc": "A journal lies open on the desk, its pages bloated and wavy from old water damage.",
        "examine": "The ink has bled into ghostly shapes, but a few entries survive. The handwriting is yours — you're certain of it, though you don't know how. Dates from 1923. Sketches of botanical specimens. Notes about a garden.",
        "memory": (
            "Sunlight through a greenhouse. Dirt under your fingernails. "
            "The satisfaction of watching something grow. You were a gardener — "
            "no, a botanist. You STUDIED plants. There was a university, "
            "a laboratory with jars of pressed flowers. Students called you "
            "\"Professor.\" You had a PURPOSE. You had a life of the mind."
        ),
        "memory_tag": "A life of science — you were a professor of botany.",
        "order": 2,
    },
    "pocketwatch": {
        "name": "Stopped Pocket Watch",
        "room_desc": "A pocket watch sits on the nightstand, its glass cracked in a starburst pattern. It has stopped at 11:47.",
        "examine": "The watch is heavier than it should be, as though it carries the weight of every second it has counted. Engraved on the back: \"To E.W. — Until the end of time. — M.\" The hands are frozen. 11:47. Why does that time fill you with dread?",
        "memory": (
            "A wedding. YOUR wedding. A autumn garden strung with lights. "
            "\"M\" — Margaret. Her name was MARGARET. She placed this watch "
            "in your hand and said, \"So you'll never lose track of time "
            "with me.\" You laughed. You danced. You were happy once. "
            "E.W. — your initials. Edward? Elias? The first name slips away, "
            "but the last name surfaces: Wren. You were E. Wren."
        ),
        "memory_tag": "A great love — you were married to someone named Margaret.",
        "order": 3,
    },
    "toy_train": {
        "name": "Painted Wooden Train",
        "room_desc": "A small hand-painted wooden train sits on a shelf, its red paint chipped to reveal bare wood beneath.",
        "examine": "You pick up the train and it fits perfectly in your palm, as though your hand was made for holding it — or made it. The paint is applied with love but not skill. An adult painted this for a child.",
        "memory": (
            "A small boy with your eyes. YOUR boy. He sits cross-legged on "
            "a rug, pushing a wooden train in circles, making 'choo-choo' sounds. "
            "\"Again, Papa! Make the whistle!\" You purse your lips and whistle, "
            "and he shrieks with delight. Thomas. His name was Thomas. "
            "Your SON. The memory is so vivid it burns."
        ),
        "memory_tag": "A child's laughter — you had a son named Thomas.",
        "order": 4,
    },
    "newspaper": {
        "name": "Yellowed Newspaper Clipping",
        "room_desc": "A yellowed newspaper clipping is pinned to the wall, curling at the edges.",
        "examine": "The clipping is from the Ashworth Gazette, dated November 3rd, 1923. The headline is partially obscured. You lean closer, and the words rearrange themselves as though the paper is afraid to show you what it says.",
        "memory": (
            "The headline finally holds still: \"PROFESSOR FOUND IN HOME — "
            "TRAGIC END TO BRILLIANT CAREER.\" Below, a photograph. YOUR "
            "photograph. The article speaks of a man found in his study, "
            "slumped over his desk. A weak heart, they said. 11:47 PM. "
            "The time the watch stopped. The time YOU stopped. "
            "The room goes cold. The house groans around you. "
            "You begin to understand."
        ),
        "memory_tag": "The truth draws near — a man died in this house.",
        "order": 5,
    },
}

# ──────────────────────────── ROOMS ──────────────────────────────

ROOMS = {
    "foyer": {
        "name": "The Foyer",
        "description": (
            "A grand entrance hall stretches before you, though 'grand' may be "
            "generous. Wallpaper peels from the walls in long strips, revealing "
            "dark plaster beneath. A chandelier hangs overhead, its crystals "
            "thick with dust, swaying gently though there is no wind. "
            "A staircase climbs into shadow to the north. Doorways lead "
            "east and west."
        ),
        "exits": {"north": "upstairs_hall", "east": "parlor", "west": "dining_room"},
        "artifact": None,
        "first_visit": True,
        "ambient": [
            "The chandelier sways. You don't feel any breeze.",
            "Dust motes drift in a shaft of pale light from nowhere.",
            "A floorboard creaks upstairs, though you haven't gone up yet.",
            "You catch movement in the corner of your eye. Nothing is there.",
        ],
    },
    "parlor": {
        "name": "The Parlor",
        "description": (
            "A sitting room frozen in time. Two armchairs face a cold fireplace, "
            "a chess game left mid-play on a small table between them. "
            "Bookshelves line the walls, their volumes coated in grey dust. "
            "Above the mantelpiece hangs a portrait, but the face has been "
            "scratched away — or has it faded? The foyer lies to the west."
        ),
        "exits": {"west": "foyer"},
        "artifact": "locket",
        "first_visit": True,
        "ambient": [
            "A chess piece topples on its own. The black king.",
            "You swear the scratched-out portrait watched you.",
            "The fireplace exhales a breath of cold ash.",
            "Pages of a book flutter open, then slam shut.",
        ],
    },
    "dining_room": {
        "name": "The Dining Room",
        "description": (
            "A long table set for a dinner party that never arrived — or never "
            "ended. Plates, glasses, and tarnished silverware sit before empty "
            "chairs. Cobwebs drape from the candelabra like lace. A door to the "
            "south leads to the kitchen. The foyer is to the east."
        ),
        "exits": {"east": "foyer", "south": "kitchen"},
        "artifact": None,
        "first_visit": True,
        "ambient": [
            "A wine glass vibrates, producing a single clear note.",
            "The candles flicker despite having no flame.",
            "A chair scrapes back from the table on its own.",
            "You hear the faint clink of silverware from the kitchen.",
        ],
    },
    "kitchen": {
        "name": "The Kitchen",
        "description": (
            "Copper pots hang from a rack over a cast-iron stove gone to rust. "
            "The smell of something — herbs? medicine? — lingers impossibly "
            "after all this time. A door to the north returns to the dining room. "
            "A narrow staircase descends into darkness to the east — the cellar."
        ),
        "exits": {"north": "dining_room", "east": "cellar"},
        "artifact": "toy_train",
        "first_visit": True,
        "ambient": [
            "A pot rocks gently on its hook.",
            "The herbal smell intensifies, then fades.",
            "Water drips from a faucet that isn't connected to pipes.",
            "Something scratches inside the walls.",
        ],
    },
    "cellar": {
        "name": "The Cellar",
        "description": (
            "Stone steps lead down into a damp, low-ceilinged space. Wine racks "
            "line the walls, most bottles shattered long ago. The air is thick "
            "and cold — colder than anywhere else in the house. There is a "
            "presence here. Something watching from the dark corners. "
            "The stairs lead west back up to the kitchen."
        ),
        "exits": {"west": "kitchen"},
        "artifact": "newspaper",
        "first_visit": True,
        "ambient": [
            "A bottle rolls off a rack and shatters. The sound echoes too long.",
            "The cold intensifies, pressing against you like a hand.",
            "You see your breath — wait. You don't breathe. Do you?",
            "A low moan rises from the stone floor, then stops.",
        ],
    },
    "upstairs_hall": {
        "name": "The Upstairs Hallway",
        "description": (
            "A long hallway stretches east and west, lined with closed doors. "
            "The carpet is worn to threads in a path between them, as though "
            "someone paced here for years. Decades. A tall mirror stands at "
            "the end of the hall, but when you look into it... you see only "
            "the empty hallway behind you. The stairs lead south back down "
            "to the foyer."
        ),
        "exits": {
            "south": "foyer",
            "east": "bedroom",
            "west": "study",
            "north": "nursery",
        },
        "artifact": None,
        "first_visit": True,
        "ambient": [
            "The mirror shows the hallway. Only the hallway. Never you.",
            "A door at the far end rattles in its frame.",
            "Footsteps echo yours, half a beat behind.",
            "The wallpaper pattern seems to shift when you're not looking directly at it.",
        ],
    },
    "bedroom": {
        "name": "The Master Bedroom",
        "description": (
            "A four-poster bed dominates the room, its canopy shredded by time "
            "or something with claws. The sheets are pulled back as though "
            "someone just rose from sleep. A vanity table holds a hairbrush "
            "with long grey hairs still tangled in its bristles. "
            "The hallway lies to the west."
        ),
        "exits": {"west": "upstairs_hall"},
        "artifact": "pocketwatch",
        "first_visit": True,
        "ambient": [
            "The bed shifts, as if something invisible just sat down.",
            "The hairbrush slides an inch across the vanity.",
            "A wardrobe door creaks open. Moth-eaten clothes hang inside.",
            "You feel a profound sadness that doesn't belong to this moment.",
        ],
    },
    "study": {
        "name": "The Study",
        "description": (
            "Walls of books and specimen jars. A heavy oak desk sits beneath "
            "a window that looks out onto... nothing. Just white. No garden, "
            "no street, no sky. Just a pale emptiness. The desk is cluttered "
            "with papers, dried flowers pressed under glass, and a magnifying "
            "lens. The hallway is to the east."
        ),
        "exits": {"east": "upstairs_hall"},
        "artifact": "journal",
        "first_visit": True,
        "ambient": [
            "The window shows nothing. Absolutely nothing. It's unsettling.",
            "A specimen jar glows faintly, then goes dark.",
            "Papers rustle on the desk though the air is still.",
            "You reach for a book and your hand passes through the shelf.",
        ],
    },
    "nursery": {
        "name": "The Nursery",
        "description": (
            "A small room painted in faded blue. A wooden crib stands against "
            "one wall, a rocking chair beside it — still rocking, slowly, as if "
            "someone just stood up. Toys are scattered on the floor: wooden "
            "blocks, a stuffed bear missing one eye, and scattered tin soldiers. "
            "The hallway lies to the south."
        ),
        "exits": {"south": "upstairs_hall"},
        "artifact": None,
        "first_visit": True,
        "ambient": [
            "The rocking chair continues its slow, measured sway.",
            "A music box somewhere plays three notes, then stops.",
            "The stuffed bear seems to track you with its remaining eye.",
            "You hear a child's giggle from far, far away.",
        ],
    },
}

# ────────────────────── GAME STATE ───────────────────────────────

class GameState:
    def __init__(self):
        self.current_room = "foyer"
        self.inventory = []         # artifact keys
        self.memories_unlocked = [] # artifact keys, in order found
        self.moves = 0
        self.has_seen_intro = False
        self.game_over = False
        self.artifacts_examined = set()

    @property
    def memory_count(self):
        return len(self.memories_unlocked)

    @property
    def total_artifacts(self):
        return len(MEMORY_FRAGMENTS)

    def has_artifact(self, key):
        return key in self.inventory

    def has_memory(self, key):
        return key in self.memories_unlocked

# ────────────────────── GAME ENGINE ──────────────────────────────

def show_title():
    clear_screen()
    title = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║            T H E   F O R G O T T E N   O N E             ║
    ║                                                          ║
    ║          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░          ║
    ║          ░  A game of memory, loss, and truth ░          ║
    ║          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░          ║
    ║                        M.B. Parks                        ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(title)
    dramatic_pause(1.5)

def show_intro():
    clear_screen()
    print_separator("═")
    print()
    slow_print("You open your eyes.", delay=0.05)
    dramatic_pause(1.0)
    slow_print("At least, you think you do. It's hard to tell.", delay=0.04)
    dramatic_pause(0.8)
    print()
    slow_print(
        "You are standing in a house. A very old house. You know this "
        "the way you know your own heartbeat — except you can't feel "
        "your heartbeat. You can't feel much of anything.",
        delay=0.025,
    )
    dramatic_pause(0.5)
    print()
    slow_print(
        "Who are you? The question echoes in the hollow place where "
        "your memories should be. You reach for your name and find "
        "only fog. You reach for your face and feel nothing.",
        delay=0.025,
    )
    dramatic_pause(0.5)
    print()
    slow_print(
        "But the house... the house feels familiar. Like a song you've "
        "forgotten the words to. Maybe if you look around, you'll find "
        "something. Some piece of the puzzle. Some fragment of whoever "
        "you used to be.",
        delay=0.025,
    )
    print()
    print_separator("═")
    print()
    print("  Type HELP for a list of commands.")
    print()

def show_help():
    print()
    print_separator()
    print("  COMMANDS:")
    print("    go <direction>   — Move (north, south, east, west)")
    print("    look             — Examine your surroundings")
    print("    take <item>      — Pick up an artifact")
    print("    examine <item>   — Study an artifact closely")
    print("    inventory / inv  — Check what you're carrying")
    print("    memories         — Review recovered memories")
    print("    quit             — End the game")
    print()
    print("  You can also just type a direction: n, s, e, w")
    print_separator()

def describe_room(state):
    room = ROOMS[state.current_room]
    print()
    print_boxed(room["name"])
    print()

    # Main description
    for line in textwrap.wrap(room["description"], width=TERM_WIDTH):
        print(f"  {line}")

    # Show artifact if present and not taken
    artifact_key = room["artifact"]
    if artifact_key and not state.has_artifact(artifact_key):
        print()
        artifact = MEMORY_FRAGMENTS[artifact_key]
        for line in textwrap.wrap(artifact["room_desc"], width=TERM_WIDTH):
            print(f"  {line}")

    # Show exits
    exits = room["exits"]
    exit_str = ", ".join(f"{d.upper()} ({ROOMS[r]['name']})" for d, r in exits.items())
    print()
    print(f"  Exits: {exit_str}")

    # Ambient flavor on revisits
    if not room["first_visit"]:
        print()
        ambient = random.choice(room["ambient"])
        print(f"  {ambient}")

    room["first_visit"] = False

def do_move(state, direction):
    direction_map = {
        "n": "north", "s": "south", "e": "east", "w": "west",
        "north": "north", "south": "south", "east": "east", "west": "west",
    }
    direction = direction_map.get(direction)
    if not direction:
        print("\n  That's not a direction you understand.")
        return

    room = ROOMS[state.current_room]
    if direction not in room["exits"]:
        print("\n  You drift in that direction but find only a wall.")
        print("  Your hand passes through the plaster. There is nothing beyond.")
        return

    state.current_room = room["exits"][direction]
    state.moves += 1

    # Ghostly travel flavor
    travel_msgs = [
        "You drift through the doorway.",
        "You float forward, barely touching the floor.",
        "The shadows part to let you pass.",
        "You move without walking. It doesn't feel strange. Should it?",
        "The air ripples around you as you glide onward.",
    ]
    print(f"\n  {random.choice(travel_msgs)}")
    describe_room(state)

def find_artifact_key(text, state):
    """Match partial artifact names from input text."""
    text = text.lower().strip()
    # Direct key match
    if text in MEMORY_FRAGMENTS:
        return text
    # Search by name fragments
    for key, art in MEMORY_FRAGMENTS.items():
        name_lower = art["name"].lower()
        if text in name_lower or text in key:
            return key
    # Try single-word matches
    for key, art in MEMORY_FRAGMENTS.items():
        for word in text.split():
            if word in art["name"].lower() or word == key:
                return key
    return None

def do_take(state, item_text):
    key = find_artifact_key(item_text, state)
    room = ROOMS[state.current_room]

    if not key:
        print("\n  You reach out, but there's nothing by that name to take.")
        return

    if room["artifact"] != key:
        print("\n  That isn't here.")
        return

    if state.has_artifact(key):
        print("\n  You already have that.")
        return

    artifact = MEMORY_FRAGMENTS[key]
    state.inventory.append(key)
    print(f"\n  You reach for the {artifact['name']}.")
    dramatic_pause(0.5)

    # Ghost struggle flavor
    struggle_msgs = [
        "Your fingers close on empty air twice before you concentrate hard enough to grasp it.",
        "It takes all your focus. The object flickers, then solidifies in your grip.",
        "The effort of touching something physical exhausts you in a way you don't understand.",
    ]
    slow_print(f"  {random.choice(struggle_msgs)}", delay=0.02)
    print(f"\n  Acquired: {artifact['name']}")

def do_examine(state, item_text):
    key = find_artifact_key(item_text, state)

    if not key:
        print("\n  Examine what? You see nothing by that description.")
        return

    if not state.has_artifact(key):
        # Check if it's in the current room but not picked up
        room = ROOMS[state.current_room]
        if room["artifact"] == key:
            print("\n  You should pick it up first. Try: take " + key)
        else:
            print("\n  You don't have anything like that.")
        return

    artifact = MEMORY_FRAGMENTS[key]
    print()
    print_separator("·")

    # Show examination text
    for line in textwrap.wrap(artifact["examine"], width=TERM_WIDTH):
        print(f"  {line}")

    dramatic_pause(1.0)

    # Unlock memory if not already seen
    if not state.has_memory(key):
        state.memories_unlocked.append(key)
        state.artifacts_examined.add(key)
        print()
        print_separator("✦")
        print()
        print("  ░░░  M E M O R Y   R E C O V E R E D  ░░░")
        print()
        slow_print(f"  {artifact['memory']}", delay=0.025)
        print()
        print(f"  ▸ {artifact['memory_tag']}")
        print(f"  ▸ Memories recovered: {state.memory_count}/{state.total_artifacts}")
        print()
        print_separator("✦")

        # Check for finale
        if state.memory_count == state.total_artifacts:
            trigger_finale(state)
    else:
        print()
        print(f"  You've already drawn what memories you can from this.")

def do_inventory(state):
    print()
    print_separator()
    if not state.inventory:
        print("  You carry nothing. You ARE almost nothing.")
        print("  Perhaps there are objects in this house that can change that.")
    else:
        print("  You are carrying:")
        for key in state.inventory:
            artifact = MEMORY_FRAGMENTS[key]
            marker = " ✦" if key in state.memories_unlocked else ""
            print(f"    • {artifact['name']}{marker}")
    print_separator()

def do_memories(state):
    print()
    print_separator("✦")
    if not state.memories_unlocked:
        print("  Your mind is a blank page. An empty room.")
        print("  Who were you? The house might hold answers.")
    else:
        print("  F R A G M E N T S   O F   Y O U:")
        print()
        for key in state.memories_unlocked:
            artifact = MEMORY_FRAGMENTS[key]
            print(f"    ✦ {artifact['memory_tag']}")
        print()
        remaining = state.total_artifacts - state.memory_count
        if remaining > 0:
            print(f"  {remaining} memory fragment{'s' if remaining != 1 else ''} remain hidden...")
    print_separator("✦")

# ───────────────────────── FINALE ────────────────────────────────

def trigger_finale(state):
    dramatic_pause(2.0)
    clear_screen()
    print()
    print_separator("═")
    print()
    slow_print(
        "The house shudders. Every door slams shut at once. The walls "
        "groan as if the building itself is in pain — or relief.",
        delay=0.03,
    )
    dramatic_pause(1.5)
    print()
    slow_print(
        "The artifacts in your hands begin to glow. The locket. The journal. "
        "The watch. The train. The newspaper. They orbit around you like "
        "satellites, casting long shadows that aren't shaped like objects "
        "at all — they're shaped like moments. Like a LIFE.",
        delay=0.03,
    )
    dramatic_pause(2.0)
    print()
    slow_print(
        "And then you see it. All of it. Not in fragments — in full.",
        delay=0.04,
    )
    dramatic_pause(1.5)

    print()
    print_separator("✦")
    print()
    slow_print("  Your name was Elias Wren.", delay=0.05)
    dramatic_pause(0.8)
    slow_print("  You were a professor of botany at Ashworth University.", delay=0.04)
    dramatic_pause(0.8)
    slow_print("  You married Margaret on an October evening in 1911.", delay=0.04)
    dramatic_pause(0.8)
    slow_print("  Your son Thomas had your eyes and her laugh.", delay=0.04)
    dramatic_pause(0.8)
    slow_print("  On November 2nd, 1923, you sat at your desk in the study.", delay=0.04)
    dramatic_pause(0.8)
    slow_print("  You felt a tightness in your chest.", delay=0.05)
    dramatic_pause(0.8)
    slow_print("  Your pocket watch read 11:47.", delay=0.05)
    dramatic_pause(1.5)
    slow_print("  And then...", delay=0.1)
    dramatic_pause(2.0)
    print()

    slow_print(
        "You look down at your hands. You can see the floorboards "
        "through them. You have ALWAYS been able to see through them. "
        "You simply chose not to notice.",
        delay=0.03,
    )
    dramatic_pause(1.5)
    print()
    slow_print(
        "You are not exploring a haunted house.",
        delay=0.05,
    )
    dramatic_pause(1.0)
    slow_print(
        "You ARE the haunting.",
        delay=0.06,
    )
    dramatic_pause(2.0)
    print()
    slow_print(
        "The mirror at the end of the upstairs hall — the one that never "
        "showed your reflection — it wasn't broken. It was honest. There "
        "is nothing to reflect. You are the cold spot in the cellar. The "
        "creaking floorboard with no one on it. The rocking chair that "
        "won't stop moving. All this time, you were looking for a ghost "
        "in this house.",
        delay=0.025,
    )
    dramatic_pause(1.0)
    print()
    slow_print(
        "You found one.",
        delay=0.08,
    )
    dramatic_pause(2.5)

    print()
    print_separator("═")
    print()
    slow_print(
        "The light changes. The pale emptiness outside the study window "
        "is no longer empty. It's warm. Golden. You hear Margaret's voice, "
        "very far away and very close, all at once:",
        delay=0.03,
    )
    dramatic_pause(1.0)
    print()
    slow_print('  "Elias? It\'s time to come home."', delay=0.05)
    dramatic_pause(2.0)
    print()

    slow_print(
        "For the first time in a hundred years, you smile.",
        delay=0.04,
    )
    dramatic_pause(1.0)
    slow_print(
        "You step toward the light.",
        delay=0.05,
    )
    dramatic_pause(1.0)
    slow_print(
        "The house is empty now. Truly empty. The rocking chair is still. "
        "The chandelier hangs motionless. The watch on the nightstand reads "
        "11:47, and always will.",
        delay=0.025,
    )
    print()
    dramatic_pause(1.0)
    slow_print(
        "But if you press your ear to the wall of the nursery, just so, "
        "you can almost hear a music box playing.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    slow_print(
        "Almost.",
        delay=0.12,
    )

    print()
    print()
    print_separator("═")
    print()
    print("              T H E   F O R G O T T E N   O N E")
    print()
    print(f"                 Memories recovered: {state.memory_count}/{state.total_artifacts}")
    print(f"                 Rooms explored: {len([r for r in ROOMS.values() if not r['first_visit']])}/{len(ROOMS)}")
    print(f"                 Moves taken: {state.moves}")
    print()
    print("          Thank you for helping Elias remember.")
    print("          Thank you for helping him go home.")
    print()
    print_separator("═")
    print()

    state.game_over = True

# ─────────────────────── MAIN LOOP ───────────────────────────────

def parse_command(raw):
    """Parse player input into (command, argument)."""
    parts = raw.split(None, 1)
    if not parts:
        return None, None
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    # Shorthand directions
    if cmd in ("n", "s", "e", "w", "north", "south", "east", "west"):
        return "go", cmd

    # Aliases
    aliases = {
        "go": "go", "move": "go", "walk": "go", "head": "go",
        "look": "look", "l": "look", "examine": "examine", "x": "examine",
        "inspect": "examine", "study": "examine", "read": "examine",
        "take": "take", "get": "take", "grab": "take", "pick": "take",
        "inventory": "inventory", "inv": "inventory", "i": "inventory",
        "memories": "memories", "memory": "memories", "remember": "memories",
        "help": "help", "?": "help", "commands": "help",
        "quit": "quit", "exit": "quit", "q": "quit",
    }
    return aliases.get(cmd, cmd), arg

def main():
    show_title()
    input("  Press ENTER to begin...\n")

    state = GameState()
    show_intro()
    describe_room(state)

    while not state.game_over:
        raw = prompt()
        if not raw:
            continue

        cmd, arg = parse_command(raw)

        if cmd == "go":
            do_move(state, arg)
        elif cmd == "look":
            describe_room(state)
        elif cmd == "examine":
            if arg:
                do_examine(state, arg)
            else:
                print("\n  Examine what? Try: examine <item name>")
        elif cmd == "take":
            if arg:
                do_take(state, arg)
            else:
                print("\n  Take what? Try: take <item name>")
        elif cmd == "inventory":
            do_inventory(state)
        elif cmd == "memories":
            do_memories(state)
        elif cmd == "help":
            show_help()
        elif cmd == "quit":
            print()
            slow_print(
                "You try to leave, but the doors won't open from the inside. "
                "They never have. Perhaps you should keep looking.",
                delay=0.03,
            )
            print()
            confirm = input("  Really quit? (yes/no) > ").strip().lower()
            if confirm in ("yes", "y"):
                print()
                slow_print("The house waits. It has always been waiting.", delay=0.04)
                print()
                state.game_over = True
        else:
            unknown_responses = [
                "You try, but the concept dissolves like mist in your mind.",
                "That word means nothing to you anymore. Try HELP.",
                "The house doesn't understand. Neither do you.",
                "You reach for that thought and find only emptiness. Try HELP.",
            ]
            print(f"\n  {random.choice(unknown_responses)}")

    print("  Goodbye.\n")

if __name__ == "__main__":
    main()

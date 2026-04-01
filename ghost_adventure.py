#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              T H E   F O R G O T T E N   O N E               ║
║         A Text Adventure of Memory and Discovery             ║
║                          M.B. Parks                          ║
╚══════════════════════════════════════════════════════════════╝
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
# The artifacts tell a warm, human story. No death clues.
# The 5th artifact is a letter that reads as ambiguous until the finale.

MEMORY_FRAGMENTS = {
    "locket": {
        "name": "Tarnished Silver Locket",
        "room_desc": (
            "A tarnished silver locket lies on the mantelpiece, its chain "
            "coiled in a neat circle."
        ),
        "examine": (
            "You open the locket. Inside is a faded photograph: a woman "
            "with kind eyes and a child on her lap. The photo is so old "
            "the edges have turned to velvet. But the woman's face — "
            "you know that face. A certainty rises in you like a tide."
        ),
        "memory": (
            "The scent of lavender. A kitchen with copper pots and flour "
            "dusting every surface. A voice singing — not well, but with "
            "such tenderness it didn't matter. \"My little sparrow,\" she "
            "called you. Mother. She was your MOTHER. The memory is warm "
            "and complete, like stepping into sunlight. But her name — "
            "her name stays just out of reach."
        ),
        "memory_tag": "A mother's love — she called you her little sparrow.",
    },
    "journal": {
        "name": "Water-Damaged Journal",
        "room_desc": (
            "A journal lies open on the desk, its pages bloated and wavy "
            "from old water damage."
        ),
        "examine": (
            "Most of the ink has bled beyond reading, but you find a few "
            "surviving entries. The handwriting is meticulous, scientific. "
            "Dates from 1923. Detailed sketches of ferns and wildflowers "
            "with Latin names in careful script. You know this handwriting. "
            "It's yours."
        ),
        "memory": (
            "A greenhouse. Rows of specimen trays. The earthy smell of "
            "peat moss and the scratch of a pen on paper. You were a "
            "botanist — a professor at a university. Students filed into "
            "your lecture hall every Tuesday and Thursday. You loved it. "
            "The thrill of classification, of pinning a name to something "
            "wild. Ashworth University. That was the place."
        ),
        "memory_tag": "A vocation — you were a professor of botany at Ashworth.",
    },
    "pocketwatch": {
        "name": "Stopped Pocket Watch",
        "room_desc": (
            "A pocket watch sits on the nightstand, its crystal cracked "
            "in a starburst pattern. The hands have stopped."
        ),
        "examine": (
            "It's a beautiful piece — silver case, Roman numerals, a "
            "delicate chain. The crystal is cracked but the face is "
            "legible. Stopped at 11:47. On the back, an engraving: "
            "\"To E.W. — Until the end of time. — M.\""
        ),
        "memory": (
            "An October evening. Lanterns hung in the garden, and the "
            "maples were the color of fire. She stood across from you "
            "in white, and you couldn't breathe for how beautiful she was. "
            "Margaret. Her name was MARGARET. After the ceremony, she pressed "
            "this watch into your hand. \"So you'll always come home on "
            "time,\" she said, and everyone laughed. E.W. — Elias Wren. "
            "That was your name. YOUR name. Elias Wren."
        ),
        "memory_tag": "A wedding — you married Margaret. Your name is Elias Wren.",
    },
    "toy_train": {
        "name": "Painted Wooden Train",
        "room_desc": (
            "A small hand-painted wooden train sits on a shelf, its red "
            "paint chipped to reveal bare wood beneath."
        ),
        "examine": (
            "The train is light in your hand. The paint was applied by "
            "someone who cared more about the giving than the craft — "
            "the brushstrokes are uneven, a little clumsy. An adult "
            "made this for a child."
        ),
        "memory": (
            "A boy. Brown curls, gap-toothed grin, your eyes in a smaller "
            "face. He sits on the rug pushing this very train in circles, "
            "making engine sounds with his lips. \"Again, Papa! Make the "
            "whistle!\" You whistle — two short, one long — and he falls "
            "over laughing. Thomas. Your son's name was Thomas. You carved "
            "this train for his third birthday from a piece of cherry wood."
        ),
        "memory_tag": "A son — you had a boy named Thomas.",
    },
    "letter": {
        "name": "Sealed Envelope",
        "room_desc": (
            "A cream-colored envelope lies on the side table, sealed "
            "but never posted. The name on the front has faded to "
            "nothing."
        ),
        "examine": (
            "The envelope is unsealed — the glue gave up long ago. Inside "
            "is a single page in a woman's handwriting, the ink a deep "
            "blue. It begins: \"My dearest Elias.\""
        ),
        "memory": (
            "Margaret's handwriting. You'd know it anywhere now. "
            "\"My dearest Elias — It has been a year and I still set your "
            "place at dinner. Thomas drew you a picture of a train. I put "
            "it on your desk. I've kept the study exactly as you left it. "
            "I know you'd scold me for the mess, but I can't bring myself "
            "to move a single paper. The house is so quiet without you. "
            "I hope wherever you are, you can hear me. I hope you know "
            "we're all right. — Your Margaret.\""
            "\n\n  You read it twice. A year since what? Where did you go?"
        ),
        "memory_tag": "Margaret's letter — she missed you terribly.",
    },
}

# ──────────────────────────── ROOMS ──────────────────────────────
# Ambient messages focus on FAMILIARITY and the strangeness of
# knowing this house too well. No ghost tropes. The house is just
# old and abandoned — in a normal, mundane way.

ROOMS = {
    "foyer": {
        "name": "The Foyer",
        "description": (
            "A once-handsome entrance hall. Wallpaper peels in long strips "
            "and the tile floor is gritty underfoot. A chandelier hangs "
            "overhead, its crystals clouded. The front door is behind you. "
            "A staircase leads north to the upper floor. Doorways open "
            "east and west."
        ),
        "exits": {"north": "upstairs_hall", "east": "parlor", "west": "dining_room"},
        "artifact": None,
        "first_visit": True,
        "ambient": [
            "You try the front door. It's swollen shut — the wood has warped "
            "in its frame. You could force it, maybe, but something keeps you here.",
            "A coat rack stands by the door. One hook holds a wool overcoat, "
            "grey with dust. It looks like it would fit you perfectly.",
            "You know this house. You knew where the staircase was before you "
            "saw it. How?",
            "Light comes in from a high window. It's the same pale, overcast "
            "light as when you arrived. What time is it?",
            "There are no sounds from outside. No birds, no wind, no traffic. "
            "Just the house and its silences.",
        ],
    },
    "parlor": {
        "name": "The Parlor",
        "description": (
            "A sitting room with two armchairs facing a fireplace. A chess "
            "game sits mid-play on a small table between them — white was "
            "winning. Bookshelves line two walls. Above the mantelpiece "
            "hangs a portrait of a family: a man, a woman, and a small boy. "
            "The foyer lies to the west."
        ),
        "exits": {"west": "foyer"},
        "artifact": "locket",
        "first_visit": True,
        "ambient": [
            "The portrait. You keep looking at the man's face. Something about "
            "the shape of his jaw, the way he stands. He looks like someone "
            "you used to know.",
            "You sit in the left armchair without thinking. It feels natural. "
            "Like the chair was shaped by years of exactly your posture.",
            "The books are mostly botany — Latin nomenclature, pressed flower "
            "guides, university texts. Someone had a very specific passion.",
            "The chess game. White was three moves from checkmate. The players "
            "left mid-game. Why would someone walk away from a winning position?",
            "You pull a book from the shelf. 'Flora of the British Isles.' "
            "Your hand went right to it, like muscle memory.",
        ],
    },
    "dining_room": {
        "name": "The Dining Room",
        "description": (
            "A long oak table set for four. Plates, glasses, tarnished "
            "silverware — everything laid out for a dinner that was never "
            "cleared. A candelabra at the center has melted down to stubs. "
            "The kitchen is to the south. The foyer is east."
        ),
        "exits": {"east": "foyer", "south": "kitchen"},
        "artifact": None,
        "first_visit": True,
        "ambient": [
            "Four place settings. A family of four sat here. Or was about to.",
            "A napkin has been folded into a swan at the smallest place setting. "
            "Someone wanted to make a child smile.",
            "The silverware is real silver — tarnished black. This was a household "
            "that cared about appearances.",
            "You notice a crack in one of the plates. You already knew it was there. "
            "You knew before you looked.",
            "Dust lies thick and undisturbed. Nobody has eaten here in a very long time.",
        ],
    },
    "kitchen": {
        "name": "The Kitchen",
        "description": (
            "Copper pots on hooks, a cast-iron stove gone to rust, a stone "
            "sink with a hand pump. There's a faint smell — rosemary, maybe "
            "thyme. Impossible that it would last, but old houses hold onto "
            "things. The dining room is north. A narrow staircase descends "
            "east into a cellar."
        ),
        "exits": {"north": "dining_room", "east": "cellar"},
        "artifact": "toy_train",
        "first_visit": True,
        "ambient": [
            "There's a calendar on the wall. October 1923. Someone drew a small "
            "heart around the 14th.",
            "The herb smell comes and goes. It's strongest near the stove.",
            "A teacup sits on the counter, a ring of dried tea at the bottom. "
            "Someone's last cup, never washed.",
            "You open a cupboard without looking — your hand finds the handle "
            "by instinct. Inside: jars of preserves, labels in a neat hand.",
            "The window over the sink shows the same flat, overcast sky. "
            "It hasn't changed since you've been here.",
        ],
    },
    "cellar": {
        "name": "The Cellar",
        "description": (
            "Stone steps lead into a cool, low-ceilinged space. Wine racks "
            "line the walls — a few bottles survive, most are broken. "
            "It smells of damp earth and old wood. The stairs lead west "
            "back to the kitchen."
        ),
        "exits": {"west": "kitchen"},
        "artifact": None,
        "first_visit": True,
        "ambient": [
            "A good cellar. Someone took wine seriously. The surviving bottles "
            "have handwritten labels — 'Bordeaux 1908,' 'Port 1912.'",
            "The cold down here is the honest, mineral cold of stone. "
            "It's almost refreshing after the stuffy rooms above.",
            "You notice scratches on the wall near the bottom of the stairs. "
            "Height marks. 'T.W. — age 3.' 'T.W. — age 4.' They stop at age 5.",
            "The height marks. T.W. Thomas Wren? If you've found the watch, "
            "W could be Wren. But who stopped measuring?",
            "It's quiet down here. The house above feels far away.",
        ],
    },
    "upstairs_hall": {
        "name": "The Upstairs Hallway",
        "description": (
            "A long hallway with doors east, west, and north. A carpet runner "
            "is worn thin in a path between the rooms — decades of footsteps "
            "ground into the weave. Framed photographs line the walls, "
            "too faded to make out clearly. The stairs lead south to the foyer."
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
            "The photographs. Formal poses, stiff collars. You lean close but "
            "the images are ghosted — overexposed by decades of hallway light.",
            "The carpet is worn in a very particular path — study to nursery "
            "and back. Someone paced this route thousands of times.",
            "A mirror stands at the end of the hall. It's so clouded with age "
            "you can barely see the hallway reflected in it, let alone yourself.",
            "You walk the worn path in the carpet. Your feet fit the pattern "
            "exactly. Step for step.",
            "How long have you been exploring? It feels like hours, but the "
            "light from the windows hasn't changed at all.",
        ],
    },
    "bedroom": {
        "name": "The Master Bedroom",
        "description": (
            "A four-poster bed with a canopy gone threadbare. The covers "
            "are pulled back on the left side, the right side still neatly "
            "made — as if only one person slept here. A vanity table holds "
            "a hairbrush and a dried flower in a small vase. "
            "The hallway is west."
        ),
        "exits": {"west": "upstairs_hall"},
        "artifact": "pocketwatch",
        "first_visit": True,
        "ambient": [
            "Only the left side of the bed was slept in. For a long time, "
            "from the look of the impression in the mattress.",
            "A woman's shawl hangs on the bedpost. Lavender and wool. "
            "You almost recognize the scent.",
            "A framed photograph on the nightstand. A wedding portrait — "
            "a young couple in an autumn garden. The groom's face is yours. "
            "You're almost certain.",
            "You know which drawer of the nightstand holds the watch before "
            "you open it. Left drawer. How do you know that?",
            "The pressed flower on the vanity is a primrose. You know the "
            "Latin name without trying: Primula vulgaris. Odd thing to know.",
        ],
    },
    "study": {
        "name": "The Study",
        "description": (
            "A room that feels more lived-in than any other in the house. "
            "Books and specimen jars crowd every surface. A heavy oak desk "
            "sits under a window with drawn curtains. The desk is covered "
            "in papers, pressed flowers under glass, and a magnifying lens. "
            "A leather chair is pushed back from the desk at an angle. "
            "The hallway is east."
        ),
        "exits": {"east": "upstairs_hall"},
        "artifact": "journal",
        "first_visit": True,
        "ambient": [
            "This room smells of old paper and dried flowers. A warm, "
            "scholarly smell. You feel at ease here in a way you haven't "
            "felt anywhere else in the house.",
            "The desk chair is pushed back at an odd angle. As if someone "
            "stood up in a hurry. Or was pulled away from their work.",
            "You recognize every jar on the shelf. Pressed ferns, orchid "
            "specimens, seed pods in labeled vials. You know what's in "
            "each one before you read the label.",
            "You sit in the desk chair. It fits you perfectly — the height, "
            "the angle, the worn spots on the armrests where hands rested "
            "for years.",
            "A drawing by a child is pinned above the desk. A train, "
            "crayoned in red. 'For Papa' is written in a wobbly hand.",
        ],
    },
    "nursery": {
        "name": "The Nursery",
        "description": (
            "A small room painted faded blue. A wooden crib stands against "
            "one wall, a rocking chair beside it. Toys dot the floor: "
            "wooden blocks, a one-eyed stuffed bear, tin soldiers on the "
            "windowsill. A side table holds a lamp and a sealed envelope. "
            "The hallway is south."
        ),
        "exits": {"south": "upstairs_hall"},
        "artifact": "letter",
        "first_visit": True,
        "ambient": [
            "The rocking chair is still. This was a loved room — you can "
            "feel it. Someone spent hours here, rocking, waiting, watching "
            "a child sleep.",
            "The tin soldiers are arranged in a careful battle formation. "
            "A child's serious work.",
            "You pick up the stuffed bear. One button eye is missing. The "
            "other stares at the ceiling. Something about holding it makes "
            "your chest tight.",
            "A music box sits on the shelf. You wind it — three notes of a "
            "lullaby play, then the mechanism sticks. You know the rest of "
            "the melody anyway.",
            "Thomas's room. You know that now. Your boy slept here.",
        ],
    },
}

# ────────────────────── GAME STATE ───────────────────────────────

class GameState:
    def __init__(self):
        self.current_room = "foyer"
        self.inventory = []
        self.memories_unlocked = []
        self.moves = 0
        self.game_over = False

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
    ║           T H E   F O R G O T T E N   O N E              ║
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
    slow_print(
        "You're standing in the entrance hall of a house. An old one — "
        "peeling wallpaper, dust on every surface, the particular silence "
        "of a place where no one has spoken in a long time.",
        delay=0.025,
    )
    dramatic_pause(0.5)
    print()
    slow_print(
        "You can't remember how you got here. You must have come in "
        "through the front door, but you don't remember opening it. "
        "You don't remember walking up to the house. You don't remember "
        "what you were doing before this moment.",
        delay=0.025,
    )
    dramatic_pause(0.5)
    print()
    slow_print(
        "Come to think of it, you can't remember much of anything. "
        "Your name, your face, where you live — it's all fog. But "
        "this house feels familiar. Not the way a stranger's house "
        "feels, but the way your own does after a long trip away.",
        delay=0.025,
    )
    dramatic_pause(0.5)
    print()
    slow_print(
        "Maybe there's something here that will help you remember.",
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

    for line in textwrap.wrap(room["description"], width=TERM_WIDTH):
        print(f"  {line}")

    artifact_key = room["artifact"]
    if artifact_key and not state.has_artifact(artifact_key):
        print()
        artifact = MEMORY_FRAGMENTS[artifact_key]
        for line in textwrap.wrap(artifact["room_desc"], width=TERM_WIDTH):
            print(f"  {line}")

    exits = room["exits"]
    exit_str = ", ".join(
        f"{d.upper()} ({ROOMS[r]['name']})" for d, r in exits.items()
    )
    print()
    print(f"  Exits: {exit_str}")

    if not room["first_visit"]:
        ambient = random.choice(room["ambient"])
        print()
        for line in textwrap.wrap(ambient, width=TERM_WIDTH):
            print(f"  {line}")

    room["first_visit"] = False

def do_move(state, direction):
    direction_map = {
        "n": "north", "s": "south", "e": "east", "w": "west",
        "north": "north", "south": "south", "east": "east", "west": "west",
    }
    direction = direction_map.get(direction)
    if not direction:
        print("\n  That's not a direction you recognize.")
        return

    room = ROOMS[state.current_room]
    if direction not in room["exits"]:
        print("\n  There's nothing that way — just a wall.")
        return

    state.current_room = room["exits"][direction]
    state.moves += 1

    msgs = [
        "You walk through the doorway.",
        "You step into the next room.",
        "You head onward.",
        "Your footsteps are quiet on the old floor.",
        "You make your way forward.",
    ]
    print(f"\n  {random.choice(msgs)}")
    describe_room(state)

def find_artifact_key(text, state):
    text = text.lower().strip()
    if text in MEMORY_FRAGMENTS:
        return text
    for key, art in MEMORY_FRAGMENTS.items():
        name_lower = art["name"].lower()
        if text in name_lower or text in key:
            return key
    for key, art in MEMORY_FRAGMENTS.items():
        for word in text.split():
            if len(word) > 2 and (word in art["name"].lower() or word == key):
                return key
    return None

def do_take(state, item_text):
    key = find_artifact_key(item_text, state)
    room = ROOMS[state.current_room]

    if not key:
        print("\n  You don't see anything by that name.")
        return
    if room["artifact"] != key:
        print("\n  That isn't here.")
        return
    if state.has_artifact(key):
        print("\n  You already have that.")
        return

    artifact = MEMORY_FRAGMENTS[key]
    state.inventory.append(key)
    print(f"\n  You pick up the {artifact['name']}.")
    print(f"  Acquired: {artifact['name']}")

def do_examine(state, item_text):
    key = find_artifact_key(item_text, state)

    if not key:
        print("\n  Examine what? You don't see anything by that name.")
        return
    if not state.has_artifact(key):
        room = ROOMS[state.current_room]
        if room["artifact"] == key:
            print(f"\n  You should pick it up first. Try: take {key}")
        else:
            print("\n  You don't have anything like that.")
        return

    artifact = MEMORY_FRAGMENTS[key]
    print()
    print_separator("·")
    for line in textwrap.wrap(artifact["examine"], width=TERM_WIDTH):
        print(f"  {line}")

    dramatic_pause(1.0)

    if not state.has_memory(key):
        state.memories_unlocked.append(key)
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

        # Emotional beats at milestones — focused on identity, not death
        if state.memory_count == 3:
            dramatic_pause(0.8)
            print()
            slow_print(
                "  Elias Wren. Professor. Husband. You have a name now. You have "
                "a life. The house makes sense — it's YOURS. This is where you "
                "lived. So why can't you remember leaving?",
                delay=0.025,
            )
        elif state.memory_count == 4:
            dramatic_pause(0.8)
            print()
            slow_print(
                "  A mother, a career, a wife, a son. The pieces are assembling "
                "into someone real. Someone who loved and was loved. But there's "
                "a gap at the center — a question you keep circling without "
                "asking: what happened to Elias Wren?",
                delay=0.025,
            )

        if state.memory_count == state.total_artifacts:
            trigger_finale(state)
    else:
        print()
        print("  You've already studied this. The memory is vivid.")

def do_inventory(state):
    print()
    print_separator()
    if not state.inventory:
        print("  You're not carrying anything.")
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
        print("  Nothing. You must have been someone, but who?")
    else:
        print("  W H A T   Y O U   R E M E M B E R:")
        print()
        for key in state.memories_unlocked:
            artifact = MEMORY_FRAGMENTS[key]
            print(f"    ✦ {artifact['memory_tag']}")
        print()
        remaining = state.total_artifacts - state.memory_count
        if remaining > 0:
            print(f"  {remaining} fragment{'s' if remaining != 1 else ''} still missing...")
    print_separator("✦")

# ───────────────────────── FINALE ────────────────────────────────

def trigger_finale(state):
    dramatic_pause(2.0)
    clear_screen()
    print()
    print_separator("═")
    print()

    slow_print(
        "Margaret's letter. You read it a third time, slower.",
        delay=0.035,
    )
    dramatic_pause(1.0)
    print()

    slow_print(
        "\"It has been a year.\"",
        delay=0.04,
    )
    dramatic_pause(0.8)
    slow_print(
        "\"I've kept the study exactly as you left it.\"",
        delay=0.04,
    )
    dramatic_pause(0.8)
    slow_print(
        "\"I hope wherever you are, you can hear me.\"",
        delay=0.04,
    )
    dramatic_pause(2.0)
    print()

    slow_print(
        "You told yourself she was writing to someone away on a trip. "
        "A long journey. An absence that could be explained.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    slow_print(
        "But people on trips come home. Margaret didn't say \"when you "
        "come home.\" She said \"wherever you are.\" She said \"I hope "
        "you can hear me.\"",
        delay=0.03,
    )
    dramatic_pause(1.5)
    slow_print(
        "Those aren't words you write to someone who's coming back.",
        delay=0.04,
    )
    dramatic_pause(2.5)

    print()
    print_separator()
    print()

    slow_print(
        "The pocket watch. Stopped at 11:47. You said the crystal was "
        "cracked — but you never asked what cracked it. A watch doesn't "
        "crack on a nightstand.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    slow_print(
        "It cracks when it hits a desk. When someone falls forward onto it.",
        delay=0.035,
    )
    dramatic_pause(1.5)
    print()
    slow_print(
        "The study. The desk chair pushed back at that angle. The papers "
        "scattered. You thought someone stood up in a hurry.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    slow_print(
        "Nobody stood up.",
        delay=0.05,
    )
    dramatic_pause(2.5)

    print()
    print_separator()
    print()

    slow_print(
        "You walk to the hallway. You stand in front of the old mirror. "
        "You told yourself it was clouded with age. You couldn't see "
        "yourself because the glass was fogged.",
        delay=0.03,
    )
    dramatic_pause(1.5)
    slow_print(
        "You wipe it with your sleeve.",
        delay=0.04,
    )
    dramatic_pause(1.0)
    slow_print(
        "The glass is clean.",
        delay=0.05,
    )
    dramatic_pause(1.5)
    slow_print(
        "The hallway behind you is reflected perfectly — the photographs, "
        "the worn carpet, the light from the window.",
        delay=0.03,
    )
    dramatic_pause(1.5)
    slow_print(
        "Where you are standing, there is nothing.",
        delay=0.05,
    )
    dramatic_pause(3.0)

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
    print()
    slow_print(
        "  On November 2nd, 1923, you were working late in your study. "
        "You felt a tightness in your chest. You reached for the desk "
        "to steady yourself. Your watch struck the wood and cracked.",
        delay=0.035,
    )
    dramatic_pause(1.0)
    slow_print("  The time was 11:47 PM.", delay=0.05)
    dramatic_pause(1.5)
    slow_print(
        "  Margaret found you the next morning, slumped across your "
        "papers. She kept your study exactly as you left it.",
        delay=0.035,
    )
    dramatic_pause(1.0)
    slow_print("  She never moved a single paper.", delay=0.04)
    dramatic_pause(2.5)

    print()
    print_separator("✦")
    print()

    slow_print(
        "The front door that wouldn't open. The light that never "
        "changed. The silence outside — no birds, no wind, no world "
        "beyond the walls. You thought the house was abandoned.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    print()
    slow_print(
        "The house isn't abandoned. The house is all that's left.",
        delay=0.04,
    )
    dramatic_pause(1.5)
    slow_print(
        "You didn't find this place. You never left it.",
        delay=0.04,
    )
    dramatic_pause(1.5)
    slow_print(
        "You have been here since 11:47 PM on November 2nd, 1923, "
        "walking the same hallway, sitting in the same chair, "
        "reaching for the same doorknobs — for a hundred years.",
        delay=0.03,
    )
    dramatic_pause(2.0)
    print()
    slow_print(
        "And the only reason you couldn't see yourself in the mirror "
        "is that there is nothing left to see.",
        delay=0.035,
    )
    dramatic_pause(3.0)

    print()
    print_separator("═")
    print()

    slow_print(
        "But something is different now. The window in the study — the "
        "one with the drawn curtains that you never opened — light is "
        "pouring through the edges. Not the flat, grey light of the "
        "house. Something warmer. Something golden.",
        delay=0.03,
    )
    dramatic_pause(1.5)
    print()
    slow_print(
        "You pull the curtains open.",
        delay=0.04,
    )
    dramatic_pause(1.0)
    slow_print(
        "Beyond the glass, an October garden. Maples the color of fire. "
        "Lanterns strung between the trees. And standing in the middle "
        "of it all, a woman in a white dress, holding the hand of a "
        "small boy with brown curls.",
        delay=0.03,
    )
    dramatic_pause(2.0)
    print()
    slow_print(
        "Margaret looks up at the window. She smiles.",
        delay=0.04,
    )
    dramatic_pause(1.0)
    print()
    slow_print('  "There you are," she says. "We\'ve been waiting."', delay=0.05)
    dramatic_pause(1.5)
    slow_print(
        '  Thomas waves. "Come ON, Papa!"',
        delay=0.05,
    )
    dramatic_pause(2.0)

    print()
    slow_print(
        "The window opens easily. The October air smells like wood smoke "
        "and apples. For the first time in a hundred years, you can "
        "feel the breeze on your skin.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    print()
    slow_print("You step through.", delay=0.06)
    dramatic_pause(2.0)

    print()
    print_separator()
    print()

    slow_print(
        "The house stands quiet. The rocking chair in the nursery is "
        "still. The chandelier hangs motionless. The pocket watch on "
        "the nightstand reads 11:47.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    print()
    slow_print(
        "On the desk in the study, Margaret's letter rests open "
        "beside the journal and the magnifying lens. The chair is "
        "pushed neatly into the desk now — tucked in, as though "
        "someone has finally finished their work.",
        delay=0.03,
    )
    dramatic_pause(1.5)
    print()
    slow_print(
        "The front door swings open on its own. Autumn light floods "
        "the foyer.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    slow_print(
        "The house breathes out, long and slow, and is still.",
        delay=0.04,
    )

    print()
    print()
    print_separator("═")
    print()
    visited = len([r for r in ROOMS.values() if not r["first_visit"]])
    print("              T H E   F O R G O T T E N   O N E")
    print()
    print(f"                 Memories recovered: {state.memory_count}/{state.total_artifacts}")
    print(f"                 Rooms explored: {visited}/{len(ROOMS)}")
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
    parts = raw.split(None, 1)
    if not parts:
        return None, None
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    if cmd in ("n", "s", "e", "w", "north", "south", "east", "west"):
        return "go", cmd

    aliases = {
        "go": "go", "move": "go", "walk": "go", "head": "go",
        "look": "look", "l": "look",
        "examine": "examine", "x": "examine", "inspect": "examine",
        "study": "examine", "read": "examine",
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
            confirm = input("  Are you sure? (yes/no) > ").strip().lower()
            if confirm in ("yes", "y"):
                print()
                slow_print(
                    "You head for the front door. It won't budge. "
                    "The wood has swollen in the frame. Or maybe it was "
                    "never meant to open from the inside.",
                    delay=0.03,
                )
                dramatic_pause(0.5)
                print()
                confirm2 = input(
                    "  Force the door and leave? (yes/no) > "
                ).strip().lower()
                if confirm2 in ("yes", "y"):
                    print()
                    slow_print(
                        "You pull as hard as you can. The door doesn't move. "
                        "Not even a little. After a while, you stop trying.",
                        delay=0.03,
                    )
                    print()
                    slow_print(
                        "Maybe there's more to find here first.",
                        delay=0.03,
                    )
                else:
                    print("\n  You step back from the door. Not yet.")
        else:
            unknowns = [
                "You're not sure what you mean by that. Try HELP.",
                "That doesn't make sense. Try HELP.",
                "You pause, confused. Try HELP for a list of commands.",
            ]
            print(f"\n  {random.choice(unknowns)}")

    print("  Goodbye.\n")

if __name__ == "__main__":
    main()

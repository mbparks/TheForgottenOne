#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              T H E   F O R G O T T E N   O N E               ║
║         A Text Adventure of Memory and Discovery             ║
║                        M.B. Parks                            ║
╚══════════════════════════════════════════════════════════════╝

Dynamically generated layouts — no two games are the same.
Beware The Darkness.
"""

import sys
import textwrap
import time
import os
import random
from collections import deque

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

OPPOSITES = {"north": "south", "south": "north", "east": "west", "west": "east"}
DIR_SHORT = {"n": "north", "s": "south", "e": "east", "w": "west"}

# ────────────────────── MEMORY FRAGMENTS ─────────────────────────

MEMORY_FRAGMENTS = {
    "locket": {
        "name": "Tarnished Silver Locket",
        "room_desc": (
            "A tarnished silver locket lies here, its chain coiled in "
            "a neat circle."
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
            "\n\n  And the song. You can almost hum it. A lullaby — three "
            "notes rising, three notes falling. It sits at the edge of "
            "your mind like a candle in a window."
        ),
        "memory_tag": "A mother's love — she called you her little sparrow.",
        "is_memory": True,
    },
    "journal": {
        "name": "Water-Damaged Journal",
        "room_desc": (
            "A journal lies here, its pages bloated and wavy from old "
            "water damage."
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
        "is_memory": True,
    },
    "pocketwatch": {
        "name": "Stopped Pocket Watch",
        "room_desc": (
            "A pocket watch sits here, its crystal cracked in a starburst "
            "pattern. The hands have stopped."
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
        "is_memory": True,
    },
    "toy_train": {
        "name": "Painted Wooden Train",
        "room_desc": (
            "A small hand-painted wooden train sits here, its red paint "
            "chipped to reveal bare wood beneath."
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
        "is_memory": True,
    },
    "letter": {
        "name": "Sealed Envelope",
        "room_desc": (
            "A cream-colored envelope lies here, sealed but never posted. "
            "The name on the front has faded to nothing."
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
        "is_memory": True,
    },
}

# ──────────────────── FLAVOR OBJECTS ─────────────────────────────

FLAVOR_OBJECTS = {
    "pipe": {
        "name": "Briar Pipe",
        "room_desc": "A briar pipe rests in a ceramic dish, its bowl blackened from use.",
        "examine": (
            "The pipe is well-worn — the stem has tooth marks, the bowl is "
            "caked with old tobacco. It smells faintly of cherry and oak. "
            "You hold it to your lips without thinking. It feels natural, "
            "comfortable, but no memory comes. Just the ghost of a habit."
        ),
    },
    "spectacles": {
        "name": "Wire-Rimmed Spectacles",
        "room_desc": "A pair of wire-rimmed spectacles sits folded on a surface.",
        "examine": (
            "Round lenses, thin gold wire frame, one temple slightly bent. "
            "You unfold them and put them on. The world doesn't change — "
            "the lenses are clear glass, or your eyes don't need correction. "
            "But wearing them feels right, like putting on a familiar coat."
        ),
    },
    "chess_piece": {
        "name": "Ivory Chess King",
        "room_desc": "An ivory chess king lies on its side, separated from its board.",
        "examine": (
            "The white king, hand-carved from ivory, heavier than you'd expect. "
            "There's a chip on the crown from years of play. You turn it in "
            "your fingers and feel a pang of something — competitiveness? "
            "Fondness? Someone you played against regularly. A colleague, "
            "maybe. The feeling fades without resolving into a face."
        ),
    },
    "thimble": {
        "name": "Silver Thimble",
        "room_desc": "A tiny silver thimble sits on a windowsill, catching the light.",
        "examine": (
            "It's engraved with a vine pattern — delicate, feminine work. "
            "Not yours. Someone else's hands used this, smaller hands, "
            "patient hands that mended and stitched. You close your fist "
            "around it and feel a warmth that has nothing to do with the metal."
        ),
    },
    "compass": {
        "name": "Brass Compass",
        "room_desc": "A brass compass lies here, its glass face clouded with age.",
        "examine": (
            "The needle spins slowly when you hold it flat — then stops, "
            "pointing firmly in one direction. Not north, you think. You're "
            "not sure which direction it's indicating. Toward something, "
            "or away from something? The needle holds steady, unwavering."
        ),
    },
    "pressed_flower": {
        "name": "Pressed Orchid",
        "room_desc": "A pressed orchid lies between two sheets of wax paper.",
        "examine": (
            "Dendrobium nobile. The Latin name arrives without effort, "
            "followed by a cascade of taxonomy: family Orchidaceae, "
            "tribe Dendrobieae. You know this plant. You know EVERY plant. "
            "The knowledge is there even when nothing else is."
        ),
    },
    "photograph": {
        "name": "Faded Photograph",
        "room_desc": "A loose photograph lies here, face-down, its edges curling.",
        "examine": (
            "A group of men in academic robes on stone steps — a university. "
            "One man in the second row has his hand raised, mid-wave, grinning. "
            "Something about his posture feels familiar. Is that you? The "
            "photo is too faded to be sure. On the back: 'Faculty, Autumn 1921.'"
        ),
    },
    "key": {
        "name": "Brass Key",
        "room_desc": "A small brass key lies here, attached to a leather fob.",
        "examine": (
            "A desk key, or a cabinet key — something small and personal. "
            "The leather fob is stamped with initials rubbed smooth by years "
            "of handling. You try it in the nearest keyhole. It doesn't fit. "
            "Whatever this key opened, it isn't in this room."
        ),
    },
    "tin_soldier": {
        "name": "Lead Soldier",
        "room_desc": "A small lead soldier stands at attention here, paint worn to bare metal.",
        "examine": (
            "A British infantryman in red coat and bearskin hat, three inches "
            "tall. The paint has been loved off by small fingers over many "
            "campaigns on bedroom floors. One arm is bent wrong — a casualty "
            "of play, carefully bent back. A child treasured this soldier."
        ),
    },
    "pencil_sketch": {
        "name": "Pencil Sketch",
        "room_desc": "A loose pencil sketch on yellowed paper lies here.",
        "examine": (
            "A sketch of a house — THIS house, drawn from the garden. Smoke "
            "curls from the chimney. A figure stands at an upstairs window, "
            "too small to make out. The drawing is skilled — confident lines, "
            "good perspective. In the corner: 'Home, Sept. 1919.'"
        ),
    },
    "cufflinks": {
        "name": "Enamel Cufflinks",
        "room_desc": "A pair of green enamel cufflinks sits in a small leather box.",
        "examine": (
            "Forest green enamel set in brass, each painted with a tiny fern "
            "frond. Custom work — someone had these made for a man who loved "
            "botany. A gift? The leather box is lined with blue velvet. No "
            "card, no inscription. But clearly important enough to keep."
        ),
    },
    "candle_stub": {
        "name": "Candle Stub",
        "room_desc": "A half-burned candle sits in a brass holder, wax pooled at the base.",
        "examine": (
            "Burned down to a two-inch stub, wax dripped over the holder "
            "in long runs. Someone was working by candlelight when they "
            "stopped — the wick is pinched, not blown out. Pinched between "
            "two fingers. A careful habit."
        ),
    },
    "recipe_card": {
        "name": "Handwritten Recipe",
        "room_desc": "A stained recipe card lies here, spotted with old grease.",
        "examine": (
            "In a woman's neat hand: 'Mother Wren's Blackberry Tart.' "
            "Detailed and practical — 'use only the berries from the south "
            "hedge, the north ones are too sour.' Below, in different ink: "
            "'Elias says add more sugar. Elias is wrong.' You smile."
        ),
    },
    "magnifying_lens": {
        "name": "Magnifying Lens",
        "room_desc": "A heavy magnifying lens lies here, its brass handle tarnished green.",
        "examine": (
            "A serious instrument — large lens, heavy brass frame. You hold "
            "it up and the room leaps into sharp, almost painful detail. "
            "Every crack in the plaster, every mote of dust. You lower it. "
            "Some things are better seen at a distance."
        ),
    },
    "sheet_music": {
        "name": "Sheet Music",
        "room_desc": "A few pages of sheet music lie here, held together with a rusted clip.",
        "examine": (
            "A piano arrangement of 'Clair de Lune.' Dog-eared corners, "
            "pencil annotations — 'slower here,' 'M's favorite part.' "
            "Someone practiced this piece often, for someone who loved it."
        ),
    },
    "bird_skull": {
        "name": "Small Bird Skull",
        "room_desc": "A tiny bird skull sits on a square of cotton wool.",
        "examine": (
            "Sparrow. Passer domesticus. The skull is fragile and perfect, "
            "cleaned and mounted with a naturalist's care. A specimen, not "
            "a trophy. Whoever placed this here saw beauty in small bones. "
            "You hold it to the light and feel a strange tenderness."
        ),
    },
    "garden_trowel": {
        "name": "Garden Trowel",
        "room_desc": "A garden trowel leans against the wall, blade crusted with old dirt.",
        "examine": (
            "The wooden handle is worn smooth from years of grip. Good steel, "
            "still sound despite the rust. Your hand knows exactly how to "
            "hold it, exactly how to angle the wrist for planting. Muscle "
            "memory, even when the rest is gone."
        ),
    },
    "medicine_bottle": {
        "name": "Brown Glass Bottle",
        "room_desc": "A small brown glass bottle sits here, its label half-peeled.",
        "examine": (
            "'Dr. Hartley's Cardiac Tonic — one tablespoon, twice daily.' "
            "Nearly empty. Heart medicine. Someone in this house had a bad "
            "heart. You set the bottle down and notice your hand is steady. "
            "No tremor, no weakness. You feel fine. You feel nothing at all, "
            "actually."
        ),
    },
}

# ──────────────────────────── ROOMS ──────────────────────────────

ROOM_POOL = {
    "foyer": {
        "name": "The Foyer",
        "floor": "ground",
        "required": True,
        "description": (
            "A once-handsome entrance hall. Wallpaper peels in long strips "
            "and the tile floor is gritty underfoot. A chandelier hangs "
            "overhead, its crystals clouded. The front door is behind you, "
            "swollen shut in its frame."
        ),
        "ambient": [
            "You try the front door again. It won't budge.",
            "A coat rack by the door. A wool overcoat hangs from one hook, "
            "grey with dust. It looks like it would fit you.",
            "You know this house. You knew where the staircase was before "
            "you saw it. How?",
            "Light from a high window. Same pale overcast as when you "
            "arrived. What time is it?",
            "No sounds from outside. No birds, no wind. Just the house.",
        ],
    },
    "parlor": {
        "name": "The Parlor",
        "floor": "ground",
        "required": False,
        "description": (
            "A sitting room with two armchairs facing a cold fireplace, a "
            "chess game mid-play on a table between them. Bookshelves line "
            "the walls. Above the mantelpiece: a portrait of a man, a "
            "woman, and a small boy."
        ),
        "ambient": [
            "The portrait. The man's jaw, the way he stands. He looks like "
            "someone you know.",
            "You sit in the left armchair without thinking. It feels natural.",
            "The books are mostly botany. Someone had a specific passion.",
            "White was three moves from checkmate. Why walk away from a "
            "winning position?",
            "You pull 'Flora of the British Isles' without looking. "
            "Muscle memory.",
        ],
    },
    "dining_room": {
        "name": "The Dining Room",
        "floor": "ground",
        "required": False,
        "description": (
            "A long oak table set for four. Plates, glasses, tarnished "
            "silverware — a dinner never cleared. A candelabra at center "
            "has melted to stubs."
        ),
        "ambient": [
            "Four settings. A family of four. Or was about to be.",
            "A napkin folded into a swan at the smallest setting.",
            "Real silver — tarnished black. A household that cared.",
            "A crack in one plate. You knew it was there before you looked.",
            "Dust undisturbed. Nobody has eaten here in a very long time.",
        ],
    },
    "kitchen": {
        "name": "The Kitchen",
        "floor": "ground",
        "required": False,
        "description": (
            "Copper pots on hooks, a cast-iron stove gone to rust, a stone "
            "sink with a hand pump. Faint smell of rosemary. Old houses "
            "hold onto things."
        ),
        "ambient": [
            "A calendar: October 1923. A heart drawn around the 14th.",
            "The herb smell comes and goes. Strongest near the stove.",
            "A teacup with a dried ring of tea. Someone's last cup.",
            "You open a cupboard by instinct. Jars of preserves inside.",
            "The window shows the same flat sky. It hasn't changed.",
        ],
    },
    "cellar": {
        "name": "The Cellar",
        "floor": "ground",
        "required": False,
        "description": (
            "Cool, low-ceilinged. Smells of damp earth. Wine racks line "
            "the walls — a few bottles survive, most broken."
        ),
        "ambient": [
            "Surviving bottles: 'Bordeaux 1908,' 'Port 1912.' Someone "
            "took wine seriously.",
            "Honest mineral cold of stone. Almost refreshing.",
            "Height marks scratched into the wall. 'T.W. — age 3.' "
            "'T.W. — age 4.' They stop at 5.",
            "T.W. Thomas Wren? Who stopped measuring?",
            "Quiet down here. The house above feels far away.",
        ],
    },
    "conservatory": {
        "name": "The Conservatory",
        "floor": "ground",
        "required": False,
        "description": (
            "Glass walls, most panes cracked or missing. Wrought-iron "
            "plant stands hold husks of dead ferns. A potting bench under "
            "dried soil and broken terracotta."
        ),
        "ambient": [
            "Plant stands labeled in tiny handwriting. Latin names.",
            "One fern survives — a single green frond uncurling. Stubborn.",
            "Soil under your fingernails. Wait — your nails are clean. "
            "But you felt it. A sense memory.",
            "Broken glass underfoot. Open to the elements for years.",
            "A rusted watering can. The care here is obvious even in ruin.",
        ],
    },
    "library": {
        "name": "The Library",
        "floor": "ground",
        "required": False,
        "description": (
            "Floor-to-ceiling shelves. A leather chair by a standing lamp "
            "with no bulb. Smells of old paper and binding glue."
        ),
        "ambient": [
            "Botany, taxonomy, natural history. A whole section on orchids.",
            "A bookmark halfway through a chapter on alpine pollination.",
            "The reading chair fits you like it was broken in by your body.",
            "'Proceedings of the Royal Botanical Society.' 1920 to 1923.",
            "Penciled notes in every margin. Small, meticulous. Yours.",
        ],
    },
    "pantry": {
        "name": "The Pantry",
        "floor": "ground",
        "required": False,
        "description": (
            "Narrow room. Shelves of mason jars, tins, crockery. Most "
            "labels peeled. A few jars hold dark, unidentifiable preserves."
        ),
        "ambient": [
            "Crystallized honey in a jar. Still good, probably.",
            "Labels in feminine hand: 'Blackberry 1922,' 'Plum 1923.'",
            "You reach for the tea tin without looking. Knew exactly where.",
            "Flour hardened to a white crust on one shelf. Years old.",
            "A well-stocked house. Comfortable, but hands-on.",
        ],
    },
    "wash_room": {
        "name": "The Wash Room",
        "floor": "ground",
        "required": False,
        "description": (
            "Stone basin, wooden washboard, a mangle for wringing. Rope "
            "lines criss-cross overhead, empty now."
        ),
        "ambient": [
            "Folded linens in a wicker basket. Yellowed but neat.",
            "The washboard worn smooth in the center.",
            "Two aprons on wall pegs — one large, one small.",
            "Harsh soap, cracked and dry, on the basin edge.",
            "A working household. Not wealthy. Comfortable.",
        ],
    },
    "upstairs_hall": {
        "name": "The Upstairs Hallway",
        "floor": "upper",
        "required": True,
        "description": (
            "A long hallway with closed doors. Carpet runner worn thin — "
            "decades of footsteps ground into the weave. Faded photographs "
            "line the walls."
        ),
        "ambient": [
            "Photographs. Formal poses, stiff collars. Ghosted by decades "
            "of light.",
            "The carpet worn in a particular path. Thousands of trips.",
            "A mirror at the end of the hall, clouded with age.",
            "You walk the worn path. Your feet fit step for step.",
            "How long have you been here? The light hasn't changed.",
        ],
    },
    "bedroom": {
        "name": "The Master Bedroom",
        "floor": "upper",
        "required": False,
        "description": (
            "Four-poster bed, canopy threadbare. Covers pulled back on the "
            "left, the right neatly made. A vanity holds a hairbrush and "
            "a dried flower."
        ),
        "ambient": [
            "Only the left side slept in. For a long time.",
            "A woman's shawl on the bedpost. Lavender and wool.",
            "A wedding portrait on the nightstand. The groom might be you.",
            "You know which drawer holds the watch. Left. How?",
            "The vanity flower is a primrose. Primula vulgaris. You just know.",
        ],
    },
    "study": {
        "name": "The Study",
        "floor": "upper",
        "required": False,
        "description": (
            "The most lived-in room. Books and specimen jars on every "
            "surface. A heavy desk under drawn curtains, covered in papers "
            "and pressed flowers. The chair is pushed back at an angle."
        ),
        "ambient": [
            "Old paper and dried flowers. You feel at ease here.",
            "The chair at an odd angle. Someone stood up fast. Or was "
            "pulled from their work.",
            "You recognize every jar. Know the contents before reading.",
            "The chair fits you perfectly. Worn by your exact hands.",
            "A child's drawing above the desk. A red train. 'For Papa.'",
        ],
    },
    "nursery": {
        "name": "The Nursery",
        "floor": "upper",
        "required": False,
        "description": (
            "Faded blue paint. A wooden crib, a rocking chair. Toys on the "
            "floor: blocks, a one-eyed stuffed bear, tin soldiers on the "
            "windowsill."
        ),
        "ambient": [
            "A loved room. Someone spent hours here, watching a child sleep.",
            "Tin soldiers in careful formation. A child's serious work.",
            "The stuffed bear. One button eye. Your chest tightens.",
            "A music box — three notes of a lullaby, then it sticks.",
            "Thomas's room. You know that now.",
        ],
    },
    "guest_room": {
        "name": "The Guest Room",
        "floor": "upper",
        "required": False,
        "description": (
            "A modest room. Single iron bed, neatly made. Washstand, small "
            "wardrobe. The sterile tidiness of a space rarely used."
        ),
        "ambient": [
            "Hospital corners on the bed. Pride in maintenance.",
            "Guest book in the nightstand. Last entry: September 1923.",
            "Wire hangers chime in the empty wardrobe.",
            "Same unchanging sky through the window.",
            "This room doesn't feel like yours. The only one that doesn't.",
        ],
    },
    "sewing_room": {
        "name": "The Sewing Room",
        "floor": "upper",
        "required": False,
        "description": (
            "A treadle sewing machine, a mannequin draped in unfinished "
            "fabric. Spools of thread fill a wall rack. A pincushion "
            "bristles on the worktable."
        ),
        "ambient": [
            "The fabric: a child's coat, half-finished. Expert stitching.",
            "A basket of mending. Socks, a collar, small patched trousers.",
            "Margaret's room. You're certain without evidence.",
            "Spools organized by color. Order and beauty in equal measure.",
            "A thimble on the windowsill, catching thin light.",
        ],
    },
    "bathroom": {
        "name": "The Bathroom",
        "floor": "upper",
        "required": False,
        "description": (
            "Claw-foot tub, enamel yellowed. Pedestal sink. Medicine "
            "cabinet, mirrored door ajar. Black and white tile, cracked."
        ),
        "ambient": [
            "Brown bottles in the cabinet. Tinctures from another era.",
            "A straight razor on the ledge, still sharp. Ivory handle.",
            "The cabinet mirror at a bad angle. You can see the wall "
            "behind you but not yourself.",
            "Dried soap, cracked, on the sink. Someone's last wash.",
            "Mineral ring in the tub. Hard water. A well, probably.",
        ],
    },
    "attic": {
        "name": "The Attic",
        "floor": "upper",
        "required": False,
        "description": (
            "Under the eaves. Trunks, hatboxes, furniture in dust cloths. "
            "Cobwebs span the rafters. A round window, a disc of grey."
        ),
        "ambient": [
            "A trunk of letters tied with ribbon. Dozens, too faded to read.",
            "A cradle, older than the nursery crib. An heirloom.",
            "Under a cloth: a rocking horse with a cracked eye.",
            "A bowler hat in a hatbox. It fits you exactly.",
            "The round window shows grey sky. No trees, no rooftops. Just grey.",
        ],
    },
}


# ─────────────────── THE DARKNESS ────────────────────────────────

DARKNESS_ARRIVAL = [
    (
        "The temperature drops. Not gradually — all at once, as though "
        "something swallowed the warmth from the room. The shadows in the "
        "corners aren't just dark. They're DEEP. They're moving."
    ),
    (
        "A heaviness settles over the room like a held breath. The light "
        "dims — not the way clouds cover the sun, but the way a candle "
        "gutters when something passes through the air."
    ),
    (
        "Something is here. You can't see it. You can't name it. But "
        "the room feels smaller, the walls closer. The air itself has "
        "thickened into something that resists you."
    ),
]

DARKNESS_ESCALATION = {
    3: [
        "The shadows shift at the edges of your vision. When you look "
        "directly at them, they stop. When you look away, they inch closer.",
        "There is a pressure in the air. A low hum below the threshold of "
        "hearing. It presses against your thoughts like a thumb on wet clay.",
        "The room is dimmer now. The objects around you are losing their "
        "edges, blurring into the dark.",
    ],
    2: [
        "The darkness is closer. You can FEEL it — not on your skin, but "
        "deeper. On your memories. The lullaby, the greenhouse, the boy "
        "with your eyes — they flicker like a candle in a wind.",
        "You can't remember which direction you came from. The exits are "
        "there, but the darkness is between you and the details.",
        "Something is pulling at you. Not your body — your NAME. You can "
        "feel yourself fraying at the edges, like old cloth.",
    ],
    1: [
        "The darkness has a voice. Not words — something older. A low "
        "sound like forgetting itself, like the moment a name slips off "
        "the tongue. It says: you are nothing. You were never anything.",
        "You are dissolving. Not your body — your SELF. The memories you "
        "fought to recover are flickering out one by one. Mother. Margaret. "
        "Thomas. Their faces are going dark.",
        "This is what it means to be truly forgotten. Not by others — by "
        "yourself. The darkness isn't a thing. It's an absence. And it's "
        "where you're going.",
    ],
}

DARKNESS_NEARBY = [
    "A chill seeps in from somewhere close. Not the cold of winter — "
    "something less natural. Something that makes you want to leave.",
    "The light in this room seems thinner than before. The shadows are "
    "a shade too dark in one direction.",
    "You feel a pull — a faint, unsettling gravity toward one of the "
    "exits. Or away from something behind it.",
    "The air has a weight to it. Somewhere nearby, something is wrong.",
    "A low vibration in the floor, below hearing. Your teeth ache. "
    "It's coming from close by.",
]

DARKNESS_BANISHED = [
    (
        "You open your mouth and the lullaby comes out. Fragile, "
        "wavering, barely a sound — but real. Three notes rising, "
        "three notes falling. Your mother's song.\n\n"
        "  The darkness FLINCHES. It recoils like a living thing "
        "struck by light. The shadows peel back from the walls, the "
        "air warms, the pressure lifts. For a moment you feel her — "
        "your mother, standing behind you, hands on your shoulders. "
        "\"My little sparrow.\"\n\n"
        "  Then she's gone. But the darkness is gone too."
    ),
    (
        "The lullaby rises in your chest before you think to hum it. "
        "Three notes up, three notes down. A simple melody. A mother's "
        "voice carried across decades.\n\n"
        "  The darkness shudders. It contracts, pulling away from the "
        "sound the way oil pulls from water. The room brightens. The "
        "weight lifts from your mind. You can think again. You can "
        "remember.\n\n"
        "  The melody fades, but the warmth stays."
    ),
    (
        "You hum. It's barely audible — a breath with shape. But the "
        "lullaby knows itself. The notes find their order: rising, "
        "falling, rising. The song your mother sang when the world was "
        "too dark and too large.\n\n"
        "  The darkness screams — not with sound but with silence. A "
        "silence so total it hurts. Then it breaks apart, scattering "
        "into the corners and dissolving like smoke.\n\n"
        "  You are alone again. But not empty."
    ),
]

DARKNESS_NO_SONG = [
    "You try to hum but nothing comes out. You don't know any songs. "
    "You don't know anything worth singing.",
    "You open your mouth but there's no melody there. Just silence. "
    "The darkness presses closer.",
    "Hum what? You reach for a song and find only the void where "
    "music used to live.",
]

DARKNESS_CONSUMED = [
    (
        "The darkness reaches you.\n\n"
        "  It doesn't hurt. That's the worst part. It feels like "
        "falling asleep — like letting go of something you were "
        "holding too tightly. The memories unspool: Thomas, Margaret, "
        "the greenhouse, the lullaby. One by one, like beads sliding "
        "off a broken string.\n\n"
        "  You forget your son's name.\n"
        "  You forget your wife's face.\n"
        "  You forget your mother's song.\n"
        "  You forget that you forgot.\n\n"
        "  And then..."
    ),
]


# ──────────────────── MAP GENERATION ─────────────────────────────

def generate_house():
    """Build a randomized house layout. Returns (rooms, all_ids, all_items)."""
    ground_req = [k for k, v in ROOM_POOL.items()
                  if v["floor"] == "ground" and v["required"]]
    ground_opt = [k for k, v in ROOM_POOL.items()
                  if v["floor"] == "ground" and not v["required"]]
    upper_req = [k for k, v in ROOM_POOL.items()
                 if v["floor"] == "upper" and v["required"]]
    upper_opt = [k for k, v in ROOM_POOL.items()
                 if v["floor"] == "upper" and not v["required"]]

    random.shuffle(ground_opt)
    random.shuffle(upper_opt)

    ground = ground_req + ground_opt[:random.randint(3, 4)]
    upper = upper_req + upper_opt[:random.randint(3, 5)]
    all_ids = ground + upper

    rooms = {}
    for rid in all_ids:
        t = ROOM_POOL[rid]
        rooms[rid] = {
            "name": t["name"], "floor": t["floor"],
            "description": t["description"],
            "ambient": list(t["ambient"]),
            "exits": {}, "items": [], "first_visit": True,
        }

    directions = ["north", "south", "east", "west"]

    def connect(rdict, rlist):
        if len(rlist) <= 1:
            return
        random.shuffle(rlist)
        connected = [rlist[0]]
        remaining = list(rlist[1:])
        while remaining:
            nr = remaining.pop(0)
            cands = list(connected)
            random.shuffle(cands)
            for partner in cands:
                ap = [d for d in directions if d not in rdict[partner]["exits"]]
                an = [d for d in directions if d not in rdict[nr]["exits"]]
                for d in ap:
                    o = OPPOSITES[d]
                    if o in an:
                        rdict[partner]["exits"][d] = nr
                        rdict[nr]["exits"][o] = partner
                        break
                else:
                    continue
                break
            connected.append(nr)
        # Extra loop
        for _ in range(30):
            a, b = random.sample(rlist, 2)
            if b in rdict[a]["exits"].values():
                continue
            af = [d for d in directions if d not in rdict[a]["exits"]]
            bf = [d for d in directions if d not in rdict[b]["exits"]]
            for d in af:
                if OPPOSITES[d] in bf:
                    rdict[a]["exits"][d] = b
                    rdict[b]["exits"][OPPOSITES[d]] = a
                    return

    connect(rooms, ground)
    connect(rooms, upper)

    # Stairs
    dirs_shuf = list(directions)
    random.shuffle(dirs_shuf)
    for sp in dirs_shuf:
        o = OPPOSITES[sp]
        if sp not in rooms["foyer"]["exits"] and o not in rooms["upstairs_hall"]["exits"]:
            rooms["foyer"]["exits"][sp] = "upstairs_hall"
            rooms["upstairs_hall"]["exits"][o] = "foyer"
            break

    # Verify connectivity
    vis = set()
    q = deque(["foyer"])
    while q:
        r = q.popleft()
        if r in vis:
            continue
        vis.add(r)
        for nb in rooms[r]["exits"].values():
            if nb not in vis:
                q.append(nb)
    for ur in set(all_ids) - vis:
        for vr in vis:
            vf = [d for d in directions if d not in rooms[vr]["exits"]]
            uf = [d for d in directions if d not in rooms[ur]["exits"]]
            for d in vf:
                if OPPOSITES[d] in uf:
                    rooms[vr]["exits"][d] = ur
                    rooms[ur]["exits"][OPPOSITES[d]] = vr
                    vis.add(ur)
                    break
            if ur in vis:
                break

    # Place items
    all_items = {}
    all_items.update(MEMORY_FRAGMENTS)
    all_items.update(FLAVOR_OBJECTS)

    eligible = [rid for rid in all_ids if rid != "foyer"]
    random.shuffle(eligible)

    mkeys = list(MEMORY_FRAGMENTS.keys())
    random.shuffle(mkeys)
    targets = list(eligible)
    for mk in mkeys:
        rooms[targets.pop(0)]["items"].append(mk)

    fkeys = list(FLAVOR_OBJECTS.keys())
    random.shuffle(fkeys)
    n_flav = random.randint(6, min(9, len(fkeys)))
    fe = list(eligible)
    random.shuffle(fe)
    for i, fk in enumerate(fkeys[:n_flav]):
        rooms[fe[i % len(fe)]]["items"].append(fk)

    return rooms, all_ids, all_items


# ────────────────────── GAME STATE ───────────────────────────────

class GameState:
    def __init__(self):
        self.reset_count = 0
        self._init_world()

    def _init_world(self):
        self.rooms, self.all_room_ids, self.all_items = generate_house()
        self.current_room = "foyer"
        self.inventory = []
        self.memories_unlocked = []
        self.moves = 0
        self.game_over = False

        # Darkness state
        eligible = [r for r in self.all_room_ids if r != "foyer"]
        self.darkness_room = random.choice(eligible)
        self.darkness_timer = random.randint(5, 8)  # turns until it moves
        self.encounter_turns = 0  # 0 = not in encounter
        self.darkness_active = True
        self.darkness_banished_until = 0  # move count when it reappears

    def reset(self):
        """The Darkness consumed you. Start over."""
        self.reset_count += 1
        self._init_world()

    @property
    def memory_count(self):
        return len(self.memories_unlocked)

    @property
    def total_artifacts(self):
        return len(MEMORY_FRAGMENTS)

    def has_item(self, key):
        return key in self.inventory

    def has_memory(self, key):
        return key in self.memories_unlocked

    def has_lullaby(self):
        return "locket" in self.memories_unlocked

    def get_adjacent_rooms(self, room_id):
        return list(self.rooms[room_id]["exits"].values())

    def is_darkness_nearby(self):
        if not self.darkness_active:
            return False
        adj = self.get_adjacent_rooms(self.current_room)
        return self.darkness_room in adj

    def is_in_darkness(self):
        return (self.darkness_active
                and self.current_room == self.darkness_room)

    def move_darkness(self):
        """Relocate The Darkness to a new room."""
        eligible = [r for r in self.all_room_ids
                    if r != "foyer" and r != self.current_room
                    and r != self.darkness_room]
        if eligible:
            self.darkness_room = random.choice(eligible)
        self.darkness_timer = random.randint(5, 8)
        self.encounter_turns = 0

    def tick_darkness(self):
        """Called after each player action. Returns event string or None."""
        # If banished, check if it should reactivate
        if not self.darkness_active:
            if self.moves >= self.darkness_banished_until:
                self.darkness_active = True
                eligible = [r for r in self.all_room_ids
                            if r != "foyer" and r != self.current_room]
                if eligible:
                    self.darkness_room = random.choice(eligible)
                self.darkness_timer = random.randint(5, 8)
            return None

        # Tick roaming timer
        self.darkness_timer -= 1
        if self.darkness_timer <= 0 and not self.is_in_darkness():
            self.move_darkness()

        # Check encounter
        if self.is_in_darkness():
            if self.encounter_turns == 0:
                # Just entered or it just arrived
                self.encounter_turns = 3
                return "arrival"
            else:
                self.encounter_turns -= 1
                if self.encounter_turns <= 0:
                    return "consumed"
                else:
                    return "escalation"
        else:
            self.encounter_turns = 0
            if self.is_darkness_nearby():
                return "nearby"
        return None


# ────────────────── ITEM RESOLUTION ──────────────────────────────

def find_item_key(text, all_items):
    text = text.lower().strip()
    if text in all_items:
        return text
    for key, item in all_items.items():
        if text in item["name"].lower() or text in key:
            return key
    for key, item in all_items.items():
        for word in text.split():
            if len(word) > 2 and (word in item["name"].lower() or word == key):
                return key
    return None


# ────────────────────── DISPLAY ──────────────────────────────────

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
    ║                       M.B. Parks                         ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(title)
    dramatic_pause(1.5)

def show_intro(state):
    clear_screen()
    print_separator("═")
    print()
    if state.reset_count == 0:
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
            "You don't remember what you were doing before this moment.",
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
    else:
        slow_print("You open your eyes.", delay=0.05)
        dramatic_pause(1.0)
        slow_print(
            "You're standing in a house. You've been here before — you're "
            "sure of it. But the rooms are different. The doors lead to "
            "different places. As if the house rearranged itself while "
            "you weren't looking.",
            delay=0.025,
        )
        dramatic_pause(0.5)
        print()
        slow_print(
            "Your mind is blank again. Whatever you knew, whatever you "
            "found — it's gone. Swallowed by that darkness. But the house "
            "still has its secrets. And somewhere in its rooms, the things "
            "you need to remember are waiting.",
            delay=0.025,
        )
        dramatic_pause(0.5)
        print()
        slow_print(
            "You have to be faster this time. The darkness is still here. "
            "You can feel it — patient, circling, hungry.",
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
    print("    take <item>      — Pick up an item")
    print("    examine <item>   — Study an item closely")
    print("    hum              — Hum whatever melody comes to mind")
    print("    inventory / inv  — Check what you're carrying")
    print("    memories         — Review recovered memories")
    print("    map              — See rooms you've visited")
    print("    quit             — End the game")
    print()
    print("  You can also just type a direction: n, s, e, w")
    print_separator()

def describe_room(state):
    room = state.rooms[state.current_room]
    print()
    print_boxed(room["name"])
    print()

    for line in textwrap.wrap(room["description"], width=TERM_WIDTH):
        print(f"  {line}")

    uncollected = [k for k in room["items"] if not state.has_item(k)]
    if uncollected:
        print()
        for ik in uncollected:
            item = state.all_items[ik]
            for line in textwrap.wrap(item["room_desc"], width=TERM_WIDTH):
                print(f"  {line}")

    exits = room["exits"]
    parts = []
    for d, rid in exits.items():
        tname = state.rooms[rid]["name"]
        cf, tf = room["floor"], state.rooms[rid]["floor"]
        if cf != tf:
            label = " ↑stairs" if cf == "ground" else " ↓stairs"
            parts.append(f"{d.upper()}{label} ({tname})")
        else:
            parts.append(f"{d.upper()} ({tname})")
    print()
    print(f"  Exits: {', '.join(parts)}")

    if not room["first_visit"]:
        ambient = random.choice(room["ambient"])
        print()
        for line in textwrap.wrap(ambient, width=TERM_WIDTH):
            print(f"  {line}")

    room["first_visit"] = False

def do_move(state, direction):
    direction = DIR_SHORT.get(direction, direction)
    if direction not in ("north", "south", "east", "west"):
        print("\n  That's not a direction you recognize.")
        return False

    room = state.rooms[state.current_room]
    if direction not in room["exits"]:
        print("\n  There's nothing that way — just a wall.")
        return False

    old_floor = room["floor"]
    state.current_room = room["exits"][direction]
    new_floor = state.rooms[state.current_room]["floor"]
    state.moves += 1
    state.encounter_turns = 0  # left the dark room

    if old_floor != new_floor:
        msgs = (["You climb the stairs.", "You head upstairs."]
                if new_floor == "upper"
                else ["You head downstairs.", "You descend the steps."])
    else:
        msgs = [
            "You walk through the doorway.",
            "You step into the next room.",
            "You head onward.",
            "Your footsteps are quiet on the old floor.",
        ]
    print(f"\n  {random.choice(msgs)}")
    describe_room(state)
    return True

def do_take(state, item_text):
    key = find_item_key(item_text, state.all_items)
    room = state.rooms[state.current_room]
    if not key:
        print("\n  You don't see anything by that name.")
        return
    if key not in room["items"]:
        print("\n  That isn't here.")
        return
    if state.has_item(key):
        print("\n  You already have that.")
        return
    item = state.all_items[key]
    state.inventory.append(key)
    print(f"\n  You pick up the {item['name']}.")
    print(f"  Acquired: {item['name']}")

def do_examine(state, item_text):
    key = find_item_key(item_text, state.all_items)
    if not key:
        print("\n  Examine what? You don't see anything by that name.")
        return
    if not state.has_item(key):
        room = state.rooms[state.current_room]
        if key in room["items"]:
            print(f"\n  You should pick it up first. Try: take {key}")
        else:
            print("\n  You don't have anything like that.")
        return

    item = state.all_items[key]
    print()
    print_separator("·")
    for line in textwrap.wrap(item["examine"], width=TERM_WIDTH):
        print(f"  {line}")

    if item.get("is_memory") and not state.has_memory(key):
        state.memories_unlocked.append(key)
        dramatic_pause(1.0)
        print()
        print_separator("✦")
        print()
        print("  ░░░  M E M O R Y   R E C O V E R E D  ░░░")
        print()
        slow_print(f"  {item['memory']}", delay=0.025)
        print()
        print(f"  ▸ {item['memory_tag']}")
        print(f"  ▸ Memories recovered: {state.memory_count}/{state.total_artifacts}")
        if key == "locket":
            print()
            print("  ▸ You learned the lullaby. You can HUM it now.")
        print()
        print_separator("✦")

        if state.memory_count == 3:
            dramatic_pause(0.8)
            print()
            slow_print(
                "  Elias Wren. Professor. Husband. You have a name now. You "
                "have a life. The house makes sense — it's YOURS. So why "
                "can't you remember leaving?",
                delay=0.025,
            )
        elif state.memory_count == 4:
            dramatic_pause(0.8)
            print()
            slow_print(
                "  A mother, a career, a wife, a son. The pieces are "
                "assembling into someone real. But there's a gap at the "
                "center: what happened to Elias Wren?",
                delay=0.025,
            )

        if state.memory_count == state.total_artifacts:
            trigger_finale(state)
    elif item.get("is_memory") and state.has_memory(key):
        print("\n  You've already studied this. The memory is vivid.")
    else:
        print("\n  It doesn't stir any memories, but something about it")
        print("  feels important. You hold onto it.")

def do_hum(state):
    """Attempt to hum the lullaby."""
    if not state.has_lullaby():
        print(f"\n  {random.choice(DARKNESS_NO_SONG)}")
        return

    if state.is_in_darkness():
        print()
        slow_print(f"  {random.choice(DARKNESS_BANISHED)}", delay=0.02)
        # Banish the darkness
        state.darkness_active = False
        state.darkness_banished_until = state.moves + random.randint(8, 14)
        state.encounter_turns = 0
    else:
        print()
        print("  You hum the lullaby — three notes rising, three notes falling.")
        print("  The melody fills the empty room. It feels like company.")
        if state.is_darkness_nearby():
            print()
            print("  Somewhere close, you feel something recoil. The heaviness")
            print("  in the air thins. Whatever was nearby has moved away.")
            state.move_darkness()

def do_inventory(state):
    print()
    print_separator()
    if not state.inventory:
        print("  You're not carrying anything.")
    else:
        print("  You are carrying:")
        for key in state.inventory:
            item = state.all_items[key]
            if key in state.memories_unlocked:
                marker = " ✦"
            elif item.get("is_memory"):
                marker = " (not yet examined)"
            else:
                marker = ""
            print(f"    • {item['name']}{marker}")
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
            item = state.all_items[key]
            print(f"    ✦ {item['memory_tag']}")
        print()
        remaining = state.total_artifacts - state.memory_count
        if remaining > 0:
            print(f"  {remaining} fragment{'s' if remaining != 1 else ''} still missing...")
    print_separator("✦")

def do_map(state):
    print()
    print_separator()
    print("  R O O M S   V I S I T E D:")
    print()
    for rid in state.all_room_ids:
        room = state.rooms[rid]
        if not room["first_visit"] or rid == state.current_room:
            here = " ◄ you are here" if rid == state.current_room else ""
            uncol = [k for k in room["items"] if not state.has_item(k)]
            inote = f" [{len(uncol)} item{'s' if len(uncol) != 1 else ''}]" if uncol else ""
            fl = "▲" if room["floor"] == "upper" else "▼"
            print(f"    {fl} {room['name']}{inote}{here}")
    print()
    print("  ▲ = upper floor  ▼ = ground floor")
    print_separator()


# ────────────────── DARKNESS EVENTS ──────────────────────────────

def handle_darkness_event(state, event):
    """Display darkness events. Returns True if game should reset."""
    if event == "arrival":
        print()
        print_separator("░")
        slow_print(f"\n  {random.choice(DARKNESS_ARRIVAL)}", delay=0.02)
        print()
        remaining = state.encounter_turns
        if state.has_lullaby():
            slow_print(
                f"  You have {remaining} moment{'s' if remaining != 1 else ''} "
                "before it reaches you. You could HUM, or you could RUN.",
                delay=0.02,
            )
        else:
            slow_print(
                f"  You have {remaining} moment{'s' if remaining != 1 else ''} "
                "before it reaches you. You need to LEAVE. NOW.",
                delay=0.02,
            )
        print_separator("░")
        return False

    elif event == "escalation":
        remaining = state.encounter_turns
        msgs = DARKNESS_ESCALATION.get(remaining, DARKNESS_ESCALATION[1])
        print()
        print_separator("░")
        slow_print(f"\n  {random.choice(msgs)}", delay=0.02)
        print()
        if remaining == 1:
            if state.has_lullaby():
                slow_print(
                    "  This is your last chance. HUM or LEAVE.",
                    delay=0.03,
                )
            else:
                slow_print(
                    "  This is your last chance. RUN.",
                    delay=0.03,
                )
        else:
            slow_print(
                f"  {remaining} moment{'s' if remaining != 1 else ''} left.",
                delay=0.02,
            )
        print_separator("░")
        return False

    elif event == "consumed":
        print()
        print_separator("░")
        slow_print(f"\n  {random.choice(DARKNESS_CONSUMED)}", delay=0.03)
        dramatic_pause(2.0)
        print()
        print_separator("░")
        return True  # trigger reset

    elif event == "nearby":
        print()
        print(f"  {random.choice(DARKNESS_NEARBY)}")
        return False

    return False


# ───────────────────────── FINALE ────────────────────────────────

def trigger_finale(state):
    dramatic_pause(2.0)
    clear_screen()
    print()
    print_separator("═")
    print()

    slow_print("Margaret's letter. You read it a third time, slower.", delay=0.035)
    dramatic_pause(1.0)
    print()
    slow_print("\"It has been a year.\"", delay=0.04)
    dramatic_pause(0.8)
    slow_print("\"I've kept the study exactly as you left it.\"", delay=0.04)
    dramatic_pause(0.8)
    slow_print("\"I hope wherever you are, you can hear me.\"", delay=0.04)
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
        "The pocket watch. Stopped at 11:47. The crystal cracked — but "
        "you never asked what cracked it. A watch doesn't crack on a "
        "nightstand.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    slow_print(
        "It cracks when it hits a desk. When someone falls forward.",
        delay=0.035,
    )
    dramatic_pause(1.5)
    print()
    slow_print(
        "The study. The chair pushed back at that angle. You thought "
        "someone stood up in a hurry.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    slow_print("Nobody stood up.", delay=0.05)
    dramatic_pause(2.5)

    print()
    print_separator()
    print()

    slow_print(
        "You walk to the nearest mirror. Wipe it clean. The glass is "
        "perfectly clear.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    slow_print(
        "The room is reflected perfectly. Where you are standing, "
        "there is nothing.",
        delay=0.03,
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
        "  On November 2nd, 1923, you were working late. You felt a "
        "tightness in your chest. Your watch struck the desk and cracked.",
        delay=0.035,
    )
    dramatic_pause(1.0)
    slow_print("  The time was 11:47 PM.", delay=0.05)
    dramatic_pause(1.5)
    slow_print(
        "  Margaret found you the next morning. She kept your study "
        "exactly as you left it.",
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
        "changed. The silence outside. You thought the house was "
        "abandoned.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    print()
    slow_print(
        "The house isn't abandoned. The house is all that's left.",
        delay=0.04,
    )
    dramatic_pause(1.5)
    slow_print("You didn't find this place. You never left it.", delay=0.04)
    dramatic_pause(1.5)

    if state.reset_count > 0:
        print()
        slow_print(
            f"  You have been here since 11:47 PM on November 2nd, 1923. "
            f"The darkness that swallowed you {state.reset_count} "
            f"time{'s' if state.reset_count != 1 else ''} — it wasn't a "
            f"monster. It was forgetting. Every time it took you, you "
            f"lost yourself completely, and the house reshuffled around "
            f"the gap where you used to be. But you came back. You "
            f"always came back.",
            delay=0.025,
        )
    else:
        slow_print(
            "You have been here since 11:47 PM on November 2nd, 1923, "
            "walking the same rooms for a hundred years.",
            delay=0.03,
        )
    dramatic_pause(2.0)
    print()
    slow_print(
        "And the only reason you couldn't see yourself in the mirror "
        "is that there is nothing left to see.",
        delay=0.035,
    )
    dramatic_pause(2.0)

    # The Darkness resolves
    if state.reset_count > 0:
        print()
        slow_print(
            "The darkness stirs one last time — somewhere deep in the "
            "cellar, or the attic, or whatever corner of the house it "
            "was hiding in. It reaches for you.",
            delay=0.03,
        )
        dramatic_pause(1.0)
        slow_print(
            "But you are Elias Wren. You are a husband and a father "
            "and a son and a scholar. You are five memories and a "
            "hundred years of stubbornness. You are not nothing.",
            delay=0.03,
        )
        dramatic_pause(1.0)
        slow_print(
            "You hum the lullaby — all of it this time, start to finish "
            "— and the darkness dissolves like frost in morning sun.",
            delay=0.03,
        )
        dramatic_pause(1.5)

    print()
    print_separator("═")
    print()

    slow_print(
        "Somewhere in the house, a curtain falls open. Beyond the glass "
        "— not grey sky, not silence — there is light. Warm, golden, "
        "the color of an October afternoon.",
        delay=0.03,
    )
    dramatic_pause(1.5)
    print()
    slow_print(
        '  "There you are," Margaret says. "We\'ve been waiting."',
        delay=0.05,
    )
    dramatic_pause(1.5)
    slow_print('  Thomas waves. "Come ON, Papa!"', delay=0.05)
    dramatic_pause(2.0)
    print()
    slow_print(
        "The window opens easily. October air. Wood smoke and apples. "
        "For the first time in a hundred years, you feel the breeze.",
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
        "The house stands quiet. The rocking chair is still. The "
        "chandelier motionless. The pocket watch reads 11:47.",
        delay=0.03,
    )
    dramatic_pause(1.0)
    print()
    slow_print(
        "The chair in the study is pushed neatly in — tucked in, as "
        "though someone has finally finished their work.",
        delay=0.03,
    )
    dramatic_pause(1.5)
    print()
    slow_print(
        "The front door swings open. Autumn light floods the foyer.",
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
    visited = len([r for r in state.rooms.values() if not r["first_visit"]])
    total = len(state.rooms)
    collected = len(state.inventory)
    total_items = sum(len(r["items"]) for r in state.rooms.values())
    print("              T H E   F O R G O T T E N   O N E")
    print()
    print(f"                 Memories recovered: {state.memory_count}/{state.total_artifacts}")
    print(f"                 Items collected: {collected}/{total_items}")
    print(f"                 Rooms explored: {visited}/{total}")
    print(f"                 Moves taken: {state.moves}")
    if state.reset_count > 0:
        print(f"                 Times consumed: {state.reset_count}")
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
        "run": "go", "flee": "go", "escape": "go",
        "look": "look", "l": "look",
        "examine": "examine", "x": "examine", "inspect": "examine",
        "study": "examine", "read": "examine",
        "take": "take", "get": "take", "grab": "take", "pick": "take",
        "hum": "hum", "sing": "hum", "lullaby": "hum",
        "inventory": "inventory", "inv": "inventory", "i": "inventory",
        "memories": "memories", "memory": "memories", "remember": "memories",
        "help": "help", "?": "help", "commands": "help",
        "map": "map", "m": "map",
        "quit": "quit", "exit": "quit", "q": "quit",
        "whisper": "whisper", "credits": "whisper", "about": "whisper", "author": "whisper",
    }
    return aliases.get(cmd, cmd), arg

def main():
    show_title()
    input("  Press ENTER to begin...\n")

    state = GameState()

    while True:
        show_intro(state)
        describe_room(state)

        while not state.game_over:
            raw = prompt()
            if not raw:
                continue

            cmd, arg = parse_command(raw)
            acted = True  # did the player spend a turn?

            if cmd == "go":
                acted = do_move(state, arg)
            elif cmd == "look":
                describe_room(state)
                acted = False
            elif cmd == "examine":
                if arg:
                    do_examine(state, arg)
                else:
                    print("\n  Examine what? Try: examine <item name>")
                    acted = False
            elif cmd == "take":
                if arg:
                    do_take(state, arg)
                else:
                    print("\n  Take what? Try: take <item name>")
                    acted = False
            elif cmd == "hum":
                do_hum(state)
            elif cmd == "inventory":
                do_inventory(state)
                acted = False
            elif cmd == "memories":
                do_memories(state)
                acted = False
            elif cmd == "map":
                do_map(state)
                acted = False
            elif cmd == "help":
                show_help()
                acted = False
            elif cmd == "quit":
                print()
                confirm = input("  Are you sure? (yes/no) > ").strip().lower()
                if confirm in ("yes", "y"):
                    print()
                    slow_print(
                        "You head for the front door. It won't budge.",
                        delay=0.03,
                    )
                    dramatic_pause(0.5)
                    print()
                    c2 = input("  Force the door? (yes/no) > ").strip().lower()
                    if c2 in ("yes", "y"):
                        print()
                        slow_print(
                            "It doesn't move. Maybe there's more to find.",
                            delay=0.03,
                        )
                    else:
                        print("\n  You step back. Not yet.")
                acted = False
            elif cmd == "whisper":
                print()
                print_separator("·")
                print()
                slow_print(
                    "  You lean close to the wall and whisper.",
                    delay=0.025,
                )
                dramatic_pause(0.5)
                print()
                slow_print(
                    "  For a moment, nothing. Then — from somewhere beyond the "
                    "wallpaper, beyond the plaster, beyond the house itself — "
                    "a voice whispers back. Not Elias. Not Margaret. Someone "
                    "else entirely. Someone who built these walls from words.",
                    delay=0.025,
                )
                print()
                print('  "This story was crafted by Michael B. Parks.')
                print('  Visit him at https://michaelbparks.com')
                print()
                print('  Thank you for listening."')
                print()
                print_separator("·")
                acted = False
            else:
                unknowns = [
                    "You're not sure what you mean. Try HELP.",
                    "That doesn't make sense. Try HELP.",
                    "You pause, confused. Try HELP.",
                ]
                print(f"\n  {random.choice(unknowns)}")
                acted = False

            if state.game_over:
                break

            # Tick darkness only on real actions
            if acted:
                event = state.tick_darkness()
                if event:
                    consumed = handle_darkness_event(state, event)
                    if consumed:
                        dramatic_pause(2.0)
                        print()
                        slow_print(
                            "You open your eyes.",
                            delay=0.06,
                        )
                        dramatic_pause(2.0)
                        state.reset()
                        break  # restart inner loop

        if state.game_over:
            break  # true ending reached

    print("  Goodbye.\n")

if __name__ == "__main__":
    main()

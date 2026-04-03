#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              T H E   F O R G O T T E N   O N E               ║
║         A Text Adventure of Memory and Discovery             ║
║                       ~ M.B. Parks ~                         ║
╚══════════════════════════════════════════════════════════════╝

Dynamically generated layouts — no two games are the same.
Beware The Darkness.
"""

import sys, textwrap, time, os, random, re
from datetime import datetime
from collections import deque

TERM_WIDTH = 72

def clear_screen(): os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.03, width=TERM_WIDTH):
    for ch in textwrap.fill(text, width=width):
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    print()

def dramatic_pause(s=1.0): time.sleep(s)
def print_separator(ch="─", w=TERM_WIDTH): print(ch * w)

def print_boxed(text, w=TERM_WIDTH):
    lines = textwrap.wrap(text, width=w - 6)
    print("╔" + "═" * (w - 2) + "╗")
    for l in lines: print(f"║  {l}{' ' * (w - 4 - len(l))}║")
    print("╚" + "═" * (w - 2) + "╝")

def prompt():
    print()
    return input("  > ").strip().lower()

OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}
DSH = {"n": "north", "s": "south", "e": "east", "w": "west"}

# ─────────────── TEXTUAL SOUND DESCRIPTIONS ──────────────────────

SND_DRONE_G = ["  [A low hum vibrates through the floorboards, barely audible.]",
               "  [The house settles with a deep, wooden groan.]"]
SND_DRONE_U = ["  [The rafters creak. A thin, high tone hovers at the edge of hearing.]",
               "  [Something resonates in the walls — not a sound, but a pressure.]"]
SND_LULLABY = ("  [Three crystalline notes ring out — rising, rising, rising.\n"
               "   Then three more — falling, falling, falling.\n"
               "   A music box. Your mother's lullaby.]")
SND_MEMORY = ("  [A warmth swells in the air — not heat, but presence.\n"
              "   As if the house itself is remembering alongside you.]")
SND_DK_RUMBLE = [
    "  [A low vibration presses against your eardrums. Below hearing, felt in your teeth.]",
    "  [The rumble deepens. The walls hum a note that shouldn't exist.]",
    "  [The sound is inside you. A frequency that makes your thoughts shudder.]"]
SND_BANISH = ("  [The lullaby cuts through the rumble like a blade of light.\n"
              "   Three notes up. Three notes down.\n"
              "   Then: warmth. A chord that fills the room like sunlight through glass.]")
SND_FINALE = ("  [Silence. A silence so complete it has weight.\n"
              "   Then — slowly — a chord. Warm, major, building.\n"
              "   Note by note, like someone opening curtains\n"
              "   on a window shuttered for a century.]")

# ─────────────── CORRUPTION SYSTEM ───────────────────────────────

CORRUPT_SWAPS = [
    ("four","five"),("three","four"),("left","right"),("warm","cold"),
    ("light","dark"),("open","closed"),("old","ancient"),("quiet","silent"),
    ("dust","ash"),("home","tomb"),("room","cage"),("door","wall"),
    ("family","strangers"),("morning","midnight"),("remember","forget"),
    ("alive","gone"),("love","loss"),("name","nothing"),("here","nowhere"),
    ("you","no one"),("chair","coffin"),("bed","grave"),("window","mirror"),
    ("waiting","watching"),("empty","hollow"),("still","dead")]

def corrupt_text(text, level):
    if level <= 0: return text
    chance = {1: 0.06, 2: 0.15}.get(level, 0.3)
    result = []
    for word in text.split(" "):
        if random.random() > chance:
            result.append(word); continue
        clean = word.lower().strip(".,!?;:'\"")
        swapped = False
        for f, t in CORRUPT_SWAPS:
            if clean == f:
                result.append("█" * len(word) if level >= 3 else t)
                swapped = True; break
        if not swapped:
            result.append("—" * len(word) if level >= 3 and len(word) > 3 else word)
    return " ".join(result)

# ─────────────── TRACE TEMPLATES ─────────────────────────────────

TRACE_TEMPLATES = [
    "There are scratches on the doorframe. Tally marks — {n} of them. You don't remember making them, but you know they're yours.",
    'A note in your own handwriting, behind a baseboard: "DON\'T FORGET THE LULLABY."',
    'Something written in the dust: "E.W. WAS HERE." The handwriting is frantic.',
    'Scratched into the plaster: "THE DARKNESS LIES."',
    "A smudge on the wall at shoulder height. Someone leaned here, exhausted, many times.",
    "Faint circles worn into the floor. Someone paced this exact room, over and over.",
    'A note in a crack: "The locket. Find the locket first."',
    'Written on the wall in a shaking hand: "MARGARET I\'M SORRY."',
    "Tally marks on the windowsill. {n} groups of five. How long have you been doing this?",
    'A single word carved into the floor: "REMEMBER."']

# ─────────────── CLOCK SYSTEM ────────────────────────────────────

def get_clock_ambient():
    h, m = datetime.now().hour, datetime.now().minute
    if h == 23 and m == 47:
        return ("The pocket watch in your hand grows warm. 11:47. Something about "
                "this moment — right now — is significant. The house holds its breath.")
    if h >= 22 or h < 3:
        return random.choice(["It's late — you feel it in your bones.",
            "Middle of the night. The house feels more awake than it should.",
            "A late hour. The kind when bad things happen to weak hearts."])
    if h < 7: return random.choice(["It should be early morning. The light hasn't changed.",
        "Dawn should be breaking. But the light never changes."])
    if h < 12: return random.choice(["Morning light should be streaming in. Same flat grey.",
        "The morning should feel fresh. This house doesn't know morning."])
    if h < 17: return random.choice(["Afternoon. The light should be shifting. It isn't.",
        "The day should be half over. Time doesn't pass here."])
    return random.choice(["Evening. The light should be golden. Same grey as always.",
        "The hour when families gather. The table is still set."])

# ────────────────────── MEMORY FRAGMENTS ─────────────────────────

MEM = {
    "locket": {"name": "Tarnished Silver Locket", "room_desc": "A tarnished silver locket lies here, its chain coiled in a neat circle.",
        "examine": "You open the locket. Inside is a faded photograph: a woman with kind eyes and a child on her lap. The photo is so old the edges have turned to velvet. But the woman's face — you know that face.",
        "memory": "The scent of lavender. A kitchen with copper pots and flour dusting every surface. A voice singing — not well, but with such tenderness it didn't matter. \"My little sparrow,\" she called you. Mother. She was your MOTHER. The memory is warm and complete, like stepping into sunlight. But her name stays just out of reach.\n\n  And the song. You can almost hum it. A lullaby — three notes rising, three notes falling. It sits at the edge of your mind like a candle in a window.",
        "memory_tag": "A mother's love — she called you her little sparrow.", "is_memory": True},
    "journal": {"name": "Water-Damaged Journal", "room_desc": "A journal lies here, its pages bloated and wavy from old water damage.",
        "examine": "Most of the ink has bled beyond reading, but you find a few surviving entries. The handwriting is meticulous, scientific. Dates from 1923. Detailed sketches of ferns with Latin names. You know this handwriting. It's yours.",
        "memory": "A greenhouse. Rows of specimen trays. The earthy smell of peat moss and the scratch of a pen on paper. You were a botanist — a professor at a university. Students filed into your lecture hall every Tuesday and Thursday. You loved it. Ashworth University. That was the place.",
        "memory_tag": "A vocation — you were a professor of botany at Ashworth.", "is_memory": True},
    "pocketwatch": {"name": "Stopped Pocket Watch", "room_desc": "A pocket watch sits here, its crystal cracked in a starburst pattern.",
        "examine": "Silver case, Roman numerals, a delicate chain. The crystal is cracked but legible. Stopped at 11:47. On the back: \"To E.W. — Until the end of time. — M.\"",
        "memory": "An October evening. Lanterns in the garden, maples the color of fire. She stood across from you in white. Margaret. Her name was MARGARET. She pressed this watch into your hand. \"So you'll always come home on time,\" she said. E.W. — Elias Wren. YOUR name. Elias Wren.",
        "memory_tag": "A wedding — you married Margaret. Your name is Elias Wren.", "is_memory": True},
    "toy_train": {"name": "Painted Wooden Train", "room_desc": "A small hand-painted wooden train sits here, red paint chipped to bare wood.",
        "examine": "Light in your hand. The paint applied by someone who cared more about giving than craft. An adult made this for a child.",
        "memory": "A boy. Brown curls, gap-toothed grin, your eyes in a smaller face. \"Again, Papa! Make the whistle!\" You whistle — two short, one long — and he falls over laughing. Thomas. Your son's name was Thomas. You carved this train for his third birthday.",
        "memory_tag": "A son — you had a boy named Thomas.", "is_memory": True},
    "letter": {"name": "Sealed Envelope", "room_desc": "A cream-colored envelope lies here, sealed but never posted.",
        "examine": "The glue gave up long ago. Inside: a single page in a woman's handwriting. \"My dearest Elias.\"",
        "memory": "Margaret's handwriting. \"My dearest Elias — It has been a year and I still set your place at dinner. Thomas drew you a picture of a train. I put it on your desk. I've kept the study exactly as you left it. The house is so quiet without you. I hope wherever you are, you can hear me. I hope you know we're all right. — Your Margaret.\"\n\n  You read it twice. A year since what? Where did you go?",
        "memory_tag": "Margaret's letter — she missed you terribly.", "is_memory": True},
    "fathers_letter": {"name": "Father's Letter",
        "room_desc": "A brittle, yellowed letter lies in the open strongbox.",
        "examine": "The handwriting is rigid, deliberate — each letter formed with the precision of a man who said exactly what he meant. Black ink. Heavy stock. It begins: \"Elias —\" Not \"Dear Elias.\" Not \"My son.\" Just your name, followed by a dash.",
        "memory": "Your father's study. Not like yours — no pressed flowers, no Latin. Ledgers. Account books. Pipe tobacco and boot polish. He stood behind his desk — never sat when delivering a verdict — and said: \"You have chosen weeds over this family's legacy. Three generations of Wrens have worked this land.\"\n\n  You tried to explain. Botany. Research. The university. He held up a hand.\n\n  \"I have nothing more to say to you.\"\n\n  The letter came six months later. Formal. Final. The farm went to your cousin. You were no longer welcome at holidays. He signed it \"R. Wren\" — not \"Father.\" Not even \"Robert.\"\n\n  Margaret held you that night while you wept. You never wrote back. He died in 1919 without another word between you.\n\n  You kept the letter in a locked box because you couldn't bear to read it again. And you couldn't bear to throw it away.",
        "memory_tag": "A father's silence — some wounds never heal.", "is_memory": True},
}

# ──────────────────── FLAVOR OBJECTS ─────────────────────────────

FLAV = {
    "pipe": {"name": "Briar Pipe", "room_desc": "A briar pipe rests in a ceramic dish.", "examine": "Well-worn. Tooth marks, old tobacco. Cherry and oak. Natural in your hand, but no memory comes."},
    "spectacles": {"name": "Wire-Rimmed Spectacles", "room_desc": "Wire-rimmed spectacles, folded.", "examine": "Round lenses, gold wire. You put them on. Nothing changes. But they feel right."},
    "chess_piece": {"name": "Ivory Chess King", "room_desc": "An ivory chess king on its side.", "examine": "Hand-carved, heavy. A chip on the crown. A pang — fondness? The feeling fades."},
    "thimble": {"name": "Silver Thimble", "room_desc": "A tiny silver thimble.", "examine": "Engraved vines. Not yours. Smaller, patient hands. Warmth."},
    "compass": {"name": "Brass Compass", "room_desc": "A brass compass, glass clouded.", "examine": "The needle stops. Not north. Toward something. It holds steady."},
    "pressed_flower": {"name": "Pressed Orchid", "room_desc": "A pressed orchid between wax paper.", "examine": "Dendrobium nobile. The Latin arrives effortlessly. You know EVERY plant."},
    "photograph": {"name": "Faded Photograph", "room_desc": "A loose photograph, face-down.", "examine": "Men in academic robes. One waves. Something familiar. 'Faculty, Autumn 1921.'"},
    "key": {"name": "Brass Key", "room_desc": "A brass key on a leather fob.", "examine": "Initials rubbed smooth. You try the nearest keyhole. Doesn't fit."},
    "tin_soldier": {"name": "Lead Soldier", "room_desc": "A lead soldier, paint worn bare.", "examine": "Three inches tall. Paint loved off. One arm bent wrong — carefully bent back. Treasured."},
    "pencil_sketch": {"name": "Pencil Sketch", "room_desc": "A pencil sketch on yellowed paper.", "examine": "THIS house. Smoke from the chimney. A figure at an upstairs window. 'Home, Sept. 1919.'"},
    "cufflinks": {"name": "Enamel Cufflinks", "room_desc": "Green enamel cufflinks in a box.", "examine": "Tiny fern fronds. Custom work for a botanist. Important enough to keep."},
    "candle_stub": {"name": "Candle Stub", "room_desc": "A half-burned candle.", "examine": "Wick pinched, not blown. Someone stopped working by candlelight. A careful habit."},
    "recipe_card": {"name": "Handwritten Recipe", "room_desc": "A stained recipe card.", "examine": "'Mother Wren's Blackberry Tart.' Below: 'Elias says add more sugar. Elias is wrong.' You smile."},
    "magnifying_lens": {"name": "Magnifying Lens", "room_desc": "A magnifying lens, brass tarnished.", "examine": "The room leaps into painful detail. Every crack, every mote. You lower it."},
    "sheet_music": {"name": "Sheet Music", "room_desc": "Sheet music, rusted clip.", "examine": "'Clair de Lune.' Annotated — 'M's favorite part.' Practiced often."},
    "bird_skull": {"name": "Small Bird Skull", "room_desc": "A tiny skull on cotton wool.", "examine": "Sparrow. Passer domesticus. A naturalist's care. Beauty in small bones."},
    "garden_trowel": {"name": "Garden Trowel", "room_desc": "A trowel, blade crusted.", "examine": "Your hand knows exactly how to hold it. Muscle memory."},
    "medicine_bottle": {"name": "Brown Glass Bottle", "room_desc": "A brown glass bottle, label peeling.", "examine": "'Dr. Hartley's Cardiac Tonic — twice daily.' Nearly empty. Heart medicine. You feel nothing at all."},
    "iron_key": {"name": "Blackened Iron Key", "room_desc": "A blackened iron key lies here, heavy for its size.", "examine": "Heavy, dark iron. Not a house key — something more deliberate. A safe, or a strongbox. Whatever this opens was meant to stay closed. You turn it in your fingers and feel a reluctance you can't explain. Part of you doesn't want to know."},
}

# ──────────────────────────── ROOMS ──────────────────────────────

RP = {
    "foyer": {"name": "The Foyer", "floor": "ground", "required": True,
        "description": "A once-handsome entrance hall. Wallpaper peels in long strips. A chandelier overhead, crystals clouded. The front door is swollen shut.",
        "ambient": ["You try the front door. Won't budge.", "A wool overcoat on the rack. It would fit you.", "You knew where the staircase was before you saw it.", "Same pale light. What time is it?", "No sounds from outside. Nothing."],
        "decay": ["Wallpaper worse. Whole sheets on the floor, dark plaster exposed.", "Ceiling plaster fallen. Lath above, like ribs.", "A chandelier crystal has fallen and shattered."]},
    "parlor": {"name": "The Parlor", "floor": "ground",
        "description": "Two armchairs face a cold fireplace, chess game mid-play. Bookshelves. A portrait: man, woman, small boy.",
        "ambient": ["The man in the portrait. Something about his jaw.", "The left armchair fits naturally.", "Books: mostly botany.", "White was three moves from checkmate.", "You pull 'Flora of the British Isles' without looking."],
        "decay": ["The portrait darker. Faces harder to see.", "One armchair collapsed. Upholstery split.", "Books fallen. Pages scattered like dead leaves."]},
    "dining_room": {"name": "The Dining Room", "floor": "ground",
        "description": "A long table set for four. Tarnished silverware. A candelabra melted to stubs.",
        "ambient": ["Four settings.", "A napkin swan at the smallest place.", "Tarnished silver. Cared about.", "A crack you knew before looking.", "Dust undisturbed."],
        "decay": ["A glass toppled. Nothing touched it.", "Table warped. Plates slide toward center.", "Candelabra tipped. Frozen wax flood."]},
    "kitchen": {"name": "The Kitchen", "floor": "ground",
        "description": "Copper pots, cast-iron stove, stone sink. Faint rosemary.",
        "ambient": ["Calendar: October 1923. Heart on the 14th.", "Herb smell comes and goes.", "A teacup. Someone's last cup.", "Cupboard by instinct.", "Same flat sky."],
        "decay": ["Herb smell gone. Dust and rust.", "A pot fallen. House swallowed the sound.", "Stove rusted through."]},
    "cellar": {"name": "The Cellar", "floor": "ground",
        "description": "Cool, low. Damp earth. Wine racks — few bottles survive.",
        "ambient": ["'Bordeaux 1908.' Took wine seriously.", "Mineral cold.", "Height marks: 'T.W. — age 3.' Stops at 5.", "T.W. Thomas Wren?", "Quiet down here."],
        "decay": ["More bottles fallen. Stain spreading.", "Height marks crumbling.", "Water seeping through mortar."]},
    "conservatory": {"name": "The Conservatory", "floor": "ground",
        "description": "Glass walls, most cracked. Dead ferns on wrought-iron stands. A potting bench.",
        "ambient": ["Plant stands labeled in Latin.", "One fern survives. Stubborn.", "Soil under your fingernails. Wait — clean.", "Broken glass underfoot.", "Rusted watering can."],
        "decay": ["The fern has browned. Even stubbornness has limits.", "More panes fallen. More outside than inside.", "Potting bench collapsed."]},
    "library": {"name": "The Library", "floor": "ground",
        "description": "Floor-to-ceiling shelves. Leather chair. Old paper and binding glue.",
        "ambient": ["Botany, taxonomy, orchids.", "Bookmark halfway through alpine pollination.", "Chair fits like yours.", "'Royal Botanical Society.' 1920-1923.", "Penciled notes. Yours."],
        "decay": ["Books swelling with damp.", "Leather chair splitting.", "A shelf buckled. Cairn of knowledge."]},
    "pantry": {"name": "The Pantry", "floor": "ground",
        "description": "Narrow room. Mason jars, tins. Labels peeled.",
        "ambient": ["Crystallized honey.", "'Blackberry 1922.'", "Tea tin without looking.", "Flour crust.", "Hands-on household."],
        "decay": ["A jar cracked. Dark preserves leak.", "Shelves sagging.", "Half the jars broken. Vinegar and time."]},
    "wash_room": {"name": "The Wash Room", "floor": "ground",
        "description": "Stone basin, washboard, mangle. Rope lines overhead, empty.",
        "ambient": ["Folded linens, yellowed.", "Washboard worn smooth.", "Two aprons — large and small.", "Harsh soap, cracked.", "Working household."],
        "decay": ["A rope snapped, dangling.", "Washboard split.", "Mangle frozen. Never again."]},
    "upstairs_hall": {"name": "The Upstairs Hallway", "floor": "upper", "required": True,
        "description": "Long hallway, closed doors. Carpet worn thin. Faded photographs.",
        "ambient": ["Photographs ghosted by light.", "Carpet worn. Thousands of trips.", "Mirror at the end, clouded.", "Your feet fit the worn path.", "The light hasn't changed."],
        "decay": ["A photograph fallen. Glass cracked across the face.", "Carpet disintegrating. Threads trail behind.", "A door swollen open. Beyond: shadow."]},
    "bedroom": {"name": "The Master Bedroom", "floor": "upper",
        "description": "Four-poster bed, canopy threadbare. Left side pulled back. Vanity with hairbrush and dried flower.",
        "ambient": ["Left side slept in. Long time.", "Shawl on bedpost. Lavender.", "Wedding portrait. Groom might be you.", "You know which drawer. Left.", "Primula vulgaris. You know."],
        "decay": ["Canopy in strips like shed skin.", "Dried flower crumbled to powder.", "Mattress sagged in. No one will sleep here."]},
    "study": {"name": "The Study", "floor": "upper",
        "description": "Most lived-in room. Books, specimen jars. Desk under drawn curtains. Chair pushed back at an angle.",
        "ambient": ["Old paper, dried flowers. At ease.", "Chair at an odd angle.", "Every jar recognized before reading.", "Chair fits. Your hands.", "Red train drawing. 'For Papa.'"],
        "decay": ["Specimen jar cracked. Flower curling in air.", "Desk warping. Papers sliding.", "Curtains rotted. Window shows nothing."]},
    "nursery": {"name": "The Nursery", "floor": "upper",
        "description": "Faded blue. Crib, rocking chair. Blocks, one-eyed bear, tin soldiers.",
        "ambient": ["Hours watching a child sleep.", "Tin soldiers in formation.", "The bear. One eye. Chest tight.", "Music box — three notes.", "Thomas's room."],
        "decay": ["Blue paint flaking to bone-colored plaster.", "Bear slumped. Eye stares at floor.", "Crib collapsed. Gently, as if it laid itself down."]},
    "guest_room": {"name": "The Guest Room", "floor": "upper",
        "description": "Single iron bed. Washstand. Sterile tidiness.",
        "ambient": ["Hospital corners.", "Guest book: September 1923.", "Hangers chime.", "Unchanging sky.", "Doesn't feel yours."],
        "decay": ["Bedspread yellowed further.", "Basin cracked. Irreversible.", "Dust on the hospital corners."]},
    "sewing_room": {"name": "The Sewing Room", "floor": "upper",
        "description": "Treadle sewing machine. Mannequin in unfinished fabric. Spools of thread.",
        "ambient": ["Child's coat, half-finished.", "Basket of mending.", "Margaret's room. Certain.", "Spools by color.", "Thimble on the sill."],
        "decay": ["Coat faded. See-through.", "Thread spools unraveled. Tangled.", "Needle rusted into plate. Frozen mid-stitch."]},
    "bathroom": {"name": "The Bathroom", "floor": "upper",
        "description": "Claw-foot tub. Pedestal sink. Medicine cabinet ajar. Cracked tile.",
        "ambient": ["Brown bottles. Tinctures.", "Straight razor. Ivory.", "Mirror at a bad angle. Wall behind, not yourself.", "Dried soap.", "Mineral ring. Hard water."],
        "decay": ["Mirror cracked. Non-reflection in two pieces.", "Tiles shifting like teeth.", "Enamel peeling. Yellow flakes."]},
    "attic": {"name": "The Attic", "floor": "upper",
        "description": "Under the eaves. Trunks, hatboxes, dust cloths. Cobwebs. Round window, disc of grey.",
        "ambient": ["Letters tied with ribbon. Too faded.", "Cradle, older than the crib.", "Rocking horse, cracked eye.", "Bowler hat. Fits exactly.", "Grey sky. No trees. Just grey."],
        "decay": ["A rafter cracked. Ceiling sagging.", "Dust cloths disintegrating.", "Round window darker. Grey pressing in."]},
}

DK_ARR = ["Temperature drops. All at once. Shadows are DEEP. Moving.",
          "Heaviness settles. Light gutters like a candle.",
          "Something here. Room smaller. Air resists you."]
DK_ESC = {2: ["Darkness closer. You FEEL it — on your memories.",
              "Can't remember which direction. Darkness between you and details.",
              "Something pulls. Not body — NAME. Fraying."],
          1: ["Darkness has a voice. Forgetting itself. You are nothing.",
              "Dissolving. Mother. Margaret. Thomas. Going dark.",
              "Truly forgotten. Not by others — by yourself."]}
DK_NEAR = ["A chill. Not winter — less natural.",
           "Light thinner. Shadows too dark.",
           "A pull toward one exit. Or away from something.",
           "Air has weight. Nearby, something wrong."]
DK_BAN = ["Lullaby comes out. Fragile — but real. Three notes rising, three falling.\n\n  The darkness FLINCHES. Recoils. Shadows peel back, pressure lifts. Your mother, behind you. \"My little sparrow.\"\n\n  She's gone. But the darkness is gone too.",
          "The lullaby rises before you think. Three up, three down.\n\n  Darkness shudders. Contracts. Pulls away like oil from water.\n\n  Melody fades. Warmth stays."]
DK_NO = ["You try to hum. Nothing comes.", "No melody. Darkness presses closer.", "Only void where music should be."]

# ──────────────────── MAP GENERATION ─────────────────────────────

def generate_house():
    gR = [k for k, v in RP.items() if v["floor"] == "ground" and v.get("required")]
    gO = [k for k, v in RP.items() if v["floor"] == "ground" and not v.get("required")]
    uR = [k for k, v in RP.items() if v["floor"] == "upper" and v.get("required")]
    uO = [k for k, v in RP.items() if v["floor"] == "upper" and not v.get("required")]
    random.shuffle(gO); random.shuffle(uO)
    ground = gR + gO[:random.randint(3, 4)]
    upper = uR + uO[:random.randint(3, 5)]
    all_ids = ground + upper
    rooms = {}
    for rid in all_ids:
        t = RP[rid]
        rooms[rid] = {"name": t["name"], "floor": t["floor"], "description": t["description"],
            "ambient": list(t["ambient"]), "decay": list(t.get("decay", [])),
            "exits": {}, "items": [], "first_visit": True, "visits": 0}
    dirs = ["north", "south", "east", "west"]
    def conn(rd, rl):
        if len(rl) <= 1: return
        random.shuffle(rl); co = [rl[0]]; rem = list(rl[1:])
        while rem:
            nr = rem.pop(0); cands = list(co); random.shuffle(cands)
            for p in cands:
                ap = [d for d in dirs if d not in rd[p]["exits"]]
                an = [d for d in dirs if d not in rd[nr]["exits"]]
                for d in ap:
                    o = OPP[d]
                    if o in an:
                        rd[p]["exits"][d] = nr; rd[nr]["exits"][o] = p; break
                else: continue
                break
            co.append(nr)
        for _ in range(30):
            pair = random.sample(rl, 2); a, b = pair
            if b in rd[a]["exits"].values(): continue
            af = [d for d in dirs if d not in rd[a]["exits"]]
            bf = [d for d in dirs if d not in rd[b]["exits"]]
            for d in af:
                if OPP[d] in bf:
                    rd[a]["exits"][d] = b; rd[b]["exits"][OPP[d]] = a; return
    conn(rooms, ground); conn(rooms, upper)
    for sp in random.sample(dirs, len(dirs)):
        o = OPP[sp]
        if sp not in rooms["foyer"]["exits"] and o not in rooms["upstairs_hall"]["exits"]:
            rooms["foyer"]["exits"][sp] = "upstairs_hall"; rooms["upstairs_hall"]["exits"][o] = "foyer"; break
    vis = set(); q = deque(["foyer"])
    while q:
        r = q.popleft()
        if r in vis: continue
        vis.add(r)
        for nb in rooms[r]["exits"].values():
            if nb not in vis: q.append(nb)
    for ur in set(all_ids) - vis:
        for vr in vis:
            vf = [d for d in dirs if d not in rooms[vr]["exits"]]
            uf = [d for d in dirs if d not in rooms[ur]["exits"]]
            for d in vf:
                if OPP[d] in uf:
                    rooms[vr]["exits"][d] = ur; rooms[ur]["exits"][OPP[d]] = vr; vis.add(ur); break
            if ur in vis: break
    ai = {}; ai.update(MEM); ai.update(FLAV)
    el = [r for r in all_ids if r != "foyer"]; random.shuffle(el)
    # Place normal memory artifacts (excluding fathers_letter — it lives in the safe)
    mk = [k for k in MEM.keys() if k != "fathers_letter"]; random.shuffle(mk); tg = list(el)
    for m in mk: rooms[tg.pop(0)]["items"].append(m)
    # Place iron_key (always present, never in same room as safe)
    safe_room = random.choice([r for r in el if not rooms[r]["items"]])
    key_candidates = [r for r in el if r != safe_room]
    iron_key_room = random.choice(key_candidates)
    rooms[iron_key_room]["items"].append("iron_key")
    # Place other flavor objects
    fk = [k for k in FLAV.keys() if k != "iron_key"]; random.shuffle(fk)
    nf = random.randint(6, min(9, len(fk))); fe = list(el); random.shuffle(fe)
    for i in range(nf): rooms[fe[i % len(fe)]]["items"].append(fk[i])
    return rooms, all_ids, ai, safe_room

# ────────────────────── GAME STATE ───────────────────────────────

class GS:
    def __init__(self):
        self.rc = 0; self.traces = []; self.tm = 0; self._iw()
    def _iw(self):
        self.rooms, self.ids, self.ai, self.safe_room = generate_house()
        self.safe_opened = False
        self.cr = "foyer"; self.inv = []; self.mu = []; self.mv = 0; self.go = False
        el = [r for r in self.ids if r != "foyer"]
        self.dr = random.choice(el)
        self.dt = max(4, 6 - self.rc) + random.randint(0, 2)
        self.met = max(2, 3 - self.rc // 2)
        self.et = 0; self.da = True; self.dbu = 0
        if self.traces:
            tr = list(el); random.shuffle(tr)
            for i, t in enumerate(self.traces[:3]):
                self.rooms[tr[i]]["ambient"].append(t)
    def reset(self):
        self.rc += 1; nt = []
        t = list(TRACE_TEMPLATES); random.shuffle(t)
        nt.append(t[0].replace("{n}", str(self.rc)))
        if self.mu:
            tag = self.ai[self.mu[-1]]["memory_tag"].split("—")[0].strip()
            nt.append(f'A scrap of paper in your handwriting: "{tag}." Means nothing now.')
        self.traces = nt; self._iw()
    @property
    def mc(self): return len(self.mu)
    @property
    def ta(self): return len(MEM)
    def hi(self, k): return k in self.inv
    def hm(self, k): return k in self.mu
    def hl(self): return "locket" in self.mu
    def iid(self): return self.da and self.cr == self.dr
    def idn(self): return self.da and self.dr in self.rooms[self.cr]["exits"].values()
    def gcl(self):
        if not self.da: return 0
        if self.iid(): return 3 if self.et <= 1 else 2
        return 1 if self.idn() else 0
    def md(self):
        ha = [r for r in self.ids if r != "foyer" and r != self.cr
              and any(self.ai[i].get("is_memory") and not self.hi(i) for i in self.rooms[r]["items"])]
        el = [r for r in self.ids if r != "foyer" and r != self.cr and r != self.dr]
        if ha and random.random() < 0.6: self.dr = random.choice(ha)
        elif el: self.dr = random.choice(el)
        self.dt = max(4, 6 - self.rc) + random.randint(0, 2); self.et = 0
    def td(self):
        if not self.da:
            if self.mv >= self.dbu:
                self.da = True
                el = [r for r in self.ids if r != "foyer" and r != self.cr]
                if el: self.dr = random.choice(el)
                self.dt = max(4, 6 - self.rc) + random.randint(0, 2)
            return None
        self.dt -= 1
        if self.dt <= 0 and not self.iid(): self.md()
        if self.iid():
            if self.et == 0: self.et = self.met; return "arr"
            self.et -= 1; return "con" if self.et <= 0 else "esc"
        self.et = 0; return "near" if self.idn() else None

def fi(txt, ai):
    txt = txt.lower().strip()
    if txt in ai: return txt
    for k, it in ai.items():
        if txt in it["name"].lower() or txt in k: return k
    for k, it in ai.items():
        for w in txt.split():
            if len(w) > 2 and (w in it["name"].lower() or w == k): return k
    return None

# ────────────────────── ENGINE ───────────────────────────────────

def desc_room(s):
    rm = s.rooms[s.cr]; rm["visits"] += 1; cl = s.gcl()
    print(); print_boxed(rm["name"]); print()
    d = corrupt_text(rm["description"], cl) if cl > 0 else rm["description"]
    for l in textwrap.wrap(d, width=TERM_WIDTH): print(f"  {l}")
    if rm["decay"] and rm["visits"] >= 3:
        di = min((rm["visits"] - 3) // 2, len(rm["decay"]) - 1)
        print(); print(f"  {rm['decay'][di]}")
    uc = [k for k in rm["items"] if not s.hi(k)]
    if uc:
        print()
        for ik in uc:
            rd = s.ai[ik]["room_desc"]
            if cl > 0: rd = corrupt_text(rd, cl)
            print(f"  {rd}")
    # Show safe if this is the safe room
    if s.cr == s.safe_room:
        print()
        if s.safe_opened:
            if not s.hi("fathers_letter"):
                print("  The iron strongbox sits open. Inside: a single yellowed letter.")
            else:
                print("  The iron strongbox sits open and empty.")
        else:
            safe_desc = "An iron strongbox sits in the corner, its lock crusted with age but solid. Whatever is inside was meant to stay private."
            if cl > 0: safe_desc = corrupt_text(safe_desc, cl)
            print(f"  {safe_desc}")
    pts = []
    for d2, rid in rm["exits"].items():
        tg = s.rooms[rid]
        st = " ↑stairs" if rm["floor"] != tg["floor"] and rm["floor"] == "ground" else (" ↓stairs" if rm["floor"] != tg["floor"] else "")
        pts.append(f"{d2.upper()}{st} ({tg['name']})")
    print(); print(f"  Exits: {', '.join(pts)}")
    if not rm["first_visit"]:
        amb = random.choice(rm["ambient"])
        if cl > 0: amb = corrupt_text(amb, cl)
        print(f"\n  {amb}")
        if random.random() < 0.1: print(f"\n  {get_clock_ambient()}")
    if rm["first_visit"]:
        print(random.choice(SND_DRONE_G if rm["floor"] == "ground" else SND_DRONE_U))
    rm["first_visit"] = False

def do_mv(s, d):
    d = DSH.get(d, d)
    if d not in ("north", "south", "east", "west"): print("\n  Not a direction."); return False
    rm = s.rooms[s.cr]
    if d not in rm["exits"]: print("\n  Nothing that way."); return False
    of = rm["floor"]; s.cr = rm["exits"][d]; nf = s.rooms[s.cr]["floor"]; s.et = 0
    if of != nf: print("\n  " + random.choice(["You climb the stairs.", "You head upstairs."] if nf == "upper" else ["You descend.", "You head downstairs."]))
    else: print("\n  " + random.choice(["You walk through.", "You step in.", "You head onward.", "Quiet footsteps."]))
    desc_room(s); return True

def do_tk(s, txt):
    k = fi(txt, s.ai); rm = s.rooms[s.cr]
    if not k: print("\n  Nothing by that name."); return
    if k not in rm["items"]: print("\n  Not here."); return
    if s.hi(k): print("\n  Already have it."); return
    s.inv.append(k); print(f"\n  You pick up the {s.ai[k]['name']}.\n  Acquired: {s.ai[k]['name']}")

def do_ex(s, txt):
    # Check for safe/strongbox examination
    if txt.lower().strip() in ("safe", "strongbox", "box", "lockbox"):
        do_open_safe(s); return
    k = fi(txt, s.ai)
    if not k: print("\n  Examine what?"); return
    if not s.hi(k):
        if k in s.rooms[s.cr]["items"]: print(f"\n  Pick it up first. Try: take {k}")
        else: print("\n  Don't have that.")
        return
    it = s.ai[k]; print(); print_separator("·")
    for l in textwrap.wrap(it["examine"], width=TERM_WIDTH): print(f"  {l}")
    if it.get("is_memory") and not s.hm(k):
        s.mu.append(k); dramatic_pause(1.0); print(); print(SND_MEMORY); print()
        print_separator("✦"); print()
        print("  ░░░  M E M O R Y   R E C O V E R E D  ░░░"); print()
        slow_print(f"  {it['memory']}", delay=0.025); print()
        print(f"  ▸ {it['memory_tag']}"); print(f"  ▸ Memories: {s.mc}/{s.ta}")
        if k == "locket": print("\n  ▸ You learned the lullaby. You can HUM it now.")
        print(); print_separator("✦")
        if s.mc == 3: dramatic_pause(0.8); print(); slow_print("  Elias Wren. Professor. Husband. The house is YOURS. Why can't you remember leaving?", delay=0.025)
        if s.mc == 4: dramatic_pause(0.8); print(); slow_print("  A mother, a career, a wife, a son. What happened to Elias Wren?", delay=0.025)
        if s.mc == 5:
            dramatic_pause(0.8); print()
            slow_print("  Not all memories are kind. Some cut. But they're yours — every one of them. The greenhouse AND the closed door. The wedding AND the silence. You can't choose which parts of yourself to remember.", delay=0.025)
        if s.mc == s.ta: finale(s)
    elif it.get("is_memory"): print("\n  Memory vivid already.")
    else: print("\n  No memories stir. But it feels important.")

def do_open_safe(s):
    """Handle opening the strongbox."""
    if s.cr != s.safe_room:
        print("\n  There's no safe here.")
        return
    if s.safe_opened:
        print("\n  The strongbox is already open.")
        return
    if not s.hi("iron_key"):
        print()
        slow_print(
            "  The strongbox is locked. The lock is old iron — heavy, unyielding. "
            "You'd need a key. A substantial one, made for exactly this kind of lock.",
            delay=0.025,
        )
        return
    # Open with key
    print()
    print_separator("·")
    slow_print(
        "  You press the iron key into the lock. It resists — then turns with "
        "a grinding click that echoes through the room. The lid swings open on "
        "rusted hinges.",
        delay=0.025,
    )
    dramatic_pause(0.8)
    print()
    slow_print(
        "  Inside the strongbox: a single folded letter, its paper brittle and "
        "yellowed. Nothing else. Whatever was worth locking away, it was this.",
        delay=0.025,
    )
    print()
    slow_print(
        "  You feel a coldness that has nothing to do with the room. Part of you "
        "knew this was here. Part of you locked it away on purpose.",
        delay=0.025,
    )
    print_separator("·")
    s.safe_opened = True
    s.rooms[s.safe_room]["items"].append("fathers_letter")
    print("\n  The letter is here for the taking. If you want it.")

def do_hum(s):
    if not s.hl(): print(f"\n  {random.choice(DK_NO)}"); return
    if s.iid():
        print(); print(SND_BANISH); dramatic_pause(0.5)
        slow_print(f"  {random.choice(DK_BAN)}", delay=0.02)
        s.da = False; s.dbu = s.mv + random.randint(8, 14); s.et = 0
    else:
        print(); print(SND_LULLABY)
        print("\n  You hum the lullaby. The melody fills the room. Company.")
        if s.idn(): print("\n  Somewhere close, something recoils."); s.md()

def do_inv(s):
    print(); print_separator()
    if not s.inv: print("  Not carrying anything.")
    else:
        print("  You are carrying:"); cl = s.gcl()
        for k in s.inv:
            nm = s.ai[k]["name"]
            if cl >= 2 and random.random() < 0.3:
                nm = " ".join("—" * len(w) if random.random() < 0.4 else w for w in nm.split())
            m = " ✦" if k in s.mu else (" (not examined)" if s.ai[k].get("is_memory") else "")
            print(f"    • {nm}{m}")
    print_separator()

def do_mem(s):
    print(); print_separator("✦")
    if not s.mu: print("  Nothing. Must have been someone.")
    else:
        print("  W H A T   Y O U   R E M E M B E R:"); print()
        for k in s.mu: print(f"    ✦ {s.ai[k]['memory_tag']}")
        r = s.ta - s.mc
        if r > 0: print(f"\n  {r} fragment{'s' if r != 1 else ''} still missing...")
    print_separator("✦")

def do_map(s):
    print(); print_separator(); print("  R O O M S   V I S I T E D:"); print()
    for rid in s.ids:
        rm = s.rooms[rid]
        if not rm["first_visit"] or rid == s.cr:
            h = " ◄" if rid == s.cr else ""
            uc = [k for k in rm["items"] if not s.hi(k)]
            n = f" [{len(uc)}]" if uc else ""
            f = "▲" if rm["floor"] == "upper" else "▼"
            print(f"    {f} {rm['name']}{n}{h}")
    print(); print("  ▲ upper  ▼ ground"); print_separator()

def do_whisper():
    print(); print_separator("·"); print()
    slow_print("  You lean close to the wall and whisper.", delay=0.025)
    dramatic_pause(0.5); print()
    slow_print("  For a moment, nothing. Then — from beyond the wallpaper, beyond the plaster, beyond the house — a voice whispers back. Not Elias. Not Margaret. Someone who built these walls from words.", delay=0.025)
    print(); print('  "This story was crafted by Michael B. Parks.')
    print("  Visit him at https://michaelbparks.com"); print()
    print('  Thank you for listening."'); print(); print_separator("·")

def hde(s, ev):
    if ev == "arr":
        print(); print(SND_DK_RUMBLE[0]); print_separator("░")
        slow_print(f"\n  {random.choice(DK_ARR)}", delay=0.02); print()
        print(f"  {s.et} moment{'s' if s.et != 1 else ''}. " + ("HUM or RUN." if s.hl() else "LEAVE. NOW."))
        print_separator("░"); return False
    if ev == "esc":
        ix = min(s.met - s.et, len(SND_DK_RUMBLE) - 1); print(); print(SND_DK_RUMBLE[ix])
        ms = DK_ESC.get(s.et, DK_ESC[1]); print_separator("░")
        slow_print(f"\n  {random.choice(ms)}", delay=0.02); print()
        if s.et == 1: print("  Last chance. " + ("HUM or LEAVE." if s.hl() else "RUN."))
        else: print(f"  {s.et} left.")
        print_separator("░"); return False
    if ev == "con":
        print(); print(SND_DK_RUMBLE[-1]); print_separator("░"); print()
        slow_print("  The darkness reaches you.", delay=0.03); dramatic_pause(1.0); print()
        slow_print("  It doesn't hurt. That's the worst part. Memories unspool. One by one.", delay=0.025)
        dramatic_pause(0.8); print()
        for line in ["  You forget your son's name.", "  You forget your wife's face.",
                     "  You forget your mother's song.", "  You forget that you forgot."]:
            slow_print(line, delay=0.035); dramatic_pause(0.6)
        print(); slow_print("  And then...", delay=0.08); print()
        print_separator("░"); return True
    if ev == "near": print(f"\n  {random.choice(DK_NEAR)}"); return False
    return False

def finale(s):
    dramatic_pause(2.0); clear_screen(); print(); print_separator("═"); print()
    slow_print("  Margaret's letter. A third time, slower.", delay=0.03); dramatic_pause(0.8); print()
    for line in ['"It has been a year."', '"I\'ve kept the study exactly as you left it."', '"I hope wherever you are, you can hear me."']:
        slow_print(f"  {line}", delay=0.035); dramatic_pause(0.6)
    dramatic_pause(1.5); print()
    slow_print("  You told yourself she was writing to someone on a trip.", delay=0.025); dramatic_pause(0.8)
    slow_print('  But people on trips come home. Margaret said "wherever you are."', delay=0.025); dramatic_pause(1.0)
    slow_print("  Those aren't words for someone who's coming back.", delay=0.03); dramatic_pause(2.0)
    print(); print_separator(); print()
    slow_print("  The watch. Cracked crystal. You never asked what cracked it.", delay=0.025); dramatic_pause(0.8)
    slow_print("  It cracks when it hits a desk. When someone falls forward.", delay=0.03); dramatic_pause(1.2); print()
    slow_print("  The study. Chair at that angle. You thought someone stood up.", delay=0.025); dramatic_pause(0.8)
    slow_print("  Nobody stood up.", delay=0.04); dramatic_pause(2.0)
    print(); print_separator(); print()
    slow_print("  You walk to the nearest mirror. Wipe it clean.", delay=0.025); dramatic_pause(0.8)
    slow_print("  The room is reflected perfectly. Where you stand, there is nothing.", delay=0.025); dramatic_pause(2.5)
    # ─── INTERACTIVE TWIST ───
    print(); print_separator("✦"); print()
    slow_print("  You understand now. Don't you?", delay=0.03); dramatic_pause(1.5)
    print("\n  What happened to Elias Wren?\n")
    answer = input("  > ").strip()
    understood = bool(re.search(r'\b(die[ds]?|dead|death|kill|ghost|spirit|passed|gone|heart|buried|never\s*left)\b', answer, re.IGNORECASE))
    print(); print(SND_FINALE); dramatic_pause(1.0)
    if understood: slow_print("  Yes.", delay=0.05); dramatic_pause(1.5); print()
    else: slow_print("  You don't want to say it. So the house says it for you.", delay=0.03); dramatic_pause(1.5); print()
    print_separator("✦"); print()
    for line in ["  Your name was Elias Wren.", "  Professor of botany at Ashworth University.",
                 "  You married Margaret on an October evening in 1911.", "  Your son Thomas had your eyes and her laugh."]:
        slow_print(line, delay=0.04); dramatic_pause(0.6)
    print()
    slow_print("  Your father Robert never forgave you for leaving the farm.", delay=0.035); dramatic_pause(0.6)
    slow_print("  He died in 1919 without another word between you.", delay=0.035); dramatic_pause(0.6)
    slow_print("  You kept his letter in a locked box because you couldn't read it again.", delay=0.035); dramatic_pause(0.6)
    slow_print("  And you couldn't throw it away.", delay=0.04); dramatic_pause(1.0)
    print(); slow_print("  On November 2nd, 1923, working late. A tightness in your chest. Watch struck the desk.", delay=0.03); dramatic_pause(0.8)
    slow_print("  11:47 PM.", delay=0.05); dramatic_pause(1.2)
    slow_print("  Margaret found you the next morning. She never moved a single paper.", delay=0.03); dramatic_pause(2.0)
    print(); print_separator("✦"); print()
    slow_print("  The front door. The light. The silence.", delay=0.025); dramatic_pause(0.8); print()
    slow_print("  The house isn't abandoned. The house is all that's left.", delay=0.03); dramatic_pause(1.2)
    slow_print("  You didn't find this place. You never left it.", delay=0.03); dramatic_pause(1.5)
    if s.rc > 0:
        print(); slow_print(f"  You have been here since 11:47 PM on November 2nd, 1923. The darkness swallowed you {s.rc} time{'s' if s.rc != 1 else ''} — it was forgetting. Every time, the house reshuffled. But you came back. Always.", delay=0.02)
    else: slow_print("  A hundred years.", delay=0.025)
    dramatic_pause(1.5); print()
    slow_print("  The only reason you couldn't see yourself in the mirror is that there is nothing left to see.", delay=0.03); dramatic_pause(2.0)
    if s.rc > 0:
        print(); slow_print("  The darkness stirs one last time.", delay=0.025); dramatic_pause(0.8)
        slow_print("  But you are Elias Wren. Six memories and a hundred years of stubbornness. Not nothing.", delay=0.025); dramatic_pause(0.8)
        print(); print(SND_LULLABY)
        slow_print("  You hum the lullaby — all of it — and the darkness dissolves like frost in morning sun.", delay=0.025); dramatic_pause(1.2)
    print(); print_separator("═"); print()
    slow_print("  Somewhere, a curtain falls open. Light. Warm, golden, October.", delay=0.025); dramatic_pause(1.2); print()
    if understood:
        slow_print("  Margaret is waiting. She doesn't look surprised.", delay=0.03); dramatic_pause(0.8)
        slow_print('  "I knew you\'d figure it out. You always were the clever one."', delay=0.03)
    else: slow_print('  "There you are," Margaret says. "We\'ve been waiting."', delay=0.035)
    dramatic_pause(1.2); slow_print('  Thomas waves. "Come ON, Papa!"', delay=0.035); dramatic_pause(1.5)
    print()
    slow_print("  And behind them, further back, almost at the edge of the light — a man. Older. Stiff-backed. He doesn't smile. But he's there. He came.", delay=0.025)
    dramatic_pause(1.0)
    slow_print("  Your father lifts his hand. Not a wave. Just an open palm. The closest Robert Wren ever came to saying he was wrong.", delay=0.025)
    dramatic_pause(1.5); print()
    slow_print("  October air. Wood smoke and apples. For the first time in a hundred years, you feel the breeze.", delay=0.025)
    dramatic_pause(0.8); print(); slow_print("  You step through.", delay=0.05); dramatic_pause(2.0)
    print(); print_separator(); print()
    slow_print("  The house stands quiet. The pocket watch reads 11:47.", delay=0.025); dramatic_pause(0.8); print()
    slow_print("  The chair in the study is pushed neatly in.", delay=0.025); dramatic_pause(1.0)
    slow_print("  The strongbox sits open. The letter is gone.", delay=0.025); dramatic_pause(0.5); print()
    slow_print("  The front door swings open. Autumn light floods the foyer.", delay=0.025); dramatic_pause(0.8)
    slow_print("  The house breathes out, long and slow, and is still.", delay=0.03)
    print(); print(); print_separator("═"); print()
    vi = len([r for r in s.rooms.values() if not r["first_visit"]])
    ti = sum(len(r["items"]) for r in s.rooms.values())
    print("              T H E   F O R G O T T E N   O N E"); print()
    print(f"                 Memories: {s.mc}/{s.ta}")
    print(f"                 Items: {len(s.inv)}/{ti}")
    print(f"                 Rooms: {vi}/{len(s.rooms)}")
    print(f"                 Moves: {s.tm}")
    if s.rc > 0: print(f"                 Times consumed: {s.rc}")
    print(f"                 Understood: {'Yes' if understood else 'No'}")
    print(); print("          Thank you for helping Elias remember.")
    print("          Thank you for helping him go home."); print()
    print_separator("═"); print(); s.go = True

def pc(raw):
    parts = raw.split(None, 1)
    if not parts: return None, ""
    cmd, arg = parts[0], parts[1] if len(parts) > 1 else ""
    if cmd in ("n", "s", "e", "w", "north", "south", "east", "west"): return "go", cmd
    al = {"go":"go","move":"go","walk":"go","run":"go","flee":"go","look":"look","l":"look",
        "examine":"examine","x":"examine","inspect":"examine","study":"examine","read":"examine",
        "take":"take","get":"take","grab":"take","pick":"take","hum":"hum","sing":"hum","lullaby":"hum",
        "open":"open","unlock":"open","use":"open",
        "inventory":"inventory","inv":"inventory","i":"inventory",
        "memories":"memories","memory":"memories","remember":"memories",
        "help":"help","?":"help","map":"map","m":"map","quit":"quit","exit":"quit","q":"quit",
        "whisper":"whisper","credits":"whisper","about":"whisper","author":"whisper"}
    return al.get(cmd, cmd), arg

def main():
    clear_screen()
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║            T H E   F O R G O T T E N   O N E             ║
    ║            A game of memory, loss, and truth             ║
    ║                      M.B. Parks                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    input("  Press ENTER to begin...\n")
    s = GS()
    while True:
        clear_screen(); print_separator("═"); print()
        if s.rc == 0:
            slow_print("  You open your eyes.", delay=0.05); dramatic_pause(1.0)
            slow_print("  You're in a house. Old. Dusty. Silent. Familiar.", delay=0.025); print()
            slow_print("  You can't remember anything. But this place feels like home.", delay=0.025); print()
            slow_print("  Maybe there's something here to help you remember.", delay=0.025)
        else:
            slow_print("  You open your eyes.", delay=0.05); dramatic_pause(1.0)
            slow_print("  Different rooms. Rearranged. But the same house.", delay=0.025); print()
            slow_print("  Blank again. Faster this time.", delay=0.025)
        print(); print_separator("═"); print(); print("  Type HELP for commands."); print()
        desc_room(s); wc = False
        while not s.go:
            raw = prompt()
            if not raw: continue
            cmd, arg = pc(raw); acted = True; s.tm += 1
            if cmd == "go": acted = do_mv(s, arg)
            elif cmd == "look": desc_room(s); acted = False
            elif cmd == "examine":
                if arg: do_ex(s, arg)
                else: print("\n  Examine what?"); acted = False
            elif cmd == "take":
                if arg: do_tk(s, arg)
                else: print("\n  Take what?"); acted = False
            elif cmd == "hum": do_hum(s)
            elif cmd == "open": do_open_safe(s)
            elif cmd == "inventory": do_inv(s); acted = False
            elif cmd == "memories": do_mem(s); acted = False
            elif cmd == "map": do_map(s); acted = False
            elif cmd == "help":
                print(); print_separator()
                for c, d in [("go <dir>","Move"),("look","Look"),("take","Take"),("examine","Study"),("hum","Hum"),("inv","Carrying"),("memories","Remember"),("map","Map"),("help","Help")]:
                    print(f"    {c:<12}— {d}")
                print_separator(); acted = False
            elif cmd == "whisper": do_whisper(); acted = False
            elif cmd == "quit": print("\n  The door won't budge."); acted = False
            else: print(f"\n  {random.choice(['Try HELP.', 'Not sure what you mean.', 'Try HELP.'])}"); acted = False
            if s.go: break
            if acted:
                s.mv += 1; ev = s.td()
                if ev:
                    con = hde(s, ev)
                    if con:
                        dramatic_pause(2.0); print()
                        slow_print("  You open your eyes.", delay=0.06)
                        dramatic_pause(2.0); s.reset(); wc = True; break
        if s.go: break
        if not wc: break
    print("  Goodbye.\n")

if __name__ == "__main__":
    main()

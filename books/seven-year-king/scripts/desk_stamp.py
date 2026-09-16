"""Prepend desk front matter to chapter files that lack it. Safe to re-run."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CH = ROOT / "chapters" / "book-1-shadow"

# job = what the chapter is doing in the architecture
# happens = plot beats (scan without prose)
# notes = thought process, locks, provisionals, edit flags
# status = locked-room | sit | thin | gap | draft
# room = named locked room if any

DESK: dict[str, dict] = {
    "ch-00-last-day.md": {
        "status": "locked-room",
        "room": "Prologue",
        "job": "Peek, then hide. Tone-set: sex and battle as twins. Morrígan spends a champion. Reader should read predator; love is not announced.",
        "happens": [
            "Ryan, Sion Mills, last pint, cigarette, call he does not make (mam).",
            "Ford: she is a woman for the first time; three sentences uncollapsed (use / die / want); treaty sex.",
            "Night: triple face (maiden is a trap he refuses); briefing — the feeder, the one thing.",
            "Dawn, Sperrins: proto-warp, many lives, cuts the feeder, taking snaps shut, he goes down.",
            "Crow on the body. Cut: an unnamed man begins to wake (elsewhere).",
        ],
        "notes": "Do not name Horned God. Do not soften on reread. Sex grammar: tonight, morning, watch, bear, go — never stay/mine/harvest. Load-bearing sex should sit 2–5k. Invented incident, not a real atrocity. Champion is not a king. Provisional geography/name in DRAFT-CHOICES.",
    },
    "ch-01-wake.md": {
        "status": "locked-room",
        "room": "Wake",
        "job": "Present-tense cut. Unnamed man. Dream as seed, not exposition. Crow at the edge of the frame only.",
        "happens": [
            "Manchester, damp rented house, agency warehouse, Mark, meal deal.",
            "Dream: warrior and crow, river, breakfast roll — already fading. He does not write it or tell anyone.",
            "Could take a bag on the bus; does not (weapon sheathed).",
            "Crow on the back wall, then Tesco sign. Only a crow.",
        ],
        "notes": "Do not explain the dream. Do not state he is the next champion. Unnamed ≠ uncharactered: dry, class, hunger, funny in small ways. Age 26 provisional. No vampires yet.",
    },
    "ch-02-payday.md": {
        "status": "locked-room",
        "room": "Side-sex / concealment crack",
        "job": "Endangered beat: sex cracks the hiding-spell. Stage 1 — using to feel anything. Sperrins on a bus, unconnected.",
        "happens": [
            "Payday. Club. Sian (24, nurse, not nest).",
            "Taxi, Fallowfield, explicit sex. During orgasm he ENTERs — feels her, the cat, a crow, a river.",
            "Her nosebleeds. 'What did you do.' He leaves. No name given.",
            "Bus: another nosebleed. House of Vale will smell this.",
        ],
        "notes": "Not nest grammar (no mine/stay/keep). Not the Akkarin set-piece. Crow on the sill. BBC Sperrins snippet — seed, do not connect for him.",
    },
    "ch-03-what-finds-him.md": {
        "status": "locked-room",
        "room": "Recruitment",
        "job": "Cairn finds him after the dream/opening. Offer, not kidnap. Nest faces in a kitchen. Readable as urban fantasy.",
        "happens": [
            "Monday dock: Cairn Vale, coat too good, does not steam right. Mark shut down with a look.",
            "Palatine, late on purpose. Priya, tea. Drew 'the hole'. Joss takes his jaw.",
            "Offer: evenings, learn the tap, we take a little until we don't, I will try to say when.",
            "He goes home. Number saved as Vale. He goes back the next evening.",
        ],
        "notes": "No cosmology dump. Vampire is Drew's flourish later; here it is a house. Cairn: useful, not kind. Joss already the bully. Priya already the table.",
    },
    "ch-04-joss.md": {
        "status": "locked-room",
        "room": "Bully crucible",
        "job": "Hannaford/Canavan: he could wreck Joss and does not. Told ≠ yes. Stop-word invented.",
        "happens": [
            "Evenings acquire a shape. Hoodie on a peg.",
            "Thursday hall: Joss, knees, spit, stay until Priya sees.",
            "Priya: that is not yes. Word that stops him — he picks 'kettles'.",
            "Cairn at the door: he will push until you push back or break.",
        ],
        "notes": "Arousal is not a vote. Split bully from kind one (Priya). Do not make Joss the sacrifice later. Kettles must exist before Cairn's set-piece.",
    },
    "ch-05-priya.md": {
        "status": "locked-room",
        "room": "Kind one / asked BIND",
        "job": "Found family starts as objects and a yes that is actually a yes. Priya is the cascade-unbearable one.",
        "happens": [
            "Key on the table. Tesco, milk, mam not lately.",
            "Weather report on Joss (taken badly — not an excuse).",
            "Kitchen: she asks; knife in the spoon drawer; he gives; she stops before she has to.",
            "Pasta. Drew's guest. 'You can be ours without being his.'",
        ],
        "notes": "Asked taking ≠ set-piece. Grammar is not mine/stay. Child in trolley at edge only — no dead-child set-pieces ever.",
    },
    "ch-06-kettles.md": {
        "status": "locked-room",
        "room": "Stop-word honoured",
        "job": "Prove kettles is law, not décor. ENTER named. War unnamed. Needed before Cairn ignores a no.",
        "happens": [
            "Candle lesson: DRAW/ENTER, Fallowfield girl, 'stay in the room'.",
            "Cairn: sire/head of house; love arrived; do not make me kind in the story.",
            "Sunday bathroom: Joss asks; kettles; Joss stops, furious.",
            "Text to Vale: received, honoured, if not you walk.",
        ],
        "notes": "Drew jokes he would ignore it — KEEP-seed, do not let him be the set-piece. Inverse of ch. 16.",
    },
    "ch-07-drew.md": {
        "status": "locked-room",
        "room": "KEEP-seed",
        "job": "Nest sex with ownership grammar. Drew will be the nest enemy-lover who fights to KEEP. Sincere, not sneered.",
        "happens": [
            "Bar, leftovers joke, Sian smell.",
            "His room: stay, mine, sex, then asked blood, stay against the cut.",
            "First sleep in the house (Drew's arm). Crow on the sill, unseen.",
            "Morning: mine / we'll see. Priya's 'Ah.'",
        ],
        "notes": "Vampire loves stay sincere. He fails the losing test later, not the feeling test. Do not collapse Drew with Joss or Priya.",
    },
    "ch-08-the-damp.md": {
        "status": "sit",
        "room": "Old life thinning",
        "job": "Belonging as a bag, not a speech. Sperrins paragraphs still unconnected. Back room.",
        "happens": [
            "Flatmate, hickey, birds in sleep, visit not moving-out.",
            "He googles Sperrins: one dead unnamed, van with a dent. Shoulder wrong.",
            "Priya: back room, sheet. Joss: stray to pet, our little marriage.",
            "First night in the dry. Crow on the hedge. Cairn: tonight you're coming with me.",
        ],
        "notes": "Chip-mug left as hostage. Do not make Ryan a speaking guide via the article.",
    },
    "ch-09-the-mess.md": {
        "status": "locked-room",
        "room": "Useful / other flag unnamed",
        "job": "Show vampire mess vs Vale taste/tactics. He stands behind Cairn. Wanting the open tap.",
        "happens": [
            "Ancoats flat, girl on sofa, tin of tomatoes, phone still playing.",
            "He ENTERs two seconds, her mum not his business, nosebleed.",
            "Cairn shuts it; taxi lie (spiked drink); tin back in the bag.",
            "Canal: other flag, standing stones, good stories — not tonight.",
        ],
        "notes": "Girl lives. Not Book 2 innocent-death room. Stay in the tin. 'Mine' from Cairn = dull/close to true. Breakfast-roll rhyme, do not explain.",
    },
    "ch-10-night-train.md": {
        "status": "locked-room",
        "room": "Crow near-miss",
        "job": "Washer/night-train beat. She looks at him like a time, not a man. He does not follow.",
        "happens": [
            "Late shift, missed tram, Victoria, pasty.",
            "Woman on the platform; air wrong; shoulder; he does not cross.",
            "She takes a train. Crow in the carriage three stops.",
            "Priya: priest-face. He does not tell Cairn. Dream rotting again.",
        ],
        "notes": "Do not warm her. Do not name Morrígan. Presence is not thesis. 'Not tonight' is time-grammar leaking, not a thesis speech.",
    },
    "ch-11-ours.md": {
        "status": "sit",
        "room": "Leaving would hurt",
        "job": "Ours as fact Cairn will defend. Joss must ask. Damp funeral. Table = home starting.",
        "happens": [
            "Pays flatmate, leaves chip-mug, charger stays.",
            "Joss kitchen kiss; Ask; Not tonight is not kettles.",
            "Cairn: close the Sperrins tab; people who wash things in rivers; you're ours.",
            "Sofa floor, plate on the knee, no name in the room.",
        ],
        "notes": "Close enough for set-piece to hurt later. Still under 110k layover test — sit more belonging before DRAW/Deal.",
    },
    "ch-12-habit.md": {
        "status": "sit",
        "room": "BIND as habit / warehouse over",
        "job": "Useful days. Asked taking with Priya, Drew, Cairn. Stone too warm — walk past. Ask forming.",
        "happens": [
            "Hands in the hi-vis. Priya pleased.",
            "Salford tap closed by the other mouth himself.",
            "Churchyard stone; Cairn: other flag's furniture; don't kneel.",
            "Milk at a back door (Priya notices). He almost goes to Joss's door.",
        ],
        "notes": "Antlers not yet. Walking past ≠ kneeling. Joss collecting asks — pay off in ch. 13.",
    },
    "ch-13-ask.md": {
        "status": "locked-room",
        "room": "Voluntary PE",
        "job": "He asks to be held down and means it. Stop exists, is tested, honoured. Aftercare. Inverse of the hall and of Cairn's study.",
        "happens": [
            "Ask on the stairs, house in, Priya hears the word.",
            "Belt, face down, peer cruelty he could walk from.",
            "Kettles mid-scene; Joss stops in him; belt off.",
            "Restart: hands, looking, he comes; water; stay as not-an-order; no name yet.",
        ],
        "notes": "2–5k band. Filthy and human-scale. Do not tidy into romance. Joss fetched water — house law. Cairn: don't be sloppy because you're happy.",
    },
    "ch-14-the-stone.md": {
        "status": "locked-room",
        "room": "Earth-current peek",
        "job": "Other flag as weather report, not conversion. Ruth talks too much. Antlers filed, not hunted.",
        "happens": [
            "Churchyard; Ruth; stone quiet ten years, not this week; Vale-smell.",
            "Milk at the wall. Polite version vs impolite (teeth or antlers).",
            "He tells Cairn. Conversion trick: land found you first.",
            "Candle: cannot feel the stone from the study — relief.",
        ],
        "notes": "Do not make Danu extractive. Do not dump Goddess. Crow: Ruth looks too long. Cairn needs both Joss and him standing.",
    },
    "ch-15-standing.md": {
        "status": "sit",
        "room": "Home as table",
        "job": "Damp buried. Pack named, pub not entered. Name is armour until the house claims one.",
        "happens": [
            "Joss less bored, not kind. Cairn takes asked, twice.",
            "Text: keep the deposit. Funeral of the damp.",
            "Ruth on the corner: pack at the park, pint offer, land isn't a mother who never slapped.",
            "Cairn: stones then stories then a pint then a kneeling then a name. Walking past allowed.",
        ],
        "notes": "He dreams kitchens as well as rivers — how they get you. Set-piece can now hurt. Do not go to the pub yet.",
    },
    "ch-16-the-study.md": {
        "status": "locked-room",
        "room": "Forced scene (once)",
        "job": "Akkarin set-piece. Power stolen; someone else holds the end. Hate and heat. He comes. Both true. Inverse of Joss's ask and of last night.",
        "happens": [
            "Door shut. Rope. Not asking. Kettles is for Joss; this is the war using a kitchen.",
            "BIND on the nerves; ENTER; bird kept even now.",
            "Hand, not fucking. He says no. He spends anyway. Extra beat of the BIND.",
            "Undo. Sorry that is true and does not help. Back room. Kettles to empty air.",
        ],
        "notes": "ONCE. Do not tidy into secretly he wanted it or ruined forever. Do not let Cairn win an argument by pointing at his cock. Morrígan never does this. Aftermath must sit in 17–18. Stone quiets — the door he meant.",
    },
    "ch-17-the-back-room.md": {
        "status": "locked-room",
        "room": "Aftermath sits",
        "job": "Stay in the hour. No joke. No meeting. Distinctions: Joss stopped; Cairn did not; table still a table.",
        "happens": [
            "Priya: water on the floor; did you ask / the word.",
            "Joss: I'll kill him; fetched water; goes to his own room.",
            "Shower, flinch, crow weather, does not cry and does not not-cry.",
            "Dreams the chair. Wakes hate and erection; neither is a vote.",
        ],
        "notes": "No Recovery chapter. Growth later, inside grief of Book 2, not here. He does not leave because leaving would hurt — that is the leash.",
    },
    "ch-18-the-table.md": {
        "status": "locked-room",
        "room": "Still ours / once not a habit",
        "job": "Get up and serve the house. Collar and table both true. Cairn: twice would be a habit.",
        "happens": [
            "Jam too sweet. Candle at nine. Don't talk about me as a tap.",
            "Flinch at stay, at hair, at study door. Asked taking paused a week.",
            "Salford wall, hands, Cairn silent. Ruth: stone quiet is not always kindness.",
            "Sleeps in Joss's bed, no belt; flinch at a wrist; hand comes off.",
            "I'm not leaving. That's the leash. Book 1 still team hunger.",
        ],
        "notes": "Do not jump to exceptional DRAW as recovery. Sit if needed, then weapon, then Deal as last-chapter wedding. Clock un-winked.",
    },
}


def fm_block(d: dict) -> str:
    happens = "\n".join(f"- {h}" for h in d["happens"])
    notes = d["notes"].strip()
    return (
        "---\n"
        f"status: {d['status']}\n"
        f"room: {d.get('room', '')}\n"
        f"job: {d['job']}\n"
        "happens:\n"
        f"{happens}\n"
        "notes: |\n"
        + "".join(f"  {line}\n" if line else "\n" for line in notes.split("\n"))
        + "---\n\n"
    )


def main() -> None:
    n = 0
    for path in sorted(CH.glob("ch-*.md")):
        raw = path.read_text(encoding="utf-8")
        if raw.startswith("---\n"):
            print(f"skip (has desk): {path.name}")
            continue
        spec = DESK.get(path.name)
        if not spec:
            print(f"no spec: {path.name}")
            continue
        path.write_text(fm_block(spec) + raw, encoding="utf-8")
        n += 1
        print(f"stamped {path.name}")
    print(f"stamped {n} files")


if __name__ == "__main__":
    main()

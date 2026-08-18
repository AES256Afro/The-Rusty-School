"""The crew of the UES Magnanimous.

Each entry is a recurring character. The roster page shows a member as
"met" once the learner has cleared any mission that features them
(missions list crew ids), so the crew page fills in as the campaign
progresses rather than dumping everybody on you at once.
"""

CREW = [
    {
        "id": "dubois",
        "name": "Captain Yves Dubois-Okonkwo",
        "role": "Commanding officer",
        "icon": "🧑‍✈️",
        "bio": "Genuinely excellent in a crisis. Cannot chair a meeting. Has strong, "
               "publicly stated views about the coffee replicator, and has now had "
               "them vindicated, which has not helped.",
        "quote": "I am not asking for perfection. I am asking for hot coffee, and I "
                 "have been asking since Tuesday.",
    },
    {
        "id": "raghunathan",
        "name": "Commander Priya Raghunathan",
        "role": "Chief Engineer",
        "icon": "🔧",
        "bio": "Exhausted genius. Communicates in sighs and precise numbers. Has not "
               "taken shore leave since the incident with the plasma manifold, about "
               "which she will not be drawn.",
        "quote": "It is a good first one. That is not a compliment about the problem. "
                 "It is a statement about my afternoon.",
    },
    {
        "id": "skree",
        "name": "Lieutenant Skree",
        "role": "Science officer, of the Vell",
        "icon": "🔬",
        "bio": "Aggressively literal. Does not understand metaphor, idiom, or why you "
               "named a variable temp2. Delivers devastating criticism entirely by "
               "accident and files everything under 'pending long-term observation'.",
        "quote": "You said the lift was 'a bit off'. It is off by exactly one deck at "
                 "every twelfth compartment. That is not 'a bit'. That is a pattern.",
    },
    {
        "id": "tannenbaum",
        "name": "Ensign Bo Tannenbaum",
        "role": "Junior systems officer",
        "icon": "🧑‍💻",
        "bio": "Enthusiastic and dangerously confident. Writes most of the broken code "
               "you will be asked to fix. Everybody likes Bo. This is the problem.",
        "quote": "I already looked at it. I mean, I looked at it. I definitely opened "
                 "the file.",
    },
    {
        "id": "tkala",
        "name": "Chief T'Kala",
        "role": "Security",
        "icon": "🛡️",
        "bio": "Two and a half metres tall, enormously strong, extremely gentle. Keeps a "
               "plant on the bridge. The plant is called Gerald. Gerald is on the duty "
               "roster and has never missed a shift.",
        "quote": "I would like my name back. There is no hurry. I will wait here.",
    },
    {
        "id": "archie",
        "name": "ARCHIE",
        "role": "Ship's computer, and your grader",
        "icon": "🖥️",
        "bio": "Deadpan, faintly disappointed, technically helpful. Reports test "
               "results in character and never lies about whether your code worked. "
               "Never sarcastic about a genuine mistake. Extremely sarcastic about "
               "the Captain.",
        "quote": "I have re-read the specification twice in case I was being unfair. "
                 "I was not.",
        "always": True,
    },
    {
        "id": "gerald",
        "name": "Gerald",
        "role": "Bridge plant (Ficus benjamina)",
        "icon": "🪴",
        "bio": "On the duty roster. Watered on a schedule that is now in the ship's "
               "standing orders. Has outlasted two captains and one entire "
               "reorganisation of the Science division. Does not comment.",
        "quote": "",
        "unlock_note": "Complete the Shakedown Cruise",
        "unlock_id": "bridge-s1m8",
    },
]

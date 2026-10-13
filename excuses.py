"""
All the content for the excuse generator lives here.
Want to add your own jam spot or excuse? Just add it to the lists below.

speed  = typical crawl speed at that spot (km/h)
stuck  = extra minutes you lose just sitting at that spot
fame   = how famous the jam is (0-100). Famous jams = more believable excuses.
"""

HOTSPOTS = {
    "Silk Board Junction": {
        "emoji": "🐢",
        "speed": 5,
        "stuck": 25,
        "fame": 99,
        "lines": [
            "I'm stuck at Silk Board. I've been here so long the traffic cop and I are now on first-name basis.",
            "Silk Board signal went green, red and green again. We moved one car length.",
            "I've accepted that Silk Board is where I live now. Please forward my mail here.",
        ],
    },
    "Outer Ring Road (Marathahalli)": {
        "emoji": "🅿️",
        "speed": 8,
        "stuck": 20,
        "fame": 92,
        "lines": [
            "Marathahalli bridge is fully jammed. I can see the office. I just can't reach it.",
            "ORR is basically a parking lot with lane markings right now.",
            "I've been on ORR long enough to finish a podcast, two calls and half my life plans.",
        ],
    },
    "Hebbal Flyover": {
        "emoji": "✈️",
        "speed": 9,
        "stuck": 18,
        "fame": 90,
        "lines": [
            "Hebbal flyover is jammed. Airport traffic and everyone else decided to leave at the same time.",
            "I'm on Hebbal flyover. Lovely view of the lake. Zero movement.",
        ],
    },
    "KR Puram (Tin Factory)": {
        "emoji": "🏭",
        "speed": 7,
        "stuck": 20,
        "fame": 88,
        "lines": [
            "Tin Factory is doing Tin Factory things. Nothing has moved in 15 minutes.",
            "Stuck near KR Puram. A bus, an auto and a water tanker are in a three-way standoff.",
        ],
    },
    "Bellandur / Sarjapur Road": {
        "emoji": "🕳️",
        "speed": 7,
        "stuck": 20,
        "fame": 86,
        "lines": [
            "Sarjapur Road has potholes so deep I think I saw a fish.",
            "Bellandur is fully stuck. I've had time to rethink every career decision I've made.",
        ],
    },
    "Whitefield / ITPL": {
        "emoji": "💻",
        "speed": 9,
        "stuck": 18,
        "fame": 85,
        "lines": [
            "Whitefield traffic has entered a new dimension. Google Maps has stopped giving estimates.",
            "Stuck near ITPL. Half of Bengaluru's IT crowd is on this one road with me.",
        ],
    },
    "Electronic City Flyover": {
        "emoji": "🛣️",
        "speed": 12,
        "stuck": 12,
        "fame": 80,
        "lines": [
            "The E-City flyover toll line is longer than a Diwali sale queue.",
            "Someone's car broke down on the E-City flyover and now all of us are paying for it.",
        ],
    },
    "Bannerghatta Road (Dairy Circle)": {
        "emoji": "🚇",
        "speed": 9,
        "stuck": 15,
        "fame": 80,
        "lines": [
            "Metro work on Bannerghatta Road has turned three lanes into one, and all of us are fighting for it.",
            "Dairy Circle is jammed. I've seen the same ice cream ad 40 times.",
        ],
    },
    "Sony World Signal, Koramangala": {
        "emoji": "📣",
        "speed": 10,
        "stuck": 12,
        "fame": 78,
        "lines": [
            "Sony World signal is a full honking concert right now.",
            "Koramangala is jammed. Every second vehicle is a food delivery bike, and they're all winning.",
        ],
    },
    "Majestic": {
        "emoji": "🚌",
        "speed": 8,
        "stuck": 15,
        "fame": 75,
        "lines": [
            "Majestic is chaos. Every bus in Karnataka is trying to leave at the same time.",
            "Stuck at Majestic. Three conductors have already offered me a seat to three different cities.",
        ],
    },
    "Mekhri Circle": {
        "emoji": "🌀",
        "speed": 11,
        "stuck": 12,
        "fame": 70,
        "lines": [
            "Mekhri Circle underpass is fully packed. We're all just sitting and reflecting on life.",
        ],
    },
}

# Extra bad luck. speed = multiplier on speed, extra = extra minutes stuck.
EXTRAS = {
    "🌧️ Rain": {
        "speed": 0.55,
        "extra": 10,
        "lines": [
            "And of course it started raining, so every underpass is now a swimming pool.",
            "Two drops of rain fell and the whole city forgot how to drive.",
        ],
    },
    "🚧 Metro work": {
        "speed": 0.75,
        "extra": 8,
        "lines": ["There's metro work here, so the road is now one lane and a prayer."],
    },
    "🏏 Match day": {
        "speed": 0.7,
        "extra": 10,
        "lines": ["There's a cricket match at Chinnaswamy, so half the city is driving towards the stadium."],
    },
    "🚨 VIP convoy": {
        "speed": 0.6,
        "extra": 15,
        "lines": ["Police stopped all traffic for a VIP convoy. We're all waiting like it's a red carpet."],
    },
    "🐄 Cow on road": {
        "speed": 0.9,
        "extra": 5,
        "lines": ["A cow has decided to sit in the middle of the road. Nobody is arguing with her."],
    },
    "🚌 Bus breakdown": {
        "speed": 0.8,
        "extra": 8,
        "lines": ["A BMTC bus broke down right in front of us and the whole lane has given up."],
    },
    "🥁 Procession": {
        "speed": 0.65,
        "extra": 12,
        "lines": ["There's a festival procession going on, with drums and everything. Very nice. Very slow."],
    },
}

# Who you're texting. {name} gets replaced with the name you type.
AUDIENCES = {
    "Boss 👔": {
        "greeting": "Hi {name},",
        "default_name": "",
        "closers": [
            "I'll join the call from the cab if needed. Really sorry for the delay.",
            "Please start without me, I'll catch up as soon as I reach.",
            "I'll make up for the lost time today. Sorry!",
        ],
    },
    "Professor 🎓": {
        "greeting": "Hello {name},",
        "default_name": "Ma'am/Sir",
        "closers": [
            "Sorry for the delay, I'll come straight to class.",
            "Kindly mark me present in spirit. I'll be there physically soon. 🙏",
        ],
    },
    "Friends 😎": {
        "greeting": "{name}",
        "default_name": "Bro,",
        "closers": [
            "Order without me, I'll pay my share.",
            "Start without me. Save me some food.",
            "Don't wait. I'll catch up. Probably by next week.",
        ],
    },
    "Date ❤️": {
        "greeting": "Hey {name},",
        "default_name": "",
        "closers": [
            "I'm so sorry. First round of chai is on me.",
            "Please don't leave. I'm coming, I promise. 🙏",
        ],
    },
    "Parents 🏠": {
        "greeting": "{name}",
        "default_name": "Amma,",
        "closers": [
            "Don't wait for dinner. Keep some rasam for me.",
            "Don't worry, I'm safe. Just very, very slow.",
        ],
    },
    "Client 💼": {
        "greeting": "Hi {name},",
        "default_name": "",
        "closers": [
            "Apologies for the delay. I'll call you as soon as I reach.",
            "Could we push our meeting by a bit? Apologies for the inconvenience.",
        ],
    },
}

# The flavour of the message.
TONES = {
    "😇 Polite": {"intros": [""], "outros": [""]},
    "🎭 Dramatic": {
        "intros": ["Update from the war zone:", "If I don't make it, tell my story.", "Breaking news from the road:"],
        "outros": ["😭", "Pray for me. 🙏", "This city is testing me. 😩"],
    },
    "💼 Corporate": {
        "intros": ["Quick heads-up on my ETA:", "Flagging a small blocker on my commute:"],
        "outros": ["Will circle back once I'm out of this bottleneck.", "Thanks for your understanding."],
    },
    "🗣️ Kannada mix": {
        "intros": ["Guru, sakkat traffic!", "Ayyo, full jam!"],
        "outros": ["Swalpa adjust maadi. 🙏", "Bandhe, bandhe! 🏃"],
    },
}

# Time of day: speed multiplier and how much of the "stuck" time applies.
TIME_SLOTS = {
    "Early morning (5–8 AM)": {"speed": 1.6, "stuck": 0.3, "rush": False},
    "Morning rush (8–11 AM)": {"speed": 0.6, "stuck": 1.0, "rush": True},
    "Afternoon (11 AM–4 PM)": {"speed": 0.9, "stuck": 0.6, "rush": False},
    "Evening rush (4–9 PM)": {"speed": 0.5, "stuck": 1.2, "rush": True},
    "Night (9 PM–12 AM)": {"speed": 1.3, "stuck": 0.4, "rush": False},
    "Late night (12–5 AM)": {"speed": 1.8, "stuck": 0.1, "rush": False},
}

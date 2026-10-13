# 🚦 Bengaluru Traffic Excuse Generator

Stuck at Silk Board again? This app writes a believable "running late" message for you, tells you how late you'll *actually* be, and rates how believable your excuse is.

Because "5 minutes away" stopped working years ago.

**Live app:** _add your Streamlit link here after deploying_

## What it does

- **Pick where you're stuck:** Silk Board, ORR, Hebbal, Tin Factory, Sarjapur Road and more
- **Pick who you're texting:** Boss, Professor, Friends, Date, Parents or Client
- **Pick a vibe:** Polite, Dramatic, Corporate or Kannada mix
- **Add extra bad luck:** rain, metro work, match day, VIP convoy, a cow on the road...
- **Get a ready-to-send message** with a copy button and a one-tap WhatsApp share
- **🔴 Live traffic:** real speed at your jam spot right now (from TomTom), with a jam level and a "traffic tax" on your trip
- **🌦️ Live weather:** checks if it's actually raining in Bengaluru, so fake rain excuses get caught
- **Believability meter:** based on live data. Claim Silk Board traffic when the road is clear and the app will call you out
- **✨ AI mode:** Google Gemini writes a brand new excuse every time, each in a random comedy style (cricket commentator, news anchor, nature documentary...). If the AI is busy or not set up, the app quietly falls back to the built-in excuses.

## Run it on your laptop

```bash
git clone https://github.com/<your-username>/bengaluru-traffic-excuse-generator.git
cd bengaluru-traffic-excuse-generator
pip install -r requirements.txt
streamlit run app.py
```

It opens at http://localhost:8501. The app works without AI. To turn on AI mode, see below.

## Turn on AI mode (free)

1. Get a free Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey). No credit card needed.
2. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and paste your key in it:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
3. Restart the app. The ✨ AI mode switch turns on by itself.

`secrets.toml` is listed in `.gitignore`, so your key never goes to GitHub. **Never paste your key into `app.py` or any file you push.**

The free tier has a daily request limit, so the app also caps each visitor at 20 AI excuses per session. You can change this with `MAX_AI_PER_SESSION` in `app.py`.

## Turn on live traffic (free)

1. Sign up at [developer.tomtom.com](https://developer.tomtom.com). No credit card needed.
2. Open your **Dashboard → API keys** and copy your key.
3. Add it to your secrets, on a new line next to the Gemini key:
   ```toml
   TOMTOM_API_KEY = "your-tomtom-key"
   ```

The free plan gives 20,000 traffic lookups a month. The app saves each jam spot's result for 10 minutes, so even heavy use stays well inside that.

Live weather comes from [Open-Meteo](https://open-meteo.com) and needs no key.

Live data is used only when "When is this?" is set to **Right now**. Without a TomTom key, or if the service is busy, the app quietly uses the built-in joke formula.

## Deploy for free on Streamlit Community Cloud

1. Push this folder to a public GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app**, pick your repo, branch `main`, and main file `app.py`.
4. Open **Advanced settings → Secrets** and paste your keys (each on its own line, in quotes):
   ```toml
   GEMINI_API_KEY = "your-gemini-key"
   TOMTOM_API_KEY = "your-tomtom-key"
   ```
5. Click **Deploy**. You get a public link in a minute or two.

Every time you push to GitHub, the live app updates on its own.

## Project structure

```
├── app.py                       # The Streamlit app (layout + logic)
├── ai.py                        # AI mode: the Gemini prompt and comedy styles
├── live.py                      # Live traffic (TomTom) and weather (Open-Meteo)
├── excuses.py                   # Built-in jam spots, excuse lines, tones and audiences
├── requirements.txt
├── .streamlit/
│   ├── config.toml              # Theme colour
│   └── secrets.toml.example     # Template for your API key
└── README.md
```

## Add your own excuses

Everything funny lives in `excuses.py`. To add a new jam spot, copy one of the blocks in `HOTSPOTS` and change it:

```python
"Tumkur Road (Yeshwanthpur)": {
    "emoji": "🚛",
    "speed": 8,      # crawl speed at this spot (km/h)
    "stuck": 15,     # extra minutes lost just sitting here
    "fame": 72,      # how famous the jam is (0-100)
    "lines": [
        "Your new excuse goes here.",
    ],
},
```

To give the AI new comedy styles, add lines to `ANGLES` in `ai.py`.

Pull requests with new excuses are welcome. Keep them clean and fun. 🙂

## Note

Made for fun. With a TomTom key, speeds at the jam spot are real, but the rest of your trip is still an estimate. Without one, travel times come from a joke formula. And if you're the one driving, let someone else send the message. 🙏

## Data credits

- Live traffic data © [TomTom](https://www.tomtom.com)
- Weather data by [Open-Meteo.com](https://open-meteo.com) (CC BY 4.0)

## License

MIT

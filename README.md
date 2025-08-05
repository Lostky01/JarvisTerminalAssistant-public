# 🧠 Jarvis v1 - Groq LLM-Based Terminal Assistant

**Jarvis** is a sarcastic, confident, and fully voice-controlled terminal assistant powered by the Groq LLM API. It responds to your voice commands, executes shell tasks, cracks jokes, plays music, opens apps, and even roasts your sorry ass if needed.

## ⚙️ Features

- 🎙️ Voice activation with `wake up` / `hey jarvis` and deactivation with `thank you jarvis`
- 🗣️ Edge TTS with `en-US-GuyNeural` for natural replies
- 🤖 Uses `llama3-70b-8192` via Groq API for witty, no-BS AI responses
- 💻 Runs real shell commands if you ask it to (npm, pip, git, etc.)
- 🌐 Opens websites like YouTube, Spotify, ChatGPT, Reddit, and more
- 🎧 Spotify integration: play songs by voice
- 💾 System stats: CPU, RAM, disk, uptime, network speed, battery
- 🔍 File/folder finder + file explorer integration
- 🎵 Media controls: volume up/down, mute, pause, next, previous
- 📅 Date & time updates
- 🌤️ Weather reports
- 🧠 Memory system to recall last user questions
- 🔥 Full-on attitude, no “as an AI” crap, just pure unfiltered sass

## 🧠 Tech Stack

- **Python**
- **Groq API (LLM: LLaMA 3 70B)** — Replace `YOUR_GROQ_API_KEY` with your real key
- **SpeechRecognition** for voice input
- **Edge-TTS** for lifelike voice output
- **SoundDevice + SoundFile** for audio playback
- **Rich, TermColor, PyFiglet** for beautiful terminal UI
- **Spotify API**, **OS**, **Subprocess**, **System Utils** for everything else

## 🚀 How to Run

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Set your Groq API key in `call_llm()`:
    ```python
    "Authorization": "Bearer YOUR_GROQ_API_KEY",
    ```

3. Run the main file:
    ```bash
    python jarvis.py
    ```

4. Say `Hey Jarvis` and give it commands like:
    - "Run `npm install express`"
    - "Open YouTube"
    - "What's my CPU usage"
    - "Play song Blinding Lights"
    - "Find file resume.pdf"

## ⚠️ Notes

- This is version **v1** — raw, functional, and unfiltered.
- Make sure your mic works.
- Jarvis *will* insult you if you ask dumb shit. He’s built different.
- This project is **NOT** privacy safe. It listens. You’ve been warned.

## 📁 Project Structure (Partial)

```
.
├── browse/
│   └── browse.py
├── memory_utils.py
├── spotify_player/
│   └── spotify_player.py
├── system_utils/
│   ├── battery_status.py
│   ├── get_uptime.py
│   ├── get_usage.py
│   ├── media_controller.py
│   ├── network_speed.py
│   ├── search_file.py
│   └── background_process.py
├── weather_detection/
│   └── weather.py
├── youtube_transcript/
│   └── youtube_transcript.py
├── jarvis.py  # <--- your main assistant logic
├── memory.json
└── README.md
```

## 💀 License

Unhinged Public License v1.0 — Do whatever the hell you want, but don’t blame me if your PC explodes.

---

Made by caffeine and not enough therapy.
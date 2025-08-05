import os
import re
import uuid
import json
import time
import psutil
import asyncio
import requests
import subprocess
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import edge_tts
import webbrowser
import fnmatch
from youtube_transcript.youtube_transcript import get_youtube_transcript
from weather_detection.weather import get_weather
from system_utils.get_uptime import get_uptime
from system_utils.battery_status import get_battery_status
from system_utils.get_usage import get_cpu_usage, get_ram_usage, get_disk_usage
from system_utils.network_speed import get_network_speed
from spotify_player.spotify_player import sp
from system_utils.background_process import get_top_processes
from system_utils.search_file import search_file_system, open_in_explorer
from system_utils.media_controller import set_volume, change_volume, media_play_pause, media_next, media_previous, media_stop
from browse.browse import open_in_chrome
from memory_utils import add_to_memory, get_last_n_conversations

from termcolor import colored
from pyfiglet import Figlet
from rich.console import Console
from rich.text import Text
# === SETUP ===


r = sr.Recognizer()
mic = sr.Microphone()
console = Console()
WAKE_WORDS = ["wake up", "hey jarvis"]
SLEEP_WORD = "thank you jarvis"
active = False

VOICE = "en-US-GuyNeural"
url_map = {
    "open youtube": "https://www.youtube.com",
    "open spotify": "https://open.spotify.com",
    "open github": "https://github.com",
    "open chatgpt": "https://chat.openai.com",
    "open google maps": "https://www.google.com/maps",
    "open gmail": "https://mail.google.com",
    "open netflix": "https://www.netflix.com",
    "open twitter": "https://x.com",
    "open reddit": "https://www.reddit.com",
    "open stackoverflow": "https://stackoverflow.com",
}
# === SPEAK (ASYNC EDGE-TTS) ===
async def speak(text):
    if not text.strip():
        return
    chunks = re.split(r'(?<=[.!?]) +', text)
    for chunk in chunks:
        filename = f"temp_{uuid.uuid4().hex}.mp3"
        communicate = edge_tts.Communicate(text=chunk.strip(), voice=VOICE)
        await communicate.save(filename)
        try:
            data, samplerate = sf.read(filename)
            sd.play(data, samplerate)
            sd.wait()
        finally:
            if os.path.exists(filename):
                os.remove(filename)

# === LLM CALL ===
def call_llm(prompt, memory_context=[]):
    messages = [
        {
            "role": "system",
            "content": (
                "You are Jarvis, a confident, sarcastic, and natural voice assistant who speaks like a real human. "
                "Your replies must NEVER include reasoning, thinking steps, or inner monologue. "
                "Do not use tags like <think>, do not explain your thoughts, and do not reflect on the user's mood. "
                "You just reply with the answer. Always stay in character. "
                "If asked to tell a joke, tell it immediately. No thinking out loud. "
                "Only respond with shell commands if the user clearly asks for a direct terminal task using keywords like 'run', 'install', 'launch', etc. "
                "Otherwise, keep replies short, sarcastic, and clever. No 'as an AI', no apologies, no backstory. Just raw wit."
            )
        }
    ]
    
    for convo in memory_context:
        messages.append({"role": "user", "content": convo["user"]})
        messages.append({"role": "assistant", "content": convo["jarvis"]})
    messages.append({"role": "user", "content": prompt})

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": "Bearer YOUR_GROQ_API_KEY",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-70b-8192",
                "messages": messages,
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("✖️ LLM error:", e)
        return "Error contacting the brain server. Try again later."

# === SHELL COMMAND DETECTION ===
def is_probably_shell_command(text):
    return re.match(r"^(cd|ls|dir|npm|npx|composer|python|pip|git|code|start|explorer|echo|mkdir|rm|del|cls|curl|wget|exit|shutdown|taskkill|open|xdg-open)\b.*", text.strip()) is not None

# === EXECUTE COMMAND ===
async def execute_command(cmd):
    try:
        print(f"⚙️ Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.stdout:
            print(result.stdout)
            await speak(result.stdout[:500])
        elif result.stderr:
            print(result.stderr)
            await speak("There was an error running that command.")
        else:
            await speak("Done.")
    except Exception as e:
        print("✖️ Exception:", e)
        await speak("Error running that command.")

# === LAST QUESTION MEMORY ===
def get_last_question():
    try:
        with open("memory.json", "r") as f:
            data = json.load(f)
            for entry in reversed(data["conversations"]):
                if "?" in entry["user"]:
                    return entry["user"]
    except Exception as e:
        print("✖️ Memory read failed:", e)
    return None

# === LISTEN FUNCTION ===
async def listen():
    global active
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=12, phrase_time_limit=15)
    except Exception as e:
        print("🎧 Mic error:", e)
        return

    try:
        text = r.recognize_google(audio).lower().strip()
        print("> You said:", text)

        if any(wake in text for wake in WAKE_WORDS):
            active = True
            print("🦾 Jarvis: Online. What's the task?")
            await speak("Online. What's the task?")
            return

        elif SLEEP_WORD in text:
            active = False
            print("🔒 Jarvis: Going silent. Say 'hey jarvis' to reactivate.")
            await speak("Going silent.")
            return

        elif not active:
            return

        if "last question i asked" in text:
            last_q = get_last_question()
            if last_q:
                reply = f"The last question you asked was: '{last_q}'"
            else:
                reply = "You haven't asked me any questions yet."
            console.print(
              Text("🦾 Jarvis: ", style="bold bright_blue") + 
              Text(reply, style="bold white on rgb(30,30,60)")
            )
            await speak(reply)
            return

        for keyword, url in url_map.items():
            if keyword in text:
                console.print(
                    Text("🌐 Jarvis :", style="bold cyan") +
                    Text(f" executing ", style="bold white") +
                    Text(f"{keyword}", style="bold italic magenta") +
                    Text(" → ", style="bold yellow") +
                    Text(f"{url}", style="bold underline blue")
                )
                await speak(f"Executing {keyword}")
                open_in_chrome(url)
                return

        if "time" in text:
            now = time.strftime("%I:%M %p")  
            reply = f"It's currently {now}"
            console.print(
              Text("🦾 Jarvis: ", style="bold bright_blue") + 
              Text(reply, style="bold white on rgb(30,30,60)")
            )
            await speak(reply)
            return
        if "date" in text:
            today = time.strftime("%A, %B %d, %Y")
            reply = f"Today's date is {today}"
            console.print(
              Text("🦾 Jarvis: ", style="bold bright_blue") + 
              Text(reply, style="bold white on rgb(30,30,60)")
            )
            await speak(reply)
            return
        if "weather" in text:
            weather_report = get_weather()
            console.print(
              Text("🦾 Jarvis: ", style="bold bright_blue") + 
              Text(weather_report, style="bold white on rgb(30,30,60)")
            )
            await speak(weather_report)
            return
        if "cpu usage" in text:
            cpu_report = get_cpu_usage()
            console.print(
              Text("🦾 Jarvis: ", style="bold bright_blue") + 
              Text(cpu_report, style="bold white on rgb(30,30,60)")
            )
            await speak(cpu_report)
            return
        
        if "ram usage" in text:
            ram_report = get_ram_usage()
            console.print(
              Text("🦾 Jarvis: ", style="bold bright_blue") + 
              Text(ram_report, style="bold white on rgb(30,30,60)")
            )
            await speak(ram_report)
            return
        
        if "what's my network speed" in text:
           network_speed = get_network_speed()
           console.print(
             Text("🦾 Jarvis: ", style="bold bright_blue") + 
             Text(network_speed, style="bold white on rgb(30,30,60)")
           )
           await speak(network_speed)
           return
            
        if "storage usage" in text or "disk usage" in text:
            disk_report = get_disk_usage()
            console.print(
              Text("🦾 Jarvis: ", style="bold bright_blue") + 
              Text(disk_report, style="bold white on rgb(30,30,60)")
            )
            await speak(disk_report)
            return
        
        if "what's my laptop uptime" in text:
          reply = get_uptime()
          console.print(
            Text("🦾 Jarvis: ", style="bold bright_blue") + 
            Text(reply, style="bold white on rgb(30,30,60)")
          )
          await speak(reply)
          return
      
      
        if "find file" in text or "find folder" in text:
            keyword = text.replace("find file", "").replace("find folder", "").strip()
            if not keyword:
                await speak("You gotta tell me what the hell to look for.")
                return

            await speak(f"Searching for {keyword} on your system...")
            results = search_file_system(keyword)

            if results:
                await speak(f"Found {len(results)} result(s). Opening the first one.")
                open_in_explorer(results[0])
                console.print(Text("🧠 Jarvis: ", style="bold magenta") + Text(f"Found: {results[0]}", style="bold white"))
            else:
                await speak("Couldn't find shit.")
            return
        
        if "play song" in text:
            song_name = text.replace("play song", "").strip()
            if not song_name:
                await speak("What song, dumbass?")
                return          
            results = sp.search(q=song_name, limit=1, type='track')
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                sp.start_playback(uris=[track_uri])
                await speak(f"Playing {song_name} on Spotify.")
                console.print(Text("🎵 Jarvis: ", style="bold green") + Text(f"Now playing: {song_name}", style="bold white"))
            else:
                await speak("No such song found, are you deaf?")
            return
        
        if "top process" in text or "using most memory" in text:
            reply = get_top_processes()
            console.print(
              Text("🦾 Jarvis: ", style="bold bright_blue") + 
              Text(reply, style="bold white on rgb(30,30,60)")
            )
            await speak(reply)
            return
        
        if "increase volume" in text:
            change_volume(0.1)
            await speak("Volume up.")

        elif "decrease volume" in text:
            change_volume(-0.1)
            await speak("Volume down.")

        elif "mute" in text:
            set_volume(0)
            await speak("Muted.")

        elif "pause the music" in text or "play the music" in text or "resume the music" in text:
            media_play_pause()
            await speak("Toggled play and pause.")

        elif "next song" in text or "skip" in text:
            media_next()
            await speak("Next track.")

        elif "previous song" in text:
            media_previous()
            await speak("Previous track.")

        elif "stop music" in text:
            media_stop()
            await speak("Music stopped.")

        await speak("Hmmm...")
        memory_context = get_last_n_conversations(5)
        response = call_llm(text, memory_context=memory_context)
        print("🦾 Jarvis:", response)
        add_to_memory(text, response)

        if is_probably_shell_command(response):
            await execute_command(response)
        else:
            if response.strip().lower() == text.strip().lower():
                response = "Okay... what about it? You want me to roast or vibe with you?"
            await speak(response)

    except sr.UnknownValueError:
        print("🤖 Didn't catch that.")
    except sr.RequestError:
        print("⚠️ API error.")
        
def show_startup_banner():
    figlet = Figlet(font='slant')
    banner = figlet.renderText('JARVIS')
    colored_banner = colored(banner, 'green')
    print(colored_banner)

   
    
# === MAIN LOOP ===
async def main_loop():
    show_startup_banner()
    console.print(Text("✔️ Jarvis booted. Say 'Hey Jarvis' to activate.", style="bold magenta"))
    console.print(Text("🎧 Listening...", style="bold cyan"))
    while True:
        await listen()

try:
    asyncio.run(main_loop())
except KeyboardInterrupt:
    print("\n🔻 Shutdown initiated. Jarvis offline.\n")


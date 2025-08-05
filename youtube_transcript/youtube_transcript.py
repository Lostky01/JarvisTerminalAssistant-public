from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_url):
    try:
        video_id = video_url.split("v=")[-1].split("&")[0]
        transcript = YouTubeTranscriptApi.fetch(video_id)   
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except Exception as e:
        return f"❌ Error fetching transcript: {e}"

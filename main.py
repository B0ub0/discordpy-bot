import requests
from googleapiclient.discovery import build
import time

# Configurations
YOUTUBE_API_KEY = 'AIzaSyBgn3uRFr_QmH8ExA0Vv2DRLVm1o0OYGp0'
CHANNEL_IDS = [
    'UCGccXmPtpSqfFFTHfN0jqMw',  # Exemple de premier ID de chaîne
    'UCQeDm0G3i-BVBIVyU-nmfAg',  # Exemple de deuxième ID de chaîne
    # Ajoutez d'autres IDs de chaîne ici...
]
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1255204520712077523/6ePJsgCbnhmOKNYTE3kILTx3jdQg-SUCuOAF9EbZVVeircnGvzbsrxKfVprJqlslyaIA'
CHECK_INTERVAL = 300  # seconds
DELAY_BEFORE_START = 10  # Délai avant de commencer à vérifier et envoyer les notifications

# Initialize YouTube API
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_latest_video(channel_id):
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=1,
        order='date'
    )
    response = request.execute()
    return response['items'][0] if response['items'] else None

def send_discord_notification(message):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    print(message)

def main():
    print("Le script de notification de nouvelles vidéos YouTube vient d'être activé!")
    send_discord_notification("Le script de notification de nouvelles vidéos YouTube vient d'être activé!")
    time.sleep(DELAY_BEFORE_START)
    
    latest_video_ids = {channel_id: None for channel_id in CHANNEL_IDS}
    while True:
        for channel_id in CHANNEL_IDS:
            latest_video = get_latest_video(channel_id)
            if latest_video:
                video_id = latest_video['id']['videoId']
                if video_id != latest_video_ids[channel_id]:
                    send_discord_notification(f"Hey , une nouvelle vidéo a été postée par {latest_video['snippet']['channelTitle']}!\nhttps://www.youtube.com/watch?v={video_id}\nScript made by Bou.")
                    latest_video_ids[channel_id] = video_id
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()


    
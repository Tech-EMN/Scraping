import re
# !pip install youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi

#Datetime para o nome do arquivo

def get_video_id(url):
    # Extrai o ID do vídeo do link do YouTube
    video_id = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
    if video_id:
        return video_id.group(1)
    else:
        raise ValueError("URL inválida")
    

def get_transcript(video_id):
    # Obtém a transcrição do vídeo
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        # Tentar obter transcrição gerada manualmente
        transcript = None
        for transcript_obj in transcript_list:
            if not transcript_obj.is_generated:
                transcript = transcript_obj.fetch()
                break
        # Caso não exista transcrição manual, obter a gerada automaticamente
        if transcript is None:
            # print('pegando as autogeradas')
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
            
    except Exception as e:
        return "Erro ao obter transcrição: {}".format(e)
    
    return '\n'.join([t['text'] for t in transcript])


# Url Examples
# url = r"https://www.youtube.com/watch?v=3KKQgJk7zn0"
# url = r"https://www.youtube.com/watch?v=NFHDHcs4BvQ"

url = r"https://www.youtube.com/watch?v=watch?v=3KKQgJk7zn0"

try:
    result = get_transcript(get_video_id(url))
    
except Exception as e:
    result = f"Erro: {e}"
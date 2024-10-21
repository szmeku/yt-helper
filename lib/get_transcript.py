from youtube_transcript_api import YouTubeTranscriptApi

def __transcript_to_string(transcript):
    return "".join([
        str(item["start"]) + " : " + item["text"] + ";\n"
        for item in transcript
    ])


def get_transcript(url):
    from urllib.parse import urlparse, parse_qs
    url_data = urlparse(url)
    query = parse_qs(url_data.query)
    return __transcript_to_string(
        YouTubeTranscriptApi.get_transcript(query["v"][0])
    )

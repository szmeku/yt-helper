import json
import openai
import tiktoken
from ramda import path, pipe, join, split, replace, map, trim
from lib.get_transcript import get_transcript
from lib.mapAsync import mapAsync


def split_into_chunks(text, tokens=2500):
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    words = encoding.encode(text)
    chunks = []
    for i in range(0, len(words), tokens):
        chunks.append(''.join(encoding.decode(words[i:i + tokens])))

    return chunks

config = json.load(open("./config.json"))
openai.api_key = config["openapi_key"]

messageContentTemplate = lambda previousSummary, nextChunk: f"""
      STORAGE1:
      {previousSummary}
      STORAGE2:
      {nextChunk}
  """

messageFromPrevSummaryAndNextChunk =  lambda previousSummary, nextChunk: {
  "role": "user",
  "content": messageContentTemplate(previousSummary, nextChunk)
}

# def totalSummaryN(previousSummary, nextChunk):
def totalSummaryN(nextChunk):

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
            "role": "system",
            "content": """
            You're gonna act as a yt transcript summarizer.
            I'm gonna pass which sentence was started in which second in format
            [second] : [sentence];
            [second] : [sentence];
            
            Return just summary. 5 points in this format.
            {"start": [second], "summary": [summary]} 
            {"start": [second], "summary": [summary]}            
            ...            
            {"start": [second], "summary": [summary]}                        

            DON'T RETURN ANYTHING ELSE!.
            Points can't be numbered!
            You're gonna return both summary point and at which second this part started.
            Please summarize in concrete but detailed style.
            Mention technical details if necessary.
            Don't repeat yourself between points. If there's something mentioned in few points you can squeeze to one.
            Time has to be provided only in integers.
            """
        },
        {
              "role": "user",
              "content": nextChunk
        },
        # messageFromPrevSummaryAndNextChunk(previousSummary, nextChunk)
      ],
      # temperature=1,
      # max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return path(['choices', 0, 'message', 'content'])(response)

def parseJson(text):

    try:
        result = json.loads(text)
        return result

    except Exception as e:
        print(e)
        print('Error parsing text to JSON. Src text:\n', text)


summarizeYtVideo = pipe(
    get_transcript,
    split_into_chunks,
    mapAsync(pipe(
        totalSummaryN,
        trim,
        replace("},", "}")
    )),
    join("\n"),
    split('\n'),
    map(parseJson),
)
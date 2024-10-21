import json

import gradio as gr
import openai
from lib.summarizeYtVideo import summarizeYtVideo

config = json.load(open("./config.json"))
openai.api_key = config["openapi_key"]
from ramda import pipe, tap, map, join, path

ask_gpt = pipe(
    lambda message: {"role": "user", "content": message},
    lambda message: openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "user will provide you text, act as summarizer. Summarize it in 10 points"},
            message
        ],
        # temperature=0.2,
        max_tokens=1000,
        # frequency_penalty=0.0

        n=1,
        stop=None,
        temperature=0.5,
    ),
    tap(pipe(str, print)),
    path(["choices", 0, "message", "content"]),
    str,

)

def action(yt_url):

    return pipe(
            summarizeYtVideo,
            map(lambda x: f"""  
                <li><a target="_blank" href="{yt_url}&t={x["start"]}">{x["start"]}</a> : {x["summary"]}</li>
            """),
            join("\n"),
            lambda v: f"""<ul>{v}</ul>""",
    )(yt_url)

gr.Interface(
     action,
     inputs=[
       gr.Textbox(label="Youtube url", placeholder="Enter youtube url here...", value="https://www.youtube.com/watch?v=k5imq01uvUY"),
     ],
     outputs=[gr.HTML()],
     title="YT Helper",
     description ="",
).launch(
    server_port=8081,
    server_name="0.0.0.0"
)

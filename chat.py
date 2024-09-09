import os
import openai

openai.api_base = "http://localhost:8080/v1"
api_key = 'http://127.0.0.1:7860/'
openai.api_key = api_key

def chat(messages):
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, stream=True)

    for chunk in chat_completion:
        yield (chunk.choices[0].delta.content)
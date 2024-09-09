import os
import re

import json
import requests

def generate_text(prompt):
    url = "http://localhost:8080/v1/completions"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": "ggml-openllama.bin",
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.text
        response_dict = json.loads(response_json)
        text = response_dict["choices"][0]["text"]
        return(text)
    else:
        return "generate_text失败。状态码: " + str(response.status_code)


def generate_answer(current_file_text: str, content: str):
    url = "http://localhost:8080/v1/edits"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": str,
        "model": "ggml-openllama.bin",
        "temperature": 0.7,
        "instruction": "rephrase"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.text
        response_dict = json.loads(response_json)
        text = response_dict["choices"][0]["text"]
        return(text)
    else:
        return "generate_text失败。状态码: " + str(response.status_code)

def generate_summary(current_file_text: str):
    url = "http://localhost:8080/v1/edits"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": str,
        "model": "ggml-openllama.bin",
        "temperature": 0.7,
        "instruction": "rephrase"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.text
        response_dict = json.loads(response_json)
        text = response_dict["choices"][0]["text"]
        return(text)
    else:
        return "generate_text失败。状态码: " + str(response.status_code)


if __name__ == "__main__":
    print(generate_text("Cristiano Ronaldo is a football player."))

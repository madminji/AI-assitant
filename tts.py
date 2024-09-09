import json
import requests
import os
def text2audio(content: str):
    url = "http://localhost:8080/tts"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "input": content,
        "model": "en-us-blizzard_lessac-medium.onnx"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        file_path = "output.wav"
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    else:
        return "生成音频文件失败。状态码: " + str(response.status_code)

import os
import requests


def image_generate(content: str) -> str:
    res = requests.post(
        (os.getenv("LOCALAI_URL") or "http://localhost:8080")
        + "/v1/images/generations",
        headers={"Content-Type": "application/json"},
        json={"prompt": content, "size": "256x256"},
    )
    res_body = res.json()
    if "data" in res_body:
        return f"![]({res_body['data'][0]['url']})"
    return res_body["error"]["message"]


if __name__ == "__main__":
    image_generate("A cute baby sea otter")

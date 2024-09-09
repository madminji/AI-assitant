import requests
import os


def audio2text(file):
    """
    curl http://localhost:8080/v1/audio/transcriptions -H "Content-Type: multipart/form-data" -F file="@sun-wukong.wav" -F  model="whisper-1"
    """
    with open(file, "rb") as f:
        res = requests.post(
            (os.getenv("LOCALAI_URL") or "http://localhost:8080")
            + "/v1/audio/transcriptions",
            files={"file": f},
            data={"model": "whisper-1"},
        )

    res_body = res.json()
    # print(res_body)
    if "segments" in res_body:
        ans = ""
        for segment in res_body["segments"]:
            ans += segment["text"]
        return ans
    return res_body["error"]["message"]


if __name__ == "__main__":
    print(audio2text("sun-wukong.wav"))

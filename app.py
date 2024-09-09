import gradio as gr
import os
import time
import requests
import json
from chat import chat
from fetch import fetch
from function import function_calling
from image_generate import image_generate
from mnist import image_classification
from search import search
from stt import audio2text
from tts import text2audio
from pdf import generate_text


# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.

messages = []
current_file_text = None

def add_text(history, text):
    history = history + [(text, None)]
    messages.append({"role": "user", "content": text})
    if not (messages[-1]["content"].startswith("/search ")) and not (messages[-1]["content"].startswith("/audio ")) and not (messages[-1]["content"].startswith("/fetch ")) and not (messages[-1]["content"].startswith("/image ")) and not (messages[-1]["content"].startswith("/function ")):
        messages.append({"role": "assistant", "content": None})
    return history, gr.update(value="", interactive=False)


def add_file(history, file):
    history = history + [((file.name,), None)]
    return history

def bot(history):
    history[-1][1] = ""
    if isinstance(history[-1][0], tuple):
        file: str = history[-1][0][0]
        # 语音输入
        if file.lower().endswith('.wav'):
            response1 = audio2text(file)
            history[-1][1] = response1
        # 图片分类
        elif file.lower().endswith('.png'):
            classification_result = image_classification(file)
            history[-1][1] = classification_result
        # 文件输入
        elif file.lower().endswith('.txt'):
            with open(file, 'r') as f:
                file_content = f.read()
                txt_result = generate_text(file_content)
                history[-1][1] = txt_result
    # 网络搜索
    elif history[-1][0].startswith("/search "):
        search_content = history[-1][0][8:]  # 获取content
        search_result = search(search_content)
        history[-1][1] = search_result.split("\n\n", 1)[-1]
        messages[-1]["content"] = search_result
    # 语音输出
    elif history[-1][0].startswith("/audio "):
        response = chat(messages)
        for response_chunk in response:
            response_chunk = response_chunk.rstrip('\n')
            history[-1][1] += response_chunk
            print(history)
            time.sleep(0.05)
            # yield history
        messages[-1]["content"] = history[-1][1]
        # 生成音频并将其路径添加到history中
        assistant_response = messages[-1]["content"] if len(messages[-1]["content"]) >= 2 else "No response"
        audio_file_path = text2audio(assistant_response)
        history[-1][1] = (audio_file_path,)
        yield history
    #网页总结
    elif history[-1][0].startswith("/fetch "):
        arg = history[-1][0][7:]
        result1 = fetch(arg)
        history[-1][1] = result1.split("\n\n",1)[-1]
        messages[-1]["content"] = result1
    #图片生成
    elif history[-1][0].startswith("/image "):
        arg = history[-1][0][7:]
        result2 = image_generate(arg)
        history[-1][1] = result2.split("\n\n",1)[-1]
        messages[-1]["content"] = result2
    # 函数调用
    elif history[-1][0].startswith("/function "):
        arg = history[-1][0][10:]
        message = [{"role": "user", "content": arg}]
        result3 = function_calling(message)
        history[-1][1] = result3.split("\n\n",1)[-1]
        messages[-1]["content"] = result3
    else:
        response = chat(messages)
        # 流式更新history
        for response_chunk in response:
            response_chunk = response_chunk.rstrip('\n')
            history[-1][1] += response_chunk
            time.sleep(0.05)
            yield history
        messages[-1]["content"] = history[-1][1]
    yield history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        clear_btn = gr.Button('Clear')
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio", "text"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear_btn.click(lambda: messages.clear(), None, chatbot, queue=False)

demo.queue()
demo.launch()
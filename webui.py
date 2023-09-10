import gradio as gr
import os
import pandas as pd
import time
from backend import generate_answer
import base64

init_state_dict = {
    "question":"",
    "file_uploaded":False,
    "dataframe":None,
    "file_path":None
}

def add_text(state_dict, history, text):
    #接收提问
    history = history + [(text, None)]
    state_dict["question"] = text
    return state_dict, history, gr.update(value="", interactive=False)


def add_file(state_dict, history, file):
    #接收文件
    try:
        path = file.name
        filename = os.path.basename(path)
        df = pd.read_csv(path)
        state_dict["dataframe"] = df
        state_dict["file_uploaded"] = True
        state_dict["file_path"] = path
        msg = [f'📁[{filename}]', None]
        history.append(msg)
    except:
        state_dict["file_uploaded"] = False
        msg = ["Upload failed", None]
        history.append(msg)

    return state_dict, history


def file_check(state_dict, history):
    #解析引入文件
    print(state_dict["file_path"])
    print(type(state_dict["file_path"]))
    if state_dict["file_uploaded"]:
        response = "File is uploaded, let's chat"
    else:
        response = "Uploaded failed, make sure it's a .csv file"
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history


def images_to_base64_md():
    #将图片转为Markdown

    
    path = './cache'
    markdown_list = []
    files = [f for f in os.listdir(path) if f.lower().endswith('.jpg')]
    for file in files:
        file_path = os.path.join(path, file)
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            markdown_img = f"![{file}](data:image/jpeg;base64,{encoded_string})"
            markdown_list.append(markdown_img)
            image_file.close()
            os.remove(file_path)
    return markdown_list



def bot(state_dict, history):
    if state_dict["file_uploaded"]:
        df = state_dict["dataframe"]
        question = state_dict["question"]
        file_path = state_dict["file_path"]
        history[-1][1] = ""
        for re in generate_answer(question,df,file_path):
            if re == "[SEP]":
                history.append([None, ""])
                html_list = images_to_base64_md()
                if len(html_list)>0:
                    for img_md in html_list:
                        history[-1][1] += img_md + "\n"
                    history.append([None, ""])
                continue
            history[-1][1] += re
            time.sleep(0.005)
            yield history
    else:
        response = "Please upload the file before starting the conversation"
        history[-1][1] = ""
        for character in response:
            history[-1][1] += character
            time.sleep(0.02)
            yield history


with gr.Blocks() as demo:
    """
    Reference: https://www.gradio.app/guides/creating-a-custom-chatbot-with-blocks
    """
    states = gr.State(value=init_state_dict)
    chatbot = gr.Chatbot(
        [],
        height = 800,
        elem_id="Code Inter",
        bubble_full_width=True,
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Upload an excel file and chat with me",
            container=False,
        )
        btn = gr.UploadButton("📁", file_types=["file"])

    txt_msg = txt.submit(add_text, [states, chatbot, txt], [states, chatbot, txt], queue=False).then(
        bot, [states, chatbot], chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)


    file_msg = btn.upload(add_file, [states, chatbot, btn], [states, chatbot], queue=False).then(
        file_check, [states, chatbot], chatbot)

demo.queue()
demo.launch(server_name="0.0.0.0", server_port=7860)


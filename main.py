import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from transformers import MarianMTModel, MarianTokenizer
from modelscope.pipelines import pipeline
from modelscope.outputs import OutputKeys


def translate_chinese_to_english(chinese_text):
    model_name = "./models/model2"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    input_ids = tokenizer(chinese_text, return_tensors="pt", padding=True)["input_ids"]
    translated_ids = model.generate(input_ids)
    translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
    return translated_text


def on_entry_click(event):
    if text_input.get("1.0", "end-1c") == "在此处输入要生成视频的文字":
        text_input.delete("1.0", "end")
        text_input.insert("1.0", "")


def on_exit(event):
    if text_input.get("1.0", "end-1c") == "":
        text_input.insert("1.0", "在此处输入要生成视频的文字")


def generate_video():
    confirmed = messagebox.askokcancel("提示",
                                       "运行该文本生成视频懒人一键包需要消耗至少16GB内存+16GB显存（不足的显存可以用双倍的物理内存弥补），请确保配置符合要求。\n生成可能需要数十分钟至数小时不等（根据显卡算力决定），期间界面可能会无响应，请勿关闭")

    if confirmed:
        chinese_text = text_input.get("1.0", "end-1c")
        english_text = translate_chinese_to_english(chinese_text)
        messagebox.showinfo("选择导出路径", f"请选择导出路径")
        output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        p = pipeline('text-to-video-synthesis', model="./models/model1")



        if output_path:
            test_text = {'text': english_text}
            output_video_path = p(test_text, output_video=output_path)[OutputKeys.OUTPUT_VIDEO]
            messagebox.showinfo("生成成功", f"已经导出到路径 {output_video_path}")
        else:
            test_text = {'text': english_text}
            output_video_path = p(test_text, output_video="./output.mp4")[OutputKeys.OUTPUT_VIDEO]
            messagebox.showinfo("生成成功", f"已经导出到路径 {output_video_path}")


# 创建界面
root = tk.Tk()
root.title("视频生成界面")

text_input = tk.Text(root, height=5, width=50)
text_input.insert("1.0", "在此处输入要生成视频的文字")
text_input.bind("<FocusIn>", on_entry_click)
text_input.bind("<FocusOut>", on_exit)
text_input.pack()

generate_button = tk.Button(root, text="开始生成", command=generate_video)
generate_button.pack()

root.mainloop()

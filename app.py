import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyautogui
import os
import threading
import cv2
import numpy as np
import google.generativeai as genai
import re

# --- CONFIG ---
SAVE_DIR = "screenshots"
GEMINI_API_KEY = "AIzaSyALiGq131ysBLsheSLJMLBamsMVYGClPmk"
FIXED_PROMPT = (
    "🧠 This is a quiz image! 🎯 Please:\n"
    "1️⃣ Tell me the correct answer 100% answer\n"
    "2️⃣ Tell me the correct option (A, B, C, or D)\n"
    "3️⃣ Give a super short explanation in 1 line 💡\n"
    "Make it colorful, use emojis colrofull like 🌴🎉🔥🐥and keep it fun! 🎉"
)

# --- INIT GEMINI ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# --- GLOBALS ---
screenshot_area = None
image_files = []
current_image_index = -1

# --- FOLDER SETUP ---
os.makedirs(SAVE_DIR, exist_ok=True)

def get_selection_area():
    print("🖱️ Select screen area using mouse... Press ENTER to confirm.")
    img = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    r = cv2.selectROI("Select Area - Press ENTER to confirm", img, showCrosshair=True)
    cv2.destroyAllWindows()
    x, y, w, h = r
    return (x, y, w, h)

def take_screenshot_and_save():
    global screenshot_area
    if not screenshot_area:
        return None
    left, top, width, height = screenshot_area
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    filename = os.path.join(SAVE_DIR, f"{len(os.listdir(SAVE_DIR)):04d}.png")
    screenshot.save(filename)
    return filename

def show_image(filename):
    img = Image.open(filename)
    img = img.resize((300, 200))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

def next_image():
    global current_image_index
    filename = take_screenshot_and_save()
    if filename:
        image_files.append(filename)
        current_image_index += 1
        show_image(filename)
        response_text_widget.config(state="normal")
        response_text_widget.delete(1.0, "end")
        response_text_widget.config(state="disabled")

        # Auto-generate if checkbox is ticked
        if auto_generate_var.get():
            generate_response()

def strip_markdown(md_text):
    # Remove Markdown formatting like **, *, #, etc.
    text = re.sub(r"[*_`#\-]+", "", md_text)
    text = re.sub(r"\n{2,}", "\n", text)  # Remove extra line gaps
    return text.strip()

def generate_response():
    if current_image_index < 0:
        messagebox.showwarning("Error", "Take a screenshot first.")
        return
    prompt = prompt_entry.get()
    image_path = image_files[current_image_index]

    img = Image.open(image_path)

    response_text_widget.config(state="normal")
    response_text_widget.delete(1.0, "end")
    response_text_widget.insert("end", "Generating...\n")
    response_text_widget.config(state="disabled")

    def get_answer():
        try:
            res = model.generate_content([prompt, img])
            plain_text = strip_markdown(res.text)

            response_text_widget.config(state="normal")
            response_text_widget.delete(1.0, "end")
            response_text_widget.insert("end", plain_text)
            response_text_widget.config(state="disabled")
        except Exception as e:
            response_text_widget.config(state="normal")
            response_text_widget.insert("end", f"Error: {str(e)}")
            response_text_widget.config(state="disabled")

    threading.Thread(target=get_answer).start()

def setup_area():
    global screenshot_area
    screenshot_area = get_selection_area()
    messagebox.showinfo("Area Set", f"Screenshot area set to: {screenshot_area}")

# ... [rest of your unchanged code above]

# --- inside root setup ---
root = tk.Tk()
root.title("auto answer")
root.geometry("400x600")
root.resizable(True, True)

# Prompt Entry
prompt_entry = tk.Entry(root, font=("Segoe UI Emoji", 12))
prompt_entry.insert(0, FIXED_PROMPT)
prompt_entry.pack(pady=10, padx=10, fill="x")

# Image Display
image_label = tk.Label(root)
image_label.pack()

# Scrollable Gemini Response
response_frame = tk.Frame(root)
response_frame.pack(pady=10, padx=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(response_frame)
scrollbar.pack(side="right", fill="y")

response_text_widget = tk.Text(
    response_frame,
    wrap="word",
    height=8,
    yscrollcommand=scrollbar.set,
    font=("Segoe UI Emoji", 10),  # Emoji support
    bg="#f0f0f0"
)
response_text_widget.pack(side="left", fill="both", expand=True)
response_text_widget.config(state="disabled")

scrollbar.config(command=response_text_widget.yview)

# Auto-generate Checkbox
auto_generate_var = tk.BooleanVar()
auto_checkbox = tk.Checkbutton(
    root,
    text="✅ Auto Generate after Next",
    variable=auto_generate_var,
    font=("Segoe UI Emoji", 10)  # Emoji support
)
auto_checkbox.pack()

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

next_btn = tk.Button(btn_frame, text="➡️ Next", command=next_image, width=15, font=("Segoe UI Emoji", 10))
next_btn.grid(row=0, column=0, padx=10)

generate_btn = tk.Button(btn_frame, text="⚡ Generate", command=generate_response, width=15, font=("Segoe UI Emoji", 10))
generate_btn.grid(row=0, column=1)

# Set Screen Area Button
setup_btn = tk.Button(root, text="📐 SET SCREEN AREA", command=setup_area, font=("Segoe UI Emoji", 10))
setup_btn.pack(pady=10)

root.mainloop()

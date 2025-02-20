import os
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
import pyautogui

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        if self["state"] != "disabled":
            self["background"] = self.hover_color(self["background"])

    def on_leave(self, e):
        if self["state"] != "disabled":
            self["background"] = self.defaultBackground

    def hover_color(self, color):
        # Darken the color slightly for hover effect
        rgb = self.winfo_rgb(color)
        return f'#{int(rgb[0]/256*0.8):02x}{int(rgb[1]/256*0.8):02x}{int(rgb[2]/256*0.8*0.8):02x}'

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.captured_x = None
        self.captured_y = None
        self.position_captured = False
        self.is_running = False
        self.selected_folder = None
        self.save_dir = "images4"  # Default save directory
        
        # For tab change animation
        self.active_tab_bg = '#e3f2fd'  # Light blue background for active tab
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure('Modern.TLabelframe', padding=10, relief="flat")
        style.configure('Modern.TButton', padding=5, font=('Segoe UI', 10))
        style.configure('Modern.TLabel', font=('Segoe UI', 10))
        style.configure('Modern.TEntry', padding=5)
        style.configure('Modern.TCheckbutton', font=('Segoe UI', 10))
        style.configure('Modern.TNotebook', background='#f8f9fa')
        style.configure('Modern.TNotebook.Tab', padding=[20, 5], font=('Segoe UI', 9))
        style.map('TNotebook.Tab', background=[('selected', self.active_tab_bg)])
        
    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root, style='Modern.TNotebook')
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Capture Tab
        capture_tab = ttk.Frame(self.notebook)
        self.notebook.add(capture_tab, text="📸 Capture")
        
        # Process Tab
        process_tab = ttk.Frame(self.notebook)
        self.notebook.add(process_tab, text="🔄 Process Images")
        
        # Bind tab change event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)
        
        self.setup_capture_tab(capture_tab)
        self.setup_process_tab(process_tab)
        
    def on_tab_change(self, event):
        current_tab = self.notebook.select()
        tab_id = self.notebook.index(current_tab)
        
        # Flash effect for tab change
        def flash():
            if tab_id == 0:
                self.text_log.see(tk.END)
            else:
                self.process_log.see(tk.END)
                
        self.root.after(100, flash)

    def setup_capture_tab(self, parent):
        # Main container with padding
        main_container = ttk.Frame(parent, padding="20")
        main_container.pack(fill="both", expand=True)
        
        # Position capture frame
        frame_position = ttk.LabelFrame(main_container, text="📷 Capture Position", 
                                      style='Modern.TLabelframe')
        frame_position.pack(fill="x", pady=(0, 15))
        
        # Capture button
        self.btn_capture = HoverButton(frame_position, text="🎯 Capture Position",
                                   command=self.capture_position,
                                   font=('Segoe UI', 11, 'bold'),
                                   bg='#2196F3', fg='white',
                                   relief='flat', padx=20, pady=10,
                                   cursor="hand2")
        self.btn_capture.pack(padx=10, pady=15)
        
        self.lbl_countdown = ttk.Label(frame_position,
                                     text="Ready to capture position ⏳",
                                     style='Modern.TLabel')
        self.lbl_countdown.pack(padx=10, pady=5)
        
        self.lbl_position = ttk.Label(frame_position, text="Position: Not set 📍",
                                    style='Modern.TLabel')
        self.lbl_position.pack(padx=10, pady=5)
        
        # Lock position checkbox
        self.lock_var = tk.BooleanVar()
        check_lock = ttk.Checkbutton(frame_position, text="🔒 Lock Position",
                                    variable=self.lock_var,
                                    style='Modern.TCheckbutton')
        check_lock.pack(padx=10, pady=10)
        
        # Settings frame
        frame_settings = ttk.LabelFrame(main_container, text="⚙️ Settings",
                                      style='Modern.TLabelframe')
        frame_settings.pack(fill="x", pady=(0, 15))
        
        # Save directory selection
        save_frame = ttk.Frame(frame_settings)
        save_frame.pack(fill="x", padx=15, pady=(10,5))
        
        ttk.Label(save_frame, text="Save Directory:",
                 style='Modern.TLabel').pack(side="left", padx=(0,10))
        self.save_dir_label = ttk.Label(save_frame, text="images4",
                                      style='Modern.TLabel', foreground='gray')
        self.save_dir_label.pack(side="left", fill="x", expand=True)
        
        browse_save = HoverButton(save_frame, text="Browse", bg='#2196F3', fg='white',
                              command=self.browse_save_dir, font=('Segoe UI', 9),
                              relief='flat', padx=15, pady=5)
        browse_save.pack(side="right", padx=5)
        
        # Settings grid
        settings_grid = ttk.Frame(frame_settings)
        settings_grid.pack(padx=15, pady=10, fill="x")
        
        ttk.Label(settings_grid, text="Number of Clicks:",
                 style='Modern.TLabel').grid(row=0, column=0, padx=(0,10), pady=10)
        self.entry_clicks = ttk.Entry(settings_grid, width=12)
        self.entry_clicks.grid(row=0, column=1, padx=10, pady=10)
        self.entry_clicks.insert(0, "29")
        
        ttk.Label(settings_grid, text="Start Index:",
                 style='Modern.TLabel').grid(row=0, column=2, padx=(20,10), pady=10)
        self.entry_start_index = ttk.Entry(settings_grid, width=12)
        self.entry_start_index.grid(row=0, column=3, padx=10, pady=10)
        self.entry_start_index.insert(0, "71")
        
        # Control buttons frame
        buttons_frame = ttk.Frame(main_container)
        buttons_frame.pack(fill="x", pady=15)
        
        # Start button
        self.btn_start = HoverButton(buttons_frame, text="▶ START",
                                 bg="red", fg="white",
                                 font=('Segoe UI', 12, 'bold'),
                                 relief='flat', padx=30, pady=12,
                                 command=self.thread_start_capture,
                                 state="disabled",
                                 cursor="hand2")
        self.btn_start.pack(side="left", padx=5, expand=True)
        
        # Stop button
        self.btn_stop = HoverButton(buttons_frame, text="⏹ STOP",
                               bg="#32CD32", fg="white",
                               font=('Segoe UI', 12, 'bold'),
                               relief='flat', padx=30, pady=12,
                               command=self.stop_capture,
                               state="disabled",
                               cursor="hand2")
        self.btn_stop.pack(side="left", padx=5, expand=True)
        
        # Log area
        log_frame = ttk.LabelFrame(main_container, text="📋 Activity Log",
                                 style='Modern.TLabelframe')
        log_frame.pack(fill="both", expand=True, pady=(5, 0))
        
        self.text_log = tk.Text(log_frame, height=12, 
                               font=('Segoe UI', 9),
                               bg='#fafafa', 
                               relief='flat',
                               padx=10, pady=10)
        self.text_log.pack(fill="both", expand=True, padx=5, pady=5)
        self.text_log.insert(tk.END, "📝 Ready to start capturing...\n")
        
        scrollbar = ttk.Scrollbar(self.text_log, orient="vertical",
                                command=self.text_log.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_log.configure(yscrollcommand=scrollbar.set)

    def browse_save_dir(self):
        directory = filedialog.askdirectory(title="Select Save Directory",
                                          initialdir=os.getcwd())
        if directory:
            self.save_dir = directory
            self.save_dir_label.config(text=os.path.basename(directory))
            self.log_message(f"📁 Save directory set to: {directory}")

    def setup_process_tab(self, parent):
        main_container = ttk.Frame(parent, padding="20")
        main_container.pack(fill="both", expand=True)
        
        # Input Folder Selection Frame
        folder_frame = ttk.LabelFrame(main_container, text="📁 Input/Output Folders", 
                                    style='Modern.TLabelframe')
        folder_frame.pack(fill="x", pady=(0, 15))
        
        # Input folder selection
        input_frame = ttk.Frame(folder_frame)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Input Folder:", 
                 style='Modern.TLabel').pack(side="left", padx=(0, 10))
        self.folder_label = ttk.Label(input_frame, text="No folder selected", 
                                    style='Modern.TLabel', foreground='gray')
        self.folder_label.pack(side="left", fill="x", expand=True)
        
        browse_btn = HoverButton(input_frame, text="Browse", bg='#2196F3', fg='white',
                               command=self.browse_folder, font=('Segoe UI', 9),
                               relief='flat', padx=15, pady=5)
        browse_btn.pack(side="right", padx=5)
        
        # Text color selection
        color_frame = ttk.Frame(folder_frame)
        color_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(color_frame, text="Text Color:", 
                 style='Modern.TLabel').pack(side="left", padx=(0, 10))
        self.text_color_var = tk.StringVar(value="white")
        color_entry = ttk.Entry(color_frame, textvariable=self.text_color_var, width=10)
        color_entry.pack(side="left")
        
        # Output folders info
        info_frame = ttk.Frame(folder_frame)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(info_frame, text="Output folders will be created:", 
                 style='Modern.TLabel').pack(anchor="w", pady=(5,0))
        ttk.Label(info_frame, text="• 'crop' - For cropped images", 
                 style='Modern.TLabel', foreground='gray').pack(anchor="w")
        ttk.Label(info_frame, text="• 'work' - For combined images", 
                 style='Modern.TLabel', foreground='gray').pack(anchor="w")

        # Progress Frame
        progress_frame = ttk.LabelFrame(main_container, text="📊 Progress", 
                                      style='Modern.TLabelframe')
        progress_frame.pack(fill="x", pady=(0, 15))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                          maximum=100, mode='determinate')
        self.progress_bar.pack(fill="x", padx=10, pady=10)
        
        self.progress_label = ttk.Label(progress_frame, text="Waiting to start...",
                                      style='Modern.TLabel')
        self.progress_label.pack(padx=10, pady=(0, 10))
        
        # Process button
        self.process_btn = HoverButton(main_container, text="🔄 Process Images",
                                     bg="#4CAF50", fg="white",
                                     font=('Segoe UI', 12, 'bold'),
                                     relief='flat', padx=30, pady=12,
                                     command=self.thread_process_images,
                                     state="disabled",
                                     cursor="hand2")
        self.process_btn.pack(pady=15)
        
        # Log area
        log_frame = ttk.LabelFrame(main_container, text="📋 Processing Log",
                                 style='Modern.TLabelframe')
        log_frame.pack(fill="both", expand=True)
        
        self.process_log = tk.Text(log_frame, height=12,
                                 font=('Segoe UI', 9),
                                 bg='#fafafa',
                                 relief='flat',
                                 padx=10, pady=10)
        self.process_log.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.process_log, orient="vertical",
                                command=self.process_log.yview)
        scrollbar.pack(side="right", fill="y")
        self.process_log.configure(yscrollcommand=scrollbar.set)
        
        self.process_log.insert(tk.END, "📝 Select an input folder to begin processing...\n")

    def update_progress(self, value, text):
        self.progress_var.set(value)
        self.progress_label.config(text=text)
        self.root.update_idletasks()

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder",
                                       initialdir=os.getcwd())
        if folder:
            self.selected_folder = folder
            self.folder_label.config(text=os.path.basename(folder))
            self.process_btn.config(state="normal")
            self.log_process(f"Selected folder: {folder}")
            
            # Create output directories
            crop_dir = os.path.join(folder, "crop")
            work_dir = os.path.join(folder, "work")
            os.makedirs(crop_dir, exist_ok=True)
            os.makedirs(work_dir, exist_ok=True)
            self.log_process(f"📁 Created output directories:\n- {os.path.basename(crop_dir)}\n- {os.path.basename(work_dir)}")

    def log_process(self, message):
        self.process_log.insert(tk.END, message + "\n")
        self.process_log.see(tk.END)
        self.root.update_idletasks()

    def process_images(self):
        """Process images by cropping and combining them into groups of 10."""
        if not self.selected_folder:
            self.log_process("❌ No folder selected!")
            self.process_btn.config(state="normal")
            return

        self.process_btn.config(state="disabled")
        self.update_progress(0, "Starting...")

        try:
            # Define directories
            input_dir = self.selected_folder
            crop_dir = os.path.join(input_dir, "crop")
            work_dir = os.path.join(input_dir, "work")
            os.makedirs(crop_dir, exist_ok=True)
            os.makedirs(work_dir, exist_ok=True)
            self.log_process(f"📁 Using directories:\n- Input: {input_dir}\n- Crop: {crop_dir}\n- Work: {work_dir}")

            # List and sort PNG images numerically
            image_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.png') and f[:-4].isdigit()]
            if not image_files:
                self.log_process("❌ No sequentially numbered PNG images found!")
                self.update_progress(0, "Processing failed")
                self.process_btn.config(state="normal")
                return
            image_files.sort(key=lambda f: int(f[:-4]))
            total_images = len(image_files)
            self.log_process(f"🔍 Found {total_images} images: {', '.join(image_files[:5])}{'...' if total_images > 5 else ''}")

            # Crop images and collect paths
            cropped_images = []
            self.log_process("\n📷 Cropping images...")
            for i, img_file in enumerate(image_files, 1):
                number = img_file[:-4]  # Extract number, e.g., '1' from '1.png'
                input_path = os.path.join(input_dir, img_file)
                output_path = os.path.join(crop_dir, f"c_{number}.png")
                try:
                    with Image.open(input_path) as img:
                        width, height = img.size
                        left, top, right, bottom = 0, 320, width - 514, height - 208
                        if right <= left or bottom <= top:
                            self.log_process(f"⚠️ Skipping {img_file}: Invalid dimensions")
                            continue
                        cropped_img = img.crop((left, top, right, bottom))
                        cropped_img.save(output_path)
                        cropped_images.append((int(number), output_path))
                        self.log_process(f"✅ Cropped: {img_file} -> c_{number}.png")
                except Exception as e:
                    self.log_process(f"❌ Error cropping {img_file}: {str(e)}")
                progress = (i / total_images) * 50
                self.update_progress(progress, f"Cropping image {i}/{total_images}")

            if not cropped_images:
                self.log_process("❌ No images were successfully cropped!")
                self.update_progress(0, "Processing failed")
                self.process_btn.config(state="normal")
                return

            # Sort cropped images by number to ensure ascending order
            cropped_images.sort(key=lambda x: x[0])
            cropped_paths = [path for _, path in cropped_images]

            # Determine cropped image height (assuming all are the same)
            with Image.open(cropped_paths[0]) as first_cropped:
                h_cropped = first_cropped.height

            # Group into chunks of 10 and combine
            chunk_size = 10
            number_of_chunks = (len(cropped_paths) + chunk_size - 1) // chunk_size
            self.log_process(f"\n📚 Combining images into {number_of_chunks} chunks...")
            for chunk_index in range(number_of_chunks):
                start = chunk_index * chunk_size
                end = start + chunk_size
                chunk = cropped_paths[start:end]
                chunk_name = f"cb_{chunk_index + 1}.png"
                self.log_process(f"📚 Creating {chunk_name} from {len(chunk)} images...")
                try:
                    # Load images in the chunk
                    images = []
                    for crop_path in chunk:
                        try:
                            images.append(Image.open(crop_path))
                        except Exception as e:
                            self.log_process(f"❌ Error loading {os.path.basename(crop_path)}: {str(e)}")
                    if not images:
                        self.log_process(f"⚠️ No images in chunk {chunk_index + 1}, skipping.")
                        continue

                    # Create combined image
                    max_width = max(img.width for img in images)
                    combined_height = chunk_size * h_cropped  # Fixed height for 10 images
                    combined = Image.new('RGB', (max_width, combined_height), color='white')
                    y_offset = 0
                    for img in images:
                        combined.paste(img, (0, y_offset))
                        y_offset += h_cropped
                    output_path = os.path.join(work_dir, chunk_name)
                    combined.save(output_path)
                    self.log_process(f"✅ Created combined image: {chunk_name}")

                    # Clean up
                    for img in images:
                        img.close()

                    # Update progress (50% to 100% during combining)
                    progress = 50 + ((chunk_index + 1) / number_of_chunks) * 50
                    self.update_progress(progress, f"Combining chunk {chunk_index + 1}/{number_of_chunks}")
                except Exception as e:
                    self.log_process(f"❌ Error creating {chunk_name}: {str(e)}")

            self.update_progress(100, "Processing completed!")
            self.log_process("\n✅ Processing completed successfully!")
        except Exception as e:
            self.log_process(f"\n❌ Unexpected error: {str(e)}")
            self.update_progress(0, "Processing failed")
        finally:
            self.process_btn.config(state="normal")

    def thread_process_images(self):
        self.process_btn.config(state="disabled")
        self.log_process("⏳ Starting image processing...")
        t = threading.Thread(target=self.process_images)
        t.daemon = True
        t.start()

    def stop_capture(self):
        self.is_running = False
        self.btn_stop.config(state="disabled")
        self.btn_start.config(state="normal")
        self.log_message("⏹ Process stopped by user")

    def log_message(self, message):
        self.text_log.insert(tk.END, message + "\n")
        self.text_log.see(tk.END)
        self.root.update_idletasks()

    def capture_position(self):
        self.btn_capture.config(state="disabled")
        countdown = 10

        def update_countdown():
            nonlocal countdown
            if countdown > 0:
                self.lbl_countdown.config(
                    text=f"Capturing position in {countdown} seconds... ⏳")
                countdown -= 1
                self.root.after(1000, update_countdown)
            else:
                pos = pyautogui.position()
                self.captured_x, self.captured_y = pos[0], pos[1]
                self.position_captured = True
                self.lbl_position.config(
                    text=f"Position: ({self.captured_x}, {self.captured_y}) 📍")
                self.log_message(
                    f"Captured position: ({self.captured_x}, {self.captured_y})")
                self.btn_start.config(state="normal")
                
                if self.lock_var.get():
                    self.btn_capture.config(state="disabled")
                    self.log_message("🔒 Position fixed!")
                else:
                    self.btn_capture.config(state="normal")
            
        update_countdown()

    def start_capture(self):
        if not self.position_captured or self.captured_x is None or self.captured_y is None:
            self.log_message("❌ Position not set! Please capture the position first.")
            return

        try:
            number_of_clicks = int(self.entry_clicks.get())
            start_index = int(self.entry_start_index.get())
            
            if number_of_clicks <= 0 or start_index < 0:
                self.log_message("❌ Please enter positive numbers for settings!")
                return
                
        except ValueError:
            self.log_message("❌ Please enter valid numbers for settings!")
            return

        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.btn_capture.config(state="disabled")
        self.entry_clicks.config(state="disabled")
        self.entry_start_index.config(state="disabled")
        
        self.is_running = True
        os.makedirs(self.save_dir, exist_ok=True)
        self.log_message(f"📁 Using save directory: {self.save_dir}")
        self.log_message("⏳ Process will start in 10 seconds! Switch to your target window...")
        time.sleep(10)
        
        try:
            for i in range(number_of_clicks):
                if not self.is_running:
                    break
                    
                current_index = start_index + i
                pyautogui.click(self.captured_x, self.captured_y)
                self.log_message(f"📍 Clicked at ({self.captured_x}, {self.captured_y}) - Index {current_index}")
                time.sleep(2)
                
                try:
                    screenshot = pyautogui.screenshot()
                    screenshot_path = os.path.join(self.save_dir, f"{current_index}.png")
                    screenshot.save(screenshot_path)
                    self.log_message(f"💾 Screenshot saved as {current_index}.png")
                except Exception as e:
                    self.log_message(f"❌ Error saving screenshot {current_index}: {str(e)}")
                    continue
                    
                time.sleep(1)
                
            if self.is_running:
                self.log_message("✅ Screenshot capture completed!")
                self.notebook.select(1)  # Switch to Process tab
                self.selected_folder = self.save_dir
                self.folder_label.config(text=os.path.basename(self.save_dir))
                self.process_btn.config(state="normal")
                self.log_process(f"📁 Ready to process images from: {self.save_dir}")
                
        except Exception as e:
            self.log_message(f"❌ Error during capture: {str(e)}")
        finally:
            self.is_running = False
            self.btn_start.config(state="normal")
            self.btn_stop.config(state="disabled")
            if not self.lock_var.get():
                self.btn_capture.config(state="normal")
            self.entry_clicks.config(state="normal")
            self.entry_start_index.config(state="normal")

    def thread_start_capture(self):
        t = threading.Thread(target=self.start_capture)
        t.daemon = True
        t.start()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("✨ Screenshot Capture & Process Tool")
    root.geometry("650x750")
    root.configure(bg='#f8f9fa')
    root.resizable(True, True)
    
    try:
        root.iconbitmap("icon.ico")
    except:
        pass
    
    app = ScreenshotApp(root)
    root.mainloop()

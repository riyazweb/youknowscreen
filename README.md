# ✨ Prakah Exam Screenshot Capture & Process Tool - Made by Riyaz 📸🔄

[![Made by Riyaz with Python](https://img.shields.io/badge/Made%20by-Riyaz%20with%20Python-blueviolet.svg)](https://www.python.org/)

This Python GUI application, created by Riyaz, is specifically designed to help you capture and process screenshots for the Prakah exam or similar online assessments. It automates the process of taking screenshots of a specific screen position, which can be invaluable for documenting your progress during the exam. It also includes tools to process these images afterwards.

## 🚀 Key Features for Prakah Exam Prep

*   **🎯 Precise Position Capture for Exam Windows:**  Accurately select the area of the screen relevant to your Prakah exam tasks.
*   **⏱️ Countdown for Exam Readiness:**  Get mentally prepared with a countdown before screenshot capture begins, ensuring you are focused on the exam window.
*   **🔒 Lock Position for Consistent Exam Screenshots:** Securely lock the capture position to maintain consistency throughout your Prakah exam session.
*   **⚙️ Customizable for Exam Needs:** Adjust the number of screenshots and starting index to match the documentation requirements of the Prakah exam.
*   **📁 Organized Save Directory for Exam Evidence:** Keep your Prakah exam screenshots neatly organized in a designated folder.
*   **🔄 Image Processing for Review and Submission:** Crop and combine screenshots to create a comprehensive record of your Prakah exam work for review or submission purposes.
*   **📊 Progress Tracking During Processing:** Monitor the image processing steps to ensure all your Prakah exam screenshots are handled correctly.
*   **📋 Detailed Logs for Exam Documentation:**  Maintain a clear record of each screenshot captured and processing step, useful for audit trails or personal review of your Prakah exam process.
*   **🎨 User-Friendly Interface for Stress-Free Exam Prep:**  Designed for ease of use, so you can focus on your Prakah exam without wrestling with complex tools.

## 🛠️ Installation for Prakah Exam Tool

1.  **Clone the repository (if applicable):**
    ```bash
    git clone [repository-url]
    cd [repository-directory]
    ```

2.  **Run `make.bat` to install dependencies and launch the Prakah Exam Tool:**
    Double-click on the `make.bat` file. This will:
    *   Install essential Python packages (`Pillow` and `pyautogui`) required for the tool.
    *   Execute `aapp.pyw` to start the Prakah Exam Screenshot Capture & Process Tool.

    Alternatively, for manual installation:

    ```bash
    pip install Pillow
    pip install pyautogui
    pythonw aapp.pyw
    ```

## ⚙️ Using the Prakah Exam Tool

### 📸 Capture Tab - Setting Up for Your Prakah Exam Screenshots

1.  **Capture Exam Window Position:**
    *   Click **🎯 Capture Position**.
    *   A 10-second countdown starts. Immediately switch to your Prakah exam window.
    *   After countdown, the tool records the mouse position within your exam window as **Position: (X, Y) 📍**. This is where screenshots will be taken.
    *   For consistent screenshots during your exam, check **🔒 Lock Position**.

2.  **Exam Screenshot Settings:**
    *   **Number of Clicks:**  Enter how many screenshots you anticipate needing for your Prakah exam documentation (e.g., `29`).
    *   **Start Index:** Set a starting number for your screenshot filenames (e.g., `71`). Files will be named `71.png`, `72.png`, and so on, which can be helpful for referencing specific exam stages.
    *   **Save Directory:** Screenshots will be saved in `images4` by default.  For better organization of your Prakah exam files, use **Browse** to select a dedicated folder for your exam screenshots.

3.  **Start/Stop Exam Screenshot Capture:**
    *   Click **▶ START** just before you begin a section of your Prakah exam where screenshots are needed. Be ready to switch to your exam window as a 10-second delay is initiated.
    *   Use **⏹ STOP** to halt the screenshot process if needed during your Prakah exam.

4.  **Activity Log - Monitoring Your Exam Screenshots:** The **📋 Activity Log** shows each screenshot taken, confirming that the tool is capturing your Prakah exam progress.

### 🔄 Process Images Tab - Reviewing and Compiling Prakah Exam Screenshots

1.  **Select Prakah Exam Screenshot Folder:**
    *   Click **Browse** to choose the folder where you saved your Prakah exam screenshots.
    *   The tool will create `crop` and `work` subfolders within this folder to organize processed images.

2.  **Text Color (Future Feature for Prakah Exam Notes):**
    *   *(Currently inactive)* In future versions, this might allow you to add notes to your Prakah exam screenshots (feature not in current script).

3.  **Process Exam Screenshots:**
    *   Click **🔄 Process Images** after your Prakah exam session to process the screenshots.
    *   The tool will:
        *   Crop each `.png` exam screenshot to focus on relevant content.
        *   Save cropped images in the `crop` subfolder, ready for focused review.
        *   Combine all cropped exam screenshots into `combined_all.png` in the `work` folder. This provides a single, continuous view of your Prakah exam work.

4.  **Progress & Processing Log - Ensuring Complete Processing of Exam Screenshots:** The **📊 Progress Bar** and **📋 Processing Log** let you track the progress of processing your Prakah exam screenshots, ensuring no steps are missed.

## 📦 Dependencies for Prakah Exam Tool

*   **Python:**  Ensure Python is installed to run the Prakah Exam Tool.
*   **Pillow (PIL):**  Python Imaging Library, essential for processing Prakah exam screenshots.
    ```bash
    pip install Pillow
    ```
*   **PyAutoGUI:**  Used for automating screenshot capture during your Prakah exam.
    ```bash
    pip install pyautogui
    ```

## 📜 License

[Optional: Add your license information here, e.g., MIT License]

## 🙏 Contributions & Feedback for Prakah Exam Tool Improvement

[Optional:  Mention if you welcome contributions and how to contribute, or feedback on how to make it more useful for the Prakah exam]

---

**Good luck with your Prakah exam! Let this tool by Riyaz help you document your success!** 🎉

@echo off
echo --------------------------------------
echo Installing required Python packages...
echo --------------------------------------

pip install --upgrade pip
pip install Pillow
pip install pyautogui
pip install google-generativeai
pip install opencv-python
pip install numpy
pip install keyboard
echo --------------------------------------
echo All packages installed successfully!
echo --------------------------------------

echo Running the application...
python app.py

echo --------------------------------------
echo Application closed.
echo Press any key to exit...
pause >nul

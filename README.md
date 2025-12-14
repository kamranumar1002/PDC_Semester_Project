PDC Audio Processing Dashboard
This project is a web application designed to process batches of audio files. Its main purpose is to demonstrate the performance difference between running tasks serially (one-by-one) versus in parallel (all at once using multiple CPU cores).
✅ Prerequisites
Before you begin, you need to have a few essential tools installed on your computer.
Git: To download the project from GitHub.
Download Git Here
To check if it's installed, open a terminal and run: git --version
Python (Version 3.8 or newer): The backend is built with Python.
Download Python Here
Important: During installation on Windows, make sure to check the box that says "Add Python to PATH".
To check if it's installed, run: python --version
Node.js (Version 18 or newer): The frontend interactive dashboard uses this.
Download Node.js Here
To check if it's installed, run: node -v
⚙️ Step-by-Step Setup Guide
Follow these steps exactly. We will set up the Backend first, then the Frontend.
Step 1: Get the Project Code
Open your terminal (Command Prompt, PowerShell, or Git Bash) and run this command to download the project folder to your computer.
code
Bash
git clone [URL_OF_YOUR_GITHUB_REPOSITORY]
cd pdc_project # Or whatever your root folder is called
Step 2: Backend Setup (The "Brain")
The backend handles all the audio processing logic. We need to run it in its own terminal.
Navigate to the Backend Folder:
code
Bash
cd pdc_audio_dashboard
Create a Virtual Environment: This creates a clean, isolated space for our project's Python libraries.
On Windows: python -m venv venv
On Mac/Linux: python3 -m venv venv
Activate the Environment: You must do this every time you work on the project.
On Windows: venv\Scripts\activate
On Mac/Linux: source venv/bin/activate
(You should see (venv) appear at the start of your terminal line).
Install Python Libraries: This command reads the requirements.txt file and installs all necessary libraries at once.
code
Bash
pip install -r requirements.txt
Set Up the Database: This creates the database file needed to track experiments.
code
Bash
python manage.py migrate
Run the Backend Server:
code
Bash
python manage.py runserver
If it works, you will see text ending with Starting development server at http://127.0.0.1:8000/.
Leave this terminal running! Do not close it.
Step 3: Frontend Setup (The "Face")
The frontend is the website you interact with. It needs to run in a separate terminal.
Open a NEW Terminal Window.
Navigate to the Frontend Folder:
code
Bash
cd pdc_project # Go back to the root folder first
cd frontend
Install Frontend Packages: This downloads all the libraries needed for the user interface.
code
Bash
npm install
Run the Frontend Server:
code
Bash
npm run dev
If it works, you will see a message with a Local URL, usually http://localhost:5173.
Step 4: Final System Setup (FFmpeg for Audio)
The audio processing library (pydub) needs a helper tool called FFmpeg.
On Windows:
Download the ffmpeg-essentials.zip file here.
Extract the ZIP file somewhere you won't delete it (e.g., C:\ffmpeg).
Copy the path to the bin folder inside (e.g., C:\ffmpeg\bin).
Add this path to your Windows "System Environment Variables". (Here is a guide on how to do that).
On Mac (using Homebrew):
code
Bash
brew install ffmpeg
🖥️ How to Use the Application
If you have completed all the steps, you should have two terminals running.
Open your web browser (Chrome, Firefox, etc.).
Go to the frontend URL from Step 3: http://localhost:5173.
Upload Files: Drag and drop at least 8 audio files (.wav or .mp3) into the upload box.
Run Serial: Click the "START" button for "Serial Processing". Watch the CPU visualizer and note the time it takes.
Run Parallel: Click the "START" button for "Parallel Processing". Watch all the cores light up and see how much faster it is.
Check Results: The speedup factor will appear, and you can Play or Download the processed files from the table at the bottom.
🐛 Troubleshooting
'python' is not recognized...: Python was not added to your PATH during installation. Reinstall it and make sure to check the "Add to PATH" box.
Play/Download buttons don't work: Make sure the backend server (in the first terminal) is running and doesn't show any errors.
Parallel is NOT faster than Serial!: This is expected if you only use 1-2 small files. The cost of starting up the parallel workers is high. The speedup is only visible with more files (8+) and/or larger files.
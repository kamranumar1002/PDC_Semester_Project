# 🚀 PDC Audio Processing Dashboard

This project is a web application designed to process batches of audio files. Its main purpose is to demonstrate the performance difference between running tasks **serially** (one-by-one) versus **in parallel** (all at once using multiple CPU cores).

## ✅ Prerequisites

Before you begin, you need to have a few essential tools installed on your computer.

1.  **Git:** To download the project from GitHub.
    *   [Download Git Here](https://git-scm.com/downloads)
    *   To check if it's installed, open a terminal and run: `git --version`

2.  **Python (Version 3.8 or newer):** The backend is built with Python.
    *   [Download Python Here](https://www.python.org/downloads/)
    *   **Important:** During installation on Windows, make sure to check the box that says **"Add Python to PATH"**.
    *   To check if it's installed, run: `python --version`

3.  **Node.js (Version 18 or newer):** The frontend interactive dashboard uses this.
    *   [Download Node.js Here](https://nodejs.org/en)
    *   To check if it's installed, run: `node -v`

---

## ⚙️ Step-by-Step Setup Guide

Follow these steps exactly. We will set up the Backend first, then the Frontend.

### Step 1: Get the Project Code

Open your terminal (Command Prompt, PowerShell, or Git Bash) and run this command to download the project folder to your computer.

```bash
git clone [URL_OF_YOUR_GITHUB_REPOSITORY]
cd pdc_project # Or whatever your root folder is called
```

### Step 2: Backend Setup (The "Brain")

The backend handles all the audio processing logic. We need to run it in its own terminal.

1.  **Navigate to the Backend Folder:**
    ```bash
    cd pdc_audio_dashboard
    ```

2.  **Create a Virtual Environment:** This creates a clean, isolated space for our project's Python libraries.
    *   **On Windows:** `python -m venv venv`
    *   **On Mac/Linux:** `python3 -m venv venv`

3.  **Activate the Environment:** You must do this every time you work on the project.
    *   **On Windows:** `venv\Scripts\activate`
    *   **On Mac/Linux:** `source venv/bin/activate`
    *(You should see `(venv)` appear at the start of your terminal line).*

4.  **Install Python Libraries:** This command reads the `requirements.txt` file and installs all necessary libraries at once.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set Up the Database:** This creates the database file needed to track experiments.
    ```bash
    python manage.py migrate
    ```

6.  **Run the Backend Server:**
    ```bash
    python manage.py runserver
    ```
    If it works, you will see text ending with `Starting development server at http://127.0.0.1:8000/`.

    **Leave this terminal running!** Do not close it.

### Step 3: Frontend Setup (The "Face")

The frontend is the website you interact with. It needs to run in a **separate** terminal.

1.  **Open a NEW Terminal Window.**

2.  **Navigate to the Frontend Folder:**
    ```bash
    cd pdc_project # Go back to the root folder first
    cd frontend
    ```

3.  **Install Frontend Packages:** This downloads all the libraries needed for the user interface.
    ```bash
    npm install
    ```

4.  **Run the Frontend Server:**
    ```bash
    npm run dev
    ```
    If it works, you will see a message with a **Local URL**, usually `http://localhost:5173`.

### Step 4: Final System Setup (FFmpeg for Audio)

The audio processing library (`pydub`) needs a helper tool called **FFmpeg**.

*   **On Windows:**
    1.  [Download the ffmpeg-essentials.zip file here](https://www.gyan.dev/ffmpeg/builds/).
    2.  Extract the ZIP file somewhere you won't delete it (e.g., `C:\ffmpeg`).
    3.  Copy the path to the `bin` folder inside (e.g., `C:\ffmpeg\bin`).
    4.  Add this path to your Windows "System Environment Variables". ([Here is a guide on how to do that](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)).

*   **On Mac (using Homebrew):**
    ```bash
    brew install ffmpeg
    ```

---

## 🖥️ How to Use the Application

If you have completed all the steps, you should have **two terminals running**.

1.  Open your web browser (Chrome, Firefox, etc.).
2.  Go to the frontend URL from Step 3: **`http://localhost:5173`**.
3.  **Upload Files:** Drag and drop at least **8 audio files** (`.wav` or `.mp3`) into the upload box.
4.  **Run Serial:** Click the "START" button for "Serial Processing". Watch the CPU visualizer and note the time it takes.
5.  **Run Parallel:** Click the "START" button for "Parallel Processing". Watch all the cores light up and see how much faster it is.
6.  **Check Results:** The speedup factor will appear, and you can Play or Download the processed files from the table at the bottom.

---

## 🐛 Troubleshooting

*   **`'python' is not recognized...`**: Python was not added to your PATH during installation. Reinstall it and make sure to check the "Add to PATH" box.
*   **Play/Download buttons don't work**: Make sure the backend server (in the first terminal) is running and doesn't show any errors.
*   **Parallel is NOT faster than Serial!**: This is expected if you only use 1-2 small files. The cost of starting up the parallel workers is high. The speedup is only visible with **more files (8+)** and/or **larger files**.
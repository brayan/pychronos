# PyChronos

**PyChronos** is a minimalist timer desktop app built with PyQt5. It guides your workflow with dynamic colors and beeps based on the current time. The app follows a fixed cycle:

- **IN_PROGRESS (00:00 to 40:00)**: Work phase (Blue background, startup beep)
- **LAST_MINUTES (40:01 to 49:59)**: Final minutes of work (Red background)
- **BREAK (50:00 to 59:59)**: Break time (Green background, break beep)

## Features

- Fixed-size floating window (always on top)
- Large digital timer display
- Color-coded background based on session status
- Toggleable sound (🔊/🔇)
- Draggable interface
- Frameless window for distraction-free workflow

## Logic Summary

The app divides each hour into two zones:

- **Work:** `00:00` to `49:59`
  - **Last 10 minutes of work:** from `40:01` onward
- **Break:** `50:00` to `59:59`

Each second, the UI checks the current system time and:
- Updates the countdown timer
- Changes background color based on the status
- Plays a **startup beep** at the beginning of the IN_PROGRESS phase
- Plays a **break beep** when transitioning to BREAK

## How to Run

```bash
git clone https://github.com/brayan/pychronos.git
cd pychronos
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/pychronos/__main__.py

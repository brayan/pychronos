import os
import subprocess
import sys

sound_enabled = True


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, "resources", relative_path)


BEEP_STARTED_PATH = resource_path("beep_started.wav")
BEEP_FINISHED_PATH = resource_path("beep_finished.wav")


def play_beep_started():
    if sound_enabled:
        subprocess.Popen(["afplay", BEEP_STARTED_PATH])


def play_beep_finished():
    if sound_enabled:
        subprocess.Popen(["afplay", BEEP_FINISHED_PATH])


def toggle_sound() -> bool:
    global sound_enabled
    sound_enabled = not sound_enabled
    return sound_enabled

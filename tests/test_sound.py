import unittest
from unittest.mock import patch

import pychronos.sound as sound_module


class TestSoundModule(unittest.TestCase):

    def test_resource_path(self):
        relative = "file.wav"
        with patch("pychronos.sound.os.path.abspath", return_value="/fake/base"):
            path = sound_module.resource_path(relative)
            self.assertEqual(path, "/fake/base/resources/file.wav")

    @patch("pychronos.sound.subprocess.Popen")
    def test_play_beep_started(self, mock_popen):
        sound_module.sound_enabled = True
        sound_module.BEEP_STARTED_PATH = "mock_beep_started.wav"
        sound_module.play_beep_started()
        mock_popen.assert_called_once_with(["afplay", "mock_beep_started.wav"])

    @patch("pychronos.sound.subprocess.Popen")
    def test_play_beep_finished(self, mock_popen):
        sound_module.sound_enabled = True
        sound_module.BEEP_FINISHED_PATH = "mock_beep_finished.wav"
        sound_module.play_beep_finished()
        mock_popen.assert_called_once_with(["afplay", "mock_beep_finished.wav"])

    def test_toggle_sound(self):
        original_state = sound_module.sound_enabled
        new_state = sound_module.toggle_sound()
        self.assertNotEqual(original_state, new_state)
        self.assertEqual(sound_module.toggle_sound(), original_state)


if __name__ == '__main__':
    unittest.main()

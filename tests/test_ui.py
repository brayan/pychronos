import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from pychronos.ui import ChronosWindow
from pychronos.constants import IN_PROGRESS, LAST_MINUTES, BREAK

app = QApplication([])


class TestChronosWindow(unittest.TestCase):

    @patch("pychronos.ui.calculate_timer", return_value=(10, 5))
    @patch("pychronos.ui.get_status", return_value=IN_PROGRESS)
    @patch("pychronos.ui.play_beep_started")
    @patch("pychronos.ui.play_beep_finished")
    def test_update_timer_logic(self, mock_finished, mock_started, mock_status, mock_timer):
        window = ChronosWindow()
        window.last_status = BREAK
        window.update_timer()

        self.assertEqual(window.time_label.text(), "10:05")
        self.assertIn("background-color: #80B3FF", window.styleSheet())
        self.assertEqual(mock_started.call_count, 3)
        mock_finished.assert_not_called()

    @patch("pychronos.ui.toggle_sound", return_value=False)
    def test_handle_toggle_sound_mute(self, mock_toggle):
        window = ChronosWindow()
        window.handle_toggle_sound()
        self.assertEqual(window.sound_toggle.text(), "🔇")

    @patch("pychronos.ui.toggle_sound", return_value=True)
    def test_handle_toggle_sound_unmute(self, mock_toggle):
        window = ChronosWindow()
        window.handle_toggle_sound()
        self.assertEqual(window.sound_toggle.text(), "🔊")

    def test_mouse_drag_updates_position(self):
        window = ChronosWindow()
        start_pos = window.pos()
        mock_event = MagicMock()
        mock_event.button.return_value = 1
        mock_event.globalPos.return_value = start_pos + window.pos()

        window.mousePressEvent(mock_event)
        window.mouseMoveEvent(mock_event)
        window.mouseReleaseEvent(mock_event)
        self.assertIsNone(window.old_pos)


if __name__ == '__main__':
    unittest.main()

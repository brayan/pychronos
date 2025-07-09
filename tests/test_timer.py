import unittest

from PyQt5.QtCore import QDateTime

from pychronos.constants import IN_PROGRESS, LAST_MINUTES, BREAK
from pychronos.timer import get_status, calculate_timer


class TestTimerLogic(unittest.TestCase):

    def dt(self, minute, second=0):
        return QDateTime.fromString(f"2000-01-01T00:{minute:02}:{second:02}", "yyyy-MM-ddThh:mm:ss")

    def test_in_progress_initial_minute(self):
        self.assertEqual(get_status(self.dt(0, 0)), IN_PROGRESS)

    def test_in_progress_normal_case(self):
        self.assertEqual(get_status(self.dt(25, 30)), IN_PROGRESS)

    def test_last_minutes_exactly_41_minutes(self):
        self.assertEqual(get_status(self.dt(41, 0)), LAST_MINUTES)

    def test_last_minutes_edge_case(self):
        self.assertEqual(get_status(self.dt(40, 1)), LAST_MINUTES)

    def test_in_progress_edge_case_just_before_last_minutes(self):
        self.assertEqual(get_status(self.dt(40, 0)), IN_PROGRESS)

    def test_break_period(self):
        self.assertEqual(get_status(self.dt(50, 0)), BREAK)

    def test_break_period_end_of_hour(self):
        self.assertEqual(get_status(self.dt(59, 59)), BREAK)

    def test_calculate_timer_start_of_work(self):
        minutes, seconds = calculate_timer(self.dt(0, 0))
        self.assertEqual((minutes, seconds), (50, 0))

    def test_calculate_timer_middle_of_work(self):
        minutes, seconds = calculate_timer(self.dt(10, 30))
        self.assertEqual((minutes, seconds), (39, 30))

    def test_calculate_timer_last_second_before_break(self):
        minutes, seconds = calculate_timer(self.dt(49, 59))
        self.assertEqual((minutes, seconds), (0, 1))

    def test_calculate_timer_break_period(self):
        minutes, seconds = calculate_timer(self.dt(50, 0))
        self.assertEqual((minutes, seconds), (10, 0))

    def test_calculate_timer_second_wraparound(self):
        minutes, seconds = calculate_timer(self.dt(49, 0))
        self.assertEqual((minutes, seconds), (1, 0))

    def test_calculate_timer_handles_60_second_wrap(self):
        minutes, seconds = calculate_timer(self.dt(49, 59))
        self.assertEqual((minutes, seconds), (0, 1))

    def test_calculate_timer_rounds_up_to_next_minute(self):
        minutes, seconds = calculate_timer(self.dt(10, 0))
        self.assertEqual((minutes, seconds), (40, 0))


if __name__ == '__main__':
    unittest.main()

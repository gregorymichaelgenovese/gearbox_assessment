import unittest
from unittest.mock import patch

from assessment import Gearbox
from assessment.engine import Engine
from assessment.types import Mode, Gear, Action


class TestGearbox(unittest.TestCase):

    def test_auto_shift_not_needed(self):
        Engine.running = True
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.THREE
        Gearbox.auto_shift(rpm=1500)
        self.assertEqual(Gearbox.gear.value, 3)

    def test_auto_shift_up(self):
        Engine.running = True
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.TWO
        Gearbox.auto_shift(rpm=3000)
        self.assertEqual(Gearbox.gear.value, 3)

    def test_auto_shift_up_at_max_gear(self):
        Engine.running = True
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.FIVE
        Gearbox.auto_shift(rpm=3000)
        self.assertEqual(Gearbox.gear.value, 5)

    def test_auto_shift_down(self):
        Engine.running = True
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.THREE
        Gearbox.auto_shift(rpm=1200)
        self.assertEqual(Gearbox.gear.value, 2)

    def test_auto_shift_down_at_min_gear(self):
        Engine.running = True
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.ONE
        Gearbox.auto_shift(rpm=1200)
        self.assertEqual(Gearbox.gear.value, 1)

    def test_friendly_mode(self):
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.ONE
        self.assertEqual(Gearbox.friendly_mode(), "D1")

        Gearbox.mode = Mode.MANUAL
        Gearbox.gear = Gear.TWO
        self.assertEqual(Gearbox.friendly_mode(), "M2")

        Gearbox.mode = Mode.NEUTRAL
        Gearbox.gear = Gear.NEUTRAL
        self.assertEqual(Gearbox.friendly_mode(), "N")

        Gearbox.mode = Mode.REVERSE
        Gearbox.gear = Gear.REVERSE
        self.assertEqual(Gearbox.friendly_mode(), "R")

        Gearbox.mode = Mode.PARK
        Gearbox.gear = Gear.NEUTRAL
        self.assertEqual(Gearbox.friendly_mode(), "P")


class TestGearboxShifting(unittest.TestCase):

    # misc
    @patch("assessment.gearbox.n_print")
    def test_shift_without_engine_running(self, mock_n_print):
        Gearbox.mode = Mode.PARK
        Gearbox.gear = Gear.NEUTRAL
        Gearbox.parking_pawl_engaged = True
        Gearbox.shift(action=Action.REVERSE, engine_running=False)
        self.assertEqual(Gearbox.mode, Mode.PARK)
        self.assertEqual(Gearbox.gear, Gear.NEUTRAL)
        self.assertEqual(Gearbox.parking_pawl_engaged, True)
        mock_n_print.assert_called_once_with("please start the car first!")

    # reverse
    def test_shift_into_reverse_from_drive(self):
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.ONE
        Gearbox.shift(action=Action.REVERSE, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.REVERSE)
        self.assertEqual(Gearbox.gear, Gear.REVERSE)

    def test_shift_into_reverse_from_neutral(self):
        Gearbox.mode = Mode.NEUTRAL
        Gearbox.gear = Gear.NEUTRAL
        Gearbox.shift(action=Action.REVERSE, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.REVERSE)
        self.assertEqual(Gearbox.gear, Gear.REVERSE)

    def test_shift_into_reverse_from_park(self):
        Gearbox.mode = Mode.PARK
        Gearbox.gear = Gear.NEUTRAL
        Gearbox.parking_pawl_engaged = True
        Gearbox.shift(action=Action.REVERSE, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.REVERSE)
        self.assertEqual(Gearbox.gear, Gear.REVERSE)
        self.assertEqual(Gearbox.parking_pawl_engaged, False)

    def test_shift_into_reverse_from_improper_state(self):
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.TWO
        Gearbox.shift(action=Action.REVERSE, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.DRIVE)
        self.assertEqual(Gearbox.gear, Gear.TWO)

    # neutral
    def test_shift_into_neutral_from_drive(self):
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.ONE
        Gearbox.shift(action=Action.NEUTRAL, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.NEUTRAL)
        self.assertEqual(Gearbox.gear, Gear.NEUTRAL)

    def test_shift_into_neutral_from_reverse(self):
        Gearbox.mode = Mode.REVERSE
        Gearbox.gear = Gear.REVERSE
        Gearbox.shift(action=Action.NEUTRAL, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.NEUTRAL)
        self.assertEqual(Gearbox.gear, Gear.NEUTRAL)

    def test_shift_into_neutral_from_park(self):
        Gearbox.mode = Mode.PARK
        Gearbox.gear = Gear.NEUTRAL
        Gearbox.parking_pawl_engaged = True
        Gearbox.shift(action=Action.NEUTRAL, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.NEUTRAL)
        self.assertEqual(Gearbox.gear, Gear.NEUTRAL)
        self.assertEqual(Gearbox.parking_pawl_engaged, False)

    @patch("assessment.gearbox.n_print")
    def test_shift_into_neutral_from_improper_state(self, mock_n_print):
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.TWO
        Gearbox.shift(action=Action.NEUTRAL, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.DRIVE)
        self.assertEqual(Gearbox.gear, Gear.TWO)
        mock_n_print.assert_called_once_with(
            "please put the car into first gear or reverse before switching to neutral!"
        )

    # park
    def test_shift_into_park_from_park(self):
        Gearbox.mode = Mode.PARK
        Gearbox.gear = Gear.NEUTRAL
        Gearbox.parking_pawl_engaged = True
        Gearbox.shift(action=Action.PARK, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.PARK)
        self.assertEqual(Gearbox.gear, Gear.NEUTRAL)
        self.assertEqual(Gearbox.parking_pawl_engaged, True)

    def test_shift_into_park_from_drive(self):
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.ONE
        Gearbox.parking_pawl_engaged = False
        Gearbox.shift(action=Action.PARK, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.PARK)
        self.assertEqual(Gearbox.gear, Gear.NEUTRAL)
        self.assertEqual(Gearbox.parking_pawl_engaged, True)

    def test_shift_into_park_from_neutral(self):
        Gearbox.mode = Mode.NEUTRAL
        Gearbox.gear = Gear.NEUTRAL
        Gearbox.parking_pawl_engaged = False
        Gearbox.shift(action=Action.PARK, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.PARK)
        self.assertEqual(Gearbox.gear, Gear.NEUTRAL)
        self.assertEqual(Gearbox.parking_pawl_engaged, True)

    def test_shift_into_park_from_reverse(self):
        Gearbox.mode = Mode.REVERSE
        Gearbox.gear = Gear.REVERSE
        Gearbox.parking_pawl_engaged = False
        Gearbox.shift(action=Action.PARK, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.PARK)
        self.assertEqual(Gearbox.gear, Gear.NEUTRAL)
        self.assertEqual(Gearbox.parking_pawl_engaged, True)

    @patch("assessment.gearbox.n_print")
    def test_shift_into_park_from_improper_state(self, mock_n_print):
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.TWO
        Gearbox.parking_pawl_engaged = False
        Gearbox.shift(action=Action.PARK, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.DRIVE)
        self.assertEqual(Gearbox.gear, Gear.TWO)
        self.assertEqual(Gearbox.parking_pawl_engaged, False)
        mock_n_print.assert_called_once_with(
            "please put the car into neutral, first gear or reverse before parking!"
        )

    # drive
    def test_shift_into_drive_from_drive(self):
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.TWO
        Gearbox.shift(action=Action.DRIVE, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.DRIVE)
        self.assertEqual(Gearbox.gear, Gear.TWO)

    def test_shift_into_drive_from_neutral(self):
        Gearbox.mode = Mode.NEUTRAL
        Gearbox.gear = Gear.NEUTRAL
        Gearbox.shift(action=Action.DRIVE, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.DRIVE)
        self.assertEqual(Gearbox.gear, Gear.ONE)

    def test_shift_into_drive_from_reverse(self):
        Gearbox.mode = Mode.REVERSE
        Gearbox.gear = Gear.REVERSE
        Gearbox.shift(action=Action.DRIVE, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.DRIVE)
        self.assertEqual(Gearbox.gear, Gear.ONE)

    def test_shift_into_drive_from_park(self):
        Gearbox.mode = Mode.PARK
        Gearbox.gear = Gear.NEUTRAL
        Gearbox.parking_pawl_engaged = True
        Gearbox.shift(action=Action.DRIVE, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.DRIVE)
        self.assertEqual(Gearbox.gear, Gear.ONE)
        self.assertEqual(Gearbox.parking_pawl_engaged, False)

    # manual
    def test_shift_into_manual_from_manual(self):
        Gearbox.mode = Mode.MANUAL
        Gearbox.gear = Gear.TWO
        Gearbox.shift(action=Action.MANUAL, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.MANUAL)
        self.assertEqual(Gearbox.gear, Gear.TWO)

    def test_shift_into_manual_from_drive(self):
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.ONE
        Gearbox.shift(action=Action.MANUAL, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.MANUAL)
        self.assertEqual(Gearbox.gear, Gear.ONE)

    @patch("assessment.gearbox.n_print")
    def test_shift_into_manual_from_improper_state(self, mock_n_print):
        Gearbox.mode = Mode.NEUTRAL
        Gearbox.gear = Gear.NEUTRAL
        Gearbox.shift(action=Action.MANUAL, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.NEUTRAL)
        self.assertEqual(Gearbox.gear, Gear.NEUTRAL)
        mock_n_print.assert_called_once_with("please put the car into drive first!")

    # up
    def test_shift_up(self):
        Gearbox.mode = Mode.MANUAL
        Gearbox.gear = Gear.ONE
        Gearbox.shift(action=Action.UP, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.MANUAL)
        self.assertEqual(Gearbox.gear, Gear.TWO)

    def test_shift_up_at_max_gear(self):
        Gearbox.mode = Mode.MANUAL
        Gearbox.gear = Gear.FIVE
        Gearbox.shift(action=Action.UP, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.MANUAL)
        self.assertEqual(Gearbox.gear, Gear.FIVE)

    @patch("assessment.gearbox.n_print")
    def test_shift_up_outside_manual_mode(self, mock_n_print):
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.TWO
        Gearbox.shift(action=Action.UP, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.DRIVE)
        self.assertEqual(Gearbox.gear, Gear.TWO)
        mock_n_print.assert_called_once_with("please put the car into manual first!")

    # down
    def test_shift_down(self):
        Gearbox.mode = Mode.MANUAL
        Gearbox.gear = Gear.TWO
        Gearbox.shift(action=Action.DOWN, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.MANUAL)
        self.assertEqual(Gearbox.gear, Gear.ONE)

    def test_shift_down_at_min_gear(self):
        Gearbox.mode = Mode.MANUAL
        Gearbox.gear = Gear.ONE
        Gearbox.shift(action=Action.DOWN, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.MANUAL)
        self.assertEqual(Gearbox.gear, Gear.ONE)

    @patch("assessment.gearbox.n_print")
    def test_shift_down_outside_manual_mode(self, mock_n_print):
        Gearbox.mode = Mode.DRIVE
        Gearbox.gear = Gear.TWO
        Gearbox.shift(action=Action.DOWN, engine_running=True)
        self.assertEqual(Gearbox.mode, Mode.DRIVE)
        self.assertEqual(Gearbox.gear, Gear.TWO)
        mock_n_print.assert_called_once_with("please put the car into manual first!")


if __name__ == "__main__":
    unittest.main()

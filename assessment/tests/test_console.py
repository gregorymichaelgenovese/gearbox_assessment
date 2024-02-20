import unittest
from unittest.mock import patch

from assessment import Console, Gearbox
from assessment.engine import Engine
from assessment.types import Mode, Action, Gear


class TestConsole(unittest.TestCase):

    # exit
    @patch("assessment.console.print_n")
    def test_exit(self, mock_print_n):
        with patch.object(Console, "get_input", return_value="exit"):
            Engine.running = False
            Gearbox.mode = Mode.PARK
            Gearbox.gear = Gear.NEUTRAL
            exit_command_received = Console.user_input(engine=Engine, gearbox=Gearbox)
            self.assertTrue(exit_command_received)
            mock_print_n.assert_called_once_with("exiting vehicle....")

    @patch("assessment.console.print_n")
    def test_exit_with_engine_running(self, mock_print_n):
        Console.allow_unmanned_idle = True
        with patch.object(Console, "get_input", return_value="exit"):
            Engine.running = True
            Gearbox.mode = Mode.PARK
            Gearbox.gear = Gear.NEUTRAL
            exit_command_received = Console.user_input(engine=Engine, gearbox=Gearbox)
            self.assertTrue(exit_command_received)
            mock_print_n.assert_called_once_with("exiting vehicle....")

    @patch("assessment.console.n_print")
    def test_exit_with_engine_running_without_allow_unmanned_idle(self, mock_n_print):
        Console.allow_unmanned_idle = False
        with patch.object(Console, "get_input", return_value="exit"):
            Engine.running = True
            Gearbox.mode = Mode.PARK
            Gearbox.gear = Gear.NEUTRAL
            exit_command_received = Console.user_input(engine=Engine, gearbox=Gearbox)
            self.assertTrue(not exit_command_received)
            mock_n_print.assert_called_once_with(
                "please Park and Stop the engine before exiting!"
            )

    @patch("assessment.console.n_print")
    def test_exit_with_engine_running_allow_unmanned_idle_not_parked(
        self, mock_n_print
    ):
        Console.allow_unmanned_idle = True
        with patch.object(Console, "get_input", return_value="exit"):
            Engine.running = True
            Gearbox.mode = Mode.DRIVE
            Gearbox.gear = Gear.ONE
            exit_command_received = Console.user_input(engine=Engine, gearbox=Gearbox)
            self.assertTrue(not exit_command_received)
            mock_n_print.assert_called_once_with("please Park the car before exiting!")

    # start
    def test_start(self):
        with patch.object(Console, "get_input", return_value="start"):
            Engine.running = False
            Gearbox.mode = Mode.PARK
            Gearbox.gear = Gear.NEUTRAL
            Console.user_input(engine=Engine, gearbox=Gearbox)
            self.assertTrue(Engine.running)

    # stop
    def test_stop(self):
        with patch.object(Console, "get_input", return_value="stop"):
            Engine.running = True
            Gearbox.mode = Mode.PARK
            Gearbox.gear = Gear.NEUTRAL
            Console.user_input(engine=Engine, gearbox=Gearbox)
            self.assertTrue(not Engine.running)

    @patch("assessment.console.n_print")
    def test_stop_from_improper_state(self, mock_n_print):
        with patch.object(Console, "get_input", return_value="stop"):
            Engine.running = True
            Gearbox.mode = Mode.DRIVE
            Gearbox.gear = Gear.ONE
            Console.user_input(engine=Engine, gearbox=Gearbox)
            self.assertTrue(Engine.running)
            mock_n_print.assert_called_once_with(
                "please put the car into park before shutting down the engine!"
            )

    # up
    def test_up(self):
        with patch.object(Console, "get_input", return_value="up"):
            with patch.object(Gearbox, "shift") as mock_shift:
                Engine.running = True
                Console.user_input(engine=Engine, gearbox=Gearbox)
                mock_shift.assert_called_once()
                mock_shift.assert_called_with(action=Action.UP, engine_running=True)

    # down
    def test_down(self):
        with patch.object(Console, "get_input", return_value="down"):
            with patch.object(Gearbox, "shift") as mock_shift:
                Engine.running = True
                Console.user_input(engine=Engine, gearbox=Gearbox)
                mock_shift.assert_called_once()
                mock_shift.assert_called_with(action=Action.DOWN, engine_running=True)

    # drive
    def test_drive(self):
        with patch.object(Console, "get_input", return_value="drive"):
            with patch.object(Gearbox, "shift") as mock_shift:
                Engine.running = True
                Console.user_input(engine=Engine, gearbox=Gearbox)
                mock_shift.assert_called_once()
                mock_shift.assert_called_with(action=Action.DRIVE, engine_running=True)

    # manual
    def test_manual(self):
        with patch.object(Console, "get_input", return_value="manual"):
            with patch.object(Gearbox, "shift") as mock_shift:
                Engine.running = True
                Console.user_input(engine=Engine, gearbox=Gearbox)
                mock_shift.assert_called_once()
                mock_shift.assert_called_with(action=Action.MANUAL, engine_running=True)

    # park
    def test_park(self):
        with patch.object(Console, "get_input", return_value="park"):
            with patch.object(Gearbox, "shift") as mock_shift:
                Engine.running = True
                Console.user_input(engine=Engine, gearbox=Gearbox)
                mock_shift.assert_called_once()
                mock_shift.assert_called_with(action=Action.PARK, engine_running=True)

    # neutral
    def test_neutral(self):
        with patch.object(Console, "get_input", return_value="neutral"):
            with patch.object(Gearbox, "shift") as mock_shift:
                Engine.running = True
                Console.user_input(engine=Engine, gearbox=Gearbox)
                mock_shift.assert_called_once()
                mock_shift.assert_called_with(
                    action=Action.NEUTRAL, engine_running=True
                )

    # reverse
    def test_reverse(self):
        with patch.object(Console, "get_input", return_value="reverse"):
            with patch.object(Gearbox, "shift") as mock_shift:
                Engine.running = True
                Console.user_input(engine=Engine, gearbox=Gearbox)
                mock_shift.assert_called_once()
                mock_shift.assert_called_with(
                    action=Action.REVERSE, engine_running=True
                )

    @patch("assessment.console.n_print")
    # invalid
    def test_invalid_input(self, mock_n_print):
        with patch.object(Console, "get_input", return_value="someinvalidinput"):
            with patch.object(Gearbox, "shift") as mock_shift:
                Engine.running = True
                Console.user_input(engine=Engine, gearbox=Gearbox)
                mock_shift.assert_not_called()
                mock_n_print.assert_called_once_with("invalid input")


if __name__ == "__main__":
    unittest.main()

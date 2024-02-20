from collections import OrderedDict

from assessment.helper import n_print, print_n, clear
from assessment.types import Mode, Action


def exit_vehicle(engine, parked: bool, **kwargs):
    """Exit the vehicle
    :return: True if able to exit else False"""
    warning = ""
    if Console.allow_unmanned_idle:
        if not parked:
            warning = "please Park the car before exiting!"
    elif engine.running:
        warning = "please Park and Stop the engine before exiting!"

    if warning:
        n_print(warning)
    else:
        clear()
        print_n("exiting vehicle....")
        return True
    return False


def start(engine, **kwargs):
    if not engine.running:
        engine.start()


def stop(engine, parked: bool, **kwargs):
    if not parked:
        n_print("please put the car into park before shutting down the engine!")
    else:
        if engine.running:
            engine.stop()


def up(engine, gearbox, **kwargs):
    gearbox.shift(action=Action.UP, engine_running=engine.running)


def down(engine, gearbox, **kwargs):
    gearbox.shift(action=Action.DOWN, engine_running=engine.running)


def drive(engine, gearbox, **kwargs):
    gearbox.shift(action=Action.DRIVE, engine_running=engine.running)


def manual(engine, gearbox, **kwargs):
    gearbox.shift(action=Action.MANUAL, engine_running=engine.running)


def park(engine, gearbox, **kwargs):
    gearbox.shift(action=Action.PARK, engine_running=engine.running)


def neutral(engine, gearbox, **kwargs):
    gearbox.shift(action=Action.NEUTRAL, engine_running=engine.running)


def reverse(engine, gearbox, **kwargs):
    gearbox.shift(action=Action.REVERSE, engine_running=engine.running)


class Console:
    """Process user input"""

    allow_unmanned_idle = True

    COMMANDS = OrderedDict(
        {
            "start": start,
            "stop": stop,
            "park": park,
            "drive": drive,
            "manual": manual,
            "neutral": neutral,
            "reverse": reverse,
            "up": up,
            "down": down,
            "exit": exit_vehicle,
        }
    )
    AVAILABLE_COMMANDS = list(COMMANDS.keys())
    AVAILABLE_COMMANDS_LINE = ", ".join([_.title() for _ in AVAILABLE_COMMANDS])

    @staticmethod
    def get_input() -> str:  # pragma: no cover
        return input(f"Commands: {Console.AVAILABLE_COMMANDS_LINE}\n").lower()

    @staticmethod
    def user_input(engine, gearbox) -> bool:
        """
        Check for user actions

        :param: engine : the Engine object
        :param: gearbox : the Gearbox object

        :return: True if exit command issued by user else False
        """
        user_input = Console.get_input()
        parked = gearbox.mode == Mode.PARK

        if user_input in Console.AVAILABLE_COMMANDS:
            received_exit_command = Console.COMMANDS[user_input](
                engine=engine, gearbox=gearbox, parked=parked
            )
            if received_exit_command:
                return True
        else:
            n_print("invalid input")

        return False

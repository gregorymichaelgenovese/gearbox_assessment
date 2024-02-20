from assessment.helper import n_print
from assessment.types import Mode, Action, Gear


class Gearbox:
    """Main transmission class"""

    parking_pawl_engaged = False

    downshift_rpm_threshold = 1200
    upshift_rpm_threshold = 3000

    mode = Mode.PARK  # current state gearbox is in
    gear = Gear.NEUTRAL  # current gear gearbox is in
    max_gear = Gear(max([_.value for _ in Gear]))

    @staticmethod
    def auto_shift(rpm: int) -> None:
        """
        Auto shift when hitting rpm thresholds in Drive mode

        :param: rpm : current Engine rpm
        """
        if rpm >= Gearbox.upshift_rpm_threshold:
            # if the user attempts to shift up or down at max or min gear, do nothing
            if Gearbox.gear != Gearbox.max_gear:
                Gearbox.shift(engine_running=True, action=Action.UP, auto_shift=True)
        elif rpm <= Gearbox.downshift_rpm_threshold:
            if Gearbox.gear != Gear.ONE:
                Gearbox.shift(engine_running=True, action=Action.DOWN, auto_shift=True)

    @staticmethod
    def friendly_mode() -> str:
        """Returns a string repr of the current gearbox mode which is nice to look at"""
        friendly_mode_name = str(Gearbox.mode).split(".")[1][0]
        if Gearbox.mode in [
            Mode.DRIVE,
            Mode.MANUAL,
        ]:
            # display the current gear when in Drive or Manual mode
            friendly_mode_name += str(Gearbox.gear.value)
        return friendly_mode_name

    @staticmethod
    def shift(engine_running: bool, action: Action, auto_shift: bool = False) -> None:
        """
        Process actions from the user or the auto shifter to change modes or shift gears

        :param: engine_running : is the engine running
        :param: action : a Gearbox.Action which either the user or automated system can issue
        :auto_shift: is this a command issued by the automated system
        """
        if not engine_running:
            n_print("please start the car first!")
            return

        # reverse
        if action == Action.REVERSE:
            if Gearbox.gear not in [
                Gear.NEUTRAL,
                Gear.ONE,
            ]:
                return
            Gearbox.mode = Mode.REVERSE
            Gearbox.gear = Gear.REVERSE
            Gearbox.parking_pawl_engaged = False

        # neutral
        elif action == Action.NEUTRAL:
            if Gearbox.mode != Mode.PARK and Gearbox.gear not in [
                Gear.REVERSE,
                Gear.ONE,
            ]:
                n_print(
                    "please put the car into first gear or reverse before switching to neutral!"
                )
                return
            Gearbox.mode = Mode.NEUTRAL
            Gearbox.gear = Gear.NEUTRAL
            Gearbox.parking_pawl_engaged = False

        # park
        elif action == Action.PARK:
            if Gearbox.mode == Mode.PARK:
                return
            if Gearbox.gear not in [
                Gear.REVERSE,
                Gear.NEUTRAL,
                Gear.ONE,
            ]:
                n_print(
                    "please put the car into neutral, first gear or reverse before parking!"
                )
                return
            Gearbox.mode = Mode.PARK
            Gearbox.gear = Gear.NEUTRAL
            Gearbox.parking_pawl_engaged = True

        # drive
        elif action == Action.DRIVE:
            if Gearbox.mode == Mode.DRIVE:
                return
            if Gearbox.mode != Mode.MANUAL:
                Gearbox.gear = Gear.ONE
            Gearbox.mode = Mode.DRIVE
            Gearbox.parking_pawl_engaged = False

        # manual
        elif action == Action.MANUAL:
            if Gearbox.mode == Mode.MANUAL:
                return
            if Gearbox.mode != Mode.DRIVE:
                n_print("please put the car into drive first!")
                return
            Gearbox.mode = Mode.MANUAL

        # up
        elif action == Action.UP:
            if not auto_shift and Gearbox.mode != Mode.MANUAL:
                n_print("please put the car into manual first!")
                return
            if Gearbox.gear == Gear.FIVE:
                return
            Gearbox.gear = Gear(Gearbox.gear.value + 1)

        # down
        elif action == Action.DOWN:
            if not auto_shift and Gearbox.mode != Mode.MANUAL:
                n_print("please put the car into manual first!")
                return
            if Gearbox.gear == Gear.ONE:
                return
            Gearbox.gear = Gear(Gearbox.gear.value - 1)

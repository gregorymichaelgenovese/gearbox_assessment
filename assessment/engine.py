from .helper import print_n, clear

from assessment import Console, Gearbox
from assessment.types import Mode


class Engine:
    """Engine class which simulates a running car engine"""

    running = False
    rpm = 0

    @staticmethod
    def start() -> None:
        """Start the car engine"""
        Engine.running = True
        # set rpm to midrange for simulating a running engine ready to be manually shifted
        Engine.rpm = 1500

    @staticmethod
    def stop() -> None:
        """Stop the car engine"""
        Engine.running = False
        Engine.rpm = 0

    @staticmethod
    def run() -> None:  # pragma: no cover
        """Simulate a running engine which pings the Gearbox and Console for shifting and input respectively"""
        try:
            while True:
                clear()
                if Engine.running:
                    if Gearbox.mode == Mode.DRIVE:
                        Gearbox.auto_shift(rpm=Engine.rpm)
                    print_n(f"engine running: gear [{Gearbox.friendly_mode()}]")
                else:
                    print_n("engine at rest")

                received_exit_command = Console.user_input(
                    engine=Engine, gearbox=Gearbox
                )

                if received_exit_command:
                    return
        except Exception as e:
            print(
                f"encountered exception: {str(e)}"
            )  # TODO :: log exception to proper db or filesystem
            raise e

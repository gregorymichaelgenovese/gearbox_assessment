import unittest

from assessment.engine import Engine


class TestEngine(unittest.TestCase):

    def test_start(self):
        Engine.running = False
        Engine.rpm = 0
        Engine.start()
        self.assertTrue(Engine.running)
        self.assertEqual(Engine.rpm, 1500)

    def test_stop(self):
        Engine.running = True
        Engine.rpm = 1500
        Engine.stop()
        self.assertTrue(not Engine.running)
        self.assertEqual(Engine.rpm, 0)


if __name__ == "__main__":
    unittest.main()

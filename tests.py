import unittest
import demoblaze as run


class DemoblazePositiveTestCases(unittest.TestCase):  # create class

    @staticmethod  # signal to Unittest that this is a static method
    def test_demoblaze():
        run.setUp()
        run.sign_up()
        run.log_in()
        run.checkout_cart()
        run.log_out()
        run.tearDown()

import unittest
from library_mixed import *

class Test_Reservation_Template(unittest.TestCase):
    def setUp(self):
        self.res_1 = Reservation_Template(5, 15, 'atlas', 'Kevin')
        self.res_2 = Reservation_Template(2, 14, 'atlas', 'Buzz')
        self.res_3 = Reservation_Template(30, 50, 'atlas', 'Frank')
        self.res_4 = Reservation_Template(10, 80, 'atlas', 'Uncle Frank')
        self.res_5 = Reservation_Template(10, 12, 'atlas', 'Helen')
        self.res_6 = Reservation_Template(15, 18, 'atlas', 'Colin')
        self.res_7 = Reservation_Template(15, 18, 'harry potter', 'Megan')
        self.res_8 = Reservation_Template(1, 5, 'atlas', 'Marph')

    def test_overlapping(self):
        self.assertTrue(self.res_1.overlapping(self.res_2))
        self.assertFalse(self.res_1.overlapping(self.res_3))
        self.assertTrue(self.res_1.overlapping(self.res_4))
        self.assertTrue(self.res_1.overlapping(self.res_5))
        self.assertTrue(self.res_1.overlapping(self.res_6))
        self.assertTrue(self.res_1.overlapping(self.res_8))
        self.assertFalse(self.res_1.overlapping(self.res_7))
        self.assertFalse(self.res_6.overlapping(self.res_7))
        self.assertFalse(self.res_2.overlapping(self.res_7))

    def test_includes(self):
        self.assertTrue(self.res_1.includes(5))
        self.assertFalse(self.res_1.includes(4))
        self.assertTrue(self.res_1.includes(10))
        self.assertTrue(self.res_1.includes(15))
        self.assertFalse(self.res_1.includes(16))

    def test_identify(self):
        self.assertEqual(self.res_1.identify(5, 'atlas', 'Kevin'), (True, 'true'))
        self.assertEqual(self.res_1.identify(20, 'atlas', 'Kevin'), (False, 'date'))
        self.assertEqual(self.res_1.identify(5, 'Dorian Grey', 'Kevin'), (False, 'book'))
        self.assertEqual(self.res_1.identify(5, 'atlas', 'Megan'), (False, 'for'))

    def test_change_for(self):
        self.assertEqual(self.res_1.change_for('Helen'), None)
        self.assertEqual(self.res_1._for, 'Helen')


if __name__ == '__main__':
    unittest.main()
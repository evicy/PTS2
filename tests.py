import unittest
from library_mixed import *

class Test_Reservation_Template(unittest.TestCase):
    def setUp(self):
        self.res_1 = Reservation_Template(5, 15, 'atlas', 'Kevin')
        self.res_2 = Reservation_Template(2, 14, 'atlas', 'Buzz')
        self.res_3 = Reservation_Template(30, 44, 'atlas', 'Frank')
        self.res_4 = Reservation_Template(15, 18, 'atlas', 'Colin')
        self.res_5 = Reservation_Template(15, 18, 'harry potter', 'Megan')
        self.res_6 = Reservation_Template(10, 80, 'atlas', 'Uncle Frank')

    def tearDown(self):
        pass

    def test_overlapping(self):
        self.assertTrue(self.res_1.overlapping(self.res_2))
        self.assertFalse(self.res_1.overlapping(self.res_3))
        self.assertTrue(self.res_1.overlapping(self.res_4))
        self.assertTrue(self.res_1.overlapping(self.res_6))
        self.assertFalse(self.res_4.overlapping(self.res_5))
        self.assertFalse(self.res_1.overlapping(self.res_5))

    def test_includes(self):
        self.assertTrue(self.res_1.includes(5))
        self.assertTrue(self.res_1.includes(10))
        self.assertTrue(self.res_1.includes(15))
        self.assertFalse(self.res_1.includes(16))

    def test_identify(self):
        self.assertEquals(self.res_1.identify(5, 'atlas', 'Kevin'), (True, 'true'))
        self.assertEquals(self.res_1.identify(20, 'atlas', 'Kevin'), (False, 'date'))
        self.assertEquals(self.res_1.identify(5, 'Dorian Grey', 'Kevin'), (False, 'book'))
        self.assertEquals(self.res_1.identify(5, 'atlas', 'Megan'), (False, 'for'))

    def test_change_for(self):
        self.res_1.change_for('Helen')
        self.assertEquals(self.res_1.identify(5, 'atlas', 'Helen'), (True, 'true'))
        self.assertEquals(self.res_1.identify(5, 'atlas', 'James'), (False, 'for'))



class Test_Library_Template(unittest.TestCase):
    def setUp(self):
        self.lib = Library_Template()
        self.lib.add_user('Kevin')
        self.lib.add_user('Peter')
        self.lib.add_book('a')
        self.lib.add_book('a')
        self.lib.add_book('b')
        self.lib.add_book('c')

    def tearDown(self):
        pass

    def test_add_user(self):
        self.assertFalse(self.lib.add_user('Kevin'))
        self.assertTrue(self.lib.add_user('Lauren'))

    def test_add_book(self):
        self.assertEquals(self.lib.add_book('a'), 3)
        self.assertEquals(self.lib.add_book('d'), 1)

    def test_reserve_book(self):
        self.assertEquals(self.lib.reserve_book('Eva', 'a', 10, 15), (False, 'user'))
        self.assertEquals(self.lib.reserve_book('Kevin', 'a', 15, 10), (False, 'date'))
        self.assertEquals(self.lib.reserve_book('Kevin', 'd', 10, 20), (False, 'book'))
        self.assertEquals(self.lib.reserve_book('Kevin', 'd', 10, 20), (False, 'book'))
        self.assertEquals(self.lib.reserve_book('Kevin', 'a', 10, 30), (True, 0))



if __name__ == '__main__':
    unittest.main()

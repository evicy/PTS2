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

    def tearDown(self):
        pass

    def test_overlapping(self):
        self.assertTrue(self.res_1.overlapping(self.res_2))
        self.assertFalse(self.res_1.overlapping(self.res_3))
        self.assertTrue(self.res_1.overlapping(self.res_4))
        self.assertTrue(self.res_1.overlapping(self.res_5))
        self.assertTrue(self.res_1.overlapping(self.res_6))
        self.assertFalse(self.res_1.overlapping(self.res_7))
        self.assertFalse(self.res_6.overlapping(self.res_7))
        self.assertFalse(self.res_2.overlapping(self.res_7))

    def test_includes(self):
        self.assertTrue(self.res_1.includes(5))
        self.assertTrue(self.res_1.includes(10))
        self.assertTrue(self.res_1.includes(15))
        self.assertFalse(self.res_1.includes(16))

    def test_identify(self):
        self.assertEqual(self.res_1.identify(5, 'atlas', 'Kevin'), (True, 'true'))
        self.assertEqual(self.res_1.identify(20, 'atlas', 'Kevin'), (False, 'date'))
        self.assertEqual(self.res_1.identify(5, 'Dorian Grey', 'Kevin'), (False, 'book'))
        self.assertEqual(self.res_1.identify(5, 'atlas', 'Megan'), (False, 'for'))

    def test_change_for(self):
        self.res_1.change_for('Helen')
        self.assertEqual(self.res_1.identify(5, 'atlas', 'Helen'), (True, 'true'))
        self.assertEqual(self.res_1.identify(5, 'atlas', 'James'), (False, 'for'))


class Mock_Reservation(object):
    _ids = count(0)

    def __init__(self, from_, to, book, for_):
        self._id = next(self._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_

    def overlapping(self, other):
        return False

    def includes(self, date):
        return False

    def identify(self, date, book, user):
        return False

    def change_for(self, new_user):
        self._for = new_user


class Mock_Reservation_True_overlapping(Mock_Reservation):
    def overlapping(self, other):
        return True


class Mock_Reservation_True_includes(Mock_Reservation_True_overlapping):
    def includes(self, date):
        return True


class Mock_Reservation_True_identify(Mock_Reservation):
    def identify(self, date, book, user):
        return True

class Test_Library_Template(unittest.TestCase):
    def setUp(self):
        Mock_Reservation._ids = count(0)
        self.lib = Library_Template()
        self.lib._users.add('Kevin')
        self.lib._users.add('Peter')
        self.lib._books['a'] = 2
        self.lib._books['b'] = 1
        self.lib._books['c'] = 1

    def tearDown(self):
        pass

    def test_add_user(self):
        self.assertFalse(self.lib.add_user('Kevin'))
        self.assertTrue(self.lib.add_user('Lauren'))

    def test_add_book(self):
        self.assertEqual(self.lib.add_book('a'), 3)
        self.assertEqual(self.lib.add_book('d'), 1)

    def test_reserve_book(self):
        self.assertEqual(self.lib.reserve_book('Eva', 'a', 10, 15, Mock_Reservation), (False, 'user'))
        self.assertEqual(self.lib.reserve_book('Kevin', 'a', 15, 10, Mock_Reservation), (False, 'date'))
        self.assertEqual(self.lib.reserve_book('Kevin', 'd', 10, 20, Mock_Reservation), (False, 'book'))
        self.assertEqual(self.lib.reserve_book('Peter', 'b', 15, 30, Mock_Reservation), (True, 0))
        Mock_Reservation._ids = count(0)
        self.assertEqual(self.lib.reserve_book('Kevin', 'c', 50, 80, Mock_Reservation_True_includes), (True, 0))
        self.assertEqual(self.lib.reserve_book('Peter', 'c', 50, 80, Mock_Reservation_True_includes), (False, 'reservation'))
        Mock_Reservation._ids = count(0)
        self.assertEqual(self.lib.reserve_book('Kevin', 'a', 10, 30, Mock_Reservation), (True, 0))

    def test_check_reservation_exist(self):
        self.lib._reservations.append(Mock_Reservation_True_identify(5, 10, 'a', 'Kevin'))
        self.assertTrue(self.lib.check_reservation('Kevin', 'a', 6))

    def test_check_reservation_not_exist(self):
        self.lib._reservations.append(Mock_Reservation(5, 10, 'a', 'Peter'))
        self.assertFalse(self.lib.check_reservation('Peter', 'a', 5))

    def test_change_reservation(self):
        self.lib._reservations.append(Mock_Reservation_True_identify(5,10, 'a', 'Kevin'))
        self.lib._users.add('Jane')
        self.assertEqual(self.lib.change_reservation('Kevin', 'a', 10, 'Jane'), (True, 'true'))
        self.assertEqual(self.lib.change_reservation('Kevin', 'a', 10, 'NoUser'), (False, 'new_user'))

    def test_change_reservation_no_relevant_reservation(self):
        self.lib._reservations.append(Mock_Reservation(5,10, 'a', 'Kevin'))
        self.assertEqual(self.lib.change_reservation('Kevin', 'b', 10, 'NoUser'), (False, 'reservation'))

class MockPrinter(object):
    def print(self, string):
        self.string = string

class Test_Reservation_String_builder(unittest.TestCase):
    def setUp(self):
        self.res_1 = Reservation(5, 15, 'atlas', 'Kevin', MockPrinter)

    def tearDown(self):
        pass

    def test_includes(self):
        self.res_1.includes(10)
        self.assertEqual(self.res_1.printer.string, F'Reservation {self.res_1._id} includes 10')
        self.res_1.includes(1)
        self.assertEqual(self.res_1.printer.string, F'Reservation {self.res_1._id} does not include 1')

    def test_identify(self):
        self.res_1.identify(10, 'Dorian Grey', 'Kevin')
        self.assertEqual(self.res_1.printer.string,
                         F'Reservation {self.res_1._id} reserves {self.res_1._book} not Dorian Grey.')
        self.res_1.identify(12, 'atlas', 'Uncle Frank')
        self.assertEqual(self.res_1.printer.string,
                         F'Reservation {self.res_1._id} is for {self.res_1._for} not Uncle Frank.')
        self.res_1.identify(20, 'atlas', 'Kevin')
        self.assertEqual(self.res_1.printer.string,
                         F'Reservation {self.res_1._id} is from {self.res_1._from} to {self.res_1._to} which does not include 20.')
        self.res_1.identify(10, 'atlas', 'Kevin')
        self.assertEqual(self.res_1.printer.string,
                         F'Reservation {self.res_1._id} is valid Kevin of atlas on 10.')

class Test_Library_String_builder(unittest.TestCase):
    def setUp(self):
        self.lib = Library(MockPrinter)
        self.lib._users.add('Kevin')

    def tearDown(self):
        pass

    def test_add_user(self):
        self.lib.add_user('Kevin')
        self.assertEqual(self.lib.printer.string, F'User not created, user with name Kevin already exists.')
        self.lib.add_user('Megan')
        self.assertEqual(self.lib.printer.string, F'User Megan created.')

    def test_add_book(self):
        self.lib.add_book('ABC')
        self.assertEqual(self.lib.printer.string, F'Book ABC added. We have 1 coppies of the book.')
        self.lib.add_book('ABC')
        self.assertEqual(self.lib.printer.string, F'Book ABC added. We have 2 coppies of the book.')


if __name__ == '__main__':
    unittest.main()

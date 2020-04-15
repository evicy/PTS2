import unittest
from library_mixed import *

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
    # used for reserve_book - problem with relevant reservations
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

    def test_reserve_book_general(self):
        self.assertEqual(self.lib.reserve_book('Eva', 'a', 10, 15, Mock_Reservation), (False, 'user'))
        self.assertEqual(self.lib.reserve_book('Kevin', 'a', 15, 10, Mock_Reservation), (False, 'date'))
        self.assertEqual(self.lib.reserve_book('Kevin', 'd', 10, 20, Mock_Reservation), (False, 'book'))
        self.assertEqual(self.lib.reserve_book('Peter', 'b', 15, 30, Mock_Reservation), (True, 0))

    def test_reserve_book_problem_with_reservation(self):
        self.lib._reservations.append(Mock_Reservation_True_includes(50, 80, 'c', 'Kevin'))
        self.assertEqual(self.lib.reserve_book('Peter', 'c', 50, 80, Mock_Reservation_True_includes), (False, 'reservation'))

    def test_check_reservation_exist(self):
        self.lib._reservations.append(Mock_Reservation_True_identify(5, 10, 'a', 'Kevin'))
        self.assertTrue(self.lib.check_reservation('Kevin', 'a', 6))

    def test_check_reservation_not_exist(self):
        self.lib._reservations.append(Mock_Reservation(5, 10, 'a', 'Peter'))
        self.assertFalse(self.lib.check_reservation('Peter', 'a', 5))

    def test_change_reservation_general(self):
        self.lib._reservations.append(Mock_Reservation_True_identify(5, 10, 'a', 'Kevin'))
        self.assertEqual(self.lib.change_reservation('Kevin', 'a', 10, 'Peter'), (True, 'true'))
        self.assertEqual(self.lib.change_reservation('Kevin', 'a', 10, 'NoUser'), (False, 'new_user'))

    def test_change_reservation_no_relevant_reservation(self):
        self.lib._reservations.append(Mock_Reservation(5,10, 'a', 'Kevin'))
        self.assertEqual(self.lib.change_reservation('Kevin', 'b', 10, 'NoUser'), (False, 'reservation'))


if __name__ == '__main__':
    unittest.main()

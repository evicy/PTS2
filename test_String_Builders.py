import unittest
from library_mixed import *


class MockPrinter(object):
    def print(self, string):
        self.string = string


class Test_Reservation_String_builder(unittest.TestCase):
    def setUp(self):
        self.res_1 = Reservation(5, 15, 'atlas', 'Kevin', MockPrinter)

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

from itertools import count

class Printer(object):
    def print(self, string):
        print(string)

class Reservation_Template(object):
    _ids = count(0)

    def __init__(self, from_, to, book, for_):
        self._id = next(self._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_
        self._changes = 0

    def overlapping(self, other):
        return (self._book == other._book and self._to >= other._from
                and self._from <= other._to)

    def includes(self, date):
        return (self._from <= date <= self._to)

    def identify(self, date, book, for_):
        if book != self._book:
            return (False, 'book')
        if for_ != self._for:
            return (False, 'for')
        if not self.includes(date):
            return (False, 'date')
        return (True, 'true')

    def change_for(self, for_):
        self._for = for_


class Reservation(Reservation_Template):

    def __init__(self, from_, to, book, for_, printer=Printer):
        self.printer = printer()
        super().__init__(from_, to, book, for_)
        self.printer.print(F'Created a reservation with id {self._id} of {self._book} ' +
                           F'from {self._from} to {self._to} for {self._for}.')

    def overlapping(self, other):
        ret = super(Reservation, self).overlapping(other)
        str = 'do'
        if not ret:
            str = 'do not'
        self.printer.print(self.printer, F'Reservations {self._id} and {other._id} {str} overlap')
        return ret

    def includes(self, date):
        ret = super(Reservation, self).includes(date)
        str = 'includes'
        if not ret:
            str = 'does not include'
        self.printer.print(F'Reservation {self._id} {str} {date}')
        return ret

    def identify(self, date, book, for_):
        ret = super(Reservation, self).identify(date, book, for_)
        if ret[0]:
            self.printer.print(F'Reservation {self._id} is valid {for_} of {book} on {date}.')
        else:
            if ret[1] == 'book': self.printer.print(F'Reservation {self._id} reserves {self._book} not {book}.')
            if ret[1] == 'for': self.printer.print(F'Reservation {self._id} is for {self._for} not {for_}.')
            if ret[1] == 'date': self.printer.print(F'Reservation {self._id} is from {self._from} to {self._to} which ' +
                                                    F'does not include {date}.')
        return ret[0]

    def change_for(self, for_):
        super(Reservation, self).change_for(for_)
        self.printer.print(F'Reservation {self._id} moved from {self._for} to {for_}')


class Library_Template(object):
    def __init__(self):
        self._users = set()
        self._books = {}  # maps name to count
        self._reservations = []  # Reservations sorted by from

    def add_user(self, name):
        if name in self._users:
            return False
        self._users.add(name)
        return True

    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1
        return self._books[name]

    def reserve_book(self, user, book, date_from, date_to, reservation_factory=Reservation):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            return (False, 'user')
        if date_from > date_to:
            return (False, 'date')
        if book_count == 0:
            return (False, 'book')

        desired_reservation = reservation_factory(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]

        # we check that if we add this reservation then for every reservation record that starts
        # between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    return (False, 'reservation')
        self._reservations += [desired_reservation]
        self._reservations.sort(key=lambda x: x._from)  # to lazy to make a getter
        return (True, desired_reservation._id)

    def check_reservation(self, user, book, date):
        return any([res.identify(date, book, user) for res in self._reservations])

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations
                                 if res.identify(date, book, user)]
        if not relevant_reservations:
            return (False, 'reservation')
        if new_user not in self._users:
            return (False, 'new_user')

        relevant_reservations[0].change_for(new_user)
        return (True, 'true')


class Library(Library_Template):
    def __init__(self, printer=Printer):
        self.printer = printer()
        self.printer.print(F'Library created.')
        super(Library, self).__init__()

    def add_user(self, name):
        ret = super(Library, self).add_user(name)
        if ret:
            self.printer.print(F'User {name} created.')
        else:
            self.printer.print(F'User not created, user with name {name} already exists.')
        return ret

    def add_book(self, name):
        ret = super(Library, self).add_book(name)
        self.printer.print(F'Book {name} added. We have {ret} coppies of the book.')

    def reserve_book(self, user, book, date_from, date_to, reservation_factory=Reservation):
        ret = super(Library, self).reserve_book(user, book, date_from, date_to, reservation_factory)
        if ret[0]:
            self.printer.print(F'Reservation {ret[1]} included.')

        else:
            if ret[1] == 'user':
                self.printer.print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                                   F'User does not exist.')

            if ret[1] == 'date':
                self.printer.print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                                   F'Incorrect dates.')

            if ret[1] == 'book':
                self.printer.print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                                   F'We do not have that book.')

            if ret[1] == 'reservation':
                self.printer.print(F'We cannot reserve book {book} for {user} from {date_from} ' +
                                   F'to {date_to}. We do not have enough books.')
        return ret[0]

    def check_reservation(self, user, book, date):
        ret = super(Library, self).check_reservation(user, book, date)
        str = 'exists'
        if not ret:
            str = 'does not exist'
        self.printer.print(F'Reservation for {user} of {book} on {date} {str}.')
        return ret

    def change_reservation(self, user, book, date, new_user):
        ret = super(Library, self).change_reservation(user, book, date, new_user)

        if ret[0]:
            self.printer.print(F'Reservation for {user} of {book} on {date} changed to {new_user}.')
        else:
            if ret[1] == 'reservation':
                self.printer.print(F'Reservation for {user} of {book} on {date} does not exist.')

            if ret[1] == 'new_user':
                self.printer.print(F'Cannot change the reservation as {new_user} does not exist.')

        return ret[0]

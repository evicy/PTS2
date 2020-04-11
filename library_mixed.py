from itertools import count

class Reservation_Template(object):

    def __init__(self, from_, to, book, for_, id):
        self._id = id
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_
        self._changes = 0

    def overlapping(self, other):
        return (self._book == other._book and self._to >= other._from 
               and self._to >= other._from)

    def includes(self, date):
        return (self._from <= date <= self._to)

    def identify(self, date, book, for_):
        pass
    
    def change_for(self, for_):
        self._for = for_

class Reservation_Message(Reservation_Template):

    def __init__(self, from_, to, book, for_, id):
        super().__init__(from_, to, book, for_, id)
        print(F'Created a reservation with id {self._id} of {self._book} ' +
              F'from {self._from} to {self._to} for {self._for}.')

    def overlapping(self, other):
        ret = super(Reservation_Message, self).overlapping(other)
        str = 'do'
        if not ret:
            str = 'do not'
        print(F'Reservations {self._id} and {other._id} {str} overlap')

    def includes(self, date):
        ret = super(Reservation_Message, self).includes(date)
        str = 'includes'
        if not ret:
            str = 'does not include'
        print(F'Reservation {self._id} {str} {date}')

    def identify_book_problem(self, book):
        print(F'Reservation {self._id} reserves {self._book} not {book}.')

    def identify_for_problem(self, for_):
        print(F'Reservation {self._id} is for {self._for} not {for_}.')

    def identify_date_problem(self, date):
        print(F'Reservation {self._id} is from {self._from} to {self._to} which ' +
              F'does not include {date}.')

    def identify(self, date, book, for_):
        print(F'Reservation {self._id} is valid {for_} of {book} on {date}.')

    def change_for(self, for_):
        print(F'Reservation {self._id} moved from {self._for} to {for_}')


class Reservation(Reservation_Template):
    _ids = count(0)
    def __init__(self, from_, to, book, for_):
        id = next(self._ids)
        self.string_constructor = Reservation_Message(from_, to, book, for_, id)
        super().__init__(from_, to, book, for_, id)

    def overlapping(self, other):
        self.string_constructor.overlapping(other)
        return super(Reservation, self).overlapping(other)
            
    def includes(self, date):
        self.string_constructor.includes(date)
        return super(Reservation, self).includes(date)
        
    def identify(self, date, book, for_):
        if book != self._book: 
            self.string_constructor.identify_book_problem(book)
            return False
        if for_!=self._for:
            self.string_constructor.identify_for_problem(for_)
            return False
        if not self.includes(date):
            self.string_constructor.identify_date_problem(date)
            return False
        self.string_constructor.identify(date, book, for_)
        return True
        
    def change_for(self, for_):
        self.string_constructor.change_for(for_)
        super(Reservation, self).change_for(for_)
        

class Library(object):
    def __init__(self):
        self._users = set()
        self._books = {}   #maps name to count
        self._reservations = [] #Reservations sorted by from
        print(F'Library created.')
                
    def add_user(self, name):
        if name in self._users:
            print(F'User not created, user with name {name} already exists.')
            return False
        self._users.add(name)
        print(F'User {name} created.')
        return True

    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1
        print(F'Book {name} added. We have {self._books[name]} coppies of the book.')

    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. '+
                  F'User does not exist.')
            return False
        if date_from > date_to:
            print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. '+
                  F'Incorrect dates.')
            return False
        if book_count == 0:
            print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. '+
                  F'We do not have that book.')
            return False
        desired_reservation = Reservation(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        #we check that if we add this reservation then for every reservation record that starts 
        #between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    print(F'We cannot reserve book {book} for {user} from {date_from} '+
                          F'to {date_to}. We do not have enough books.')
                    return False
        self._reservations+=[desired_reservation]
        self._reservations.sort(key=lambda x:x._from) #to lazy to make a getter
        print(F'Reservation {desired_reservation._id} included.')
        return True

    def check_reservation(self, user, book, date):
        res = any([res.identify(date, book, user) for res in self._reservations])
        str = 'exists'
        if not res:
            str = 'does not exist'
        print(F'Reservation for {user} of {book} on {date} {str}.')
        return res        

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations 
                                     if res.identify(date, book, user)]
        if not relevant_reservations:        
            print(F'Reservation for {user} of {book} on {date} does not exist.')
            return False
        if new_user not in self._users:
            print(F'Cannot change the reservation as {new_user} does not exist.')
            return False
            
        print(F'Reservation for {user} of {book} on {date} changed to {new_user}.')        
        relevant_reservations[0].change_for(new_user)
        return True


r = Reservation(5, 12, "dorian grey", 45)
p = Reservation(8, 10, "dorian grey", 49)

print("djhdjd")
r.overlapping(p)
r.includes(6)
p.includes(10)

r.identify(10, "dorian grey", 45)
r.identify(10, "dorian grey", 46)


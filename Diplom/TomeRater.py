class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("User’s email has been updated")

    def __repr__(self):
        return ("User {}, email: {}, books read: {}".format(self.name, self.email, len(self.books)))

    def __eq__(self, other_user):
        if other_user.name == self.name and other_user.email == self.email:
            return True
        return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        summ=0
        counter = 0
        for i in self.books.values():
            if i== None:
                continue
            summ+=i
            counter+=1
        return (summ/counter)

class Book:
    def __init__(self, title, isbn, price):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("Book`s ISBN has been updated")

    def add_rating(self, rating):
        if rating != None:
            if rating >= 0 and rating <= 4:
                self.ratings.append(rating)
            else:
                print("Invalid Rating")

    def __eq__(self, new_book):
        if self.title == new_book.title and self.isbn == new_book.isbn:
            return True
        return False

    def get_average_rating(self):
        return (sum(self.ratings)/len(self.ratings)) #without iterating, don't check for zero division

    def __hash__(self):
        return hash((self.title, self.isbn))
    
    def __repr__(self):
        return ("{title}".format(title=self.title))

class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def get_autor(self):
        return self.author

    def __repr__(self):
        return ("{title} by {author}".format(title=self.title, author=self.author))

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return ("{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject))

class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn, price):
        book = Book(title, isbn, price)
        return book

    def create_novel(self, title, author, isbn, price):
        novel = Fiction(title, author, isbn, price)
        return novel

    def create_non_fiction(self, title, subject, level, isbn, price):
        non_fiction = Non_Fiction(title, subject, level, isbn, price)
        return non_fiction

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users.keys():
            usr = self.users[email]
            usr.read_book(book, rating)
            book.add_rating(rating)
            if book in self.books.keys():
                for key, val in self.books.items():
                    if key == book:
                        self.books[book]=1+val
            else:
                self.books[book]=1
        else:
            print("No user with email {email}!".format(email=email))

    def add_user(self, name, email, user_books=None):
        if email in self.users.keys():
            print('This user already exists')
        else:
            result = self.check_valid_email(email)
            if result:
                new_user = User(name, email)
                self.users[new_user.email] = new_user
                if user_books != None:
                    for book in user_books:
                        self.add_book_to_user(book, email)
            else:
                print("Email is not valid")

    def print_catalog(self):
        for i in self.books.keys():
            print(i)

    def print_users(self):
        for i in self.users.values():
            print(i)

    def most_read_book(self):
        high=0
        for key, val in self.books.items():
            if val>high:
                high=val
                f_book=key
        return ("Book {} has been read {} times".format(f_book.title,high))

    def highest_rated_book(self):
        high = 0
        for key in self.books.keys():
            if key.get_average_rating()>high:
                high=key.get_average_rating()
                f_book=key.title
        return f_book

    def most_positive_user(self):
        high = 0
        for i in self.users.values():
            if i.get_average_rating()>high:
                high=i.get_average_rating()
                f_user = i
        return f_user.name

    def check_isbn_unique(self):
        ls = [i.isbn for i in self.books.keys()]
        for i in ls:
            if ls.count(i)>1:
                print("Book with isbn {} is not unique".format(i))

    def check_valid_email(self, email):
        result = False
        ls =['.com', '.edu', '.org']
        if '@' in email:
            for i in ls:
                if i in email[-4:]:
                    result = True
        return result

    def __eq__(self, user, book):
        if self.users[user.email] == user and book in self.books.keys():
            return True
        return False

    def __repr__(self):
        return ("We have {} customers who bought {} books".format(len(self.users), len(self.books)))

    def get_n_most_read_books(self, n):
        lst = [(key.title,val) for key, val in self.books.items() if val>n]
        ls=[]
        z=0
        while z<len(self.books.items()):
            most_read=0
            if len(lst)>0:
                for i in range(0,len(lst)):
                    if lst[i][1]>most_read:
                        most_read=lst[i][1]
                        book = lst[i][0]
                        index = i
                ls.append(book)
                lst.pop(index)
                book=None
                index=None
            z+=1
        return ls

    def get_n_most_prolific_readers(self, n):
        lst = [(i.name, len(i.books)) for i in self.users.values() if len(i.books)>n]
        ls=[]
        z=0
        while z < len(self.users):
            prolific_reader_counter=0
            if len(lst) > 0:
                for i in range(0, len(lst)):
                    if lst[i][1]>prolific_reader_counter:
                        prolific_reader_counter=lst[i][1]
                        user = lst[i][0]
                        index = i
                ls.append(user)
                lst.pop(index)
                user=None
                index=None
            z+=1
        return "Most profilic readers: "+str(ls)

    def get_n_most_expensive_books(self, n):
        lst = [(i.title, i.price) for i in self.books.keys() if i.price > n]
        ls=[]
        z=0
        while z < len(self.books):
            most_expsv_book=0
            if len(lst) > 0:
                for i in range(0, len(lst)):
                    if lst[i][1]>most_expsv_book:
                        most_expsv_book=lst[i][1]
                        book = lst[i][0]
                        index = i
                ls.append(book)
                lst.pop(index)
                book=None
                index=None
            z+=1
        return "Most expensive books: "+str(ls)

    def get_worth_of_user(self, user_email):
        user = self.users[user_email]
        total_costs=0
        for i in user.books:
            total_costs+=i.price
        return "Sum of the costs of all the books read by {}: {} $".format(self.users[user_email].name, total_costs)

    def recommend_to_buy_most_read_books(self, user_email, n):    # offer for user to by most read books, except already read (whatever it fiction or nonfiction or something else)
        recommended_books = self.get_n_most_read_books(n)
        user_books = [i.title for i in self.users[user_email].books.keys()]
        personal_recommend=[]
        max_offer=0
        for i in recommended_books:
            if max_offer>5:
                break
            if i not in user_books:
                max_offer+=1
                personal_recommend.append(i)
        return "We recommend you to read: {}".format(personal_recommend)

# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_LOANS = 3


def _valid_day(day):
    # bool 은 int 의 하위 타입이라 따로 막음
    return type(day) is int and day >= 1


class LibraryLoan:
    def __init__(self):
        self.loans = {}       # book_id -> (name, 빌린 날)
        self.banned_until = {}  # name -> 이 날부터 다시 대출 가능

    def _due(self, book_id):
        return self.loans[book_id][1] + LOAN_DAYS

    def _books_of(self, name):
        return [b for b, (who, _) in self.loans.items() if who == name]

    def borrow(self, book_id, name, day):
        if book_id not in BOOKS or not _valid_day(day):
            return False
        if book_id in self.loans:
            return False
        mine = self._books_of(name)
        if len(mine) >= MAX_LOANS:
            return False
        if any(day > self._due(b) for b in mine):
            return False
        if day < self.banned_until.get(name, 0):
            return False
        self.loans[book_id] = (name, day)
        return True

    def return_book(self, book_id, name, day):
        if book_id not in BOOKS or not _valid_day(day):
            return -1
        loan = self.loans.get(book_id)
        if loan is None or loan[0] != name or day < loan[1]:
            return -1
        late = max(0, day - self._due(book_id))
        del self.loans[book_id]
        if late:
            # 정지 기간이 겹치면 더 늦게 끝나는 쪽
            self.banned_until[name] = max(self.banned_until.get(name, 0), day + late)
        return late

    def get_loans(self, name):
        return sorted(((b, self._due(b)) for b in self._books_of(name)), key=lambda x: (x[1], x[0]))

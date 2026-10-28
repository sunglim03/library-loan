# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_LOANS = 3


def _valid_day(day):
    # 1 이상의 정수만 허용 (True/False는 정수로 보지 않음)
    return type(day) is int and day >= 1


class LibraryLoan:
    def __init__(self):
        # 대출 중인 책: book_id -> (이름, 빌린 날, 반납 기한)
        self.loans = {}
        # 대출 정지 기간: (이름, 시작일, 끝일) — 시작일~끝일(포함)에는 대출 불가
        self.suspensions = []

    def _loans_of(self, name):
        return [(b, info) for b, info in self.loans.items() if info[0] == name]

    def _is_suspended(self, name, day):
        return any(n == name and start <= day <= end
                   for n, start, end in self.suspensions)

    def borrow(self, book_id, name, day):
        if book_id not in BOOKS:              # 1. 없는 책
            return False
        if not _valid_day(day):               # 2. 잘못된 날짜
            return False
        if book_id in self.loans:             # 3. 이미 대출 중
            return False
        mine = self._loans_of(name)
        if len(mine) >= MAX_LOANS:            # 4. 이미 3권
            return False
        if any(day > info[2] for _, info in mine):   # 5. 기한 지난 책 보유
            return False
        if self._is_suspended(name, day):     # 6. 대출 정지 중
            return False
        self.loans[book_id] = (name, day, day + LOAN_DAYS)
        return True

    def return_book(self, book_id, name, day):
        if book_id not in BOOKS or book_id not in self.loans:
            return -1
        borrower, borrow_day, due = self.loans[book_id]
        if borrower != name:                  # 그 사람이 빌린 책이 아님
            return -1
        if not _valid_day(day):               # 잘못된 날짜
            return -1
        if day < borrow_day:                  # 빌린 날보다 이른 날
            return -1
        del self.loans[book_id]
        overdue = max(0, day - due)
        if overdue > 0:
            # 반납한 날부터 연체 일수만큼의 날 동안 대출 정지
            self.suspensions.append((name, day, day + overdue - 1))
        return overdue

    def get_loans(self, name):
        result = [(b, info[2]) for b, info in self._loans_of(name)]
        result.sort(key=lambda x: (x[1], x[0]))
        return result

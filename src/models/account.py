from decimal import Decimal, InvalidOperation
from enum import Enum
from datetime import date

class AccountType(Enum):
    SAVINGS = "Savings"
    CURRENT = "Current"

class AccountStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class Account:
    """
    Represents a bank account with basic operations.
    """
    MIN_BALANCE = {
        AccountType.SAVINGS.value: Decimal("500"),
        AccountType.CURRENT.value: Decimal("1000")
    }
    MAX_SINGLE_DEPOSIT = Decimal("100000.0")
    DAILY_LIMIT = Decimal("200000.0")  # Example daily limit

    def __init__(
        self,
        account_number: int,
        name: str,
        age: int,
        account_type: str,
        balance: float = 0.0,
        status: str = "Active",
        pin: str = None,
        transaction_history=None,
        daily_total=0.0,
        last_transaction_date=None
    ):
        self.account_number = int(account_number)
        self.name = name.strip()
        self.age = int(age)
        self.account_type = account_type.title()
        if self.account_type not in Account.MIN_BALANCE:
            raise ValueError(f"Invalid account type: {self.account_type}")
        self.balance = Decimal(str(balance))
        self.status = status.title()
        if self.status not in [s.value for s in AccountStatus]:
            raise ValueError(f"Invalid status: {self.status}")
        self.pin = pin  # Consider hashing in production

        # New fields for extended features
        self.transaction_history = transaction_history if transaction_history is not None else []
        self.daily_total = Decimal(str(daily_total))
        self.last_transaction_date = last_transaction_date

    def deposit(self, amount) -> tuple[bool, str]:
        try:
            amount = Decimal(str(amount))
        except (TypeError, ValueError, InvalidOperation):
            return False, "Invalid Amount"
        
        if self.status != AccountStatus.ACTIVE.value:
            return False, "Account is inactive"

        if amount <= 0:
            return False, "Deposit must be positive"
        if amount > Account.MAX_SINGLE_DEPOSIT:
            return False, f"Deposit exceeds single-deposit limit {Account.MAX_SINGLE_DEPOSIT}"

        # Daily transaction limit check
        today = str(date.today())
        if self.last_transaction_date != today:
            self.daily_total = Decimal("0.0")
            self.last_transaction_date = today
        if self.daily_total + amount > Account.DAILY_LIMIT:
            return False, f"Daily transaction limit of {Account.DAILY_LIMIT} exceeded"
        self.daily_total += amount

        self.balance += amount
        self.transaction_history.append(
            {"type": "DEPOSIT", "amount": float(amount), "balance": float(self.balance), "date": today}
        )
        return True, f"Deposit Successful.\nNew Balance: {self.balance}"
    
    def withdraw(self, amount) -> tuple[bool, str]:
        try:
            amount = Decimal(str(amount))
        except (TypeError, ValueError, InvalidOperation):
            return False, "Invalid Amount"
        
        if self.status != AccountStatus.ACTIVE.value:
            return False, "Account is inactive"
        if amount <= 0:
            return False, "Withdrawal must be positive"
        
        min_required = Account.MIN_BALANCE[self.account_type]
        if self.balance - amount < min_required:
            return False, f"Insufficient funds. Minimum required balance for {self.account_type}: {min_required}"

        # Daily transaction limit check
        today = str(date.today())
        if self.last_transaction_date != today:
            self.daily_total = Decimal("0.0")
            self.last_transaction_date = today
        if self.daily_total + amount > Account.DAILY_LIMIT:
            return False, f"Daily transaction limit of {Account.DAILY_LIMIT} exceeded"
        self.daily_total += amount

        self.balance -= amount
        self.transaction_history.append(
            {"type": "WITHDRAW", "amount": float(amount), "balance": float(self.balance), "date": today}
        )
        return True, f"Withdrawal successful.\nNew Balance: {self.balance}"
    
    def to_dict(self) -> dict:
        return {
            "account_number": self.account_number,
            "name": self.name,
            "age": self.age,
            "balance": float(self.balance),
            "account_type": self.account_type,
            "status": self.status,
            "pin": self.pin if self.pin else "",
            "transaction_history": self.transaction_history,
            "daily_total": float(self.daily_total),
            "last_transaction_date": self.last_transaction_date,
        }
    
    def __str__(self) -> str:
        return f"[{self.account_number}] {self.name} ({self.account_type}) - Balance: {self.balance} - {self.status}"









































































































































        
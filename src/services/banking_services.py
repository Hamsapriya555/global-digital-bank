from models.account import Account
from utils.file_manager import load_accounts, save_accounts, log_transaction, export_accounts, import_accounts, write_transaction_log_file, read_transaction_history
from decimal import Decimal

class BankingService:
    START_ACCOUNT_NO = 1001

    def __init__(self):
        self.accounts = load_accounts()
        if self.accounts:
            self.next_account_number = max(self.accounts.keys()) + 1
        else:
            self.next_account_number = BankingService.START_ACCOUNT_NO

    def save_to_disk(self):
        save_accounts(self.accounts)

    # --- Base Features ---
    def create_account(self, name, age, account_type, initial_deposit=0, pin=None):
        if not name.strip():
            return None, "Name cannot be empty"
        if int(age) < 18:
            return None, "Age must be 18 or above"
        account_type = account_type.title()
        if account_type not in Account.MIN_BALANCE:
            return None, f"Invalid Account type. Choose from {list(Account.MIN_BALANCE.keys())}"
        min_req = Account.MIN_BALANCE[account_type]
        if float(initial_deposit) < min_req:
            return None, f"Initial deposit must be at least {min_req}"
        acc_no = self.next_account_number
        acc = Account(acc_no, name, age, account_type, balance=float(initial_deposit), pin=pin)
        self.accounts[acc_no] = acc
        self.next_account_number += 1
        log_transaction(acc_no, "CREATE", initial_deposit, acc.balance)
        self.save_to_disk()
        return acc, "Account created successfully"

    def get_account(self, account_number):
        return self.accounts.get(int(account_number))

    def deposit(self, account_number, amount, pin=None):
        acc = self.get_account(account_number)
        if not acc:
            return False, "Account not Found"
        if not self.verify_pin(account_number, pin)[0]:
            return False, "Invalid PIN"
        if acc.status != "Active":
            return False, "Account is not Active"
        ok, msg = acc.deposit(amount)
        if ok:
            log_transaction(acc.account_number, "DEPOSIT", amount, acc.balance)
            self.save_to_disk()
        return ok, msg

    def withdraw(self, account_number, amount, pin=None):
        acc = self.get_account(account_number)
        if not acc:
            return False, "Account not Found"
        if not self.verify_pin(account_number, pin)[0]:
            return False, "Invalid PIN"
        if acc.status != "Active":
            return False, "Account is not Active"
        ok, msg = acc.withdraw(amount)
        if ok:
            log_transaction(acc.account_number, "WITHDRAW", amount, acc.balance)
            self.save_to_disk()
        return ok, msg

    def balance_inquiry(self, account_number, pin=None):
        acc = self.get_account(account_number)
        if not acc:
            return False, "Account not Found"
        if not self.verify_pin(account_number, pin)[0]:
            return False, "Invalid PIN"
        return acc, f"Balance: {acc.balance:.2f}"

    def close_account(self, account_number, pin=None):
        acc = self.get_account(account_number)
        if not acc:
            return False, "Account not Found"
        if not self.verify_pin(account_number, pin)[0]:
            return False, "Invalid PIN"
        acc.status = "Inactive"
        log_transaction(acc.account_number, "CLOSE", None, acc.balance)
        self.save_to_disk()
        return True, "Account closed successfully"

    # --- Extended Features ---
    def search_by_name(self, name):
        name = name.strip().lower()
        return [acc for acc in self.accounts.values() if acc.name.lower() == name]

    def search_by_account_number(self, account_number):
        return self.accounts.get(int(account_number))

    def list_active_accounts(self):
        return [acc for acc in self.accounts.values() if acc.status == "Active"]

    def list_closed_accounts(self):
        return [acc for acc in self.accounts.values() if acc.status == "Inactive"]

    def reopen_closed_account(self, account_number):
        acc = self.get_account(account_number)
        if not acc:
            return False, "Account not Found"
        if acc.status == "Active":
            return False, "Account is already active"
        acc.status = "Active"
        log_transaction(acc.account_number, "REOPEN", None, acc.balance)
        self.save_to_disk()
        return True, "Account reopened successfully"

    def rename_account_holder(self, account_number, new_name):
        acc = self.get_account(account_number)
        if not acc:
            return False, "Account not Found"
        if acc.status != "Active":
            return False, "Account is not Active"
        acc.name = new_name.strip()
        log_transaction(acc.account_number, "RENAME", None, acc.balance)
        self.save_to_disk()
        return True, "Account holder renamed successfully"

    def delete_all_accounts(self):
        self.accounts.clear()
        self.save_to_disk()
        return True, "All accounts deleted"

    def count_active_accounts(self):
        return len([acc for acc in self.accounts.values() if acc.status == "Active"])

    def write_transaction_log(self, account_number):
        acc = self.get_account(account_number)
        if not acc:
            return False, "Account not Found"
        write_transaction_log_file(acc.account_number)
        return True, "Transaction log written."

    def transaction_history(self, account_number):
        acc = self.get_account(account_number)
        if not acc:
            return []
        return read_transaction_history(acc.account_number)

    def check_minimum_balance(self, account_number):
        acc = self.get_account(account_number)
        if not acc:
            return False, "Account not Found"
        min_req = Account.MIN_BALANCE[acc.account_type]
        if acc.balance < min_req:
            return False, f"Balance below minimum required: {min_req}"
        return True, "Minimum balance maintained."

    def check_daily_transaction_limit(self, account_number):
        # This is a stub. You need to implement daily tracking in Account model.
        acc = self.get_account(account_number)
        if not acc:
            return False, "Account not Found"
        # Example: acc.daily_total
        return True, "Within daily transaction limit."

    def transfer_funds(self, from_acc_no, to_acc_no, amount, pin=None):
        from_acc = self.get_account(from_acc_no)
        to_acc = self.get_account(to_acc_no)
        if not from_acc or not to_acc:
            return False, "One or both accounts not found"
        if not self.verify_pin(from_acc_no, pin)[0]:
            return False, "Invalid PIN"
        if from_acc.status != "Active" or to_acc.status != "Active":
            return False, "Both accounts must be active"
        ok, msg = from_acc.withdraw(amount)
        if not ok:
            return False, msg
        to_acc.deposit(amount)
        log_transaction(from_acc.account_number, "TRANSFER_OUT", amount, from_acc.balance)
        log_transaction(to_acc.account_number, "TRANSFER_IN", amount, to_acc.balance)
        self.save_to_disk()
        return True, "Transfer successful"

    def top_n_accounts_by_balance(self, n):
        return sorted(self.accounts.values(), key=lambda acc: acc.balance, reverse=True)[:n]

    def average_balance(self):
        if not self.accounts:
            return 0
        total = sum(acc.balance for acc in self.accounts.values())
        return total / len(self.accounts)

    def youngest_account_holder(self):
        if not self.accounts:
            return None
        return min(self.accounts.values(), key=lambda acc: acc.age)

    def oldest_account_holder(self):
        if not self.accounts:
            return None
        return max(self.accounts.values(), key=lambda acc: acc.age)

    def simple_interest(self, account_number, rate, years):
        from decimal import Decimal, InvalidOperation
        acc = self.get_account(account_number)
        if not acc:
            return None, "Account not found"
        try:
            principal = Decimal(str(acc.balance))
            rate = Decimal(str(rate))
            years = Decimal(str(years))
        except (InvalidOperation, ValueError):
            return None, "Invalid input: Please enter valid numbers for rate and years."
        interest = (principal * rate * years) / Decimal("100")
        return float(interest), f"Simple Interest for {years} years at {rate}%: {float(interest)}"

    def export_accounts_to_file(self):
        export_accounts(self.accounts)
        return True, "Accounts exported successfully."

    def import_accounts_from_file(self):
        new_accounts = import_accounts()
        for acc in new_accounts:
            if acc.account_number not in self.accounts:
                self.accounts[acc.account_number] = acc
        self.save_to_disk()
        return True, "Accounts imported successfully."

    def verify_pin(self, account_number, pin):
        acc = self.get_account(account_number)
        if not acc:
            return False, "Account not Found"
        if not pin or str(acc.pin) != str(pin):
            return False, "Invalid PIN"
        return True, "PIN verified"

    def upgrade_account_type(self, account_number, new_type):
        acc = self.get_account(account_number)
        if not acc:
            return False, "Account not Found"
        new_type = new_type.title()
        if new_type not in Account.MIN_BALANCE:
            return False, "Invalid account type"
        acc.account_type = new_type
        log_transaction(acc.account_number, "UPGRADE_TYPE", None, acc.balance)
        self.save_to_disk()
        return True, f"Account type upgraded to {new_type}"
    
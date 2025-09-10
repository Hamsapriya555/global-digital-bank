import csv
import json
from models.account import Account
from datetime import datetime
import os
import logging
from typing import Dict, List, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configurable data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get("GDB_DATA_DIR", os.path.join(BASE_DIR, "data"))
ACCOUNT_FILE = os.path.join(DATA_DIR, "accounts.csv")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.log")
EXPORT_FILE = os.path.join(DATA_DIR, "accounts_export.csv")

CSV_HEADER = [
    "account_number", "name", "age", "balance", "account_type", "status", "pin",
    "transaction_history", "daily_total", "last_transaction_date"
]

def save_accounts(accounts: Dict[int, Account]) -> bool:
    """
    Save all accounts to the main CSV file. Returns True on success.
    """
    try:
        os.makedirs(os.path.dirname(ACCOUNT_FILE), exist_ok=True)
        with open(ACCOUNT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)
            for acc in accounts.values():
                d = acc.to_dict()
                writer.writerow([
                    d["account_number"],
                    d["name"],
                    d["age"],
                    d["balance"],
                    d["account_type"],
                    d["status"],
                    d["pin"],
                    json.dumps(d.get("transaction_history", [])),
                    d.get("daily_total", 0.0),
                    d.get("last_transaction_date", "")
                ])
        logging.info("Accounts saved successfully.")
        return True
    except Exception as e:
        logging.error(f"Failed to save accounts: {e}")
        return False

def load_accounts() -> Dict[int, Account]:
    """
    Load all accounts from the main CSV file. Returns a dictionary of accounts.
    """
    accounts = {}
    try:
        with open(ACCOUNT_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                transaction_history = []
                if row.get("transaction_history"):
                    try:
                        transaction_history = json.loads(row["transaction_history"])
                    except Exception:
                        transaction_history = []
                acc = Account(
                    account_number=row["account_number"],
                    name=row["name"],
                    age=row["age"],
                    account_type=row["account_type"],
                    balance=row["balance"],
                    status=row["status"],
                    pin=row["pin"] if row["pin"] else None,
                    transaction_history=transaction_history,
                    daily_total=row.get("daily_total", 0.0),
                    last_transaction_date=row.get("last_transaction_date", None)
                )
                accounts[acc.account_number] = acc
        logging.info("Accounts loaded successfully.")
    except FileNotFoundError:
        logging.warning("Account file not found. Starting with empty accounts.")
    except Exception as e:
        logging.error(f"Failed to load accounts: {e}")
    return accounts

def log_transaction(account_number: int, operation: str, amount: Optional[float], balance_after: float) -> None:
    """
    Append a transaction entry to the transactions log file.
    """
    try:
        os.makedirs(os.path.dirname(TRANSACTIONS_FILE), exist_ok=True)
        with open(TRANSACTIONS_FILE, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} | {account_number} | {operation} | {amount} | {balance_after}\n")
        logging.info(f"Transaction logged for account {account_number}.")
    except Exception as e:
        logging.error(f"Failed to log transaction: {e}")

def export_accounts(accounts: Dict[int, Account]) -> bool:
    """
    Export all accounts to a CSV file (accounts_export.csv) in the data directory.
    Returns True on success.
    """
    try:
        os.makedirs(os.path.dirname(EXPORT_FILE), exist_ok=True)
        with open(EXPORT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)
            for acc in accounts.values():
                d = acc.to_dict()
                writer.writerow([
                    d["account_number"],
                    d["name"],
                    d["age"],
                    d["balance"],
                    d["account_type"],
                    d["status"],
                    d["pin"],
                    json.dumps(d.get("transaction_history", [])),
                    d.get("daily_total", 0.0),
                    d.get("last_transaction_date", "")
                ])
        logging.info("Accounts exported successfully.")
        return True
    except Exception as e:
        logging.error(f"Failed to export accounts: {e}")
        return False

def import_accounts() -> List[Account]:
    """
    Import accounts from accounts_export.csv and return a list of Account objects.
    """
    accounts = []
    try:
        with open(EXPORT_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                transaction_history = []
                if row.get("transaction_history"):
                    try:
                        transaction_history = json.loads(row["transaction_history"])
                    except Exception:
                        transaction_history = []
                acc = Account(
                    account_number=row["account_number"],
                    name=row["name"],
                    age=row["age"],
                    account_type=row["account_type"],
                    balance=row["balance"],
                    status=row["status"],
                    pin=row["pin"] if row["pin"] else None,
                    transaction_history=transaction_history,
                    daily_total=row.get("daily_total", 0.0),
                    last_transaction_date=row.get("last_transaction_date", None)
                )
                accounts.append(acc)
        logging.info("Accounts imported successfully.")
    except FileNotFoundError:
        logging.warning("Export file not found. No accounts imported.")
    except Exception as e:
        logging.error(f"Failed to import accounts: {e}")
    return accounts

def write_transaction_log_file(account_number: int) -> bool:
    """
    Write all transactions for a given account number to a separate log file.
    Returns True on success.
    """
    log_file = os.path.join(os.path.dirname(TRANSACTIONS_FILE), f"transactions_{account_number}.log")
    try:
        with open(TRANSACTIONS_FILE, "r") as src, open(log_file, "w") as dst:
            for line in src:
                if f"| {account_number} |" in line:
                    dst.write(line)
        logging.info(f"Transaction log file written for account {account_number}.")
        return True
    except FileNotFoundError:
        logging.warning("Main transactions file not found.")
        return False
    except Exception as e:
        logging.error(f"Failed to write transaction log file: {e}")
        return False

def read_transaction_history(account_number: int) -> List[str]:
    """
    Read all transactions for a given account number from the main log file.
    Returns a list of transaction strings.
    """
    history = []
    try:
        with open(TRANSACTIONS_FILE, "r") as f:
            for line in f:
                if f"| {account_number} |" in line:
                    history.append(line.strip())
        logging.info(f"Transaction history read for account {account_number}.")
    except FileNotFoundError:
        logging.warning("Main transactions file not found.")
    except Exception as e:
        logging.error(f"Failed to read transaction history: {e}")
    return history
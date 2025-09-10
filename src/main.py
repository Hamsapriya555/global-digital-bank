from services.banking_services import BankingService

def main():
    bank = BankingService()
    print("Welcome to GlobalDigital Bank")

    while True:
        print("\n--- Main Menu ---")
        print("1) Create Account")
        print("2) Deposit")
        print("3) Withdraw")
        print("4) Balance Inquiry")
        print("5) Close Account")
        print("6) File Persistence (Save/Load)")
        print("7) Search by Name")
        print("8) Search by Account Number")
        print("9) List All Active Accounts")
        print("10) List All Closed Accounts")
        print("11) Reopen Closed Account")
        print("12) Rename Account Holder")
        print("13) Delete All Accounts")
        print("14) Count Active Accounts")
        print("15) Transaction Log File")
        print("16) Transaction History Viewer")
        print("17) Minimum Balance Check")
        print("18) Daily Transaction Limit")
        print("19) Transfer Funds")
        print("20) Top N Accounts by Balance")
        print("21) Average Balance Calculator")
        print("22) Youngest Account Holder")
        print("23) Oldest Account Holder")
        print("24) Simple Interest Calculator")
        print("25) Export Accounts to File")
        print("26) Import Accounts from File")
        print("27) PIN/Password Protection")
        print("28) Account Type Upgrade")
        print("29) System Exit with Autosave")
        print("0) Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            name = input("Enter Name: ")
            age = input("Enter age: ")
            acc_type = input("Enter account type (Savings/Current): ")
            initial = input("Initial Deposit amount: ")
            pin = input("Set a 4-digit PIN: ")
            acc, msg = bank.create_account(name, age, acc_type, initial, pin)
            print(msg)
            if acc:
                print(acc)

        elif choice == "2":
            acc_no = input("Enter account number: ")
            pin = input("Enter PIN: ")
            amount = input("Enter amount to deposit: ")
            ok, msg = bank.deposit(acc_no, amount, pin)
            print(msg)

        elif choice == "3":
            acc_no = input("Enter your account number: ")
            pin = input("Enter PIN: ")
            amount = input("Enter amount to withdraw: ")
            ok, msg = bank.withdraw(acc_no, amount, pin)
            print(msg)

        elif choice == "4":
            acc_no = input("Enter Account Number: ")
            pin = input("Enter PIN: ")
            acc, msg = bank.balance_inquiry(acc_no, pin)
            print(acc if acc else msg)

        elif choice == "5":
            acc_no = input("Enter account number to close: ")
            pin = input("Enter PIN: ")
            ok, msg = bank.close_account(acc_no, pin)
            print(msg)

        elif choice == "6":
            action = input("Type 'save' to save or 'load' to load accounts: ").strip().lower()
            if action == "save":
                ok, msg = bank.export_accounts_to_file()
                print(msg)
            elif action == "load":
                ok, msg = bank.import_accounts_from_file()
                print(msg)
            else:
                print("Invalid action.")

        elif choice == "7":
            name = input("Enter name to search: ")
            results = bank.search_by_name(name)
            if results:
                for acc in results:
                    print(acc)
            else:
                print("No account found with that name.")

        elif choice == "8":
            acc_no = input("Enter account number to search: ")
            acc = bank.search_by_account_number(acc_no)
            print(acc if acc else "Account not found.")

        elif choice == "9":
            active_accounts = bank.list_active_accounts()
            if active_accounts:
                for acc in active_accounts:
                    print(acc)
            else:
                print("No active accounts.")

        elif choice == "10":
            closed_accounts = bank.list_closed_accounts()
            if closed_accounts:
                for acc in closed_accounts:
                    print(acc)
            else:
                print("No closed accounts.")

        elif choice == "11":
            acc_no = input("Enter account number to reopen: ")
            ok, msg = bank.reopen_closed_account(acc_no)
            print(msg)

        elif choice == "12":
            acc_no = input("Enter account number to rename: ")
            new_name = input("Enter new account holder name: ")
            ok, msg = bank.rename_account_holder(acc_no, new_name)
            print(msg)

        elif choice == "13":
            confirm = input("Are you sure you want to delete all accounts? Type YES to confirm: ")
            if confirm == "YES":
                ok, msg = bank.delete_all_accounts()
                print(msg)
            else:
                print("Operation cancelled.")

        elif choice == "14":
            count = bank.count_active_accounts()
            print(f"Active accounts count: {count}")

        elif choice == "15":
            acc_no = input("Enter account number: ")
            ok, msg = bank.write_transaction_log(acc_no)
            print(msg)

        elif choice == "16":
            acc_no = input("Enter account number: ")
            history = bank.transaction_history(acc_no)
            if history:
                for entry in history:
                    print(entry)
            else:
                print("No transaction history found.")

        elif choice == "17":
            acc_no = input("Enter account number: ")
            ok, msg = bank.check_minimum_balance(acc_no)
            print(msg)

        elif choice == "18":
            acc_no = input("Enter account number: ")
            ok, msg = bank.check_daily_transaction_limit(acc_no)
            print(msg)

        elif choice == "19":
            from_acc = input("From Account Number: ")
            pin = input("Enter PIN: ")
            to_acc = input("To Account Number: ")
            amount = input("Amount to transfer: ")
            ok, msg = bank.transfer_funds(from_acc, to_acc, amount, pin)
            print(msg)

        elif choice == "20":
            n = int(input("How many top accounts by balance? "))
            top_accounts = bank.top_n_accounts_by_balance(n)
            for acc in top_accounts:
                print(acc)

        elif choice == "21":
            avg = bank.average_balance()
            print(f"Average balance across all accounts: {avg}")

        elif choice == "22":
            youngest = bank.youngest_account_holder()
            print(youngest if youngest else "No accounts found.")

        elif choice == "23":
            oldest = bank.oldest_account_holder()
            print(oldest if oldest else "No accounts found.")

        elif choice == "24":
            acc_no = input("Enter account number: ")
            rate = input("Enter annual interest rate (e.g., 5 for 5%): ")
            years = input("Enter number of years: ")
            interest = bank.simple_interest(acc_no, rate, years)
            print(f"Simple interest: {interest}")

        elif choice == "25":
            ok, msg = bank.export_accounts_to_file()
            print(msg)

        elif choice == "26":
            ok, msg = bank.import_accounts_from_file()
            print(msg)

        elif choice == "27":
            acc_no = input("Enter account number: ")
            pin = input("Enter PIN: ")
            ok, msg = bank.verify_pin(acc_no, pin)
            print(msg)

        elif choice == "28":
            acc_no = input("Enter account number: ")
            new_type = input("Enter new account type (Savings/Current): ")
            ok, msg = bank.upgrade_account_type(acc_no, new_type)
            print(msg)

        elif choice == "29":
            ok, msg = bank.save_accounts_to_file()
            print("All changes saved. Exiting system.")
            break

        elif choice == "0":
            ok, msg = bank.save_accounts_to_file()
            print("Thank you for visiting GlobalDigital Bank. All changes saved.")
            break

        else:
            print("Invalid Choice.\n Try Again!!")

if __name__ == "__main__":
    main()
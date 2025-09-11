# global-digital-bank
🌍 Global Digital Bank (GDB)
A **next-generation digital banking platform** implemented in Python, designed to deliver **secure, scalable, and user-friendly** banking services.  
This project extends beyond the standard requirements by including **robust testing, modular design, and professional documentation**.

📖 Executive Summary
The **Global Digital Bank (GDB)** is a command-line banking system developed for **Bank of Success Pvt. Ltd.**.  
It empowers customers to manage their accounts, perform transactions, and monitor activity with ease.  
The system:
- Ensures **real-time transaction processing**  
- Enforces **strict security & compliance rules**  
- Provides **comprehensive account management**  
- Maintains **transaction history with persistence (CSV + logs)**  

🎯 Goals
- ✅ **User-Centric Banking** → Easy to use, intuitive menu-driven interface  
- ✅ **Comprehensive Account Management** → Active, inactive, reopening, and upgrades  
- ✅ **Robust Architecture** → Modular, layered design for maintainability  
- ✅ **Data Logging** → CSV persistence + transaction log file for auditability  
- ✅ **Security & Compliance** → PIN protection, validation rules, and safeguards  

✨ Features
🔹 Base Features (B1–B6)
| Code | Feature | Status |
|------|----------|--------|
| B1 | Create Account (reject if age < 18) | ✅ |
| B2 | Deposit | ✅ |
| B3 | Withdraw | ✅ |
| B4 | Balance Inquiry | ✅ |
| B5 | Close Account (mark inactive) | ✅ |
| B6 | File Persistence (CSV save/load) | ✅ |

🔹 Extended Features (F1–F24)
| Code | Feature | Status |
|------|----------|--------|
| F1  | Search by Name | ✅ |
| F2  | List All Active Accounts | ✅ |
| F3  | List All Closed Accounts | ✅ |
| F4  | Account Type Upgrade | ✅ |
| F5  | Reopen Closed Account | ✅ |
| F6  | Transaction Log File | ✅ |
| F7  | Search by Account Number | ✅ |
| F8  | Minimum Balance Check | ✅ |
| F9  | Simple Interest Calculator | ✅ |
| F10 | Daily Transaction Limit | ✅ |
| F11 | Transfer Funds | ✅ |
| F12 | Transaction History Viewer | ✅ |
| F13 | Average Balance Calculator | ✅ |
| F14 | Youngest Account Holder | ✅ |
| F15 | Oldest Account Holder | ✅ |
| F16 | Top N Accounts by Balance | ✅ |
| F17 | PIN/Password Protection | ✅ |
| F18 | Export Accounts to File | ✅ |
| F19 | Age Verification at Creation | ✅ |
| F20 | Rename Account Holder | ✅ |
| F21 | Count Active Accounts | ✅ |
| F22 | Delete All Accounts (Admin) | ✅ |
| F23 | System Exit with Autosave | ✅ |
| F24 | Import Accounts from File | ✅ |
🔥 Unlike other forks, this repo goes **beyond just features** by adding **tests, CI/CD, and analytics visualizations**.

🛠️ Tech Stack
- **Language:** Python 3.10+  
- **Persistence:** CSV (`accounts.csv`) + Logs (`transactions.log`)  
- **Testing:** PyTest (automated)  
- **CI/CD:** GitHub Actions (build + tests)  
- **Optional Add-ons:** Docker, Charts (Matplotlib), Streamlit/Flask UI  

📂 Project Structure
global-digital-bank/
│── data/
│ ├── accounts.csv # Persistent account data
│── src/
│ ├── models/ # Account class, data models
│ ├── services/ # Banking services (business logic)
│ ├── utils/ # File manager, logger
│── tests/ # Automated unit tests
│── main.py # CLI entry point
│── requirements.txt # Dependencies
│── README.md # Documentation
│── LICENSE # MIT License

⚡ Installation
```bash
# Clone repository
git clone https://github.com/Thanushreems2005/global-digital-bank.git
cd global-digital-bank

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

▶️ Usage
Run the CLI app:
bash
Copy code
python main.py

🏦 Sample Workflow
--- Welcome to Global Digital Bank ---
1) Create Account
2) Deposit
3) Withdraw
4) Balance Inquiry
5) Close Account
6) List All Active Accounts
7) Transfer Funds
8) Transaction History
9) Exit

✅ Account created successfully! Account Number: 1001
📊 Deliverables
✅ Modular source code (Python)
✅ accounts.csv (persistent account storage)
✅ transactions.log (transaction history)
✅ Professional README with clear instructions
✅ Unit tests + GitHub Actions pipeline
✅ Feature ownership matrix

🧪 Testing
Run unit tests with:
bash
Copy code
pytest
All features are covered with automated tests (unlike other forks which only listed manual results).

🚀 Future Enhancements
Web-based interface (Flask/Streamlit)
Analytics dashboard with charts (top accounts, balance distribution)
Deployment via Docker

🤝 Contributing
Contributions are welcome! Please fork this repo and open a pull request.

📜 License
This project is licensed under the MIT License
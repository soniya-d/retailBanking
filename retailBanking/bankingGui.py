import mysql.connector
from tabulate import tabulate

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="soniya2193",  
        database="RetailBanking"
    )

def populate_database():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("""
    INSERT INTO Customers (CustomerID, Name, Email, Address, PhoneNumber, DateOfBirth, AccountStatus)
    VALUES
    (1, 'Alice Johnson', 'alice@example.com', '123 Main St', '123-456-7890', '1985-05-20', 'Active'),
    (2, 'Bob Smith', 'bob@example.com', '456 Oak St', '123-555-7890', '1990-11-15', 'Active'),
    (3, 'Charlie Brown', 'charlie@example.com', '789 Pine St', '123-777-8888', '1988-09-25', 'Inactive'),
    (4, 'Daisy Carter', 'daisy@example.com', '321 Birch St', '987-654-3210', '1995-07-30', 'Active')
    ON DUPLICATE KEY UPDATE Name=Name;
    """)

    cursor.execute("""
    INSERT INTO Accounts (AccountID, CustomerID, AccountType, Balance, CreatedDate, Status)
    VALUES
    (101, 1, 'Savings', 5000.00, '2023-01-01', 'Open'),
    (102, 2, 'Checking', 3000.00, '2023-02-10', 'Open'),
    (103, 3, 'Savings', 8000.00, '2023-03-05', 'Closed'),
    (104, 4, 'Checking', 2500.00, '2023-04-15', 'Open')
    ON DUPLICATE KEY UPDATE AccountType=AccountType;
    """)

    cursor.execute("""
    INSERT INTO Transactions (TransactionID, AccountID, TransactionType, Amount, Date, Description)
    VALUES
    (1001, 101, 'Deposit', 200.00, '2024-02-01', 'Monthly Savings'),
    (1002, 102, 'Withdrawal', 100.00, '2024-02-15', 'Grocery Purchase'),
    (1003, 103, 'Deposit', 500.00, '2024-03-05', 'Bonus Payment'),
    (1004, 104, 'Withdrawal', 300.00, '2024-04-10', 'Online Shopping')
    ON DUPLICATE KEY UPDATE TransactionType=TransactionType;
    """)

    cursor.execute("""
    INSERT INTO Loans (LoanID, CustomerID, LoanType, Amount, InterestRate, IssueDate, DueDate, LoanStatus)
    VALUES
    (201, 1, 'Personal', 5000.00, 5.5, '2023-03-10', '2026-03-10', 'Approved'),
    (202, 2, 'Home', 200000.00, 3.7, '2022-06-15', '2042-06-15', 'Approved'),
    (203, 3, 'Business', 15000.00, 4.2, '2023-08-20', '2028-08-20', 'Pending')
    ON DUPLICATE KEY UPDATE LoanType=LoanType;
    """)

    cursor.execute("""
    INSERT INTO CreditCards (CardID, CustomerID, CardType, CreditLimit, Balance, IssuedDate, ExpiryDate)
    VALUES
    (301, 1, 'Visa', 10000.00, 2500.00, '2023-04-01', '2028-04-01'),
    (302, 2, 'Mastercard', 15000.00, 5000.00, '2022-08-15', '2027-08-15'),
    (303, 3, 'Visa', 12000.00, 7000.00, '2023-06-10', '2028-06-10')
    ON DUPLICATE KEY UPDATE CardType=CardType;
    """)


    cursor.execute("""
    INSERT INTO Investments (InvestmentID, CustomerID, InvestmentType, Amount, StartDate, EndDate)
    VALUES
    (401, 1, 'Stocks', 10000.00, '2023-05-01', '2025-05-01'),
    (402, 2, 'Bonds', 5000.00, '2023-09-10', '2026-09-10'),
    (403, 4, 'Stocks', 15000.00, '2024-01-15', '2027-01-15')
    ON DUPLICATE KEY UPDATE InvestmentType=InvestmentType;
    """)

    db.commit()
    cursor.close()
    db.close()
    print("Database populated with sample data!")

def execute_query(query, headers):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    print("\n" + tabulate(results, headers=headers, tablefmt="grid"))  
    db.close()

def menu():
    populate_database()  
    while True:
        print("\nRetailBanking Database Menu")
        print("1. View Customers")
        print("2. View Accounts")
        print("3. Execute Advanced Queries")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            execute_query("SELECT * FROM Customers;", 
                          ["CustomerID", "Name", "Email", "Address", "PhoneNumber", "DateOfBirth", "AccountStatus"])
        elif choice == "2":
            execute_query("SELECT * FROM Accounts;", 
                          ["AccountID", "CustomerID", "AccountType", "Balance", "CreatedDate", "Status"])
        elif choice == "3":
            advanced_queries()
        elif choice == "4":
            break
        else:
            print("Invalid choice, please try again.")

def advanced_queries():
    queries = [
        ("Total Loan and Investment Amount per Customer", """
        SELECT l.CustomerID, cu.Name, 
               SUM(l.Amount) AS TotalLoans, 
               SUM(i.Amount) AS TotalInvestments
        FROM Loans l
        JOIN Customers cu ON l.CustomerID = cu.CustomerID
        LEFT JOIN Investments i ON l.CustomerID = i.CustomerID
        GROUP BY l.CustomerID, cu.Name;
        """, ["CustomerID", "Name", "TotalLoans", "TotalInvestments"]),

        ("Customers with Both Loans and Credit Cards", """
        SELECT DISTINCT cu.CustomerID, cu.Name
        FROM Customers cu
        JOIN Loans l ON cu.CustomerID = l.CustomerID
        JOIN CreditCards cc ON cu.CustomerID = cc.CustomerID;
        """, ["CustomerID", "Name"]),

        ("Average Transaction Amount by Account Type", """
        SELECT a.AccountType, AVG(t.Amount) AS AvgTransaction
        FROM Accounts a
        JOIN Transactions t ON a.AccountID = t.AccountID
        GROUP BY a.AccountType;
        """, ["AccountType", "AvgTransaction"])
    ]

    for desc, query, headers in queries:
        print(f"\n{desc}")
        execute_query(query, headers)

if __name__ == "__main__":
    menu()

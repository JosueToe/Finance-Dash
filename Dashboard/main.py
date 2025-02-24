# Import functions from respective modules
from functions.bank_functions import add_bank_account, edit_bank_account, delete_bank_account  
from functions.stock_functions import add_stock, edit_stock, delete_stock  
from functions.salary_functions import add_salary, edit_salary, delete_salary  
from functions.goal_functions import add_financial_goal, edit_financial_goal, delete_financial_goal  
from functions.expense_functions import add_expense, edit_expense, delete_expense  
from functions.crypto_functions import add_crypto, edit_crypto, delete_crypto  

# Import dashboard and reporting functions
from functions.dashboard_functions import display_dashboard  
from functions.report_functions import expense_breakdown, cash_flow_report, record_net_worth, net_worth_trend  

# Import backup and restore functions
from functions.backup_functions import backup_database, restore_database  


def main_menu():
    """
    Displays the main menu for the Finance and Budgeting Dashboard application.
    Users can navigate through various options to manage their financial data.
    """
    print("Welcome to the Finance and Budgeting Dashboard!")
    while True:
        # Display menu options.
        print("\nMain Menu:")
        print("1. Add Bank Account")
        print("2. Add Stock")
        print("3. Add Salary")
        print("4. Add Financial Goal")
        print("5. Add Expense")
        print("6. View Dashboard")
        print("7. Backup Database")
        print("8. Restore Database")
        print("9. View Expense Breakdown")
        print("10. View Cash Flow Report")
        print("11. Record Net Worth")  # Option to record net worth.
        print("12. View Net Worth Trend")  # Option to view net worth over time.
        print("13. Edit Bank Account")
        print("14. Delete Bank Account")
        print("16. Edit Stock")
        print("17. Delete Stock")
        print("18. Edit Expense")
        print("19. Delete Expense")
        print("20. Edit Salary")
        print("21. Delete Salary")
        print("22. Edit Financial Goal")
        print("23. Delete Financial Goal")
        print("24. Add Cryptocurrency")
        print("25. Edit Cryptocurrency")
        print("26. Delete Cryptocurrency")
        print("27. Exit")

        # Get the user's choice.
        choice = input("Choose an option: ")
        if choice == "1":
            add_bank_account()  # Call function to add a bank account.
        elif choice == "2":
            add_stock()  # Call function to add stock details.
        elif choice == "3":
            add_salary()  # Call function to add salary information.
        elif choice == "4":
            add_financial_goal()  # Call function to set a financial goal.
        elif choice == "5":
            add_expense()  # Call function to log an expense.
        elif choice == "6":
            display_dashboard()  # Call function to display the financial dashboard.
        elif choice == "7":
            backup_database()  # Call function to backup the database.
        elif choice == "8":
            restore_database()  # Call function to restore the database from a backup.
        elif choice == "9":
            expense_breakdown()  # Call function to view expense breakdown.
        elif choice == "10":
            cash_flow_report()  # Call function to view cash flow report.
        elif choice == "11":
            record_net_worth()  # Call function to record the user's net worth.
        elif choice == "12":
            net_worth_trend()  # Call function to view net worth trend over time.
        elif choice == "13":
            edit_bank_account()  # Call function to edit bank account details.
        elif choice == "14":
            delete_bank_account()  # Call function to delete a bank account.
            # Add these to the main menu logic:
        elif choice == "16":
            edit_stock()
        elif choice == "17":
            delete_stock()
        elif choice == "18":
            edit_expense()
        elif choice == "19":
            delete_expense()
        elif choice == "20":
            edit_salary()
        elif choice == "21":
            delete_salary()
        elif choice == "22":
             edit_financial_goal()
        elif choice == "23":
            delete_financial_goal()
        elif choice == "24":
            add_crypto()
        elif choice == "25":
            edit_crypto()
        elif choice == "26":
            delete_crypto()
        elif choice == "27":
            print("Goodbye!")  # Exit the application.
            break
        else:
            # Handle invalid input.
            print("Invalid choice. Please try again.")

# Check if the script is run directly.
if __name__ == "__main__":
    main_menu()  # Start the main menu of the application.
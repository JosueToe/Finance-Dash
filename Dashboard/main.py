from functions.user_functions import add_bank_account
from functions.stock_functions import add_stock
from functions.salary_functions import add_salary
from functions.goal_functions import add_financial_goal
from functions.expense_functions import add_expense
from functions.dashboard_functions import display_dashboard
from functions.backup_functions import backup_database, restore_database
from functions.report_functions import expense_breakdown, cash_flow_report, record_net_worth, net_worth_trend
from functions.edit_delete_functions import  edit_bank_account, delete_bank_account

def main_menu():
    print("Welcome to the Finance and Budgeting Dashboard!")
    while True:
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
        print("11. Record Net Worth")  # Corrected description
        print("12. View Net Worth Trend")  # Corrected description
        print("13. Edit Bank Account")
        print("14. Delete Bank Account")
        print("15. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            add_bank_account()
        elif choice == "2":
            add_stock()
        elif choice == "3":
            add_salary()
        elif choice == "4":
            add_financial_goal()
        elif choice == "5":
            add_expense()
        elif choice == "6":
            display_dashboard()
        elif choice == "7":
            backup_database()
        elif choice == "8":
            restore_database()
        elif choice == "9":
            expense_breakdown()
        elif choice == "10":
            cash_flow_report()
        elif choice == "11":  # Record net worth
            record_net_worth()
        elif choice == "12":  # View net worth trend
            net_worth_trend()
        elif choice == "13":
            edit_bank_account()
        elif choice == "14":
            delete_bank_account()
        elif choice == "15":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
# this is tony first comment
# Hello tony this is a test comment!
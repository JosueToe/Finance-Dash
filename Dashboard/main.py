from functions.user_functions import add_bank_account
from functions.stock_functions import add_stock
from functions.salary_functions import add_salary
from functions.goal_functions import add_financial_goal
from functions.expense_functions import add_expense   # Updated import

def main_menu():
    print("Welcome to the Finance and Budgeting Dashboard!")
    while True:
        print("\nMain Menu:")
        print("1. Add Bank Account")
        print("2. Add Stock")
        print("3. Add Salary")
        print("4. Add Financial Goal")
        print("5. Add Expense")  # Updated menu option
        print("6. Exit")

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
            add_expense()  # Updated function call
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

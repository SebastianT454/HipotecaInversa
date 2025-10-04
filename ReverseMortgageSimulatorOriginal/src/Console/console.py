import sys
sys.path.append('src')
from  ReverseMortgage import MonthlyPayment

def main_menu():
    client = None

    print("--Reverse Mortgage Simulator--")
    print('')
    while True:
        print("Main Menu:")
        print("1. Change Client Information")
        print("2. Show Client Information")
        print("3. Calculate Reverse Mortgage")
        print("4. Exit")
        print('')
        choice = input("Enter your choice: ")
        print('')

        if choice == '1':
            client = change_client_information()
        elif choice == '2':
            if client is None:
                print("Client information not found. Please enter client information first.")
                print('')
            else:
                print(client)
                print('')
        elif choice == '3':
            calculate_reverse_mortgage(client)
            break
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def change_client_information():
    while True:
        try:
            age = int(input("Enter age: "))
            gender = input("Enter gender (M/F): ").strip().upper()
            marital_status = input("Enter marital status (Married/Single/Widowed/Divorced): ").strip().lower()
            spouses_age = None
            spouses_gender = None
            if marital_status.lower() == 'married':
                print('')
                spouses_age = int(input("Enter spouse's age: "))
                spouses_gender = input("Enter spouse's gender (M/F): ").strip().upper()
            
            client = MonthlyPayment.Client(age, gender, marital_status, spouses_age, spouses_gender)

            break
        except (ValueError, MonthlyPayment.ClientException) as e:
            print('')
            print(f"Invalid input: {e}")
            print('')
    print('')
    print("Client information updated successfully.")
    print('')

    return client
            

def calculate_reverse_mortgage(client: MonthlyPayment.Client):
    while True:
        try:
            property_value = float(input("Enter property value: "))
            interest_rate = float(input("Enter interest rate: "))
            reverse_mortgage = MonthlyPayment.ReverseMortgage(property_value, interest_rate, client)
            break
        except (ValueError, MonthlyPayment.ReverseMortgageException) as e:
            print('')
            print(f"Invalid input: {e}")
            print('')
    print('')
    print("Reverse mortgage calculated successfully.")
    print('')
    print(reverse_mortgage)
    print('')
        

if __name__ == "__main__":
    main_menu()
    

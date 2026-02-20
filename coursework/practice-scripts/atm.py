balance = 1000.00

# Function to display the current balance
def display_balance():
    return f"Current balance: €{balance:.2f}"

# Function to handle withdrawals
def withdraw():
    global balance

    while True:
        try:
            amount = float(input("Enter the amount to withdraw: ")) # askes to withdraw an amount

            if amount <= 0: # negative or zero withdrawal amounts are not allowed
                print("Invalid amount. Please enter a positive number.")
                continue
            if amount > balance: # user asked to withdraw more than they have in their balance
                print(f"Insufficient funds. {display_balance()}")
                continue

            balance -= amount
            print(f"You withdrew: €{amount:.2f}")   # prints withdrawal amount
            print(f"Remaining balance: €{balance:.2f}")
            return balance # returns the updated balance after withdrawal optional, but allows for future expansion (e.g. multiple transactions in one session)

        except ValueError: # handles non-numeric input for withdrawal amount
            print("Invalid input. Please enter a numeric value.")

# starts the ATM program
def atm():
    correct_pin = "1234"
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        pin = input("Enter your PIN: ")
        if pin == correct_pin:
            print("PIN accepted.")
            print(display_balance())
            withdraw() # allows user to withdraw money and updates balance, then exits the program
            return
        else:
            attempts += 1
            if attempts < max_attempts: # lets user know how many attempts they have left
                print(f"Incorrect PIN. You have {max_attempts - attempts} attempts left.")
            else: # locks account after 3 incorrect attempts
                print("Account locked due to too many incorrect attempts.")
                return False

atm()

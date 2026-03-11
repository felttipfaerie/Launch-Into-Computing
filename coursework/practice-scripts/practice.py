balance = 1000.00

def display_balance():
    return f"Current balance: ${balance:.2f}"

def withdraw():
    amount = float(input("Enter the amount to withdraw: "))
    global balance
    while True:
        try:
            if amount <= 0:
                print("Invalid amount. Please enter a positive number.")
                continue
            if amount > balance:
                print(f"Insufficient funds. Current balance: ${display_balance()}.")
                continue
            elif amount <= balance:
                balance -= amount
                return f"Withdrawal successful. Remaining balance: ${balance:.2f}"
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
        break

def code():
    correct_pin = "1234"
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        pin = input("Enter your PIN: ")
        if pin == correct_pin:
            print("PIN accepted.")
            withdraw()
        else:
            attempts += 1
            if attempts < max_attempts:
                print(f"Incorrect PIN. You have {max_attempts - attempts} attempts left.")
            else:
                print("Account locked due to too many incorrect attempts.")
                return False
    break

code()
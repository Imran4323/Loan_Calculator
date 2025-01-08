 # -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 22:45:56 2024

@author: Talha.
"""
"""
NexGen Loans is a Python-based loan calculator designed to simplify complex financial calculations for North American consumers.
The tool provides comprehensive, user-friendly loan analysis for three critical loan types: Mortgage, Education, and Car loans,
calculating all major loans at once. By implementing advanced amortization algorithms, the calculator enables users to instantly
compute monthly payments, generate detailed repayment schedules and understand the long-term financial implications of their
borrowing decisions.

This application stands out through its robust input validation, precise calculation mechanisms and user-centric design.
With features like automatic amortization schedule generation and file export capabilities, users can input loan details such 
as principal amount, interest rate, and loan term, receiving an immediate, comprehensive breakdown of their loan's financial 
trajectory. NexGen Loans transforms financial computations into accessible, actionable insights and empowering individuals to make
informed financial choices with confidence and clarity.
"""
#Import datetime for adding timestamps to loan documentation file    
from datetime import datetime

def get_input(user, input_type=float, min_value=0):
    """Get a valid input from the user ."""
    while True:
        try:
            value = input_type(input(user))
            if value < min_value: # Ensure the input meets the minimum value requirement.
                print(f"Please enter a value greater than or equal to {min_value}.")
                continue
            return value # Return Valid input
        except ValueError:
            # Handle invalid input and ask user to try again.
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
            
            

def get_loan_type():
    """Prompt user to select a loan type."""
    loan_types = {
        '1': 'Mortgage',# Option 1: Mortgage Loan
        '2': 'Education',# Option 2: Education Loan
        '3': 'Car' # Option 3: Car Loan
    }
    print("\nWhich type of loan you want to calculate today:")
    for key, value in loan_types.items():
        print(f"{key}) {value} Loan") #Show available Loan Types.
    
    while True:
    # Validate user input for a type of loan selection.
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice in loan_types:
            return loan_types[choice] # Return selected loan type
        print("Invalid choice. Please enter 1, 2, or 3.")# Retry if invalid input.
        
        

def calculate_monthly_payment(principal, annual_interest_rate, years):
    """Calculate the monthly payment for a loan."""
    if principal<=0 or years<=0 or annual_interest_rate<0: # Check for valid loan parameters
        print("Invalid Loan Parameters.")
        return None
    if annual_interest_rate == 0: # Edge case where the interest rate is Zero
        return principal / (years * 12)# Just apply simple division.
    
    #Converting annual interest rate to monthly interest rate.
    monthly_rate = annual_interest_rate / 12 / 100
    num_payments = years * 12 #Total number of monthly payments.

    # Amortization formula applied to calculate monthly payments.
    return principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)



def amortization_table(principal, annual_interest_rate, years, monthly_payment):
    """Generate an amortization table for the loan."""
    table = []# Initialize the list to store amortization data.
    remaining_balance = principal #Begin with the loan amount.
    monthly_rate = annual_interest_rate / 12 / 100 # Convert annual interest rate to monthly interest rate.
    
    #Loop through each month of loan term
    for month in range(1, years * 12 + 1):
        interest_payment = remaining_balance * monthly_rate # Interest part of payment
        principal_payment = monthly_payment - interest_payment # Principal portion of monthly payment
        remaining_balance -= principal_payment # Update the remaining balance
        
        # Append each month's breakdown to the table.
        table.append({
            'month': month,
            'payment': monthly_payment,
            'principal': principal_payment,
            'interest': interest_payment,
            'remaining_balance': max(0, remaining_balance) # Ensure Remaining balance doesn't go negative
        })
    
    return table # Return the complete Amortization Table


def format_currency(amount):
    """Format a number as currency."""
    return f"${amount:,.2f}"# Format number with commas and two decimal places for readability


def calculate_loan_details(loan_type):
    """Generic loan calculation based on the loan type."""
    print(f"\n=== {loan_type} Loan Calculator ===")
    
    #Specific loan types(Mortgage and Car) require a  down Payment.
    if loan_type == "Mortgage" or loan_type == "Car":
        value = get_input(f"Enter the {loan_type.lower()} value: $") # Get the total loan value
        down_payment = get_input(f"Enter the down payment for your {loan_type.lower()} loan: $", min_value=0)
        
        while down_payment > value:
            # Ensure the Down Payment is not greater than or equal to Loan Value.
            print(f"Down payment cannot be greater than {loan_type.lower()} value.")
            down_payment = get_input(f"Enter the down payment for your {loan_type.lower()} loan: $", min_value=0)
        principal = value - down_payment #Calculate Principal after down payment
    else:
        # For Education Loans directly get the loan amount.
        principal = get_input(f"Enter the {loan_type.lower()} loan amount: $", min_value=0)
    
    
    #Get the interest rate and loan term from user
    annual_interest_rate = get_input("Enter the annual interest rate (%): ", float)
   
    years = int(get_input("Enter the loan term in years: ", int, min_value=1)) #Get loan term in years.
    
    # Calculate Monthly payments and generating Amortization Table.
    monthly_payment = calculate_monthly_payment(principal, annual_interest_rate, years)
    if monthly_payment is None:
        return None
    schedule = amortization_table(principal, annual_interest_rate, years, monthly_payment)
    
    return principal, annual_interest_rate, years, monthly_payment, schedule



def amortization_to_file(loan_type, schedule, filename="loan_data.txt"):
    """Save the amortization table to a file."""
    try:
        with open(filename, 'w') as f:
            # Write the current data and loan type to the file.
            f.write(f"{datetime.now().strftime('%Y-%m-%d - %A  %H:%M:%S')}\n") # The 'strftime()' method formats the current date and time
            f.write(f"Your {loan_type} Loan : Repayment Pathway\n")
            f.write("=" * 70 + "\n")
            f.write("Month\t Payment \t\tPrincipal\t \tInterest\t Remaining Balance\n")
            f.write("=" * 70 + "\n")
            
            for i in schedule: # Write each month of the installment Plan to the file.
                f.write(f"{i['month']}\t \t{format_currency(i['payment'])} \t"
                        f" \t{format_currency( i ['principal'])} \t"
                        f"\t{format_currency(i ['interest'])}\t"
                        f"\t{format_currency(i ['remaining_balance'])}\n")
            f.write("=" * 70 + "\n")
        print(f"Amortization Table saved to {filename}") # Notify user that file has been successfully saved
    except IOError:
        print(f"Error: Unable to write to file {filename}")# Handles errors during file operations.
        
        

def calculate_loan():
    """Calculate loan based on user's choice."""
    loan_type = get_loan_type() # Get the Loan type from user.
    loan_details = calculate_loan_details(loan_type)
    
    if loan_details is None:
        print("Loan calculation failed due to invalid inputs. Please try again.")
        return # Exit if loan calculations failed
    
    principal, annual_interest_rate, years, monthly_payment, schedule=loan_details
    
    # Showing Loan Summary and Results.
    print(f"\n{loan_type} Loan Summary:")
    print(f"Principal: {format_currency(principal)}")
    print(f"Annual Interest Rate: {annual_interest_rate}%")
    print(f"Loan Term: {years} years")
    print(f"Monthly Payment: {format_currency(monthly_payment)}")
    
    # Calculate and display total interest and total amount paid 
    total_interest = sum(i['interest'] for i in schedule)
    print(f"Total Interest Paid: {format_currency(total_interest)}")
    print(f"Total Amount Paid: {format_currency(principal + total_interest)}")
    
    # Saving Loan Repayment to the file
    amortization_to_file(loan_type, schedule)
    


def main():
    """Main function to run the loan calculator program."""
    print("*** Welcome to NexGen Loans ***")
    
    while True:
        calculate_loan() # Perform a Loan calculation
        
        while True:
              user_choice=input("\nWould you like to calculate another loan? (Yes/No): ").strip()
              if user_choice in ['Yes','No']:
                  break
              print("Please enter 'Yes' or 'No'." )
              
        if user_choice=='No':
              print("Thank you for choosing NexGen Loans\nYour Future, Our Focus...\nSee You Soon !")
              break         
if __name__ == "__main__":
    main() # Calling main function to start the Program
    
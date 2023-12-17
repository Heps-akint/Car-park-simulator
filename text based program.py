import csv
from datetime import datetime
import os

# Constants
PARKING_SPACES = 10
HOURLY_RATE = 2
CSV_FILE = 'parking_records.csv'

# Global Variables
parking_records = []
available_spaces = list(range(1, PARKING_SPACES + 1))

# Functions
def read_parking_records():
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                parking_records.append(row)
                if row['Exit Time'] == '':
                    available_spaces.remove(int(row['Parking Space']))
                    
def write_parking_records():
    fieldnames = ['Ticket Number', 'Registration Number', 'Entry Time', 'Exit Time', 'Parking Space', 'Parking Fee']
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in parking_records:
            writer.writerow(record)

def main_menu():
    while True:
        print("\nCar Park Simulator")
        print("1: Enter the Car Park")
        print("2: Exit the Car Park")
        print("3: View Available Parking Spaces")
        print("4: Query Parking Record by Ticket Number")
        print("5: Quit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            enter_car_park()
        elif choice == '2':
            exit_car_park()
        elif choice == '3':
            view_available_spaces()
        elif choice == '4':
            query_parking_record()
        elif choice == '5':
            write_parking_records()
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please select a valid option.")


def enter_car_park():
    if not available_spaces:
        print("Sorry, the car park is full.")
        return
    
    registration_number = input("Enter the vehicle's registration number: ").strip()
    if not registration_number:
        print("Registration number cannot be empty.")
        return
    
    entry_time = datetime.now()
    parking_space = available_spaces.pop(0)
    ticket_number = len(parking_records) + 1
    
    parking_record = {
        'Ticket Number': ticket_number,
        'Registration Number': registration_number,
        'Entry Time': entry_time.strftime("%Y-%m-%d %H:%M:%S"),
        'Exit Time': '',
        'Parking Space': parking_space,
        'Parking Fee': ''
    }
    parking_records.append(parking_record)
    
    print(f"Vehicle parked. Ticket Number: {ticket_number}, Parking Space: {parking_space}")
    print(f"Remaining Spaces: {len(available_spaces)}/{PARKING_SPACES}")


def exit_car_park():
    registration_number = input("Enter the vehicle's registration number: ").strip()
    if not registration_number:
        print("Registration number cannot be empty.")
        return
    
    exit_time = datetime.now()
    
    # Find the parking record
    parking_record = None
    for record in parking_records:
        if record['Registration Number'] == registration_number and record['Exit Time'] == '':
            parking_record = record
            break
    
    if not parking_record:
        print("Record not found. Please check the registration number and try again.")
        return
    
    # Calculate parking fee
    entry_time = datetime.strptime(parking_record['Entry Time'], "%Y-%m-%d %H:%M:%S")
    duration = exit_time - entry_time
    hours = duration.total_seconds() / 3600
    parking_fee = round(hours * HOURLY_RATE, 2)
    
    # Update parking record
    parking_record['Exit Time'] = exit_time.strftime("%Y-%m-%d %H:%M:%S")
    parking_record['Parking Fee'] = parking_fee
    available_spaces.append(int(parking_record['Parking Space']))
    available_spaces.sort()
    
    print(f"Vehicle exited. Parking Fee: £{parking_fee}")
    print(f"Remaining Spaces: {len(available_spaces)}/{PARKING_SPACES}")
    

def view_available_spaces():
    print(f"Available Parking Spaces: {len(available_spaces)}/{PARKING_SPACES}")
    if available_spaces:
        print("Available Spaces:", ", ".join(map(str, available_spaces)))
    else:
        print("No available spaces.")


def query_parking_record():
    ticket_number = input("Enter the ticket number: ").strip()
    if not ticket_number:
        print("Ticket number cannot be empty.")
        return
    if not ticket_number.isdigit():
        print("Invalid ticket number. Please enter a valid number.")
        return
    
    ticket_number = int(ticket_number)  # Convert to integer
    parking_record = next((record for record in parking_records if int(record['Ticket Number']) == ticket_number), None)
    
    if not parking_record:
        print("Record not found. Please check the ticket number and try again.")
        return
    
    print("\nParking Record:")
    for key, value in parking_record.items():
        print(f"{key}: {value}")


# Main Execution
if __name__ == "__main__":
    read_parking_records()
    main_menu()

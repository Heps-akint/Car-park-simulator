import tkinter as tk
from tkinter import simpledialog, messagebox
import csv
from datetime import datetime
import os

# Constants
PARKING_SPACES = 10  # Total number of parking spaces available
HOURLY_RATE = 2  # Hourly rate for parking
CSV_FILE = 'parking_records.csv'  # File to store parking records

class CarParkSimulatorGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parking_records = []  # List to store parking records
        self.available_spaces = list(range(1, PARKING_SPACES + 1))  # List to store available parking spaces
        self.read_parking_records()  # Initialize parking records and available spaces

        # Setting up the GUI window
        self.title("Car Park Simulator")
        self.geometry("500x300")

        # Adding buttons for different functionalities
        tk.Button(self, text="Enter the Car Park", command=self.enter_car_park).pack(pady=5)
        tk.Button(self, text="Exit the Car Park", command=self.exit_car_park).pack(pady=5)
        tk.Button(self, text="View Available Parking Spaces", command=self.view_available_spaces).pack(pady=5)
        tk.Button(self, text="Query Parking Record by Ticket Number", command=self.query_parking_record).pack(pady=5)
        tk.Button(self, text="Quit", command=self.quit_program).pack(pady=5)

        # Adding an output area to display information to the user
        self.output_area = tk.Text(self, height=10, width=50, wrap='word')
        self.output_area.pack(pady=5)
        self.output_area.insert('1.0', "Welcome to the Car Park Simulator!")

    def read_parking_records(self):
        """Reads parking records from the CSV file and updates the available spaces."""
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.parking_records.append(row)
                    if row['Exit Time'] == '':
                        self.available_spaces.remove(int(row['Parking Space']))
                        
    def write_parking_records(self):
        """Writes parking records to the CSV file."""
        fieldnames = ['Ticket Number', 'Registration Number', 'Entry Time', 'Exit Time', 'Parking Space', 'Parking Fee']
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.parking_records:
                writer.writerow(record)

    def enter_car_park(self):
        """Handles the functionality for a vehicle entering the car park."""
        if not self.available_spaces:
            messagebox.showerror("Error", "The car park is full.")
            return
        
        registration_number = tk.simpledialog.askstring("Input", "Enter the vehicle's registration number:")
        if not registration_number:
            messagebox.showerror("Error", "Registration number cannot be empty.")
            return
        
        entry_time = datetime.now()
        parking_space = self.available_spaces.pop(0)
        ticket_number = len(self.parking_records) + 1
        
        parking_record = {
            'Ticket Number': ticket_number,
            'Registration Number': registration_number,
            'Entry Time': entry_time.strftime("%Y-%m-%d %H:%M:%S"),
            'Exit Time': '',
            'Parking Space': parking_space,
            'Parking Fee': ''
        }
        self.parking_records.append(parking_record)
        
        result = f"Vehicle parked. Ticket Number: {ticket_number}, Parking Space: {parking_space}\n"
        result += f"Remaining Spaces: {len(self.available_spaces)}/{PARKING_SPACES}"
        self.output_area.delete('1.0', tk.END)
        self.output_area.insert('1.0', result)

    def exit_car_park(self):
        """Handles the functionality for a vehicle exiting the car park."""
        registration_number = tk.simpledialog.askstring("Input", "Enter the vehicle's registration number:")
        if not registration_number:
            messagebox.showerror("Error", "Registration number cannot be empty.")
            return
        
        exit_time = datetime.now()
        parking_record = None
        for record in self.parking_records:
            if record['Registration Number'] == registration_number and record['Exit Time'] == '':
                parking_record = record
                break
        
        if not parking_record:
            messagebox.showerror("Error", "Record not found. Please check the registration number and try again.")
            return
        
        entry_time = datetime.strptime(parking_record['Entry Time'], "%Y-%m-%d %H:%M:%S")
        duration = exit_time - entry_time
        hours = duration.total_seconds() / 3600
        parking_fee = round(hours * HOURLY_RATE, 2)
        
        parking_record['Exit Time'] = exit_time.strftime("%Y-%m-%d %H:%M:%S")
        parking_record['Parking Fee'] = parking_fee
        self.available_spaces.append(int(parking_record['Parking Space']))
        self.available_spaces.sort()
        
        result = f"Vehicle exited. Parking Fee: £{parking_fee}\n"
        result += f"Remaining Spaces: {len(self.available_spaces)}/{PARKING_SPACES}"
        self.output_area.delete('1.0', tk.END)
        self.output_area.insert('1.0', result)

    def view_available_spaces(self):
        """Displays the available parking spaces."""
        result = f"Available Parking Spaces: {len(self.available_spaces)}/{PARKING_SPACES}\n"
        if self.available_spaces:
            result += "Available Spaces: " + ", ".join(map(str, self.available_spaces))
        else:
            result += "No available spaces."
        self.output_area.delete('1.0', tk.END)
        self.output_area.insert('1.0', result)

    def query_parking_record(self):
        """Queries a parking record based on the ticket number provided by the user."""
        ticket_number = tk.simpledialog.askstring("Input", "Enter the ticket number:")
        if not ticket_number:
            messagebox.showerror("Error", "Ticket number cannot be empty.")
            return
        if not ticket_number.isdigit():
            messagebox.showerror("Error", "Invalid ticket number. Please enter a valid number.")
            return
        
        ticket_number = int(ticket_number)
        parking_record = next((record for record in self.parking_records if int(record['Ticket Number']) == ticket_number), None)
        
        if not parking_record:
            messagebox.showerror("Error", "Record not found. Please check the ticket number and try again.")
            return
        
        result = "\nParking Record:\n"
        for key, value in parking_record.items():
            result += f"{key}: {value}\n"
        self.output_area.delete('1.0', tk.END)
        self.output_area.insert('1.0', result)

    def quit_program(self):
        """Closes the application."""
        self.write_parking_records()  # Ensure all records are saved before exiting
        self.destroy()

if __name__ == "__main__":
    app = CarParkSimulatorGUI()
    app.mainloop()
       

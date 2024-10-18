import tkinter as tk
from tkinter import messagebox
import json
import os
import datetime

# JSON file to store patient data
DATA_FILE = "data.json"

def load_data():
    """Load data from the JSON file. If the file is empty or corrupted, initialize it with an empty dictionary."""
    if not os.path.exists(DATA_FILE):
        return {}
    
    with open(DATA_FILE, "r") as file:
        if os.stat(DATA_FILE).st_size == 0:
            return {}

        return json.load(file)

def fetch_patient_details():
    """Fetch and display patient details based on Patient ID."""
    patient_id = patient_id_entry.get()
    if not patient_id:
        messagebox.showwarning("Input Error", "Please enter a Patient ID.")
        return

    data = load_data()
    today = str(datetime.date.today())

    if today in data:
        for record in data[today]:
            if record["patient_id"] == patient_id:
                # Clear previous details
                details_text.delete("1.0", tk.END)
                details_text.insert(tk.END, f"Patient ID: {record['patient_id']}\n")
                details_text.insert(tk.END, f"Name: {record['name']}\n")
                details_text.insert(tk.END, f"Blood Group: {record['blood_group']}\n")
                details_text.insert(tk.END, f"Age: {record['age']}\n")
                details_text.insert(tk.END, f"Gender: {record['gender']}\n")
                details_text.insert(tk.END, f"Issued Medicine:\n{record['issued_medicine']}\n")
                details_text.insert(tk.END, f"Additional Prescription:\n{record['additional_prescription']}\n")
                return

    messagebox.showwarning("Not Found", "Patient ID not found.")

def create_main_window():
    """Create the main GUI window."""
    global patient_id_entry, details_text

    window = tk.Tk()
    window.title("Patient Details Display")

    # Patient ID Entry
    tk.Label(window, text="Patient ID:").grid(row=0, column=0)
    patient_id_entry = tk.Entry(window)
    patient_id_entry.grid(row=0, column=1)

    # Fetch Details Button
    tk.Button(window, text="Fetch Patient Details", command=fetch_patient_details).grid(row=0, column=2)

    # Details Display Area
    tk.Label(window, text="Patient Details:").grid(row=1, column=0, columnspan=3)
    details_text = tk.Text(window, height=15, width=50)
    details_text.grid(row=2, column=0, columnspan=3)

    window.mainloop()

if __name__ == "__main__":
    create_main_window()

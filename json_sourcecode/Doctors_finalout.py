import tkinter as tk
from tkinter import messagebox
import random
import pyperclip
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
        # Check if the file is empty
        if os.stat(DATA_FILE).st_size == 0:
            return {}

        return json.load(file)

def save_data(data):
    """Save data to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def create_patient_table():
    """Initialize the JSON database if it doesn't exist or is empty."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump({}, file)
    else:
        # If the file exists but is empty, reset it to an empty dictionary
        if os.stat(DATA_FILE).st_size == 0:
            with open(DATA_FILE, "w") as file:
                json.dump({}, file)

def get_random_patient_id():
    """Generate a random 3-digit patient ID."""
    return str(random.randint(100, 999)).zfill(3)

def submit_new_patient(patient_id=None):
    """Submit a new patient's data."""
    data = load_data()
    patient_id = patient_id or get_random_patient_id()  # Use the provided patient_id or generate a new one
    name = name_entry.get()
    blood_group = blood_group_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    issued_medicine = issued_medicine_entry.get("1.0", tk.END).strip()
    additional_prescription = additional_prescription_entry.get("1.0", tk.END).strip()

    if not name or not blood_group or not age or not gender:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    today = str(datetime.date.today())
    if today not in data:
        data[today] = []

    data[today].append({
        "patient_id": patient_id,
        "name": name,
        "blood_group": blood_group,
        "age": age,
        "gender": gender,
        "issued_medicine": issued_medicine,
        "additional_prescription": additional_prescription,
        "date": datetime.datetime.now().isoformat()
    })

    save_data(data)
    messagebox.showinfo("Success", f"New patient added with Patient ID: {patient_id}")
    clear_fields()

def check_old_patient():
    """Check if a patient exists by their ID and load their data."""
    patient_id = patient_id_entry.get()
    if not patient_id:
        messagebox.showwarning("Input Error", "Please enter a Patient ID.")
        return

    data = load_data()
    today = str(datetime.date.today())

    if today in data:
        for record in data[today]:
            if record["patient_id"] == patient_id:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, record["name"])
                blood_group_entry.delete(0, tk.END)
                blood_group_entry.insert(0, record["blood_group"])
                age_entry.delete(0, tk.END)
                age_entry.insert(0, record["age"])
                gender_entry.delete(0, tk.END)
                gender_entry.insert(0, record["gender"])
                issued_medicine_entry.delete("1.0", tk.END)
                issued_medicine_entry.insert("1.0", record["issued_medicine"])
                additional_prescription_entry.delete("1.0", tk.END)
                additional_prescription_entry.insert("1.0", record["additional_prescription"])

                pyperclip.copy(patient_id)
                messagebox.showinfo("Patient Found", f"Patient ID {patient_id} found and copied to clipboard.")
                return
    messagebox.showwarning("Not Found", "Patient ID not found.")

def update_old_patient_medicine():
    """Update the issued medicine for an old patient."""
    patient_id = patient_id_entry.get()
    if not patient_id:
        messagebox.showwarning("Input Error", "Please enter a Patient ID.")
        return

    data = load_data()
    today = str(datetime.date.today())

    if today in data:
        for record in data[today]:
            if record["patient_id"] == patient_id:
                issued_medicine = issued_medicine_entry.get("1.0", tk.END).strip()
                additional_prescription = additional_prescription_entry.get("1.0", tk.END).strip()

                if not issued_medicine and not additional_prescription:
                    messagebox.showwarning("Input Error", "Please enter new medicine or additional prescriptions to update.")
                    return

                clear_old = messagebox.askyesno("Clear Old Records", "Do you want to clear old medicine records?")
                
                if clear_old:
                    record["issued_medicine"] = issued_medicine
                else:
                    record["issued_medicine"] += f"\n{issued_medicine}"

                record["additional_prescription"] = additional_prescription
                save_data(data)

                messagebox.showinfo("Success", f"Medicine updated for Patient ID: {patient_id}")
                clear_fields()
                return
    messagebox.showwarning("Not Found", "Patient ID not found.")

def clear_fields():
    """Clear all input fields."""
    patient_id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    blood_group_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    issued_medicine_entry.delete("1.0", tk.END)
    additional_prescription_entry.delete("1.0", tk.END)

def check_biometric_device():
    """
    Simulates the detection of an external biometric device.
    In a real scenario, you would replace this with actual device detection logic.
    Returns True if a device is connected, otherwise False.
    """
    # Simulate checking for an external device
    # In real-world applications, you'd interface with the device's SDK or API
    device_connected = False  # Set this to True if a device is detected

    return device_connected

def handle_biometric_input():
    """Handle biometric input and create the main form for the user to fill additional details."""
    # First, check if a biometric device is connected
    if not check_biometric_device():
        proceed_with_id = messagebox.askyesno(
            "No Biometric Device", 
            "No external biometric device available. Could we proceed with Patient ID?"
        )
        if proceed_with_id:
            # If the user chooses to proceed with Patient ID, create the main window
            create_main_window()
        else:
            # If the user selects 'No', just exit the function without doing anything
            return
    else:
        # If a device is connected, proceed
        create_main_window()

        # Simulate getting a unique biometric hash from a fingerprint scanner
        # In a real application, you would interface with a fingerprint reader library
        biometric_hash = "FINGERPRINT_HASH_12345"  # Simulated hash

        # Pre-populate the patient_id_entry with the biometric hash
        patient_id_entry.delete(0, tk.END)
        patient_id_entry.insert(0, biometric_hash)
    
        messagebox.showinfo("Biometric ID", f"Biometric ID generated: {biometric_hash}")

def start_method_selection():
    """Start by asking the user to choose between Patient ID and Biometric ID."""
    selection_window = tk.Tk()
    selection_window.title("Select Identification Method")
    selection_window.geometry("400x300")  # Increase dialog box size

    tk.Label(selection_window, text="Choose Identification Method", font=("Arial", 16)).pack(pady=20)

    tk.Button(selection_window, text="Patient ID", command=lambda: [selection_window.destroy(), create_main_window()], font=("Arial", 14)).pack(pady=10)
    tk.Button(selection_window, text="Biometric ID", command=lambda: [selection_window.destroy(), handle_biometric_input()], font=("Arial", 14)).pack(pady=10)

    selection_window.mainloop()

def create_main_window():
    """Create the main GUI window."""
    global patient_id_entry, name_entry, blood_group_entry, age_entry, gender_entry
    global issued_medicine_entry, additional_prescription_entry

    window = tk.Tk()
    window.title("Hospital Database")
    window.geometry("800x600")  # Increase main window size

    tk.Label(window, text="Patient ID:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
    patient_id_entry = tk.Entry(window, font=("Arial", 14))
    patient_id_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(window, text="Check Old Patient", command=check_old_patient, font=("Arial", 14)).grid(row=0, column=2, padx=10, pady=10)
    tk.Button(window, text="New Patient", command=lambda: submit_new_patient(patient_id=None), font=("Arial", 14)).grid(row=0, column=3, padx=10, pady=10)
    tk.Button(window, text="Update Medicine", command=update_old_patient_medicine, font=("Arial", 14)).grid(row=0, column=4, padx=10, pady=10)

    tk.Label(window, text="Name:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
    name_entry = tk.Entry(window, font=("Arial", 14))
    name_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(window, text="Blood Group:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10)
    blood_group_entry = tk.Entry(window, font=("Arial", 14))
    blood_group_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(window, text="Age:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=10)
    age_entry = tk.Entry(window, font=("Arial", 14))
    age_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(window, text="Gender:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=10)
    gender_entry = tk.Entry(window, font=("Arial", 14))
    gender_entry.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(window, text="Issued Medicine:", font=("Arial", 14)).grid(row=5, column=0, padx=10, pady=10)
    issued_medicine_entry = tk.Text(window, height=5, width=30, font=("Arial", 14))
    issued_medicine_entry.grid(row=5, column=1, padx=10, pady=10)

    tk.Label(window, text="Additional Prescription:", font=("Arial", 14)).grid(row=6, column=0, padx=10, pady=10)
    additional_prescription_entry = tk.Text(window, height=5, width=30, font=("Arial", 14))
    additional_prescription_entry.grid(row=6, column=1, padx=10, pady=10)

    tk.Button(window, text="Clear Fields", command=clear_fields, font=("Arial", 14)).grid(row=7, columnspan=5, padx=10, pady=20)

    window.mainloop()

if __name__ == "__main__":
    create_patient_table()  
    start_method_selection()
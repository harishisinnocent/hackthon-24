import tkinter as tk
from tkinter import messagebox
import json
import os
import datetime
import hashlib

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

def is_biometric_device_connected():
    """Check if a biometric device is connected."""
    # This is a placeholder; replace it with actual device detection logic.
    return os.path.exists("/dev/biometric_device")  # Adjust this path as needed for your system

def fetch_patient_details(patient_id):
    """Fetch and display patient details based on Patient ID."""
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

def hash_fingerprint(fingerprint_data):
    """Generate a SHA-256 hash of the given fingerprint data."""
    return hashlib.sha256(fingerprint_data.encode()).hexdigest()

def scan_biometric():
    """Simulate a biometric scan to get a fingerprint ID."""
    if not is_biometric_device_connected():
        messagebox.showwarning("Device Not Connected", "No external biometric device is connected.")
        return

    # Simulate getting a unique fingerprint from a fingerprint scanner
    # In a real application, replace this with actual biometric device interaction
    simulated_fingerprint = "SimulatedFingerprintData"  # Placeholder for actual fingerprint data
    biometric_id = hash_fingerprint(simulated_fingerprint)

    messagebox.showinfo("Biometric Scan", f"Biometric ID scanned: {biometric_id}")
    # Fetch patient details based on the scanned biometric ID
    fetch_patient_details(biometric_id)

def ask_patient_id_or_biometric():
    """Ask the user if they want to enter a Patient ID or scan a Biometric ID."""
    response = messagebox.askquestion("Patient ID or Biometric", 
                                       "Do you want to fetch details using:\n- Yes: Biometric ID\n- No: Patient ID")

    if response == "yes":
        scan_biometric()
    else:
        patient_id = patient_id_entry.get()
        fetch_patient_details(patient_id)

def create_main_window():
    """Create the main GUI window."""
    global patient_id_entry, details_text

    window = tk.Tk()
    window.title("Patient Details Display")
    window.geometry("800x600")  # Increase window size

    # Patient ID Entry
    tk.Label(window, text="Patient ID:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
    patient_id_entry = tk.Entry(window, font=("Arial", 14))
    patient_id_entry.grid(row=0, column=1, padx=10, pady=10)

    # Fetch Details Button
    tk.Button(window, text="Choose ID or Biometric", command=ask_patient_id_or_biometric, font=("Arial", 14)).grid(row=0, column=2, padx=10, pady=10)

    # Details Display Area
    tk.Label(window, text="Patient Details:", font=("Arial", 16)).grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    details_text = tk.Text(window, height=20, width=70, font=("Arial", 12))
    details_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_main_window()
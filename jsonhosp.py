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

def submit_new_patient():
    """Submit a new patient's data."""
    data = load_data()
    patient_id = get_random_patient_id()
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

def create_main_window():
    """Create the main GUI window."""
    global patient_id_entry, name_entry, blood_group_entry, age_entry, gender_entry
    global issued_medicine_entry, additional_prescription_entry

    window = tk.Tk()
    window.title("Hospital Database")

    tk.Label(window, text="Patient ID:").grid(row=0, column=0)
    patient_id_entry = tk.Entry(window)
    patient_id_entry.grid(row=0, column=1)

    tk.Button(window, text="Check Old Patient", command=check_old_patient).grid(row=0, column=2)
    tk.Button(window, text="New Patient", command=submit_new_patient).grid(row=0, column=3)
    tk.Button(window, text="Update Medicine", command=update_old_patient_medicine).grid(row=0, column=4)

    tk.Label(window, text="Name:").grid(row=1, column=0)
    name_entry = tk.Entry(window)
    name_entry.grid(row=1, column=1)

    tk.Label(window, text="Blood Group:").grid(row=2, column=0)
    blood_group_entry = tk.Entry(window)
    blood_group_entry.grid(row=2, column=1)

    tk.Label(window, text="Age:").grid(row=3, column=0)
    age_entry = tk.Entry(window)
    age_entry.grid(row=3, column=1)

    tk.Label(window, text="Gender:").grid(row=4, column=0)
    gender_entry = tk.Entry(window)
    gender_entry.grid(row=4, column=1)

    tk.Label(window, text="Issued Medicine:").grid(row=5, column=0)
    issued_medicine_entry = tk.Text(window, height=5, width=30)
    issued_medicine_entry.grid(row=5, column=1)

    tk.Label(window, text="Additional Prescription:").grid(row=6, column=0)
    additional_prescription_entry = tk.Text(window, height=5, width=30)
    additional_prescription_entry.grid(row=6, column=1)

    tk.Button(window, text="Clear Fields", command=clear_fields).grid(row=7, columnspan=5)

    window.mainloop()

if __name__ == "__main__":
    create_patient_table()  
    create_main_window()

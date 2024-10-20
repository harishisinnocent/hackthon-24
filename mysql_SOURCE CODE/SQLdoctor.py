import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random
import pyperclip
import datetime
import os


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=4444,  # Your specified port
        user="root",
        password="0303",  # Your MySQL password
        database="hospital_db",
        auth_plugin="mysql_native_password"
    )

def create_patient_table():
    conn = connect_db()
    cursor = conn.cursor()
    today = datetime.date.today()
    table_name = f"prescriptions_{today}".replace('-', '_')
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        prescription_id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id VARCHAR(3),
        name VARCHAR(255),
        blood_group VARCHAR(10),
        age INT,
        gender VARCHAR(10),
        issued_medicine TEXT,
        additional_prescription TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP NULL
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_random_patient_id():
    return str(random.randint(100, 999)).zfill(3)

def submit_new_patient():
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

    conn = connect_db()
    cursor = conn.cursor()
    today = datetime.date.today()
    table_name = f"prescriptions_{today}".replace('-', '_')

    cursor.execute(f"""
    INSERT INTO {table_name} (patient_id, name, blood_group, age, gender, issued_medicine, additional_prescription)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (patient_id, name, blood_group, age, gender, issued_medicine, additional_prescription))

    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Success", f"New patient added with Patient ID: {patient_id}")
    clear_fields()

def check_old_patient():
    patient_id = patient_id_entry.get()
    if not patient_id:
        messagebox.showwarning("Input Error", "Please enter a Patient ID.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    today = datetime.date.today()
    table_name = f"prescriptions_{today}".replace('-', '_')

    cursor.execute(f"SELECT * FROM {table_name} WHERE patient_id = %s", (patient_id,))
    result = cursor.fetchone()

    if result:
        name_entry.delete(0, tk.END)
        name_entry.insert(0, result[2])
        blood_group_entry.delete(0, tk.END)
        blood_group_entry.insert(0, result[3])
        age_entry.delete(0, tk.END)
        age_entry.insert(0, result[4])
        gender_entry.delete(0, tk.END)
        gender_entry.insert(0, result[5])
        issued_medicine_entry.delete("1.0", tk.END)
        issued_medicine_entry.insert("1.0", result[6])
        additional_prescription_entry.delete("1.0", tk.END)
        additional_prescription_entry.insert("1.0", result[7])

        pyperclip.copy(patient_id)
        messagebox.showinfo("Patient Found", f"Patient ID {patient_id} found and copied to clipboard.")
    else:
        messagebox.showwarning("Not Found", "Patient ID not found.")

    cursor.close()
    conn.close()

def update_old_patient_medicine():
    patient_id = patient_id_entry.get()
    if not patient_id:
        messagebox.showwarning("Input Error", "Please enter a Patient ID.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    today = datetime.date.today()
    table_name = f"prescriptions_{today}".replace('-', '_')

    cursor.execute(f"SELECT * FROM {table_name} WHERE patient_id = %s", (patient_id,))
    result = cursor.fetchone()

    if not result:
        messagebox.showwarning("Not Found", "Patient ID not found.")
        cursor.close()
        conn.close()
        return

    issued_medicine = issued_medicine_entry.get("1.0", tk.END).strip()
    additional_prescription = additional_prescription_entry.get("1.0", tk.END).strip()

    if not issued_medicine and not additional_prescription:
        messagebox.showwarning("Input Error", "Please enter new medicine or additional prescriptions to update.")
        cursor.close()
        conn.close()
        return

    clear_old = messagebox.askyesno("Clear Old Records", "Do you want to clear old medicine records?")

    if clear_old:
        issued_medicine = issued_medicine
    else:
        existing_medicine = result[6]
        issued_medicine = existing_medicine + "\n" + issued_medicine

    cursor.execute(f"""
    UPDATE {table_name} 
    SET issued_medicine = %s, additional_prescription = %s
    WHERE patient_id = %s
    """, (issued_medicine, additional_prescription, patient_id))

    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Success", f"Medicine updated for Patient ID: {patient_id}")
    clear_fields()

def clear_fields():
    patient_id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    blood_group_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    issued_medicine_entry.delete("1.0", tk.END)
    additional_prescription_entry.delete("1.0", tk.END)

def create_main_window():
    global patient_id_entry, name_entry, blood_group_entry, age_entry, gender_entry
    global issued_medicine_entry, additional_prescription_entry

    window = tk.Tk()
    window.title("Hospital Database")
    window.geometry("700x500")  # Set the window size to 700x500 for larger space

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

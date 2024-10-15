import tkinter as tk
from tkinter import messagebox
import mysql.connector
import datetime

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=4444,  
        user="root",
        password="0303",  
        database="hospital_db",
        auth_plugin="mysql_native_password"
    )

def fetch_patient_details():
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
        # Clear previous details
        details_text.delete("1.0", tk.END)
        details_text.insert(tk.END, f"Patient ID: {result[1]}\n")
        details_text.insert(tk.END, f"Name: {result[2]}\n")
        details_text.insert(tk.END, f"Blood Group: {result[3]}\n")
        details_text.insert(tk.END, f"Age: {result[4]}\n")
        details_text.insert(tk.END, f"Gender: {result[5]}\n")
        details_text.insert(tk.END, f"Issued Medicine:\n{result[6]}\n")
        details_text.insert(tk.END, f"Additional Prescription:\n{result[7]}\n")
    else:
        messagebox.showwarning("Not Found", "Patient ID not found.")
    
    cursor.close()
    conn.close()

def create_main_window():
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

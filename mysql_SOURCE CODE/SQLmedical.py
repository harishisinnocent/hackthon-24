import tkinter as tk
from tkinter import messagebox
import mysql.connector
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

def check_biometric_driver():
    # Check if a specific biometric driver is connected
    # Adjust this check based on your actual biometric device driver
    # Example: Check if a specific driver is listed in device manager
    try:
        drivers = os.popen('wmic path Win32_PnPEntity get Name').read()
        if "Your Biometric Driver Name" in drivers:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking drivers: {e}")
        return False

def biometric_prompt():
    if not check_biometric_driver():
        proceed = messagebox.askyesno("Driver Not Connected", 
            "Biometric driver is not connected. Do you want to proceed with Patient ID?")
        if proceed:
            create_patient_id_window()
        else:
            exit_program()
    else:
        # Implement biometric ID logic here (not provided in the original request)
        messagebox.showinfo("Success", "Biometric driver is connected. Implement biometric logic here.")

def create_patient_id_window():
    global patient_id_entry, details_text

    window = tk.Tk()
    window.title("Patient Details Display")
    window.geometry("600x400")  # Set window size to 600x400

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

def exit_program():
    # Close the program
    messagebox.showinfo("Exit", "Exiting the program.")
    exit()

def main_menu():
    # Main menu dialog box for choosing between Patient ID and Biometric ID
    menu_window = tk.Tk()
    menu_window.title("Select ID Type")
    menu_window.geometry("400x200")  # Set window size to 400x200

    tk.Label(menu_window, text="Select ID Type:").grid(row=0, column=0, columnspan=2)

    # Buttons for Patient ID and Biometric ID
    tk.Button(menu_window, text="Patient ID", command=lambda: create_patient_id_window()).grid(row=1, column=0)
    tk.Button(menu_window, text="Biometric ID", command=biometric_prompt).grid(row=1, column=1)

    menu_window.mainloop()

if __name__ == "__main__":
    main_menu()  # Start the main menu

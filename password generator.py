import secrets
import string
import tkinter as tk
from tkinter import messagebox, filedialog

def generate_secure_password(length=12):
    if length < 12:
        raise ValueError("Password length should be at least 12 characters.")
    
    # Define the character sets
    alphabet = string.ascii_letters + string.digits + string.punctuation

    # Ensure the password has at least one character from each character set
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]

    # Fill the rest of the password length with random characters from the alphabet
    password += [secrets.choice(alphabet) for _ in range(length - 4)]

    # Shuffle the password list to prevent predictable sequences
    secrets.SystemRandom().shuffle(password)

    # Convert list to string
    return ''.join(password)

def show_password(length_entry, sector, result_label):
    try:
        length = int(length_entry.get())
        password = generate_secure_password(length)
        result_label.config(text=f"Your secure {sector} password is:\n{password}", fg='white')
        save_button.config(state=tk.NORMAL)  # Enable the save button
    except ValueError as e:
        result_label.config(text=str(e), fg='white')
        save_button.config(state=tk.DISABLED)  # Disable the save button

def save_password(password):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(password)
        messagebox.showinfo("Save Password", "Password saved successfully!")

def open_category_window(sector):
    window = tk.Toplevel(root)
    window.title(f"{sector.capitalize()} Password Generator")
    window.configure(bg='black')

    label = tk.Label(window, text=f"Enter {sector} password length:", bg='black', fg='white')
    label.pack(pady=10)

    length_entry = tk.Entry(window, bg='black', fg='white', insertbackground='white')
    length_entry.pack(pady=5)
    
    # Set default password lengths based on sector
    if sector == "banking":
        length_entry.insert(0, "16")
    elif sector == "social media":
        length_entry.insert(0, "12")
    elif sector == "personal":
        length_entry.insert(0, "10")

    result_label = tk.Label(window, text="", bg='black', fg='white')
    result_label.pack(pady=10)

    def on_generate():
        show_password(length_entry, sector, result_label)

    generate_button = tk.Button(window, text=f"Generate {sector.capitalize()} Password", bg='black', fg='white', command=on_generate)
    generate_button.pack(pady=20)

    global save_button
    save_button = tk.Button(window, text="Save Password", bg='black', fg='white', command=lambda: save_password(result_label.cget("text")), state=tk.DISABLED)
    save_button.pack(pady=10)

# Create the main window
root = tk.Tk()
root.title("Secure Password Generator")
root.configure(bg='black')

# Create buttons to open different password generation categories
categories = ["banking", "personal", "social media"]

for sector in categories:
    button = tk.Button(root, text=f"Open {sector.capitalize()} Password Generator", command=lambda s=sector: open_category_window(s), bg='black', fg='white')
    button.pack(pady=10)

# Run the application
root.mainloop()

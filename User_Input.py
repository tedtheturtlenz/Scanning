import tkinter as tk
from tkinter import simpledialog, messagebox

""" This is a simple function to get user inputs for the number of images per loop, number of loops, etc. """

#The main function of the script that gets the user inputs
def get_user_inputs():
    def submit():
        """Retrieve inputs and store them in variables"""
        nonlocal z_movement, num_photos, num_loops

        if stool_var.get():
            z_movement = 0.415  # Default stool height
        else:
            try:
                z_movement = float(z_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid Z value.")
                return
        
        try:
            num_photos = int(photos_entry.get())
            num_loops = int(loops_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Number of Photos and Loops must be integers.")
            return

        root.quit()  # Close the window

    root = tk.Tk()
    root.title("Tree-D Scanner User Input")
    root.geometry("300x250")

    z_movement = 0
    num_photos = 90  # Default value
    num_loops = 4  # Default value

    stool_var = tk.BooleanVar(value=True)  # Default: Using a stool

    # Checkbox for stool
    stool_check = tk.Checkbutton(root, text="Using the Stool", variable=stool_var, command=lambda: z_entry.config(state=tk.DISABLED if stool_var.get() else tk.NORMAL))
    stool_check.pack(pady=5)

    # Entry for custom Z value
    tk.Label(root, text="Custom Height Offset Value:").pack()
    z_entry = tk.Entry(root)
    z_entry.pack(pady=5)
    z_entry.config(state=tk.DISABLED)  # Disabled by default

    # Entry for Number of Photos per Loop
    tk.Label(root, text="Number of Photos per Loop:").pack()
    photos_entry = tk.Entry(root)
    photos_entry.insert(0, str(num_photos))  # Default value
    photos_entry.pack(pady=5)

    # Entry for Number of Loops
    tk.Label(root, text="Number of Loops (Must Be Even Number):").pack()
    loops_entry = tk.Entry(root)
    loops_entry.insert(0, str(num_loops))  # Default value
    loops_entry.pack(pady=5)

    # Submit Button
    submit_btn = tk.Button(root, text="Submit", command=submit)
    submit_btn.pack(pady=10)

    root.mainloop()

    root.destroy()  # Clean up the Tkinter window
    return z_movement, num_photos, num_loops


#Main code

# Get user inputs
z_movement, num_photos, num_loops = get_user_inputs()

# Confirm values with the user
messagebox.showinfo("Inputs Selected", f"Z Value: {z_movement}\nPhotos per Loop: {num_photos}\nNumber of Loops: {num_loops}")

# Write values to "user_inputs.txt"
output_file_path = r"D:\Bonsai\Code\user_inputs.txt"
with open(output_file_path, "w") as file:
    file.write(f"Z Value: {z_movement}\nPhotos per Loop: {num_photos}\nNumber of Loops: {num_loops}")

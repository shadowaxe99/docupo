import tkinter as tk

# Create a new Tkinter window
window = tk.Tk()

# Set the window title
window.title('User Interface')

# Set the window size
window.geometry('400x300')

# Add a label to the window
label = tk.Label(window, text='Welcome to the User Interface')
label.pack()

# Run the Tkinter event loop
window.mainloop()

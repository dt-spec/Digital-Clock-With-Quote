import os
import json
import random
from time import strftime
from tkinter import Label, Tk, messagebox

def show_error(message):
    """Display an error message in a message box."""
    messagebox.showerror("Error", message)

def read_json_file(filepath):
    """Read and return the data from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        show_error(f"Error reading {filepath}: {e}")
        return None

def parse_quotes(data):
    """Parse quotes from the loaded JSON data."""
    quotes = []
    if isinstance(data, dict) and "data" in data:
        for item in data["data"]:
            if "quote" in item and "author" in item:
                quotes.append(f'{item["quote"]} — {item["author"]}')
    else:
        show_error("Invalid format: Expected a dictionary with a 'data' key containing a list of quotes.")
    return quotes

def load_quotes(directory):
    """Load and parse quotes from all JSON files in the given directory."""
    quotes = []
    if not os.path.exists(directory):
        show_error(f"Directory {directory} does not exist.")
        return quotes
    
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            data = read_json_file(filepath)
            if data:
                quotes.extend(parse_quotes(data))
    
    return quotes

# Using a relative path to the 'data' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
quotes_dir = os.path.join(current_dir, 'data')
quotes = load_quotes(quotes_dir)

# Provide default quotes if no quotes are loaded
if not quotes:
    quotes = ["Keep going!", "You can do it!", "Stay positive!", "Believe in yourself!"]

# ======= Configuring window =========
window = Tk()  # Creating the main window
window.title("Motivational Clock")  # Setting the window title
window.attributes("-fullscreen", True)  # Making the window full screen
window.configure(bg="darkslategray")  # Setting the background color of the window
window.resizable(False, False)  # Disabling window resizing (fixed window size)

# Creating a label to display the clock
clock_label = Label(window, bg="black", fg="white", font=("Helvetica", 48, "bold"), relief="flat")
clock_label.place(relx=0.5, rely=0.4, anchor="center")  # Centering the label in the window

# Creating a label to display the motivational quote
quote_label = Label(window, bg="darkslategray", fg="white", font=("Helvetica", 24, "italic"), wraplength=1000, justify="center")
quote_label.place(relx=0.5, rely=0.7, anchor="center")  # Positioning the quote label

def update_label():
    """Update the clock label with the current time and date."""
    current_time = strftime("%H:%M:%S\n%A, %d %B %Y")
    clock_label.configure(text=current_time)
    clock_label.after(1000, update_label)

def update_quote():
    """Update the quote label with a random motivational quote."""
    random_quote = random.choice(quotes)
    quote_label.configure(text=random_quote)
    quote_label.after(60000, update_quote)

# Start the clock and quote updates
update_label()
update_quote()

# Running the Tkinter event loop to keep the window open
window.mainloop()

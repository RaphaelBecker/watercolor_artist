#!python3
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import os

# Add a global variable to keep track of the current image path
current_image_path = None


def load_images():
    filetypes = (('Image files', '*.jpg *.jpeg *.png'), ('All files', '*.*'))
    filenames = filedialog.askopenfilenames(title='Open files', initialdir='/', filetypes=filetypes)

    for filename in filenames:
        image = Image.open(filename)
        images[filename] = image  # Storing with full file path
        update_image_list()


def update_image_list():
    listbox.delete(0, tk.END)
    for filepath in images:
        listbox.insert(tk.END, os.path.basename(filepath))  # Inserting just the file name for display


def update_image(event):
    global current_image_path
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        displayed_filename = listbox.get(index)
        # Find the full path corresponding to the displayed filename
        full_path = next((path for path in images if os.path.basename(path) == displayed_filename), None)
        if full_path:
            current_image_path = full_path
            display_image(images[full_path])


def resize_image(event=None):
    global current_image_path
    if current_image_path:
        # Get the size of the canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Resize and display the image
        original_image = images[current_image_path]
        resized_image = original_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)  # Updated line
        display_image(resized_image)


def display_image(image):
    # Resize the image to fit the canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    resized_image = image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)

    # Process the resized image for brightness
    processed_image = process_image(resized_image, brightness_scale.get())

    # Display the processed image
    img = ImageTk.PhotoImage(processed_image)
    canvas.image = img
    canvas.create_image(20, 20, image=img, anchor='nw')


def update_brightness(value):
    global current_image_path
    if current_image_path:
        display_image(images[current_image_path])


def process_image(image, brightness_threshold):
    # Convert image to grayscale
    grayscale_image = ImageOps.grayscale(image)

    # Define a filter function for brightness
    def filter_brightness(pixel):
        return 255 if pixel > brightness_threshold else 0

    # Apply the filter function to each pixel
    filtered_image = grayscale_image.point(filter_brightness)

    return filtered_image


# Setup GUI
root = tk.Tk()
root.title("Image Brightness Tool for Artists")
# Bind the resize event
root.bind('<Configure>', resize_image)

images = {}

# Sidebar for image list
sidebar = tk.Frame(root, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
sidebar.pack(expand=False, fill='y', side='left', anchor='nw')

listbox = tk.Listbox(sidebar)
listbox.pack(expand=True, fill='both', side='left')
listbox.bind('<<ListboxSelect>>', update_image)

# Load button
load_button = tk.Button(sidebar, text='Load Images', command=load_images)
load_button.pack(side='top')

# Brightness control
brightness_scale = tk.Scale(sidebar, from_=0, to=255, orient='horizontal', command=update_brightness)
brightness_scale.set(128)
brightness_scale.pack(side='bottom')

# Canvas for image display
canvas = tk.Canvas(root, bg='white')
canvas.pack(expand=True, fill='both', side='right')

root.mainloop()

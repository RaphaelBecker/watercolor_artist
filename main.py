#!python3
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import os

# Add a global variable to keep track of the current image path
current_image_path = None

# Global variable to keep track of the inversion state
invert_mode = False

# At the beginning, with other global variables
effect_enabled = True

images = {}


def load_images_at_startup():
    images_folder = 'images'
    if os.path.exists(images_folder):
        for filename in os.listdir(images_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(images_folder, filename)
                try:
                    image = Image.open(full_path)
                    images[full_path] = image
                except IOError:
                    pass  # Handle file not opened, if necessary
        update_image_list()


def load_images():
    filetypes = (('Image files', '*.jpg *.jpeg *.png'), ('All files', '*.*'))
    filenames = filedialog.askopenfilenames(title='Open files', initialdir='/', filetypes=filetypes)

    for filename in filenames:
        image = Image.open(filename)
        images[filename] = image  # Storing with full file path
        update_image_list()
    save_all_images()


def update_image_list():
    for i in image_list.get_children():
        image_list.delete(i)
    for filepath in images:
        filename = os.path.basename(filepath)
        image_list.insert('', 'end', values=(filename, 'x'))


def update_image(event):
    global current_image_path
    selected_items = image_list.selection()
    if selected_items:
        item_id = selected_items[0]
        displayed_filename = image_list.item(item_id, 'values')[0]
        full_path = next((path for path in images if os.path.basename(path) == displayed_filename), None)
        if full_path:
            current_image_path = full_path
            display_image(images[full_path])


def save_all_images():
    save_directory = 'images'
    os.makedirs(save_directory, exist_ok=True)
    for path, image in images.items():
        filename = os.path.basename(path)
        save_path = os.path.join(save_directory, filename)
        image.save(save_path)


def on_treeview_click(event):
    region = image_list.identify("region", event.x, event.y)
    column = image_list.identify_column(event.x)
    if region == "cell" and column == "#2":  # Assuming the 'remove' button is in the second column
        remove_image()


def remove_image():
    for item_id in image_list.selection():
        displayed_filename = image_list.item(item_id, 'values')[0]
        full_path = next((path for path in images if os.path.basename(path) == displayed_filename), None)

        if full_path:
            # Remove from the images dictionary
            del images[full_path]

            # Remove from the Treeview
            image_list.delete(item_id)

            # Delete the file from the disk
            try:
                os.remove(full_path)
            except OSError as e:
                print(f"Error removing {full_path}: {e}")


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
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    resized_image = image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)

    if effect_enabled:
        processed_image = process_image(resized_image, brightness_scale.get())
    else:
        processed_image = resized_image  # Use the original resized image if effect is disabled

    img = ImageTk.PhotoImage(processed_image)
    canvas.image = img
    canvas.create_image(20, 20, image=img, anchor='nw')


def update_brightness(value):
    global current_image_path
    if current_image_path:
        display_image(images[current_image_path])


def toggle_inversion():
    global invert_mode
    invert_mode = not invert_mode
    update_display()


def update_display():
    global current_image_path
    if current_image_path:
        display_image(images[current_image_path])


def process_image(image, brightness_threshold):
    def is_bright(pixel):
        return sum(pixel) / 3 > brightness_threshold

    def process_pixel(pixel):
        if invert_mode:
            return (255, 255, 255) if not is_bright(pixel) else pixel
        else:
            return (255, 255, 255) if is_bright(pixel) else pixel

    if image.mode == 'RGB':
        pixels = list(image.getdata())
        processed_pixels = [process_pixel(pixel) for pixel in pixels]
        processed_image = Image.new('RGB', image.size)
        processed_image.putdata(processed_pixels)
        return processed_image
    else:
        return image

def toggle_effect():
    global effect_enabled
    effect_enabled = not effect_enabled
    update_display()


def increase_brightness(event=None):
    current_value = brightness_scale.get()
    if current_value < 255:
        brightness_scale.set(current_value + 4)
        update_brightness(current_value + 4)

def decrease_brightness(event=None):
    current_value = brightness_scale.get()
    if current_value > 0:
        brightness_scale.set(current_value - 4)
        update_brightness(current_value - 4)

# Setup GUI

root = tk.Tk()
root.title("Image Brightness Tool for Artists")
root.geometry("1400x900")  # Set initial size of the window

# Bind the resize event
root.bind('<Configure>', resize_image)
root.bind('<Left>', decrease_brightness)
root.bind('<Right>', increase_brightness)

# Define consistent styling for buttons
button_style = {'font': ('Helvetica', 10), 'bg': '#4a7a8c', 'fg': 'white'}

# Sidebar for controls
sidebar = tk.Frame(root, width=200, bg='#2a3d4d', relief='sunken', borderwidth=2)
sidebar.pack(fill='y', side='left', anchor='nw', padx=5, pady=5)

# Load button
load_button = tk.Button(sidebar, text='Load Images', command=load_images, **button_style)
load_button.pack(pady=10, fill='x')

# Image list Treeview
image_list = ttk.Treeview(sidebar)
image_list["columns"] = ("name", "remove")
image_list.column("#0", width=0, stretch=tk.NO)
image_list.column("name", anchor=tk.W, width=140)
image_list.column("remove", anchor=tk.CENTER, width=40)
image_list.heading("#0", text="", anchor=tk.CENTER)
image_list.heading("name", text="Image Name", anchor=tk.CENTER)
image_list.heading("remove", text="Remove", anchor=tk.CENTER)
image_list.pack(expand=True, fill='both', padx=5, pady=5)
image_list.bind('<<TreeviewSelect>>', update_image)
image_list.bind("<Button-1>", on_treeview_click)

# Brightness control and label
brightness_frame = tk.Frame(sidebar, bg='#2a3d4d')
brightness_frame.pack(padx=5, pady=10, fill='x')

brightness_label = tk.Label(brightness_frame, text="Brightness Threshold", bg='#2a3d4d', fg='white', font=('Helvetica', 10))
brightness_label.pack()  # Default is top (above the slider)

brightness_scale = tk.Scale(brightness_frame, from_=0, to=255, orient='horizontal', command=update_brightness, length=150)
brightness_scale.set(128)
brightness_scale.pack()  # Will be placed below the label

# Invert button
invert_button = tk.Button(sidebar, text='Invert', command=toggle_inversion, **button_style)
invert_button.pack(pady=5, fill='x')

# Toggle Effect button
toggle_effect_button = tk.Button(sidebar, text='Toggle Effect', command=toggle_effect, **button_style)
toggle_effect_button.pack(pady=5, fill='x')

# Canvas for image display
canvas = tk.Canvas(root, bg='white')
canvas.pack(expand=True, fill='both', padx=5, pady=5)
canvas.bind('<Configure>', resize_image)

load_images_at_startup()

root.mainloop()


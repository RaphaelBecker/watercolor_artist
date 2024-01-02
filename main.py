#!python3
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import os
import image_processing


class WatercolorArtistTool:

    def __init__(self, root):
        self.image_list = None
        self.root = root
        self.current_image_path = None
        self.invert_mode = False
        self.brightness_effect_enabled = True
        self.basic_watercolor_effect_enabled = False
        self.images = {}
        self.setup_gui()

        print(self.images)

    def setup_gui(self):
        self.root.title("Image Brightness Tool for Artists")
        self.root.geometry("1400x900")
        self.root.bind('<Left>', self.decrease_brightness)
        self.root.bind('<Right>', self.increase_brightness)

        # Sidebar setup
        self.setup_sidebar()

        # Canvas for image display
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(expand=True, fill='both', padx=5, pady=5)
        self.canvas.bind('<Configure>', self.resize_image)

        self.load_images_at_startup()

    def setup_sidebar(self):
        # Define consistent styling for buttons
        button_style = {'font': ('Helvetica', 10), 'bg': '#4a7a8c', 'fg': 'white'}

        # Sidebar for controls
        sidebar = tk.Frame(self.root, width=200, bg='#2a3d4d', relief='sunken', borderwidth=2)
        sidebar.pack(fill='y', side='left', anchor='nw', padx=5, pady=5)

        # Load button
        load_button = tk.Button(sidebar, text='Load Images', command=self.load_images, **button_style)
        load_button.pack(pady=10, fill='x')

        # Image list Treeview setup
        self.setup_image_list(sidebar)

        # Brightness control and label setup
        self.setup_brightness_control(sidebar, button_style)

    def setup_image_list(self, sidebar):
        # Image list Treeview
        self.image_list = ttk.Treeview(sidebar)
        self.image_list["columns"] = ("name", "remove")
        self.image_list.column("#0", width=0, stretch=tk.NO)
        self.image_list.column("name", anchor=tk.W, width=140)
        self.image_list.column("remove", anchor=tk.CENTER, width=40)
        self.image_list.heading("#0", text="", anchor=tk.CENTER)
        self.image_list.heading("name", text="Image Name", anchor=tk.CENTER)
        self.image_list.heading("remove", text="Remove", anchor=tk.CENTER)
        self.image_list.pack(expand=True, fill='both', padx=5, pady=5)
        self.image_list.bind('<<TreeviewSelect>>', self.update_image)
        self.image_list.bind("<Button-1>", self.on_treeview_click)

    def setup_brightness_control(self, sidebar, button_style):
        self.brightness_frame = tk.Frame(sidebar, bg='#2a3d4d')
        self.brightness_frame.pack(padx=5, pady=10, fill='x')

        self.brightness_label = tk.Label(self.brightness_frame, text="Brightness Threshold", bg='#2a3d4d', fg='white',
                                         font=('Helvetica', 10))
        self.brightness_label.pack()  # Default is top (above the slider)

        self.brightness_scale = tk.Scale(self.brightness_frame, from_=0, to=255, orient='horizontal',
                                         command=self.update_brightness, length=150)
        self.brightness_scale.set(128)
        self.brightness_scale.pack()  # Will be placed below the label

        # Invert and Toggle Effect buttons
        self.invert_brightness_button = tk.Button(sidebar, text='Invert Brightness', command=self.toggle_inversion, **button_style)
        self.invert_brightness_button.pack(pady=5, fill='x')

        self.toggle_brightness_effect_button = tk.Button(sidebar, text='Toggle Brightness',
                                                         command=self.toggle_brightness_effect, **button_style)
        self.toggle_brightness_effect_button.pack(pady=5, fill='x')

        self.toggle_basic_watercolor_effect_button = tk.Button(sidebar, text='Toggle Watercolor',
                                                               command=self.toggle_basic_watercolor_effect,
                                                               **button_style)
        self.toggle_basic_watercolor_effect_button.pack(pady=5, fill='x')

    def load_images_at_startup(self):
        images_folder = 'images'
        if os.path.exists(images_folder):
            for filename in os.listdir(images_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    full_path = os.path.join(images_folder, filename)
                    try:
                        image = Image.open(full_path)
                        self.images[full_path] = image
                    except IOError:
                        pass  # Handle file not opened, if necessary
            self.update_image_list()

    def load_images(self):
        filetypes = (('Image files', '*.jpg *.jpeg *.png'), ('All files', '*.*'))
        filenames = filedialog.askopenfilenames(title='Open files', initialdir='/', filetypes=filetypes)

        for filename in filenames:
            image = Image.open(filename)
            self.images[filename] = image  # Storing with full file path
            self.update_image_list()
        self.save_all_images()

    def update_image_list(self):
        for i in self.image_list.get_children():
            self.image_list.delete(i)
        for filepath in self.images:
            filename = os.path.basename(filepath)
            self.image_list.insert('', 'end', values=(filename, 'x'))

    def update_image(self, event):
        selected_items = self.image_list.selection()
        if selected_items:
            item_id = selected_items[0]
            displayed_filename = self.image_list.item(item_id, 'values')[0]
            full_path = next((path for path in self.images if os.path.basename(path) == displayed_filename), None)
            if full_path:
                self.current_image_path = full_path
                self.display_image(self.images[full_path])

    def save_all_images(self):
        save_directory = 'images'
        os.makedirs(save_directory, exist_ok=True)
        for path, image in self.images.items():
            filename = os.path.basename(path)
            save_path = os.path.join(save_directory, filename)
            image.save(save_path)

    def on_treeview_click(self, event):
        region = self.image_list.identify("region", event.x, event.y)
        column = self.image_list.identify_column(event.x)
        if region == "cell" and column == "#2":  # Assuming the 'remove' button is in the second column
            self.remove_image()

    def remove_image(self):
        for item_id in self.image_list.selection():
            displayed_filename = self.image_list.item(item_id, 'values')[0]
            full_path = next((path for path in self.images if os.path.basename(path) == displayed_filename), None)

            if full_path:
                # Remove from the images dictionary
                del self.images[full_path]

                # Remove from the Treeview
                self.image_list.delete(item_id)

                # Delete the file from the disk
                try:
                    os.remove(full_path)
                except OSError as e:
                    print(f"Error removing {full_path}: {e}")

    def resize_image(self, event=None):
        if self.current_image_path:
            # Get the size of the canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Resize and display the image
            original_image = self.images[self.current_image_path]
            resized_image = original_image.resize((canvas_width, canvas_height),
                                                  Image.Resampling.LANCZOS)  # Updated line
            self.display_image(resized_image)

    def display_image(self, image):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        processed_image = image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)

        if self.brightness_effect_enabled:
            processed_image = image_processing.process_image(processed_image, self.brightness_scale.get(),
                                                             self.invert_mode)
        if self.basic_watercolor_effect_enabled:
            processed_image = image_processing.watercolor_effect(processed_image)

        img = ImageTk.PhotoImage(processed_image)
        self.canvas.image = img
        self.canvas.create_image(20, 20, image=img, anchor='nw')

    def update_brightness(self, value):
        if self.current_image_path:
            self.display_image(self.images[self.current_image_path])

    def toggle_inversion(self):
        self.invert_mode = not self.invert_mode
        self.update_display()

    def update_display(self):
        if self.current_image_path:
            self.display_image(self.images[self.current_image_path])

    def toggle_brightness_effect(self):
        self.brightness_effect_enabled = not self.brightness_effect_enabled
        self.update_display()

    def toggle_basic_watercolor_effect(self):
        self.basic_watercolor_effect_enabled = not self.basic_watercolor_effect_enabled
        self.update_display()

    def increase_brightness(self, event=None):
        current_value = self.brightness_scale.get()
        if current_value < 255:
            self.brightness_scale.set(current_value + 4)
            self.update_brightness(current_value + 4)

    def decrease_brightness(self, event=None):
        current_value = self.brightness_scale.get()
        if current_value > 0:
            self.brightness_scale.set(current_value - 4)
            self.update_brightness(current_value - 4)

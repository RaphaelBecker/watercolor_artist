# Watercolor Artist Tool

## Overview
This Python-based tool is designed to assist watercolor artists in visualizing the light and dark areas of an image. It provides a simple and intuitive graphical user interface (GUI) to load images and adjust their brightness levels. The tool is especially helpful for identifying and highlighting the brightness values of different regions within an image, thereby aiding artists in planning their watercolor compositions.

## Features
- **Load Multiple Images:** Users can load multiple images into the tool for analysis.
- **Brightness Adjustment:** A slider allows users to set a brightness threshold. Pixels brighter than this threshold will be turned white, highlighting the lighter areas of the image.
- **Interactive GUI:** The tool features a list sidebar for easy navigation among loaded images and a canvas area where the adjusted images are displayed.

## Installation
To set up the Watercolor Artist Tool, follow these steps:

1. **Clone the Repository:**
   ```
   git clone [repository-url]
   ```
   
2. **Set Up a Virtual Environment (Optional):**
   - Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the main script to start the application:
```
python main.py
```

Once the application is running:
- Use the 'Load Images' button to select and load images.
- Click on an image in the sidebar to view it in the main canvas.
- Adjust the brightness threshold using the slider to highlight bright areas.
- Resize the window to scale the displayed image.

## Technologies
- Python
- Tkinter for the GUI
- Pillow for image processing

## Contributing
Contributions to the Watercolor Artist Tool are welcome! Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the [MIT License](LICENSE.md) - see the `LICENSE.md` file for details.

## Acknowledgments
- Mention any third-party assets or contributors here.

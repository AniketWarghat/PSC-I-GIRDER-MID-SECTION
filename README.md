# PSC-I-GIRDER-MID-SECTION
This project provides a Graphical User Interface (GUI) for designing the Mid Section of a PSC-I Girder. The tool uses PyQt5 for the GUI and integrates with AutoCAD using the pyautocad library for creating and manipulating drawings.

Features
Input girder parameters via a user-friendly GUI.
Automatically generate the girder design in AutoCAD.
Add dimensions, labels, and a detailed model of the girder mid-section.
Prerequisites
Before running this project, make sure you have the following installed:

Python 3.x: Download Python
AutoCAD: Ensure AutoCAD is installed and accessible (required for AutoCAD automation).
PyQt5: Install using pip.
pyautocad: Python library for interacting with AutoCAD.
You can install the required Python libraries using the following command:

bash
Copy code
pip install PyQt5 pyautocad

Setting Up
Step 1: Clone the repository
Clone this repository to your local machine:

bash
Copy code
git clone https://github.com/yourusername/PSC-I-Girder-Design-GUI.git
cd PSC-I-Girder-Design-GUI

Step 2: Download AutoCAD Model Image
Download the PSC-I_GIRDER-Model.png image and place it in the GUI Working folder in your project directory (or adjust the file path in the code if needed).

Step 3: Update Paths in Code
Make sure to update the paths to the image or AutoCAD files within the code. If you're using relative paths, they should work well once the project is organized correctly.

Step 4: Run the Script
You can now run the main script to launch the GUI:

bash
Copy code
python PSC-I_GIRDER_GUI.py
This will open the application window, where you can input girder parameters and generate the design directly in AutoCAD.

Step 5: Interact with the GUI
Input the values for the girder dimensions such as:
Top flange width
Overall height
Bottom flange width, etc.
Click the "Draw Mid Section" button to generate the girder design in AutoCAD.
The design will be drawn, and dimensions will be added automatically.
Code Structure
PSC-I_GIRDER_GUI.py: The main script containing the PyQt5 GUI and AutoCAD integration.
README.md: Documentation for setting up and using the project.
./GUI Working/: Folder containing the image file for the girder model.

Contributing
Feel free to fork the project, raise issues, and submit pull requests. Contributions to improve the functionality and user experience are welcome!

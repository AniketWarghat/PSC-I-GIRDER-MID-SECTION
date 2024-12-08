# Imports and Setup
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtCore import Qt
from pyautocad import Autocad, APoint

#Initialize AutoCAD
acad = Autocad(create_if_not_exists=True)
dwg = acad.doc

#Define Functions Here

def create_layer(layer_name, color = 7):
    layer_dict = acad.doc.Layers
    if layer_name in [layer.Name for layer in layer_dict]:
        layer = layer_dict.Item(layer_name)
    else :
        layer = layer_dict.Add(layer_name)
    layer.Color = color

def draw_line(points, layer_name3="M_GIRDER", color3= 210):
    create_layer(layer_name3,color3)
    for i in range(len(points)):
        line = acad.model.AddLine(points[i],points[(i+1)%len(points)])
        line.Layer = layer_name3
        line.Linetype = "Continuous"

def add_linear_dim(p1, p2, dim_point, layer_name1 ="CO_DIM", color1 = 4):
    create_layer(layer_name1,color1)
    dim = acad.model.AddDimAligned(p1, p2, dim_point)
    dim.Layer = layer_name1
    return dim

def draw_dotted_line(p3, p4, line_scale = 1,layer_name2 ="CO_DOTLINE", color2 = 8):
    create_layer(layer_name2,color2)
    line = acad.model.AddLine(p3, p4)
    line.Linetype = "DOT"
    line.LinetypeScale = line_scale
    line.Layer = layer_name2
    return line

def add_text(text_content, insertion_point, height, layer_name3 = "CO_TEXT", color3 = 3):
    create_layer(layer_name3,color3)
    text_obj = acad.model.AddText(text_content,insertion_point,height)
    text_obj.Layer = layer_name3

def get_default_values():
    return {
    "a": "900",
    "b": "1500",
    "c": "700",
    "d": "500",
    "e": "150",
    "f": "250",
    "g": "75",
    "h": "875",
    "i": "150"
}
#Define coordinate points to draw MId SECTION Of PSC GIRDER
def define_girder_points(values):
    base_point = APoint(0, 0)
    points = [
        base_point,
        APoint(base_point.x + values['c'], base_point.y),
        APoint(base_point.x + values['c'], base_point.y + values['f']),
        APoint(base_point.x + values['d']/2 + values['c']/2, base_point.y + values['f'] + values['i']),
        APoint(base_point.x + values['d']/2 + values['c']/2, base_point.y + values['f'] + values['i'] + values['h']),
        APoint(base_point.x + values['a']/2 + values['c']/2, base_point.y + values['f'] + values['i'] + values['h'] + values['g']),
        APoint(base_point.x + values['a']/2 + values['c']/2, base_point.y + values['f'] + values['i'] + values['h'] + values['g'] + values['e']),
        APoint(base_point.x + values['c']/2 - values['a']/2, base_point.y + values['f'] + values['i'] + values['h'] + values['g'] + values['e']),
        APoint(base_point.x + values['c']/2 - values['a']/2, base_point.y + values['f'] + values['i'] + values['h'] + values['g']),
        APoint(base_point.x + values['c']/2 - values['d']/2, base_point.y + values['f'] + values['i'] + values['h']),
        APoint(base_point.x + values['c']/2 - values['d']/2, base_point.y + values['f'] + values['i']),
        APoint(base_point.x, base_point.y + values['f']),
        APoint(base_point.x, base_point.y),
    ]
    return points

# Class Definition
class GirderInputApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()  # Call to initUI method to set up the interface

    # UI Initialization
    def initUI(self):
        self.setWindowTitle('GIRDER MID SECTION Input')
        self.setFixedSize(600, 800)

        def resource_path(relative_path):
    # """ Get absolute path to resource, works for dev and PyInstaller """
            try:
                base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))  # Checks if running in a bundled app
            except Exception:
                base_path = os.path.abspath(".")  # Development mode
            return os.path.join(base_path, "GUI Working", relative_path)
        
        diagram_label = QLabel(self)
        # pixmap = QPixmap('D:\\0.Aniket Working\\LEARNINGS\\#PSC-I GIRDER\\GUI Working\\PSC-I_GIRDER-Model.png')  # Make sure image path is correct
        print("Image path:", resource_path('PSC-I_GIRDER-Model.png'))
        pixmap = QPixmap(resource_path('PSC-I_GIRDER-Model.png'))  # Make sure image path is correct
        diagram_label.setPixmap(pixmap)
        diagram_label.setScaledContents(True)
        diagram_label.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()
        labels = {
            'Top flange width (a)': 'a', 'Overall height (b)': 'b', 'Bottom flange width (c)': 'c',
            'Web thickness (d)': 'd', 'Top flange thickness (e)': 'e', 'Bottom flange thickness (f)': 'f',
            'Depth of web below Top flange (g)': 'g', 'Web Height (h)': 'h', 'Depth of web above Bottom flange (i)': 'i'
        }

        # Call the function to get the default values (ensure it returns a dictionary)
        default_values = get_default_values()  # <-- This is the fix

        self.inputs = {}

        input_fields = []

        for i, (label_text, label_key) in enumerate(labels.items()):
            lbl = QLabel(f'{label_text}:', self)
            input_field = QLineEdit(self)

            validator = QIntValidator(0, 10000000, self)
            input_field.setValidator(validator)

            input_field.setText(default_values.get(label_key, ''))  # <-- Now works as expected

            grid.addWidget(lbl, i, 0)
            grid.addWidget(input_field, i, 1)
            self.inputs[label_key] = input_field
            input_fields.append(input_field)

        for i in range(len(input_fields)):
            if i < len(input_fields) - 1:
                input_fields[i].returnPressed.connect(input_fields[i + 1].setFocus)
            else:
                input_fields[i].returnPressed.connect(self.triggerDraw)

        self.draw_button = QPushButton('Draw Mid Section', self)
        self.draw_button.clicked.connect(self.drawGirder)

        main_layout = QVBoxLayout()
        main_layout.addWidget(diagram_label)
        main_layout.addLayout(grid)
        main_layout.addWidget(self.draw_button)
        self.setLayout(main_layout)


    # Draw Method
    def drawGirder(self):
        values = {label: float(self.inputs[label].text()) for label in self.inputs}
        points = define_girder_points(values)
        draw_line(points)

        # Add dimensions to MId SECTION Of PSC GIRDER
        #bottom flange length
        add_linear_dim(points[0], points[1], APoint(points[0].x, points[0].y - 150) )
        dim_points1 = APoint(points[0].x, points[0].y - 150)
        draw_dotted_line(points[0],dim_points1)
        dim_points1 = APoint(points[1].x, points[1].y - 150)
        draw_dotted_line(points[1],dim_points1)
        #bottom flange height
        add_linear_dim(points[1], points[2], APoint(points[1].x + 250, points[0].y) )
        dim_points2 = APoint(points[1].x + 400, points[1].y)
        draw_dotted_line(points[1],dim_points2)
        #bottom flange offset
        new_point_3 = APoint(points[3].x+values['c']/2-values['d']/2,points[3].y)
        add_linear_dim(points[2], new_point_3, APoint(points[2].x + 250, points[2].y) )
        dim_points3 = APoint(points[2].x + 250, points[2].y)
        draw_dotted_line(points[2],dim_points3)
        #web height
        add_linear_dim(points[3], points[4], APoint(points[2].x + 250, points[2].y) )
        dim_points4 = APoint(points[3].x+values['c']/2-values['d']/2+250,points[3].y)
        draw_dotted_line(points[3],dim_points4) 
        #top flange offset
        new_point_4 = APoint(points[4].x+values['a']/2-values['d']/2,points[4].y)
        add_linear_dim(new_point_4, points[5], APoint(points[5].x + 150, points[5].y) )
        dim_points5 = APoint(points[4].x+values['c']/2-values['d']/2+250,points[4].y)
        draw_dotted_line(points[4],dim_points5)
        #top flange height
        add_linear_dim(points[5], points[6], APoint(points[1].x + 250, points[0].y) )
        dim_points2 = APoint(points[5].x + 150, points[5].y)
        draw_dotted_line(points[5],dim_points2)
        dim_points2 = APoint(points[6].x + 300, points[6].y)
        draw_dotted_line(points[6],dim_points2)
        #total height
        new_point6 = APoint(points[6].x+values['c']/2-values['a']/2,points[6].y)
        add_linear_dim(points[1], new_point6, APoint(points[1].x + 400, points[0].y))
        #top flange length
        add_linear_dim(points[6], points[7], APoint(points[6].x, points[6].y + 150) )
        dim_points6 = APoint(points[6].x, points[6].y + 150)
        draw_dotted_line(dim_points6,points[6])
        dim_points7 = APoint(points[7].x, points[7].y + 150)
        draw_dotted_line(points[7],dim_points7)
        #web thickness
        add_linear_dim(points[4], points[9], APoint(points[4].x, points[4].y - values['h']/2))

        #Add text heading to MId SECTION Of PSC GIRDER
        add_text("GIRDER MID SECTION DETAILS", APoint(points[0].x,points[0].y-300), height = 50)
        
        # print("User Inputs:", values)  # Prints input values in the console
        # QMessageBox.information(self, 'Inputs Received', f"Values: {values}")

    def triggerDraw(self):
        self.drawGirder()

# Running the App
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GirderInputApp()
    window.show()
    sys.exit(app.exec_())
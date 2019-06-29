import PySide2, RLPy
from PySide2 import *
from PySide2.shiboken2 import wrapInstance

#-- Make a global variable contain dialog --#
sample_dialog = None

def run_script():

    global sample_dialog

    sample_dialog = RLPy.RUi.CreateRDialog()
    sample_dialog.SetWindowTitle("Sample Dialog")

    #-- Create Pyside layout for RDialog --#
    pyside_dialog = wrapInstance(int(sample_dialog.GetWindow()), PySide2.QtWidgets.QDialog)
    pyside_dialog.setFixedWidth(200)
    sample_layout = pyside_dialog.layout()

    #-- Create the Label --#
    label = PySide2.QtWidgets.QLabel("Test")

    col = PySide2.QtGui.QColor(111, 100, 8)
    label.setStyleSheet("QWidget { background-color: %s }" % col.name())

    #-- Add Label --#
    sample_layout.addWidget(label)

    sample_dialog.Show()    

import sys
from PySide2 import QtGui,QtWidgets
app = QtWidgets.QApplication(sys.argv)

print(app.desktop().screenGeometry())
r = app.desktop().screenGeometry()
#print(app.desktop().numScreens())
print(app.desktop().screenNumber())
print(r.width())

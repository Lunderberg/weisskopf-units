from PyQt4 import QtGui

def fill_placeholder(placeholder, widget):
    if placeholder.layout() is not None:
        QtGui.QWidget().setLayout(placeholder.layout())
    layout = QtGui.QVBoxLayout(placeholder)
    layout.addWidget(widget)
    placeholder.setLayout(layout)

def clear_layout(layout):
    for i in reversed(range(layout.count())):
        widget_to_remove = layout.itemAt(i).widget()
        layout.removeWidget(widget_to_remove)
        widget_to_remove.setParent(None)

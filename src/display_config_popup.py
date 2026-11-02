from PyQt6.QtWidgets import QWidget,QHBoxLayout,QLabel,QCheckBox,QApplication,QListWidget,QListWidgetItem
from PyQt6.QtCore import Qt,QMimeData
from PyQt6.QtGui import QDrag
import sys

class Popup(QWidget):
    def __init__(self):
        super().__init__()
        self.list_layout = QListWidget(self)
        self.list_layout.setDragDropMode(QListWidget.DragDropMode.InternalMove)

        self.list_layout.show()

    def add_row(self,text,checkbox_status):
        self.item = QListWidgetItem()
        self.list_layout.addItem(self.item)

        self.row_widget = QWidget()
        self.hbox_layout = QHBoxLayout(self.row_widget)

        self.hbox_layout.addWidget(QLabel(text))
        
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(checkbox_status)
           
        self.hbox_layout.addWidget(self.checkbox)
        self.item.setSizeHint(self.row_widget.sizeHint())
        self.list_layout.setItemWidget(self.item,self.row_widget)
    

    def read_rows_config(self,elements=0,config=0):
        self.add_row("asd",True)
        self.add_row("test",False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Popup()
    mywindow.show()
    app.exec()



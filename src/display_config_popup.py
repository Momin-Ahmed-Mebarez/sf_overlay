from PyQt6.QtWidgets import (QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QLabel,QCheckBox
                             ,QApplication,QListWidget,QListWidgetItem)
from pathlib import Path

import sys


HOME = Path(__file__).resolve().parent

def read_config():
     with open(HOME / "config.txt","r") as f:
         return f.readlines()

class Popup(QWidget):
    def __init__(self):
        super().__init__()
        self.list_layout = QListWidget()
        self.list_layout.setDragDropMode(QListWidget.DragDropMode.InternalMove)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.list_layout)
        self.main_layout.addWidget(self.save_button)

        self.read_rows_config(read_config())


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
    

    def read_rows_config(self,configs):
        for config in configs[1:]:
            splitted_config = config.split(":")

            self.add_row(splitted_config[0],int(splitted_config[1]))
    
    def save_config(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Popup()
    mywindow.show()
    app.exec()